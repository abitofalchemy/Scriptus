import pyspark as p
from os.path import expanduser, join, abspath
from datetime import date, datetime, timedelta
import time
from pyspark.sql import SparkSession
from dateutil.relativedelta import relativedelta
from _util import read_setting as read_config, script_path, read_env_config

import piad_prof_app_func as lib
import imp
imp.reload(lib)
import logging
import argparse,json
 
##*************************Spark Config********************************************************************************
warehouse_location = abspath('spark-warehouse')
hc = SparkSession \
    .builder \
    .appName("prof_scoring_app") \
    .config("spark.sql.warehouse.dir", warehouse_location) \
    .enableHiveSupport() \
    .getOrCreate()

############**********************Setup the log***********************************************************************
log = logging.getLogger() # 'root' Logger
console = logging.StreamHandler()
format_str = '%(asctime)s\t%(levelname)s -- %(processName)s %(filename)s:%(lineno)s -- %(message)s'
console.setFormatter(logging.Formatter(format_str))
log.addHandler(console) # prints to console.
log.setLevel(logging.INFO)

####**************************Import model Config parameters***********************************************************

cfg = read_config()

prefix = cfg.table_prefix
op_table_prefix = cfg.op_table_prefix

volume_vars = ['total_visits', 'total_patients', 'total_alwd_units']
util_vars =['visits_per_patient','units_per_visit','units_per_patient'
            ,'pct_of_prov_visits','pct_of_prov_patients','pct_of_prov_units']
groupby=['business_idea','txnmy_cd', 'lob', 'ctgry_3_txt']

groupby_cutoff=['business_idea']
groupby_norm=['business_idea', 'lob', 'ctgry_3_txt']

def main(date,env,release):
    a = time.time()

    ### **********************************set up date parameters*************************************************************
    #today = date.today()
    #date_suffix = today.strftime("%Y%m%d")
    #sat_date_suffix = (today - relativedelta(days=(today.weekday() + 1) % 7 + 1)).strftime("%Y%m%d")
    sat_date_suffix = date
    #prof_table_date = str(today - relativedelta(days=(today.weekday() + 1) % 7 + 1,years=2)).replace('-','_')
    prof_table_date = str(int(date[:4])-2)+"_"+date[4:6]+"_"+date[6:8]
    ###********************************set up table names *******************************
    prof_table = 'abnormal_procedure_profile_output4ui_scaled_app_ui_'+prof_table_date
    cnty_mbr_tbl = 'nppes_cnty_mbr'
    prof_new_provider = 'prof_new_provider'
    hlth_srvc_2020_new_codes = 'HLTH_SRVC_2020_NEW_codes'
    hlth_srvc = 'hlth_srvc'

    ###********************************Get configurations for database (pacakage code) *******************************
    env_cfg = read_env_config(env, release)
    wh_database=env_cfg.get('WAREHOUSE_DB')
    wk_database = env_cfg.get('WORK_DB')
    cdl_database = env_cfg.get('CDL_REF_DB')
    
    key_query = """concat(
        trim(cast(npi as string)),
        '_', 
        trim(cast(taxid as string)),
        '_',
        trim(cast(lob as string)),
        '_',
        trim(cast(hlth_srvc_cd as string)),
        '_',
        trim(cast(covid_diag_flag as string)),
        '_',
        trim(cast(business_idea as string))
        ) as covid_prof_unique_key"""

    key = ''.join(key_query).replace('\n','')    
    hc.sql("""use {database}""".format(database=wk_database))
         
    #******************Data Pull***************
    prof_table=hc.table("""{database}.{tbl}""".format(database=wh_database, tbl=prof_table))
    hlth_srvc_2020_new_codes=hc.table("""{database}.{tbl}""".format(database=wh_database, tbl=hlth_srvc_2020_new_codes))
    cnty_mbr_tbl=hc.table("""{database}.{tbl}""".format(database=wh_database, tbl=cnty_mbr_tbl))
    prof_new_provider=hc.table("""{database}.{tbl}""".format(database=wh_database, tbl=prof_new_provider))
    hlth_srvc=hc.table("""{database}.{tbl}""".format(database=cdl_database, tbl=hlth_srvc))

    cnty_mbr_tbl.registerTempTable("cnty_mbr_tbl") 
    prof_new_provider.registerTempTable("prof_new_provider") 
    hlth_srvc_2020_new_codes.registerTempTable("hlth_srvc_2020_new_codes") 
    hlth_srvc.registerTempTable("hlth_srvc")  
   
    #*********************Add upcoding text ***************************
    df = lib.upCodingTextER(hc, prof_table)
     
    #*********************Data Preparation ***********************************
    metrics = lib.selectMetrics(hc, df)
    uv_vars, vars_final = lib.createPrevvars(volume_vars,util_vars)
    casequery = lib.caseQuery(uv_vars)
    
    #*********************Modelling ***********************************
    df = lib.createModelingData(hc, df, hlth_srvc, hlth_srvc_2020_new_codes, 
                       prof_new_provider, cnty_mbr_tbl, 
                       metrics, casequery)
    df.write.mode("overwrite").saveAsTable(prefix+'_clean_'+sat_date_suffix)
    df_outlier = lib.outlierMemberCount(hc, df)
    df_mbr = lib.memberYoY(hc, df_outlier)
    df_outlier99 = lib.outlier99(hc, df_mbr, groupby_cutoff)

    df_outlier99.write.mode("overwrite").saveAsTable(prefix+'_outlierdata_all_'+ sat_date_suffix)
    df_outlier99 = hc.table("""{database}.{tbl}""".format(database=wk_database,tbl= prefix+'_outlierdata_all_'+ sat_date_suffix))
    df_norm = lib.normData(hc, df_outlier99, groupby_norm)

    df_varclnup = lib.varCleanup(hc, df_norm, util_vars, volume_vars)

    df_score = lib.generateScore(hc, df_varclnup,groupby_norm, util_vars, volume_vars, key)

    df_score.write.mode("overwrite").saveAsTable(prefix+'_scored_all_'+sat_date_suffix)

    df_dropdups = df_score.dropDuplicates(['covid_prof_unique_key'])
    df_dropdups.write.mode("overwrite").saveAsTable(prefix+'_scored_all_nodups_'+sat_date_suffix)
    
    df_dropdups = hc.table("""{database}.{tbl}""".format(database=wk_database,tbl= prefix+'_scored_all_nodups_'+sat_date_suffix))
    df_flt = lib.filterOutput(hc, df_dropdups)
    
    df1= lib.nlg1(hc, df_flt)
    df2= lib.nlg2(hc, df1)
    df3= lib.nlg3(hc, df2)
    df4= lib.nlg4(hc, df3)
    df5= lib.nlg5(hc, df4)
    
    df5.write.mode("overwrite").saveAsTable(op_table_prefix+'_scored_all_vars_'+sat_date_suffix)

    df6= lib.dropvars(hc, df5)
    final_table_nm = op_table_prefix+'_scored_'+sat_date_suffix
    df6.write.mode("overwrite").saveAsTable("""{database}.{tbl}""".format(database=wh_database,tbl=final_table_nm))
    
    df_fnl = hc.table("""{database}.{tbl}""".format(database=wh_database,tbl= final_table_nm))
    log.info("covid prof app scored table is created. Count: {ct}".format(ct=df_fnl.count()))

    b=time.time()
    c=(b-a)/60
    log.info("total used time is {c} mins".format(c=c))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=json.loads, required=True)
    args = parser.parse_args()
    config = args.config
    main(date = config['date'],env=config['env'],release=config['release'])

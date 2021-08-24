#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.insert(0, '../data_prep/')
from intrstlr_utils import setup_pyspark,initialize_logger
from pyspark.sql.functions import col, unix_timestamp, to_date
from pyspark.sql import functions as F
##
import os
import logging 
import traceback
import pandas as pd
import numpy as np 

### Canonical Source Features
def canonical_features_from_csbd():
	'''CSBD'''
	csbd_feats = """
	billg_prov_npi_id
	billg_prov_tax_id
	rndrg_prov_id
	place_of_srvc_cd
	inn_cd
	parg_stts_cd
	pn_id
	prov_sor_cd
	src_billg_prov_id
	src_billg_prov_id_type_cd
	rndrg_prov_id_type_cd
	mbr_prov_ntwk_id
	inn_cd_hdr
	serv_prov_id
	cp1_src_clm_prov_id
	clp1_src_clm_line_prov_id
	prov_srvc_agrmnt_id
	src_clm_prcg_cntrct_rgn_id
	src_prov_zip_cd
	src_prov_st_nm
	rndrg_prov_txnmy_cd
	serv_prov_state
	serv_prov_region
	attend_npi
	"""
	return csbd_feats

def canonical_features_from_fac_mad():
	'''FACILITY'''
	fc_feats = """
	billg_prov_npi_id
	billg_prov_tax_id
	rndrg_prov_medcr_id
	cntrct_plan_st_prvnc_cd
	mbr_st_prvnc_cd
	serv_npi_enty_type_cd
	serv_npi_txnmy_cd
	serv_npi_spclty_cd
	serv_npi_spclty
	serv_npi_zip
	serv_npi_cnty_nm
	serv_npi_fips_cnty_cd
	serv_npi_state
	bill_npi_enty_type_cd
	bill_npi_submrkt_cd
	bill_npi_cnty_nm
	bill_npi_fips_cnty_cd
	bill_npi_state
	"""
	fc_feats

def canonical_features_from_app():
	app_feats="""
	npi,
	cims_case_flag,
	tax_identifier,
	provider_name,
	state_code,
	region_name,
	taxonomy_code,
	lob,
	overall_risk_amount,
	peer_score_number,
	entity_type_description,
	provider_amount_percent,
	non_par_percent
	"""
	return app_feats

### Generate table subsets: 
def generate_gnn_training_table_subsets():
	queries = ["""
	--
	-- DSE_GNN_RSKYPROV_TRAIN_APP_NPIS
	-- 
	create table dv_dtlpiadph_gbd_r000_wk.dse_gnn_rskyprov_train_app_npis stored as parquet as 
	select a.npi, a.risky_prov_label,
	b.cims_case_flag,
	b.tax_identifier,
	b.provider_name,
	b.state_code,
	b.region_name,
	b.taxonomy_code,
	b.lob,
	b.overall_risk_amount,
	b.peer_score_number,
	b.entity_type_description,
	b.provider_amount_percent,
	b.non_par_percent
	from  dv_dtlpiadph_gbd_r000_wk.dse_gnn_rskyprov_combined_npis_in_csbd_list a
	left join (select distinct npi,
			cims_case_flag,
			tax_identifier,
			provider_name,
			state_code,
			region_name,
			taxonomy_code,
			lob,
			overall_risk_amount,
			peer_score_number,
			entity_type_description,
			provider_amount_percent,
			non_par_percent
			from dv_dtlpiadph_gbd_r000_ar.pingad_abnormal_procedure_profile_prodcopy) b
	on a.npi=b.npi""",
	"""
	--
	-- DSE_GNN_RSKYPROV_TRAIN_CSBD_NPIS
	--
	create table dv_dtlpiadph_gbd_r000_wk.dse_gnn_rskyprov_train_csbd_npis stored as parquet as 
	select b.billg_prov_npi_id
	,b.billg_prov_tax_id
	,b.rndrg_prov_id
	,b.place_of_srvc_cd
	,b.inn_cd
	,b.parg_stts_cd
	,b.pn_id
	,b.prov_sor_cd
	,b.src_billg_prov_id
	,b.src_billg_prov_id_type_cd
	,b.rndrg_prov_id_type_cd
	,b.mbr_prov_ntwk_id
	,b.inn_cd_hdr
	,b.serv_prov_id
	,b.cp1_src_clm_prov_id
	,b.clp1_src_clm_line_prov_id
	,b.prov_srvc_agrmnt_id
	,b.src_clm_prcg_cntrct_rgn_id
	,b.src_prov_zip_cd
	,b.src_prov_st_nm
	,b.rndrg_prov_txnmy_cd
	,b.serv_prov_state
	,b.serv_prov_region
	,b.attend_npi
	from  dv_dtlpiadph_gbd_r000_wk.dse_gnn_rskyprov_combined_npis_in_csbd_list a
	left join (select distinct billg_prov_npi_id
		,billg_prov_tax_id
		,rndrg_prov_id
		,place_of_srvc_cd
		,inn_cd
		,parg_stts_cd
		,pn_id
		,prov_sor_cd
		,src_billg_prov_id
		,src_billg_prov_id_type_cd
		,rndrg_prov_id_type_cd
		,mbr_prov_ntwk_id
		,inn_cd_hdr
		,serv_prov_id
		,cp1_src_clm_prov_id
		,clp1_src_clm_line_prov_id
		,prov_srvc_agrmnt_id
		,src_clm_prcg_cntrct_rgn_id
		,src_prov_zip_cd
		,src_prov_st_nm
		,rndrg_prov_txnmy_cd
		,serv_prov_state
		,serv_prov_region
		,attend_npi
	from dv_dtlpiadph_gbd_r000_wh.piad_clm_ln_csbd_mad) b
	on TRIM(a.npi)=TRIM(b.billg_prov_npi_id); 
	""",
	"""
	--
	-- DSE_GNN_RSKYPROV_TRAIN_FCLTY_NPIS
	--
	create table dv_dtlpiadph_gbd_r000_wk.dse_gnn_rskyprov_train_FCLTY_npis stored as parquet as 
	select b.billg_prov_npi_id
	,B.billg_prov_tax_id
	,B.rndrg_prov_medcr_id
	,B.cntrct_plan_st_prvnc_cd
	,B.mbr_st_prvnc_cd
	,B.serv_npi_enty_type_cd
	,B.serv_npi_txnmy_cd
	,B.serv_npi_spclty_cd
	,B.serv_npi_spclty
	,B.serv_npi_zip
	,B.serv_npi_cnty_nm
	,B.serv_npi_fips_cnty_cd
	,B.serv_npi_state
	,B.bill_npi_enty_type_cd
	,B.bill_npi_submrkt_cd
	,B.bill_npi_cnty_nm
	,B.bill_npi_fips_cnty_cd
	,B.bill_npi_state
	from  dv_dtlpiadph_gbd_r000_wk.dse_gnn_rskyprov_combined_npis_in_csbd_list a
	left join (select distinct billg_prov_npi_id
		, billg_prov_tax_id
		, rndrg_prov_medcr_id
		, cntrct_plan_st_prvnc_cd
		, mbr_st_prvnc_cd
		, serv_npi_enty_type_cd
		, serv_npi_txnmy_cd
		, serv_npi_spclty_cd
		, serv_npi_spclty
		, serv_npi_zip
		, serv_npi_cnty_nm
		, serv_npi_fips_cnty_cd
		, serv_npi_state
		, bill_npi_enty_type_cd
		, bill_npi_submrkt_cd
		, bill_npi_cnty_nm
		, bill_npi_fips_cnty_cd
		, bill_npi_state
	from dv_dtlpiadph_gbd_r000_wh.piad_fc_mad) b
	on TRIM(a.npi)=TRIM(b.billg_prov_npi_id);
	"""
]
def dse_gnn_rskyprov_train_fclty_rankedbymaxvalue_npis(spark, wk):
	query = """
	-- 
	-- FCLTY
	--
	create table ${wk}.dse_gnn_rskyprov_train_fclty_rankedbymaxvalue_npis stored as parquet as 
	select distinct  T.billg_prov_npi_id
	,T.billg_prov_tax_id
	,T.rndrg_prov_medcr_id
	,T.cntrct_plan_st_prvnc_cd
	,T.mbr_st_prvnc_cd
	,T.serv_npi_enty_type_cd
	,T.serv_npi_txnmy_cd
	,T.serv_npi_spclty_cd
	,T.serv_npi_spclty
	,T.serv_npi_zip
	,T.serv_npi_cnty_nm
	,T.serv_npi_fips_cnty_cd
	,T.serv_npi_state
	,T.bill_npi_enty_type_cd
	,T.bill_npi_submrkt_cd
	,T.bill_npi_cnty_nm
	,T.bill_npi_fips_cnty_cd
	,T.bill_npi_state
	from (
    select billg_prov_npi_id
	,billg_prov_tax_id
	,rndrg_prov_medcr_id
	,cntrct_plan_st_prvnc_cd
	,mbr_st_prvnc_cd
	,serv_npi_enty_type_cd
	,serv_npi_txnmy_cd
	,serv_npi_spclty_cd
	,serv_npi_spclty
	,serv_npi_zip
	,serv_npi_cnty_nm
	,serv_npi_fips_cnty_cd
	,serv_npi_state
	,bill_npi_enty_type_cd
	,bill_npi_submrkt_cd
	,bill_npi_cnty_nm
	,bill_npi_fips_cnty_cd
	,bill_npi_state, 
    rank() over ( partition by billg_prov_npi_id order by billg_prov_tax_id
				,rndrg_prov_medcr_id
				,cntrct_plan_st_prvnc_cd
				,mbr_st_prvnc_cd
				,serv_npi_enty_type_cd
				,serv_npi_txnmy_cd
				,serv_npi_spclty_cd
				,serv_npi_spclty
				,serv_npi_zip
				,serv_npi_cnty_nm
				,serv_npi_fips_cnty_cd
				,serv_npi_state
				,bill_npi_enty_type_cd
				,bill_npi_submrkt_cd
				,bill_npi_cnty_nm
				,bill_npi_fips_cnty_cd
				,bill_npi_state desc) as rank 
    from ${wk}.dse_gnn_rskyprov_train_FCLTY_npis 
    ) t  
    where rank=1;
	"""
	return 

def dse_gnn_rskyprov_train_csbd_rankedbymaxvalue_npis(spark, wk):
	query = """
	create table ${wk}.dse_gnn_rskyprov_train_csbd_rankedbymaxvalue_npis stored as parquet as 
	select distinct T.billg_prov_npi_id
	, T.billg_prov_tax_id
	, T.rndrg_prov_id
	, T.place_of_srvc_cd
	, T.inn_cd
	, T.parg_stts_cd
	, T.pn_id
	, T.prov_sor_cd
	, T.src_billg_prov_id
	, T.src_billg_prov_id_type_cd
	, T.rndrg_prov_id_type_cd
	, T.mbr_prov_ntwk_id
	, T.inn_cd_hdr
	, T.serv_prov_id
	, T.cp1_src_clm_prov_id
	, T.clp1_src_clm_line_prov_id
	, T.prov_srvc_agrmnt_id
	, T.src_clm_prcg_cntrct_rgn_id
	, T.src_prov_zip_cd
	, T.src_prov_st_nm
	, T.rndrg_prov_txnmy_cd
	, T.serv_prov_state
	, T.serv_prov_region
	, T.attend_npi
	from (
    select billg_prov_npi_id
	, billg_prov_tax_id
	, rndrg_prov_id
	, place_of_srvc_cd
	, inn_cd
	, parg_stts_cd
	, pn_id
	, prov_sor_cd
	, src_billg_prov_id
	, src_billg_prov_id_type_cd
	, rndrg_prov_id_type_cd
	, mbr_prov_ntwk_id
	, inn_cd_hdr
	, serv_prov_id
	, cp1_src_clm_prov_id
	, clp1_src_clm_line_prov_id
	, prov_srvc_agrmnt_id
	, src_clm_prcg_cntrct_rgn_id
	, src_prov_zip_cd
	, src_prov_st_nm
	, rndrg_prov_txnmy_cd
	, serv_prov_state
	, serv_prov_region
	, attend_npi, 
    rank() over ( partition by billg_prov_npi_id order by billg_prov_npi_id
				, billg_prov_tax_id
				, rndrg_prov_id
				, place_of_srvc_cd
				, inn_cd
				, parg_stts_cd
				, pn_id
				, prov_sor_cd
				, src_billg_prov_id
				, src_billg_prov_id_type_cd
				, rndrg_prov_id_type_cd
				, mbr_prov_ntwk_id
				, inn_cd_hdr
				, serv_prov_id
				, cp1_src_clm_prov_id
				, clp1_src_clm_line_prov_id
				, prov_srvc_agrmnt_id
				, src_clm_prcg_cntrct_rgn_id
				, src_prov_zip_cd
				, src_prov_st_nm
				, rndrg_prov_txnmy_cd
				, serv_prov_state
				, serv_prov_region
				, attend_npi desc) as rank 
    from ${wk}.dse_gnn_rskyprov_train_csbd_npis 
    ) t  
    where rank=1;
	"""
	return 

def dse_gnn_rskyprov_train_app_rankedbymaxvalue_npis(spark, wk):
	query = """
	create table {wk}.dse_gnn_rskyprov_train_app_rankedbymaxvalue_npis stored as parquet as 
	select distinct T.npi,
    T.cims_case_flag,
    T.tax_identifier,
    T.provider_name,
    T.state_code,
    T.region_name,
    T.taxonomy_code,
    T.lob,
    T.overall_risk_amount,
    T.peer_score_number,
    T.entity_type_description,
    T.provider_amount_percent,
    T.non_par_percent 
	from (
    select npi,cims_case_flag,
        tax_identifier,
        provider_name,
        state_code,
        region_name,
        taxonomy_code,
        lob,
        overall_risk_amount,
        peer_score_number,
        entity_type_description,
        provider_amount_percent,
        non_par_percent, 
    rank() over ( partition by npi order by cims_case_flag,
        tax_identifier,
        provider_name,
        state_code,
        region_name,
        taxonomy_code,
        lob,
        overall_risk_amount,
        peer_score_number,
        entity_type_description,
        provider_amount_percent,
        non_par_percent desc) as rank 
    from {wk}.dse_gnn_rskyprov_train_app_npis 
    ) t  
    where rank=1
	"""
	return 

# TODO ➘
def combine_dfs_rankedbymaxvalue_npis(psdfs_lst):
	'''psdfs_lst=>pyspark dataframes list'''
	cs_df = psdfs_lst[0]
	ap_df = psdfs_lst[1]
	fc_df = psdfs_lst[2]
	sdf = cs_df.join(ap_df, on=[
		ap_df.npi == cs_df.billg_prov_npi_id, 
		ap_df.tax_identifier == cs_df.billg_prov_tax_id]
		, how='leftouter')
	fc_df = fc_df.withColumnRenamed('billg_prov_npi_id',
		'npi_identifier').withColumnRenamed('billg_prov_tax_id',
		'prov_tax_id')
	sdf = sdf.join(fc_df, on = [fc_df.npi_identifier == sdf.billg_prov_npi_id, 
		fc_df.prov_tax_id == sdf.billg_prov_tax_id]
		, how='leftouter')
	logging.info("\nspark sql dataframe: ap+cs+fc using leftouter")
	logging.info(f"{sdf.select('billg_prov_npi_id').distinct().count()} \
		{sdf.select('billg_prov_tax_id').distinct().count()}")
	return sdf

def main(spark,logging):
	wk= "dv_dtlpiadph_gbd_r000_wk"
	def show_rankedbymaxval_tables():
		sdf=spark.sql(f"show tables in {wk} like 'dse_gnn_rskyprov_train_*npis'")
		for tbl in sdf.toPandas().tableName.values:
			if 'rankedbymaxvalue' in tbl:
				print(tbl)
		return 

	ap_df = spark.sql(f"select * from {wk}.dse_gnn_rskyprov_train_app_rankedbymaxvalue_npis")
	cs_df = spark.sql(f"select * from {wk}.dse_gnn_rskyprov_train_csbd_rankedbymaxvalue_npis")
	fc_df = spark.sql(f"select * from {wk}.dse_gnn_rskyprov_train_fclty_rankedbymaxvalue_npis")
	a = set(ap_df.columns)
	b = set(cs_df.columns)
	
	sdf = combine_dfs_rankedbymaxvalue_npis([cs_df,ap_df, fc_df])
	
	logging.info(f'rows: {sdf.count()}')
	logging.info(f'cols: {len(sdf.columns)}')
	logging.info(f'One Sample:\n{sdf.limit(1).toPandas().T}')	
	### store the expanded dataset to disk 
	sdf.toPandas().to_csv( 
		"../data_prep/training_graph/dse_gnn_nodes.tsv"
		, sep='\t')
	if os.path.exists("../data_prep/training_graph/dse_gnn_nodes.tsv"):
		logging.info("Training graph written to disk.")
	return 


if __name__ == "__main__":
	LOG_DIR='./logs'
	LOG_FNAME=sys.argv[0].split('.')[0]
	LOG_FNAME+='.log'
	print(LOG_FNAME)

	initialize_logger(LOG_DIR, LOG_FNAME, 'w')
	
	spark = setup_pyspark("ag23268_gnns")
	try:
		main(spark, logging)
	except Exception as e:
		logging.error('In main: ' + str(e))
		logging.info('❱❱ FAIL ❰❰')
		logging.error(str(traceback.print_exc()))
		os._exit(1)
	spark.stop()
	sys.exit(0)




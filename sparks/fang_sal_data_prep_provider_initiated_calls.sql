--
-- Provider Initiated Calls Data Generation
--
drop table if exists hcaadvaph_wk_playground.claim_linkcall_122018_ccp_sc_population_provider_sa;
create table hcaadvaph_wk_playground.claim_linkcall_122018_ccp_sc_population_provider_sa as
select hcid, mcid,clm_adjstmnt_key	,
src_billg_tax_id_type_cd	,
src_billg_tax_id	,
src_billg_prov_id	,
src_billg_prov_id_type_cd	,
src_prov_natl_prov_id	,
rndrg_prov_id	,
clm_sor_cd	,
a.clm_nbr	,
prncpl_diag_cd	,
othr_diag_1_cd	,
othr_diag_2_cd	,
othr_diag_3_cd	,
srvc_rndrg_type_cd	,
prmry_carr_rspnsbly_cd	,
clm_reimb_mthd_cd	,
src_grp_nbr	,
src_prchsr_org_nm	,
src_sbscrbr_st_cd	,
src_mbr_zip_cd	,
clm_disp_cd	,
clm_its_host_cd	,
clm_adjstmnt_nbr	,
adjdctn_type_cd	,
clm_rcvd_dt	,
clm_line_nbr	,
inc_yr	,
inc_mnth	,
--incrd_year_mnth_nbr	,
clm_line_srvc_strt_dt	,
clm_line_srvc_end_dt	,
billd_srvc_unit_cnt	,
paid_srvc_unit_cnt	,
hlth_srvc_cd	,
billd_chrg_amt	,
alwd_amt	,
paid_amt	,
adjdctn_dt	,
icd_vrsn_cd	,
proc_mdfr_1_cd	,
proc_mdfr_2_cd	,
inpat_cd	,
clm_line_pa_nbr	,
place_of_srvc_cd	,
inn_cd	,
parg_stts_cd	,
ffs_eqvlnt_amt	,
clm_nasco_par_cd	,
adjstmnt_rsn_cd	,
bnft_pkg_id	,
cob_svngs_amt	,
--clm_line_reimb_mthd_cd	,
pn_id	,
fee_sched_id	,
prod_id	,
--alwd_amt_ind	,
--clm_line_ndc	,
clm_line_stts_cd	,
auto_or_manl	,
--billg_prov_tax_id	,
--rndrg_prov_npi_id	,
src_mbr_brth_dt	,
mbr_gndr_cd	,
mbr_age	,
ctgry_1_txt	,
ctgry_2_txt	,
txnmy_cd	,
new_state	,
mbr_st_cd	,
mbr_zip_cd	,
lob	,
--cntrct_plan_st_prvnc_cd	,
--hcid	,
--hcid_target	,
--call_target	,
--sys	,
eob_cd,
src_eob_cd,
SRC_PAY_ACTN_CD,
CLM_LINE_REIMB_MTHD_CD,
inq_cnt,
RCVD_DT,
case
when inq_cnts.clm_nbr is not null then 1
else 0 end as claim_target
from hcaadvaph_wk_playground.claim_cmcl_sample_012019_population a
left join
(select substr(inq_linked_claim_id,3,11) clm_nbr, count(*) inq_cnt, min(RCVD_DT) RCVD_DT from hcaadvaph_wk_playground.sc_union_ccb_linked_calls_data a
inner join hcaadvaph_wk_playground.inquiry_comments_cmdmarch19 b
on a.inq_tracking_id = b.inq_tracking_id
where trim(inq_src)='P'
group by substr(inq_linked_claim_id,3,11)) inq_cnts
on trim(inq_cnts.clm_nbr)= trim(a.clm_nbr)
where DATEDIFF(adjdctn_dt, '2018-12-01')>=0 and DATEDIFF(adjdctn_dt, '2018-12-30')<=0;

select avg(claim_target) from hcaadvaph_wk_playground.claim_linkcall_122018_ccp_sc_population;

select inq_src, count(*)
from  hcaadvaph_wk_playground.inquiry_comments_ccb_union_sc_member_data_cmdapril19
group by inq_src;

drop table if exists hcaadvaph_wk_playground.claim_linkcall_hcid_122018_ccp_sc_population_provider_sa;
create table hcaadvaph_wk_playground.claim_linkcall_hcid_122018_ccp_sc_population_provider_sa as
select
	hcid	,
	max(call_target) call_target,
avg(	familysize 	)	familysize 	,
avg(	age_min 	)	age_min 	,
avg(	age_max 	)	age_max 	,
avg(	age_avg 	)	age_avg 	,
avg(	agesmaller10_cnt	)	agesmaller10_cnt	,
avg(	ageolder65_cnt	)	ageolder65_cnt	,
avg(	male_cnt	)	male_cnt	,
avg(	clmdaygap_avg	)	clmdaygap_avg	,
avg(	clmdaygap_min	)	clmdaygap_min	,
avg(	clmdaygap_max	)	clmdaygap_max	,
avg(	txnmy_cnt	)	txnmy_cnt	,
avg(	adjrsn_cnt	)	adjrsn_cnt	,
avg(	adjtype_cnt	)	adjtype_cnt	,
avg(	pos_cnt	)	pos_cnt	,
avg(	cpt_cnt	)	cpt_cnt	,
avg(	clm_within1month	)	clm_within1month	,
avg(	clm_within2month	)	clm_within2month	,
avg(	clm_within3month	)	clm_within3month	,
avg(	clm_within6month	)	clm_within6month	,
avg(	paid_amt_sum_1month	)	paid_amt_sum_1month	,
avg(	paid_amt_max_1month	)	paid_amt_max_1month	,
avg(	paid_amt_min_1month	)	paid_amt_min_1month	,
avg(	paid_amt_sum_3month	)	paid_amt_sum_3month	,
avg(	paid_amt_max_3month	)	paid_amt_max_3month	,
avg(	paid_amt_min_3month	)	paid_amt_min_3month	,
avg(	paid_amt_sum_6month	)	paid_amt_sum_6month	,
avg(	paid_amt_max_6month	)	paid_amt_max_6month	,
avg(	paid_amt_min_6month	)	paid_amt_min_6month	,
avg(	paid_amt_sum_2month	)	paid_amt_sum_2month	,
avg(	paid_amt_max_2month	)	paid_amt_max_2month	,
avg(	paid_amt_min_2month	)	paid_amt_min_2month	,
avg(	oop_amt_sum_1month	)	oop_amt_sum_1month	,
avg(	oop_amt_max_1month	)	oop_amt_max_1month	,
avg(	oop_amt_min_1month	)	oop_amt_min_1month	,
avg(	oop_amt_sum_3month	)	oop_amt_sum_3month	,
avg(	oop_amt_max_3month	)	oop_amt_max_3month	,
avg(	oop_amt_min_3month	)	oop_amt_min_3month	,
avg(	oop_amt_sum_6month	)	oop_amt_sum_6month	,
avg(	oop_amt_max_6month	)	oop_amt_max_6month	,
avg(	oop_amt_min_6month	)	oop_amt_min_6month	,
avg(	oop_amt_sum_2month	)	oop_amt_sum_2month	,
avg(	oop_amt_max_2month	)	oop_amt_max_2month	,
avg(	oop_amt_min_2month	)	oop_amt_min_2month	,
avg(	ercnt_1month	)	ercnt_1month	,
avg(	ercnt_3month	)	ercnt_3month	,
avg(	ercnt_6month	)	ercnt_6month	,
avg(	ercnt_2month	)	ercnt_2month	,
avg(	er_related_1month	)	er_related_1month	,
avg(	er_related_3month	)	er_related_3month	,
avg(	er_related_6month	)	er_related_6month	,
avg(	er_related_2month	)	er_related_2month	,
avg(	diffst_1month	)	diffst_1month	,
avg(	diffst_3month	)	diffst_3month	,
avg(	diffst_6month	)	diffst_6month	,
avg(	diffst_2month	)	diffst_2month	,
avg(	oon_1month	)	oon_1month	,
avg(	oon_3month	)	oon_3month	,
avg(	oon_6month	)	oon_6month	,
avg(	oon_2month	)	oon_2month	,
--avg(	dnd_1month	)	dnd_1month	,
--avg(	dnd_3month	)	dnd_3month	,
--avg(	dnd_6month	)	dnd_6month	,
--avg(	dnd_2month	)	dnd_2month	,
avg(	prmry_mdcr_1month	)	prmry_mdcr_1month	,
avg(	prmry_mdcr_3month	)	prmry_mdcr_3month	,
avg(	prmry_mdcr_6month	)	prmry_mdcr_6month	,
avg(	prmry_mdcr_2month	)	prmry_mdcr_2month	,
avg(	call_within1month	)	call_within1month	,
avg(	call_within2month	)	call_within2month	,
avg(	call_within3month	)	call_within3month	,
avg(	daygap_small	)	daygap_small	,
avg(	week_id	)	week_id	,
--avg(	reason_category	)	reason_category	,
avg(	day_int	)	day_int	,
avg(	weeklycnt_min	)	weeklycnt_min	,
avg(	weeklycnt_avg	)	weeklycnt_avg	,
avg(	weeklycnt_max	)	weeklycnt_max	,
avg(	weekcnt	)	weekcnt	,
avg(	dailycnt_min	)	dailycnt_min	,
avg(	dailycnt_avg	)	dailycnt_avg	,
avg(	dailycnt_max	)	dailycnt_max	,
avg(	daycnt	)	daycnt	,
avg(	monthlycnt_min	)	monthlycnt_min	,
avg(	monthlycnt_avg	)	monthlycnt_avg	,
avg(	monthlycnt_max	)	monthlycnt_max	,
avg(	monthcnt	)	monthcnt
from hcaadvaph_wk_playground.call_cmcl_sample3_122018_ccp_sc_population
group by hcid;

create table hcaadvaph_wk_playground.claim2_linkcall_122018_ccp_sc_population_provider_sa as
select a.*,
call_target ,
familysize 	,
age_min 	,
age_max 	,
age_avg 	,
agesmaller10_cnt	,
ageolder65_cnt	,
male_cnt	,
clmdaygap_avg	,
clmdaygap_min	,
clmdaygap_max	,
txnmy_cnt	,
adjrsn_cnt	,
adjtype_cnt	,
pos_cnt	,
cpt_cnt	,
clm_within1month	,
clm_within2month	,
clm_within3month	,
clm_within6month	,
paid_amt_sum_1month	,
paid_amt_max_1month	,
paid_amt_min_1month	,
paid_amt_sum_3month	,
paid_amt_max_3month	,
paid_amt_min_3month	,
paid_amt_sum_6month	,
paid_amt_max_6month	,
paid_amt_min_6month	,
paid_amt_sum_2month	,
paid_amt_max_2month	,
paid_amt_min_2month	,
oop_amt_sum_1month	,
oop_amt_max_1month	,
oop_amt_min_1month	,
oop_amt_sum_3month	,
oop_amt_max_3month	,
oop_amt_min_3month	,
oop_amt_sum_6month	,
oop_amt_max_6month	,
oop_amt_min_6month	,
oop_amt_sum_2month	,
oop_amt_max_2month	,
oop_amt_min_2month	,
ercnt_1month	,
ercnt_3month	,
ercnt_6month	,
ercnt_2month	,
er_related_1month	,
er_related_3month	,
er_related_6month	,
er_related_2month	,
diffst_1month	,
diffst_3month	,
diffst_6month	,
diffst_2month	,
oon_1month	,
oon_3month	,
oon_6month	,
oon_2month	,
--dnd_1month	,
--dnd_3month	,
--dnd_6month	,
--dnd_2month	,
prmry_mdcr_1month	,
prmry_mdcr_3month	,
prmry_mdcr_6month	,
prmry_mdcr_2month	,
call_within1month	,
call_within2month	,
call_within3month	,
daygap_small	,
week_id	,
--reason_category	,
day_int	,
weeklycnt_min	,
weeklycnt_avg	,
weeklycnt_max	,
weekcnt	,
dailycnt_min	,
dailycnt_avg	,
dailycnt_max	,
daycnt	,
monthlycnt_min	,
monthlycnt_avg	,
monthlycnt_max	,
monthcnt
from hcaadvaph_wk_playground.claim_linkcall_122018_ccp_sc_population as a
inner join hcaadvaph_wk_playground.claim_linkcall_hcid_122018_ccp_sc_population b
on trim(a.hcid)=trim(b.hcid);

drop table if exists hcaadvaph_wk_playground.claim2_linkcall_122018_ccp_sc_population_test01_provider_sa;
create table hcaadvaph_wk_playground.claim2_linkcall_122018_ccp_sc_population_test01_provider_sa as

with clm as (
select
clm_adjstmnt_key
,	src_billg_tax_id_type_cd
,	src_billg_tax_id
,	src_billg_prov_id
,	src_billg_prov_id_type_cd
,	src_prov_natl_prov_id
,	rndrg_prov_id
,	clm_sor_cd
,	clm_nbr
,	prncpl_diag_cd
,	othr_diag_1_cd
,	othr_diag_2_cd
,	othr_diag_3_cd
,	srvc_rndrg_type_cd
,	prmry_carr_rspnsbly_cd
,	clm_reimb_mthd_cd
,	src_grp_nbr
,	src_prchsr_org_nm
,	src_sbscrbr_st_cd
,	src_mbr_zip_cd
,	clm_disp_cd
,	clm_its_host_cd
,	clm_adjstmnt_nbr
,	adjdctn_type_cd
,	clm_rcvd_dt
,	inn_cd
,	parg_stts_cd
,	clm_nasco_par_cd
,	adjstmnt_rsn_cd
,	auto_or_manl
,	src_mbr_brth_dt
,	mbr_gndr_cd
,	mcid
,	mbr_age
,	txnmy_cd
,	new_state
,	mbr_st_cd
,	mbr_zip_cd
,	lob
,	inq_cnt
, claim_target
, rcvd_dt as call_rcd_date
, src_pay_actn_cd
, familysize as mem_familysize
, age_min as mem_age_min
, age_max as mem_age_max
, age_avg as mem_age_avg
, agesmaller10_cnt as mem_agesmaller10_cnt
, ageolder65_cnt as mem_ageolder65_cnt
, male_cnt as mem_male_cnt
, clmdaygap_avg as mem_clmdaygap_avg
, clmdaygap_min as mem_clmdaygap_min
, clmdaygap_max as mem_clmdaygap_max
, txnmy_cnt as mem_txnmy_cnt
, adjrsn_cnt as mem_adjrsn_cnt
, adjtype_cnt as mem_adjtype_cnt
, pos_cnt as mem_pos_cnt
, cpt_cnt as mem_cpt_cnt
, clm_within1month as mem_clm_within1month
, clm_within2month as mem_clm_within2month
, clm_within3month as mem_clm_within3month
, clm_within6month as mem_clm_within6month
, paid_amt_sum_1month as mem_paid_amt_sum_1month
, paid_amt_max_1month as mem_paid_amt_max_1month
, paid_amt_min_1month as mem_paid_amt_min_1month
, paid_amt_sum_3month as mem_paid_amt_sum_3month
, paid_amt_max_3month as mem_paid_amt_max_3month
, paid_amt_min_3month as mem_paid_amt_min_3month
, paid_amt_sum_6month as mem_paid_amt_sum_6month
, paid_amt_max_6month as mem_paid_amt_max_6month
, paid_amt_min_6month as mem_paid_amt_min_6month
, paid_amt_sum_2month as mem_paid_amt_sum_2month
, paid_amt_max_2month as mem_paid_amt_max_2month
, paid_amt_min_2month as mem_paid_amt_min_2month
, oop_amt_sum_1month as mem_oop_amt_sum_1month
, oop_amt_max_1month as mem_oop_amt_max_1month
, oop_amt_min_1month as mem_oop_amt_min_1month
, oop_amt_sum_3month as mem_oop_amt_sum_3month
, oop_amt_max_3month as mem_oop_amt_max_3month
, oop_amt_min_3month as mem_oop_amt_min_3month
, oop_amt_sum_6month as mem_oop_amt_sum_6month
, oop_amt_max_6month as mem_oop_amt_max_6month
, oop_amt_min_6month as mem_oop_amt_min_6month
, oop_amt_sum_2month as mem_oop_amt_sum_2month
, oop_amt_max_2month as mem_oop_amt_max_2month
, oop_amt_min_2month as mem_oop_amt_min_2month
, ercnt_1month as mem_ercnt_1month
, ercnt_3month as mem_ercnt_3month
, ercnt_6month as mem_ercnt_6month
, ercnt_2month as mem_ercnt_2month
, er_related_1month as mem_er_related_1month
, er_related_3month as mem_er_related_3month
, er_related_6month as mem_er_related_6month
, er_related_2month as mem_er_related_2month
, diffst_1month as mem_diffst_1month
, diffst_3month as mem_diffst_3month
, diffst_6month as mem_diffst_6month
, diffst_2month as mem_diffst_2month
, oon_1month as mem_oon_1month
, oon_3month as mem_oon_3month
, oon_6month as mem_oon_6month
, oon_2month as mem_oon_2month
, prmry_mdcr_1month as mem_prmry_mdcr_1month
, prmry_mdcr_3month as mem_prmry_mdcr_3month
, prmry_mdcr_6month as mem_prmry_mdcr_6month
, prmry_mdcr_2month as mem_prmry_mdcr_2month
, call_within1month as mem_call_within1month
, call_within2month as mem_call_within2month
, call_within3month as mem_call_within3month
, daygap_small as mem_daygap_small
, week_id as mem_week_id
, day_int as mem_day_int
, weeklycnt_min as mem_weeklycnt_min
, weeklycnt_avg as mem_weeklycnt_avg
, weeklycnt_max as mem_weeklycnt_max
, weekcnt as mem_weekcnt
, dailycnt_min as mem_dailycnt_min
, dailycnt_avg as mem_dailycnt_avg
, dailycnt_max as mem_dailycnt_max
, daycnt as mem_daycnt
, monthlycnt_min as mem_monthlycnt_min
, monthlycnt_avg as mem_monthlycnt_avg
, monthlycnt_max as mem_monthlycnt_max
, monthcnt as mem_monthcnt
from hcaadvaph_wk_playground.claim2_linkcall_122018_ccp_sc_population
group by
clm_adjstmnt_key
,	src_billg_tax_id_type_cd
,	src_billg_tax_id
,	src_billg_prov_id
,	src_billg_prov_id_type_cd
,	src_prov_natl_prov_id
,	rndrg_prov_id
,	clm_sor_cd
,	clm_nbr
,	prncpl_diag_cd
,	othr_diag_1_cd
,	othr_diag_2_cd
,	othr_diag_3_cd
,	srvc_rndrg_type_cd
,	prmry_carr_rspnsbly_cd
,	clm_reimb_mthd_cd
,	src_grp_nbr
,	src_prchsr_org_nm
,	src_sbscrbr_st_cd
,	src_mbr_zip_cd
,	clm_disp_cd
,	clm_its_host_cd
,	clm_adjstmnt_nbr
,	adjdctn_type_cd
,	clm_rcvd_dt
,	inn_cd
,	parg_stts_cd
,	clm_nasco_par_cd
,	adjstmnt_rsn_cd
,	auto_or_manl
,	src_mbr_brth_dt
,	mbr_gndr_cd
,	mcid
,	mbr_age
,	txnmy_cd
,	new_state
,	mbr_st_cd
,	mbr_zip_cd
,	lob
,	inq_cnt
, claim_target
, rcvd_dt
, src_pay_actn_cd
, familysize
, age_min
, age_max
, age_avg
, agesmaller10_cnt
, ageolder65_cnt
, male_cnt
, clmdaygap_avg
, clmdaygap_min
, clmdaygap_max
, txnmy_cnt
, adjrsn_cnt
, adjtype_cnt
, pos_cnt
, cpt_cnt
, clm_within1month
, clm_within2month
, clm_within3month
, clm_within6month
, paid_amt_sum_1month
, paid_amt_max_1month
, paid_amt_min_1month
, paid_amt_sum_3month
, paid_amt_max_3month
, paid_amt_min_3month
, paid_amt_sum_6month
, paid_amt_max_6month
, paid_amt_min_6month
, paid_amt_sum_2month
, paid_amt_max_2month
, paid_amt_min_2month
, oop_amt_sum_1month
, oop_amt_max_1month
, oop_amt_min_1month
, oop_amt_sum_3month
, oop_amt_max_3month
, oop_amt_min_3month
, oop_amt_sum_6month
, oop_amt_max_6month
, oop_amt_min_6month
, oop_amt_sum_2month
, oop_amt_max_2month
, oop_amt_min_2month
, ercnt_1month
, ercnt_3month
, ercnt_6month
, ercnt_2month
, er_related_1month
, er_related_3month
, er_related_6month
, er_related_2month
, diffst_1month
, diffst_3month
, diffst_6month
, diffst_2month
, oon_1month
, oon_3month
, oon_6month
, oon_2month
, prmry_mdcr_1month
, prmry_mdcr_3month
, prmry_mdcr_6month
, prmry_mdcr_2month
, call_within1month
, call_within2month
, call_within3month
, daygap_small
, week_id
, day_int
, weeklycnt_min
, weeklycnt_avg
, weeklycnt_max
, weekcnt
, dailycnt_min
, dailycnt_avg
, dailycnt_max
, daycnt
, monthlycnt_min
, monthlycnt_avg
, monthlycnt_max
, monthcnt
),

-- claim line ranked by billd_chrg_amt
clmrk as (
select
clm_adjstmnt_key
, src_eob_cd
,	clm_line_nbr
,	inc_yr
,	inc_mnth
,	clm_line_srvc_strt_dt
,	clm_line_srvc_end_dt
,	billd_srvc_unit_cnt
,	paid_srvc_unit_cnt
,	hlth_srvc_cd
,	billd_chrg_amt
,	alwd_amt
,	paid_amt
,	adjdctn_dt
,	icd_vrsn_cd
,	proc_mdfr_1_cd
,	proc_mdfr_2_cd
,	inpat_cd
,	clm_line_pa_nbr
,	place_of_srvc_cd
,	ffs_eqvlnt_amt
,	bnft_pkg_id
,	cob_svngs_amt
,	clm_line_reimb_mthd_cd
,	pn_id
,	fee_sched_id
,	prod_id
,	clm_line_stts_cd
,	ctgry_1_txt
,	ctgry_2_txt
, row_number() over(partition by (clm_adjstmnt_key) order by billd_chrg_amt desc) as cpt_cost_rank
from hcaadvaph_wk_playground.claim2_linkcall_122018_ccp_sc_population
),

-- aggregated claim line table
clmag as (
select
clm_adjstmnt_key
, sum(billd_chrg_amt) as sum_billd_chrg_amt
, sum(alwd_amt) as sum_alwd_amt
, sum(paid_amt) as sum_paid_amt
, count(*) as count_claim_line
from hcaadvaph_wk_playground.claim2_linkcall_122018_ccp_sc_population
group by clm_adjstmnt_key
),

-- join table
clmjoin as (
select clm.*
, cr1.src_eob_cd as c1_src_eob_cd
, cr1.clm_line_nbr as c1_clm_line_nbr
, cr1.inc_yr as c1_inc_yr
, cr1.inc_mnth as c1_inc_mnth
, cr1.clm_line_srvc_strt_dt as c1_clm_line_srvc_strt_dt
, cr1.clm_line_srvc_end_dt as c1_clm_line_srvc_end_dt
, cr1.billd_srvc_unit_cnt as c1_billd_srvc_unit_cnt
, cr1.paid_srvc_unit_cnt as c1_paid_srvc_unit_cnt
, cr1.hlth_srvc_cd as c1_hlth_srvc_cd
, cr1.billd_chrg_amt as c1_billd_chrg_amt
, cr1.alwd_amt as c1_alwd_amt
, cr1.paid_amt as c1_paid_amt
, cr1.adjdctn_dt as c1_adjdctn_dt
, cr1.icd_vrsn_cd as c1_icd_vrsn_cd
, cr1.proc_mdfr_1_cd as c1_proc_mdfr_1_cd
, cr1.proc_mdfr_2_cd as c1_proc_mdfr_2_cd
, cr1.inpat_cd as c1_inpat_cd
, cr1.clm_line_pa_nbr as c1_clm_line_pa_nbr
, cr1.place_of_srvc_cd as c1_place_of_srvc_cd
, cr1.ffs_eqvlnt_amt as c1_ffs_eqvlnt_amt
, cr1.bnft_pkg_id as c1_bnft_pkg_id
, cr1.cob_svngs_amt as c1_cob_svngs_amt
, cr1.clm_line_reimb_mthd_cd as c1_clm_line_reimb_mthd_cd
, cr1.pn_id as c1_pn_id
, cr1.fee_sched_id as c1_fee_sched_id
, cr1.prod_id as c1_prod_id
, cr1.clm_line_stts_cd as c1_clm_line_stts_cd
, cr1.ctgry_1_txt as c1_ctgry_1_txt
, cr1.ctgry_2_txt as c1_ctgry_2_txt

, clmag.sum_billd_chrg_amt
, clmag.sum_alwd_amt
, clmag.sum_paid_amt
, clmag.count_claim_line

, cr2.hlth_srvc_cd as c2_hlth_srvc_cd
, cr3.hlth_srvc_cd as c3_hlth_srvc_cd
from clm

left join (select * from clmrk where clmrk.cpt_cost_rank = 1) as cr1
on clm.clm_adjstmnt_key = cr1.clm_adjstmnt_key

left join clmag
on clm.clm_adjstmnt_key = clmag.clm_adjstmnt_key

left join (select * from clmrk where clmrk.cpt_cost_rank = 2) as cr2
on clm.clm_adjstmnt_key = cr2.clm_adjstmnt_key

left join (select * from clmrk where clmrk.cpt_cost_rank = 3) as cr3
on clm.clm_adjstmnt_key = cr3.clm_adjstmnt_key
)

select * from clmjoin;

set APPX_COUNT_DISTINCT=true;

------------------------- claim level input add NLP ------------------------------
--Inserted 253551 row(s)
drop table if exist hcaadvaph_wk_playground.cc_call_notes_topic_feature_201812_hcid_provider_sa;
create table hcaadvaph_wk_playground.cc_call_notes_topic_feature_201812_hcid_provider_sa  as
select trim(hcid) hcid,
avg(	t_1	)	t_1	,
avg(	t_2	)	t_2	,
avg(	t_3	)	t_3	,
avg(	t_4	)	t_4	,
avg(	t_5	)	t_5	,
avg(	t_6	)	t_6	,
avg(	t_7	)	t_7	,
avg(	t_8	)	t_8	,
avg(	t_9	)	t_9	,
avg(	t_10	)	t_10	,
avg(	t_11	)	t_11
from
(select trim(hcid) hcid,
t_1	,
t_2	,
t_3	,
t_4	,
t_5	,
t_6	,
t_7	,
t_8	,
t_9	,
t_10,
t_11 from hcaadvaph_wk_playground.cc_call_notes_topic_feature_201811_20190328 where hcid is not null) a group by hcid;


drop table if exists hcaadvaph_wk_playground.mcid_onehcid_122018_provider_sa;
create table hcaadvaph_wk_playground.mcid_onehcid_122018_provider_sa as
select mcid, hcid, hcid_cnt from
(select mcid, hcid, count(*) over (partition by mcid) hcid_cnt
from
(select distinct mcid, hcid
from hcaadvaph_wk_playground.hcid_cmcl_sample_122018_ccp_sc_population where hcid is not null and mcid is not null) a
) b
where b.hcid_cnt=1;

drop table if exists hcaadvaph_wk_playground.claim2_linkcall_122018_ccp_sc_population_test02_provider_sa;
create table hcaadvaph_wk_playground.claim2_linkcall_122018_ccp_sc_population_test02_provider_sa as
select b.hcid, a.*,
t_1	,
t_2	,
t_3	,
t_4	,
t_5	,
t_6	,
t_7	,
t_8	,
t_9	,
t_10,
t_11
from hcaadvaph_wk_playground.claim2_linkcall_122018_ccp_sc_population_test01_provider_sa a
inner join
hcaadvaph_wk_playground.mcid_onehcid_122018 b
on trim(cast(a.mcid as varchar))=trim(cast(b.mcid as varchar))
left join
hcaadvaph_wk_playground.cc_call_notes_topic_feature_201812_hcid c
on trim(b.hcid)=trim(c.hcid);

select count() from hcaadvaph_wk_plhcaadvaph_wk_playground.claim2_linkcall_122018_ccp_sc_population_test01_provider_sa

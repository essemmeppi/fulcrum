import csv, html, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parents[3]/'work'/'cdit-export'
OUT.mkdir(parents=True,exist_ok=True)
sources={}
def src(id,url,title,scope,version,depth,access='read'):
    sources[id]=dict(id=id,url=url,title=title,scope=scope,version=version,depth=depth,access=access,checked_at='2026-10-31',independence_group=id)
src('norms544','https://legislatie.just.ro/Public/DetaliiDocument/256296','HG 123/2002 implementing norms','national','Consolidation 28 June 2022; inspected amendments to Arts.20-27 and 34','internal_legal_procedure')
src('petitions27','https://legislatie.just.ro/Public/DetaliiDocument/290817','OG 27/2002 petitions','national','Consolidation 1 December 2024, including harassment exception','internal_legal_procedure')
src('transparency52','https://legislatie.just.ro/public/detaliidocument/41571','Law 52/2003 transparency','national','Consolidation displayed 2 March 2022','legal_procedure')
src('tax207','https://static.anaf.ro/static/10/Anaf/legislatie/Cod_Procedura_Fiscala_2023.htm','Law 207/2015 fiscal procedure','national','Page header says updated through OUG 38/2026; URL year is not version date','legal_procedure')
src('grant-reg2025','https://www.detatm.ro/wp-content/uploads/2025/05/REGULAMENT-2025.pdf','Deta grant regulation, HCL 65/29 April 2025','Deta','Adopted 2025 edition; not assumed applicable to post-amendment 2026 calls','internal_local_procedure')
src('grant-eval2025','https://www.detatm.ro/wp-content/uploads/2025/05/Anexa-9-Procedura-de-conformitate-evaluare-si-selectie-2025.pdf','Deta grant conformity and evaluation annex','Deta','2025 edition; same rule package as grant regulation','internal_local_procedure')
sources['grant-eval2025']['independence_group']='grant-reg2025'
src('grant-report2025','https://www.detatm.ro/wp-content/uploads/2026/01/Raport-anual-2025-1.pdf','Deta annual grant report 2025','Deta','Report year 2025; uploaded January 2026','reported_outputs')
src('transparency-local','https://www.detatm.ro/info-interes-public/transparenta-decizionala/','Deta consultation register','Deta','Dated entries include 2026; individual notices not all read','local_index')
src('transparency-report2025','https://www.detatm.ro/wp-content/uploads/2026/03/Raport-anual-privind-transparenta-decizionala-2025.pdf','Deta transparency report 2025','Deta','Report year 2025; uploaded March 2026','self_reported_statistics')
src('tax-local','https://www.detatm.ro/info-interes-public/formulare-si-acte-necesare/taxe-si-impozite/','Deta tax forms','Deta','Undated; observed on screen date','forms_index')
src('catalogue','https://deta.regista.ro/formulare','Deta electronic catalogue','Deta','Undated; individual forms gated by login','catalogue')
src('foi-local','https://www.detatm.ro/info-interes-public/legea-544-2001/','Deta information-access page','Deta','Undated; current personnel designation unconfirmed','local_index')
src('urban-local','https://www.detatm.ro/info-interes-public/formulare-si-acte-necesare/urbanism/','Deta urbanism forms','Deta','Undated; references older law; form existence is not current legal validity','forms_index')
src('agricultural-local','https://www.detatm.ro/info-interes-public/formulare-si-acte-necesare/agricol/','Deta agricultural forms','Deta','Undated','forms_index')
src('hr-local','https://www.detatm.ro/info-interes-public/concursuri-si-salarizare/','Deta recruitment publications','Deta','2026 index inspected; mapped completed sequence is explicitly June 2021','historical_reported_sequence')
src('org-local','https://www.detatm.ro/primarie/structura-organizatorica/','Deta organisation','Deta','Organigram links through 2024; 2026 reorganisation draft found separately','organisation_index')
src('procurement-local','https://www.detatm.ro/info-interes-public/achizitii-publice/achizitii-publice-2026/','Deta 2026 procurement','Deta','2026 catering and site-supervision notices','local_index')
src('catering-norms','https://www.detatm.ro/wp-content/uploads/2026/01/2.-Norme-interne-Atribuire-contract-servicii-catering.pdf','Deta catering internal norms','Deta','January 2026 scan, 8 pages','untranscribed_scan','pdf_accessible_text_unavailable')
src('health-education','https://www.detatm.ro/info-interes-public/achizitii-publice/achizitii-publice-2026/','School catering / recovery-centre procurement leads','Deta','2026; service execution not read','index_only')
sources['health-education']['independence_group']='procurement-local'
src('waste-local','https://www.detatm.ro/','Deta waste-service operator notice','Deta','Search result only this pass; not process evidence','lead','search_lead')
src('civil-law119','https://legislatie.just.ro/Public/DetaliiDocument/8624','Law 119/1996 civil status','national','Portal displays consolidation 6 July 2026; operative sections failed to open','lead','partial_header_only')
src('budget-local','https://www.detatm.ro/info-interes-public/bugetul-si-executie/','Deta budgets','Deta','Search lead; financial execution not reconstructed','lead','search_lead')
src('deta-heating','https://www.detatm.ro/info-interes-public/formulare-si-acte-necesare/asistenta-sociala/','Deta social-benefit and housing forms','Deta','Heating guidance explicitly 2021-22; other forms undated','historical_guidance_and_forms')
src('grant-law350','https://legislatie.just.ro/Public/DetaliiDocument/66812','Law 350/2005 grants','national','Portal note: Law91 of 10 June 2026 applies to procedures initiated after entry into force; operative amendment not fully inspected','version_note_only','partial_header_read')

maps=[]
def process(id,name,family,level,scope,rows,links=(),rules=(),questions=(),local_evidence=()):
    claims=[]
    for n,(statement,actor,source,locator) in enumerate(rows,1):
        claims.append(dict(id=f'{id}:{n}',statement=statement,actor=actor,actor_scope='local_document_role' if sources[source]['scope']=='Deta' else 'national_legal_role',evidence=[dict(source_id=source,locator=locator)],evidence_check='source_located_manual_read',quote_verified=None,automation='unknown',local_execution_validated=False))
    edges=[dict(source=f'{id}:{a}',target=f'{id}:{b}',condition=condition,evidence=dict(source_id=source,locator=locator)) for a,b,condition,source,locator in links]
    maps.append(dict(id=id,name=name,family=family,evidence_level=level,temporal_scope=scope,claims=claims,explicit_links=edges,rules=[dict(statement=s,source_id=source,locator=loc) for s,source,loc in rules],local_evidence=list(local_evidence),open_questions=list(questions),complete=False,operationally_validated=False))

process('foi','Public-information request handling','information-access','national_procedure_with_local_channel','Amended norms; Deta actual routing unvalidated',[
('Receive request','public_information_role','norms544','Art.20(1)'),
('Register request immediately','public_information_role','norms544','Art.20(4)'),
('Communicate registration number and date','public_information_role','norms544','Art.20(5)'),
('Assess information-access scope','public_information_role','norms544','Art.21(1)'),
('Reclassify qualifying requests as petitions','public_information_role','norms544','Art.21(2)'),
('Notify requests outside both regimes','unknown','norms544','Art.21(3)'),
('Direct requester to published information','public_information_role','norms544','Art.21(4)-(5)'),
('Route request to information-holding units','public_information_role','norms544','Art.22(1)'),
('Check exemptions','competent_unit','norms544','Art.22(1)-(2)'),
('Anonymise exempt material in mixed records','unknown','norms544','Art.22(2^1)'),
('Receive unit response','public_information_role','norms544','Art.23(1)'),
('Draft reply','public_information_role','norms544','Art.23(1)'),
('Register reply','unknown','norms544','Art.23(2)'),
('Send reply','unknown','norms544','Art.23(2)'),
('Forward out-of-competence request','public_information_role','norms544','Art.24'),
('Notify external forwarding','public_information_role','norms544','Art.24'),
],[(2,3,'after registration','norms544','Art.20(5)'),(2,4,'after receipt and registration','norms544','Art.21(1)'),(4,5,'qualifies as petition','norms544','Art.21(2)'),(4,6,'outside both regimes','norms544','Art.21(3)'),(4,7,'already published','norms544','Art.21(4)'),(8,9,'not proactively published','norms544','Art.22(1)'),(11,12,'unit response received','norms544','Art.23(1)')],
[('10-day reply / extension notice; 30-day extended reply; 5-day refusal; deadline calculation in Art.16(2)-(3).','norms544','Art.16'),('Postal registration number communicated on request; immediate verbal answers have a separate branch.','norms544','Art.20(3),(5)')],
['Who owns each Deta desk task and signs the reply?','Do email, paper and Regista share a register?','What local software and redaction review are used?'],['catalogue','foi-local'])

process('foi-complaint','Information-access administrative complaints','information-access','national_procedure_with_local_channel','Amended norms; no Deta commission mandate read',[
('Submit complaint to institution head','requester','norms544','Art.32-33'),
('Receive complaint','review_commission','norms544','Art.35(2)(a)'),
('Analyse complaint','review_commission','norms544','Art.35(2)(a)'),
('Conduct administrative investigation','review_commission','norms544','Art.35(2)(b)'),
('Determine merits','review_commission','norms544','Art.35(2)(c)'),
('Propose remedy and disciplinary referral when justified','review_commission','norms544','Art.35(2)(d)'),
('Draft reasoned reply','review_commission','norms544','Art.35(2)(e);34'),
('Send reply','review_commission','norms544','Art.35(2)(e);34'),
],[],[('Complaint within 30 days of learning of refusal; reply within 15 days of registration regardless of outcome.','norms544','Art.33-34')],['Which Deta disposition establishes the commission?','What is the local complaint register and recusal process?'],['catalogue','foi-local'])

process('petitions','Petition handling','petitions','national_procedure_with_local_intake_lead','Consolidated 1 December 2024; local assignment unvalidated',[
('Receive petition','public_relations','petitions27','Art.6(1)'),
('Register petition','public_relations','petitions27','Art.6(1)'),
('Forward to specialist unit with reply deadline','public_relations','petitions27','Art.6(2)'),
('Assign petition to specialist staff','specialist_unit_head','petitions27','Art.12(1)'),
('Investigate and resolve assigned petition','specialist_staff','petitions27','Art.5;12(2)'),
('Monitor timely reply preparation','public_relations','petitions27','Art.6(3)'),
('Sign reply','institution_head_or_delegate','petitions27','Art.13'),
('Co-sign reply','specialist_unit_head','petitions27','Art.13'),
('Dispatch reply','public_relations','petitions27','Art.6(4)'),
('Archive petition','public_relations','petitions27','Art.6(4)'),
('Forward misdirected petition and notify petitioner','public_relations','petitions27','Art.6^1'),
('Combine duplicate pending petitions','unknown','petitions27','Art.10(1)'),
('Close identical repeat after response','unknown','petitions27','Art.10(2)'),
('Route anonymous harassment allegations for specialised analysis','harassment_role_or_commission','petitions27','Art.7(2)-(4)'),
],[(2,3,'registered petition','petitions27','Art.6(2)'),(3,4,'received by specialist unit','petitions27','Art.12(1)'),(4,5,'staff assignment','petitions27','Art.12(2)')],
[('Ordinary reply: 30 days; justified extension up to 15, or 30 for energy/gas, with prior notification.','petitions27','Art.8-9'),('Anonymous petitions are generally closed, but harassment exception added in 2024 must be handled.','petitions27','Art.7'),('Reply includes legal basis; subject of complaint and subordinates cannot resolve it.','petitions27','Art.11;13')],
['Which Deta intake is a petition rather than FOI or a service application?','Who is delegated to sign?','How are recusal and harassment exceptions routed?'],['catalogue','org-local'])

process('consultation','Consulting on draft normative acts','normative-consultation','national_procedure_with_local_report','Law 52 consolidation displayed 2022; local report 2025',[
('Publish draft notice and supporting material','authority','transparency52','Art.7(1)-(2)'),
('Send drafts to registered recipients','authority','transparency52','Art.7(1)'),
('Receive written recommendations','designated_civil_society_role','transparency52','Art.7(7)'),
('Record recommendations in register','unknown','transparency52','Art.7(5)'),
('Organise debate when qualifying written request requires it','authority','transparency52','Art.7(9)-(10)'),
('Analyse all recommendations','authority','transparency52','Art.7(12)'),
('Finalise draft after consultation','unknown','transparency52','Art.7(8)'),
('Send finalised draft for review','authority','transparency52','Art.7(8)'),
('Publish debate material and final adopted text','authority','transparency52','Art.7(10)(d)'),
('Explain non-adoption of written recommendations','authority','transparency52','Art.12(3)'),
],[(7,8,'only after finalisation','transparency52','Art.7(8)')],
[('Ordinary notice at least 30 working days before review; at least 10 calendar days for written recommendations.','transparency52','Art.7(2),(4)'),('Urgent circumstances can shorten ordinary period; qualifying debate request and disclosure deadlines remain distinct rules.','transparency52','Art.7(9)-(13)')],
['Which local employee maintains the register?','Are website, office and media notices synchronised?','What evidence supports urgency exceptions?'],['transparency-local','transparency-report2025'])

process('public-meetings','Public meeting participation and minutes','public-meetings','national_procedure_with_local_report','Law 52; local 2025 reported meeting activity',[
('Publish meeting notice and agenda','civil_society_role','transparency52','Art.8(1)-(2)'),
('Notify interested prior contributors','civil_society_role','transparency52','Art.8(1)(b),(2)'),
('Manage attendance priority within capacity','meeting_chair','transparency52','Art.8(3)-(4)'),
('Give participants opportunity to speak','meeting_chair','transparency52','Art.9'),
('Adopt administrative decisions','competent_authority','transparency52','Art.10(1)'),
('Prepare minutes','authority','transparency52','Art.12(1)'),
('Archive minutes','authority','transparency52','Art.12(1)'),
('Publish minutes and voting record where applicable','authority','transparency52','Art.11'),
],[],[('Meeting announcement at least 3 days beforehand.','transparency52','Art.8(1)(a)')],
['Obtain council ROF for voting, agenda approval and legal review.','Who prepares and checks minutes?'],['transparency-report2025'])

process('fiscal-certificate','Local fiscal certificate','tax-certificate','national_rules_with_local_forms','ANAF displayed update through OUG 38/2026',[
('Request local fiscal certificate','taxpayer_or_authorised_requester','tax207','Art.159(1);160(1)'),
('Issue certificate using local tax-claims records','local_fiscal_authority','tax207','Art.159(2)'),
('Present certificate where required','taxpayer','tax207','Art.159(4)-(5)'),
],[],[('Issuance within two working days; validity 30 days.','tax207','Art.159(3)'),('Third-party consent, succession and electronic-verification exceptions require separate variants.','tax207','Art.159(5)-(7);160')],
['Who checks identity, consent and discrepancies locally?','Is issuance actually automated?','Which current local form and signature procedure apply?'],['tax-local','catalogue'])

process('tax-refund','Local tax overpayment refund','tax-refund','national_rules_with_local_form','ANAF displayed update through OUG 38/2026; local form listed',[
('Request refund of undue payment','taxpayer','tax207','Art.168(1)'),
('Offset outstanding obligations before refund','competent_fiscal_authority','tax207','Art.168(8);167'),
('Communicate offset decision','competent_fiscal_authority','tax207','Art.167(8)'),
('Refund remaining eligible sum','competent_fiscal_authority','tax207','Art.168(1),(8)'),
],[(2,4,'outstanding obligations offset first','tax207','Art.168(8)')],[],
['Obtain local refund procedure and current form fields.','Who establishes entitlement and approves payment?','How is treasury execution reconciled?'],['tax-local'])

process('grant-award','Local nonprofit grant selection and award','local-grants','local_operational_regulation','2025 programme edition; 2026 legal amendment unresolved',[
('Publish annual programme','organising_authority','grant-reg2025','Art.17(a)'),
('Publish call and documentation','organising_authority','grant-reg2025','Art.17(b)'),
('Submit application at registry','applicant','grant-reg2025','Art.17(c);18'),
('Forward registered documents to commission secretariat','unknown','grant-reg2025','Art.32'),
('Return late submissions','commission_secretariat','grant-reg2025','Art.32'),
('Check conformity','evaluation_commission','grant-eval2025','p.1 conformity'),
('Request eligibility evidence if needed','evaluation_commission','grant-eval2025','p.1 footnote'),
('Score eligible proposals','evaluation_commission','grant-reg2025','Art.33'),
('Re-evaluate excessive scoring differences','evaluation_commission','grant-eval2025','p.2 footnote'),
('Submit winners minutes for endorsement','evaluation_commission','grant-reg2025','Art.34'),
('Communicate selection result','commission_secretary','grant-reg2025','Art.35'),
('Conclude funding contract','funding_authority_and_selected_applicant','grant-reg2025','Art.36'),
('Publish award notice','organising_authority','grant-reg2025','Art.17(i)'),
],[(1,2,'listed programme stages','grant-reg2025','Art.17(a)-(b)'),(3,4,'as registered','grant-reg2025','Art.32'),(4,5,'late','grant-reg2025','Art.32'),(6,8,'conformity passed','grant-eval2025','p.1 footnote'),(8,9,'score gap exceeds 10','grant-eval2025','p.2 footnote'),(11,12,'after result communication','grant-reg2025','Art.36')],
[('At least 65/100 points; scoring gap above 10 triggers re-evaluation.','grant-eval2025','p.2'),('Result communication within 10 days; contracting within 20 days of communication.','grant-reg2025','Art.35-36')],
['Resolve Art.17 result/endorsement ordering against Arts.34-35.','Obtain 2026 applicable call and rules after national amendment.','Who records checks and manages conflicts of interest?'],['grant-reg2025','grant-eval2025','grant-report2025'])

process('grant-settlement','Grant reporting, instalments and control','local-grants','local_operational_regulation','2025 programme edition; payment desk detail incomplete',[
('Submit intermediate report and supporting evidence','beneficiary','grant-reg2025','Art.40;43'),
('Provide next instalment after justification','funding_authority','grant-reg2025','Art.40'),
('Submit final project report','beneficiary','grant-reg2025','Art.43'),
('Withhold final settlement for missing timely report','unknown','grant-reg2025','Art.44'),
('Exercise financial control','municipal_specialist_staff','grant-reg2025','Art.48'),
('Audit use of funds','specialist_units_or_auditors_or_commission','grant-reg2025','Art.49'),
('Retain complete project file','beneficiary','grant-reg2025','Art.49'),
],[(1,2,'prior tranche justified; first tranche excepted','grant-reg2025','Art.40')],
[('Advance capped at 50%; final reporting within 15 days of completion and by 15 December; retain file five years.','grant-reg2025','Art.41-43;49')],
['Who validates evidence and approves each payment?','What treasury/accounting steps intervene?','What are the recovery and complaint procedures?'],['grant-report2025'])

process('recruitment-history','Completed municipal recruitment sequence','recruitment','historical_local_output_sequence','One June 2021 municipal competition; not current recruitment rules',[
('Select applications','unknown','hr-local','17 June 2021 final report: selection 4 June'),
('Conduct written examination','unknown','hr-local','17 June 2021 final report: written 11 June'),
('Conduct interview','unknown','hr-local','17 June 2021 final report: interview 15 June'),
('Publish final result','unknown','hr-local','17 June 2021 final report'),
],[(1,2,'dated outputs 4 June then 11 June 2021','hr-local','17 June 2021 final report'),(2,3,'11 June then 15 June 2021','hr-local','17 June 2021 final report'),(3,4,'15 June then 17 June 2021','hr-local','17 June 2021 final report')],[],
['Read current 2026 vacancy notice and applicable recruitment law.','Which stages differ for civil servants and contractual employees?','What appeals and no-candidate branches apply?'],['hr-local'])

portfolio=dict(municipality='Deta',scope='CDIT member town hall; ADR Vest investment discovery',as_of='2026-10-31',baseline_commit='1e67353d1455dbedc5950ffe0fd3cfae5777c0ac',sources=list(sources.values()),workflows=maps,evidence_contract={
 'source_located_manual_read':'Researcher paraphrase tied to inspected passage; not independently quote-verified.',
 'no_closed_graph':'Only explicit supported links included; missing sequence is a question.',
 'automation':'Unknown throughout; legal permission is not observed implementation.',
 'law_vs_execution':'National legal roles remain national roles until mapped to local positions.',
 'independence':'Regulation and its annexes share an origin; output reports corroborate activity, not each desk step.',
 'completion':'All workflows partial and none validated by municipality. No recall percentage or all-process count claimed.'},
 statistics=[dict(source_id='grant-report2025',period='2025',measure='Listed funding contracts',value=11),dict(source_id='grant-report2025',period='2025',measure='Sum of listed allocations in lei',value=220000,method='Sum 20000+40000+15000+10000+15000+30000+8000+45000+9000+20000+8000; allocations, not audited disbursements'),dict(source_id='transparency-report2025',period='2025',measure='Publicly announced draft acts',value=130),dict(source_id='transparency-report2025',period='2025',measure='Public debates reported',value=4),dict(source_id='transparency-report2025',period='2025',measure='Public meetings reported',value=27),dict(source_id='transparency-report2025',period='2025',measure='Recommendations received reported',value=0)],
 unresolved_conflicts=[dict(subject='Information-access deadlines',finding='Older CNCAN copy uses working-day wording; amended Art.16 uses days with explicit calculation provisions.',resolution='Use amended norms as legal baseline; preserve old source as historical.'),dict(subject='Grant version',finding='Local HCL edition is 2025; national law portal signals Law 91/2026 applies to procedures started after its entry into force.',resolution='2025 map retained; no assumption of applicability to a new 2026 call.'),dict(subject='Grant ordering',finding='Art.17 lists communication before principal credit officer review; Arts.34-35 describe minutes to mayor and later notice.',resolution='Do not force endorsement/communication sequence; ask owner.'),dict(subject='Public-information annual report routing',finding='HG830/2022 includes conditional repeal of earlier reporting route once implementing order takes effect.',resolution='Do not configure annual-routing workflow until order applicability checked.'),dict(subject='Organisation',finding='2026 draft reorganisation is more recent than 2024 organigram links, but draft adoption not checked.',resolution='Draft does not supersede approved organisation by date alone.'),dict(subject='Fiscal code filename',finding='ANAF URL says 2023 but header reports OUG38/2026.',resolution='Record content version independently of filename.')])

# Reconcile expanded candidates with the initial portal inventory; do not equate a form or a department with a complete process.
old=list(csv.DictReader((ROOT/'deta-process-inventory.csv').open()))
inventory=[]
for r in old:
    inventory.append(dict(id=r['id'],family=r['provisional_family'],area=r['area'],basis='catalogue_entry',source_ids='catalogue',status='candidate',workflow_ids=''))
extra=[
('tax-refund','Local tax overpayment refund','revenue_business','tax-local'),('tax-exemption','Tax exemption applications','revenue_business','tax-local'),('advertising-tax','Advertising tax declaration','revenue_business','tax-local'),('moped-registration','Moped registration','revenue_business','tax-local'),
('onsite-wastewater','Individual wastewater-system registration','land_environment','urban-local'),('building-tax-regularisation','Construction fee regularisation','land_environment','urban-local'),('building-completion-certificate','Building existence/completion certificate','land_environment','urban-local'),('building-stage-certificate','Construction stage certificate','land_environment','urban-local'),('building-removal-certificate','Building removal certificate','land_environment','urban-local'),('land-allocation','Free land / ownership applications','land_environment','urban-local'),('utility-connection','Utility connection request','land_environment','urban-local'),('street-opening','Street-opening request','land_environment','urban-local'),('prefect-order','Prefect land-order request','land_environment','urban-local'),('farmland-sale','Farmland sale publication and acceptance','land_environment','agricultural-local'),
('petitions','Petitions','government_operations','catalogue'),('normative-consultation','Draft normative-act consultation','government_operations','transparency-local'),('public-meetings','Public meeting participation and minutes','government_operations','transparency-report2025'),('local-grants','Local nonprofit grants: award and settlement','government_operations','grant-reg2025'),('recruitment','Recruitment: civil-service / contractual variants','government_operations','hr-local'),('procurement','Procurement: catering / direct-purchase variants','government_operations','procurement-local'),('budget-cycle','Budget preparation and execution','government_operations','budget-local'),('civil-status','Civil-status services: birth/marriage/death/certificates','identity_rights','org-local'),('identity-documents','Identity-document services','identity_rights','org-local'),('social-housing','Social housing allocation','social_services','deta-heating'),('heating-aid','Heating aid and energy supplement','social_services','deta-heating'),('child-benefits','Child allowance / parental benefit intake','social_services','deta-heating'),('disability-intake','Disability assessment application intake','social_services','deta-heating'),('waste-service','Waste-service relationship with delegated operator','public_services','waste-local'),('school-meals','School meal service commissioning','public_services','health-education'),('recovery-centre','Health/social recovery-centre project procurement','public_services','health-education'),
]
for id,name,area,source in extra:
    inventory.append(dict(id=id,family=name,area=area,basis='index_or_form' if source not in ('grant-reg2025','transparency-report2025') else 'inspected_local_document',source_ids=source,status='candidate',workflow_ids=''))
for row in inventory:
    sheets=[m['id'] for m in maps if m['family']==row['id']]
    if sheets:row.update(status='partial_evidence_map',workflow_ids=';'.join(sheets))
# Separate enabling functions whose existence is plausible but whose actual workflow has not been inspected.
for id,name in [('payroll','Payroll'),('records-retention','Records retention and disposal'),('internal-audit','Internal audit'),('legal-casework','Legal casework'),('it-support','IT support and access management'),('civil-protection','Civil protection'),('municipal-assets','Municipal asset administration')]:
    inventory.append(dict(id=id,family=name,area='government_operations',basis='search_target_not_established_process',source_ids='org-local',status='unverified_search_target',workflow_ids=''))
with (ROOT/'deta-whole-hall-inventory.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(inventory[0]));w.writeheader();w.writerows(inventory)
(ROOT/'deta-portfolio.json').write_text(json.dumps(portfolio,ensure_ascii=False,indent=2)+'\n')
with (ROOT/'deta-review-sheet.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['workflow','claim_id','claim','legal_or_document_actor','source_url','locator','temporal_scope','we_do_this','differently','we_do_not','ask_person','reviewer','review_date'])
    for m in maps:
        for c in m['claims']:
            e=c['evidence'][0];w.writerow([m['name'],c['id'],c['statement'],c['actor'],sources[e['source_id']]['url'],e['locator'],m['temporal_scope'],'','','','','',''])

assert len({r['id'] for r in inventory})==len(inventory)
for row in inventory:
    for sid in row['source_ids'].split(';'):assert sid in sources
for m in maps:
    ids={c['id'] for c in m['claims']}
    for c in m['claims']:
        assert c['automation']=='unknown' and not c['local_execution_validated']
        for e in c['evidence']: assert e['source_id'] in sources and e['locator']
    for e in m['explicit_links']:assert e['source'] in ids and e['target'] in ids and e['evidence']['source_id'] in sources
    for r in m['rules']:assert r['source_id'] in sources
stats=dict(inventory_rows=len(inventory),evidence_backed_candidates=sum(r['basis']!='search_target_not_established_process' for r in inventory),search_targets=sum(r['basis']=='search_target_not_established_process' for r in inventory),workflow_sheets=len(maps),families_with_sheets=len({m['family'] for m in maps}),claims=sum(len(m['claims']) for m in maps),explicit_links=sum(len(m['explicit_links']) for m in maps),sources=len(sources),agency_validated=0)
portfolio['counts']=stats
(ROOT/'deta-portfolio.json').write_text(json.dumps(portfolio,ensure_ascii=False,indent=2)+'\n')

lines=['# Deta: municipal process evidence portfolio','','CDIT member town hall · ADR Vest strategy · 31 October 2026','',f"This pass identifies **{stats['evidence_backed_candidates']} provisional families/leads**, plus **{stats['search_targets']} enabling-function search targets**. It produces **{stats['workflow_sheets']} partial workflow sheets across {stats['families_with_sheets']} families**, with **{stats['claims']} source-located action claims** and **{stats['explicit_links']} explicit supported links**. None is municipality-validated. There is no defensible denominator for all municipal processes yet.",'','## Main findings','','The best local mapping candidate is now nonprofit grants: an adopted 2025 regulation, evaluation checklist, reporting/payment forms and a 2025 output report. The latter lists 11 contracts totalling 220,000 lei allocated; it does not independently validate each workflow step. Keep this map tied to the 2025 edition until the 2026 national amendment and local call have been reconciled.','','Information-access norms and petitions legislation provide internal legal routing and exceptions. Deta-specific actors, software, actual handling times and automation are still unknown. The 2024 petitions amendment adds an anonymous-harassment exception: old copies that close every anonymous petition miss a real branch.','','The 2025 transparency report records 130 publicly announced drafts, four debates and 27 public meetings, with zero recommendations reported. These are self-reported figures, not proof of participation quality or compliance. The PDF includes spreadsheet errors/odd layout; validate counts with the owner before using them for investment scoring.','','A 2026 catering procurement publishes internal norms, but they are an untranscribed scan. This is a high-priority acquisition lead, not an absence of internal guidance. Several department pages have only a title; other department pages carry unrelated repeated announcements. Navigation and boilerplate must not be extracted as workflow.','','## Coverage','', '| Area | Inspected evidence | Remaining gap |','|---|---|---|','| Social services | Historical local forms/intake pages | Current operating procedures and season rules |','| Revenue/business | Tax forms; amended fiscal procedure Art.159,167–168 | Local checks, signatures and payment execution |','| Identity/rights | Civil/identity units; Law119 consolidation header | Operative provisions and current local digital routing |','| Land/environment | Urbanism and agricultural form lists | Current law, procedures, permits and transfer variants |','| Public services | 2026 school-catering/recovery-centre procurement | Scanned norms, operator delivery boundaries |','| Government operations | Grants, consultations, meetings, recruitment, petitions | ROF, records schedule, enabling-process register |','','All six areas received a bounded check. This is not exhaustive search saturation, nor evidence that every service within an area was inspected.','','## Workflow sheets','']
for m in maps:
    lines += ['### '+m['name'],'', '**Evidence:** '+m['evidence_level']+'. **Time:** '+m['temporal_scope']+'.','', '| Claim | Actor in source | Evidence |','|---|---|---|']
    for c in m['claims']:
        e=c['evidence'][0];s=sources[e['source_id']]
        lines.append(f"| {c['id']}: {c['statement']} | {c['actor']} | [{e['locator']}]({s['url']}) |")
    if m['explicit_links']:
        lines += ['', '**Explicit partial order:**']
        lines += [f"- {e['source']} → {e['target']} ({e['condition']}; {e['evidence']['locator']})." for e in m['explicit_links']]
    if m['rules']:
        lines+=['','**Rules:**']+[f"- {r['statement']} [{r['locator']}]({sources[r['source_id']]['url']})" for r in m['rules']]
    lines+=['','**Owner review:**']+['- '+q for q in m['open_questions']]+['']
lines += ['## What each input added','','| Input | Observed contribution |','|---|---|','| Catalogue | Initial 29 form entries; 22 grouped candidates |','| Additional municipal form lists | Refunds, exemptions, construction regularisation, farmland and benefit leads absent from electronic catalogue |','| National procedural law | Information-access routing, petition assignment and exceptions, fiscal data/rules |','| Adopted local regulation | Registry-to-commission handoff, named local roles, award and settlement constraints |','| Annexes | Conformity checklist, scoring threshold and re-evaluation branch |','| Output reports | Local activity and reported scale; no proof of all desk steps |','| Internal scan | Publication lead needing OCR; zero workflow claims admitted |','','This is an analyst-produced evidence portfolio, not a new run of the LLM mapper. Claims have source URLs and locators; they have not been independently quote-verified. Counts measure extracted claims, not recall or accuracy. Do not import the sheets as executable workflows.','','## Meeting with Dan / ADR Vest','','1. Show the grant lifecycle as the strongest local example; show information access/petitions as common legal templates with local unknowns.','2. Ask CDIT for Deta or another willing member: current ROF, operational-procedure register, records schedule, software list and named owners. These establish the missing inventory denominator.','3. Validate two workflows with their owners and a few redacted cases; record added steps, corrections, disagreement and review time.','4. Compare the same family in one other CDIT member; reuse legal rules while retaining local differences.','5. Prioritise investment with volumes, handling time, rework, citizen impact, readiness and integration costs. Availability of documents alone is not a priority score.','6. Confirm ADR Vest’s actual funding line, current allocation and eligibility separately. No grant eligibility or expenditure commitment is asserted here.','','## Files','','- `deta-portfolio.json`: evidence registry, claims, partial edges, rules, version conflicts and reported volumes.','- `deta-whole-hall-inventory.csv`: candidates and explicit search targets.','- `deta-review-sheet.csv`: one row per claim for counterpart review.','- Original screen and initial ledger remain historical; this portfolio supersedes their coverage assessment.']
report='\n'.join(lines)+'\n'
(ROOT/'FINDINGS.md').write_text(report)

# Standalone reading artifact; no hosted site or external writes are needed to view it.
body=['<h1>Deta municipal process evidence</h1>',f'<p>CDIT · ADR Vest · 31 October 2026</p><p><strong>{stats["workflow_sheets"]} partial workflow sheets · {stats["claims"]} action claims · {stats["evidence_backed_candidates"]} provisional families/leads</strong></p>','<p>No claim is municipality-validated. Legal requirements, local documented procedure and historical outputs are kept distinct. This is a source-located research portfolio, not an executable workflow.</p>','<p>Best local example: 2025 nonprofit grants. Full current municipality coverage requires the ROF and operational-procedure register.</p>']
for m in maps:
    body.append('<details><summary>'+html.escape(m['name'])+'</summary><p>'+html.escape(m['temporal_scope'])+'</p><table><tr><th>Action</th><th>Actor in source</th><th>Evidence</th></tr>')
    for c in m['claims']:
        e=c['evidence'][0];body.append('<tr><td>'+html.escape(c['statement'])+'</td><td>'+html.escape(c['actor'])+'</td><td><a href="'+html.escape(sources[e['source_id']]['url'],quote=True)+'">'+html.escape(e['locator'])+'</a></td></tr>')
    body.append('</table><p>Open questions: '+html.escape(' '.join(m['open_questions']))+'</p></details>')
doc='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Deta process research</title><style>body{font:16px/1.6 system-ui;margin:3rem auto;padding:0 1rem;max-width:1050px;color:#172331}summary{cursor:pointer;font-weight:650;padding:1rem;background:#edf3f6}details{margin:1rem 0}table{border-collapse:collapse;width:100%;font-size:14px}td,th{border-bottom:1px solid #ccc;padding:.7rem;text-align:left;vertical-align:top}a{color:#075581}h1{line-height:1.2}</style>'+''.join(body)+'</html>'
(OUT/'deta-process-research.html').write_text(doc)
(OUT/'deta-findings.md').write_text(report)
for name in ['deta-portfolio.json','deta-whole-hall-inventory.csv','deta-review-sheet.csv']:(OUT/name).write_bytes((ROOT/name).read_bytes())
print(json.dumps(stats,indent=2))

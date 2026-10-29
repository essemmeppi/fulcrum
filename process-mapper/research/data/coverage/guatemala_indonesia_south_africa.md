# Coverage probe: public documents that describe HOW a service runs

Probe date: 2026-10-29. Method: web search and web fetch only, about 25 searches and 16 fetches. No code written.
Purpose: decide whether a step-level process map could be built from public documents and then checked against the agency's own published procedure.

Evidence levels used below:
- **Read** = I opened the file and read the text (or extracted it from the PDF).
- **Snippet** = I only saw a search-result summary or a secondary source. The URL is a lead, not verified content.
- **Blocked** = the fetch failed (403, 404, 503, size limit, or host not on the session's network allow-list).

Hosts that could not be reached from this session: `disdukcapil.sibolgakota.go.id` and `dinsos.bulelengkab.go.id` (not on the allow-list), `peraturan.bpk.go.id` (403), `udaip.munimixco.gob.gt` home page (403), `www.sassa.gov.za` CSG page (503), `kemensos.go.id/uploads/...` (503). Each would need to be allowed or fetched from another network to read the documents behind them.

---

## 1. Guatemala

**Services probed**
- Municipal: Municipalidad de Mixco, "Traspaso de inmueble" (title/ownership transfer in the municipal IUSI/catastro register). Chosen because the Mixco "Manual de Normas, Procesos y Procedimientos" (MNPP) covers it with a full procedure sheet.
- National: MIDES "Bono Social" (conditional cash transfer).
- Water connection and business licence: not found as separate procedures. Mixco's business-type licences are not a municipal manual item I could find. The Mixco "Servicios Públicos" manual (Jan 2016) exists but exceeded the 10 MB fetch limit (Blocked).

### 1a. Mixco, Traspaso de inmueble

| Document type | Found | Best URL | Date | Approx. length | Language | Process content vs rules only |
|---|---|---|---|---|---|---|
| Statute | Yes (cited, not retrieved) | None fetched. The procedure sheet names its legal basis: Ley del IUSI (Decreto 15-98), Código Civil, Código de Notariado. Código Municipal also governs. | Various | n/a | Spanish | Rules only. The MNPP sheet cites these but does not restate them. |
| Regulation / norms | Partial | Mixco's Reglamento de Construcción y Urbanismo is named in the DDUT manual (Snippet). For title transfer, no municipal reglamento found. The MNPP itself is the operative norm (approved by Concejo Municipal). | n/a | n/a | Spanish | Rules only for the reglamento. Not opened. |
| Official citizen guidance | No | Not found. Search returned no Mixco citizen page for the transfer. The Mixco UDAIP site returned 403. | n/a | n/a | Spanish | None verified. |
| Application form | Partial | The MNPP names a "Formulario" in the inscripción de inmueble sheet, but no downloadable form was found. | n/a | n/a | Spanish | The form itself not seen. The MNPP lists the documents the citizen brings (aviso notarial, copy of escritura, registry entry under 3 months old, boleto de ornato, DPI). |
| Service catalogue entry | No | None found. The MNPP index (code 09.DCAI.04 for Traspaso de inmueble) acts as a de facto list of procedures per directorate. | n/a | n/a | Spanish | Index only. |
| Internal procedure manual / SOP (published) | **Yes, strong** | https://munimixco.gob.gt/wp-content/uploads/2024/01/TOMO-IX-MNPP-DCYAIUSI-2023-22.01.2024.pdf (Tomo IX, Dirección de Catastro y Administración del IUSI). Related: https://munimixco.gob.gt/wp-content/uploads/2024/01/TOMO-VIII-MNPP-DMP-DDUT-2023-22.01.2024.pdf and the Feb 2025 tomos at udaip.munimixco.gob.gt. | Edition 2023, approved Acta 08-2024 of Concejo Municipal, 11 Jan 2024. Revision history: Feb 2013, Jan 2016, Aug 2017, Jan 2020, Dec 2023. A Feb 2025 edition also exists (Snippet). | 117 pages (Tomo IX); 109 pages (Tomo VIII) | Spanish | **High.** Each procedure has a coded sheet (code, purpose, legal basis, users, prerequisites, definitions), a numbered sequential table (step, responsible position, document required) and a flowchart per procedure (the Tomo IX index lists a flowchart for each of its procedures). Traspaso de inmueble is 17 steps with named actors: Auxiliar del IUSI, Vecino/Interesado, Encargado Técnico Catastral, Técnico Catastral. It includes a branch (finca not up to date on IUSI, so transfer refused) and the closing document (Estado de Cuenta del IUSI). The traspaso sheet states no time limit. Other sheets in the same tomo do (20 días hábiles, 10 días hábiles for appeals, 5 días hábiles to Concejo). |
| Audit / ombudsman / court documents describing practice | Partial | Contraloría General de Cuentas audit of Mixco 2023: https://udaip.munimixco.gob.gt/wp-content/uploads/2025/04/Informe-de-Auditoria-2023.pdf (Snippet, not opened) | 2023 audit year, posted Apr 2025 | Unknown | Spanish | Probably financial/compliance. No sign it describes the transfer procedure. |
| Statistics on volumes or processing times | No | None found for Mixco. | n/a | n/a | n/a | None. |

### 1b. MIDES, Bono Social

| Document type | Found | Best URL | Date | Approx. length | Language | Process content vs rules only |
|---|---|---|---|---|---|---|
| Statute | Partial (Snippet) | MIDES mandate to "approve and publish the norms and procedures for access to its programs" is quoted in a 2023 MIDES four-monthly report hosted on the CNC site: https://website-cnc-gob-gt-website-stage-cnc-gob-gt.azurewebsites.net/wp-content/uploads/2023/09/RDC2-INFORME-MIDES.pdf | 2023 | Unknown | Spanish | Rules only (mandate). |
| Regulation / norms | No | No Bono Social reglamento or Acuerdo Ministerial found. Acuerdo Gubernativo 57-2020 (https://gt.vlex.com/vid/acuerdo-gubernativo-no-57-913637614) is for Bono Familia, a different COVID-era fund. | n/a | n/a | Spanish | Not applicable. |
| Official citizen guidance | Weak | State news agency AGN, "Mitos sobre el Bono Social": https://agn.gt/mitos-sobre-el-bono-social-conozca-el-programa-y-evite-estafas/ (Read). Other AGN items on payments and signing of "cartas de corresponsabilidad". | 12 Aug 2026 | Short news item | Spanish | Low. Says selection is only via the Registro Social de Hogares, free of charge, Q500 benefit, health and education co-responsibilities. No steps, no payment channel, no dates, no norm cited. |
| Application form | No | Enrolment is by household registry selection plus signed "carta de compromiso/corresponsabilidad" (news items). No form published. | n/a | n/a | Spanish | None. |
| Service catalogue entry | No | Not found. | n/a | n/a | n/a | None. |
| Internal procedure manual / SOP (published) | **No** | Not found. The only MIDES manual that surfaced was for comedores comunitarios (a different programme, a quality-standards supervision guide). A "Sistema de Información del Bono Social" is reported (AGN, 2022) but no procedure document. | n/a | n/a | Spanish | None. |
| Audit / ombudsman / court documents describing practice | Partial (Snippet) | Prensa Libre report on a Contraloría (CGC) special audit of the conditional-transfer programme: https://www.prensalibre.com/?p=366574 (undated in results) and https://www.prensalibre.com/guatemala/politica/planean-reestructurar-programa-de-transferencias-monetarias-condicionadas/ | Unknown | Press articles | Spanish | Medium as evidence of practice. Says co-responsibility checks are not run jointly with the other ministries and that an old (2012) roll was reused. Primary CGC report not located. |
| Statistics on volumes or processing times | Partial | AGN press items (e.g. https://agn.gt/mides-ha-duplicado-el-numero-de-beneficiarios-de-bono-social-en-dos-anos/) report beneficiary growth and coverage in 21 departments. | 2023-2026 | Press | Spanish | Volumes only. No processing times. No official dataset found. |

### Guatemala: 3-line judgement
1. **Mixco title transfer:** a step-level map (actors, order, documents, one decision branch) can be built directly from MNPP Tomo IX alone, and then checked against a second edition (Feb 2025) and the Contraloría audit. The weakness is that the manual is the only source: no citizen guide, form or volume data was found to test it against, and the traspaso sheet has no time limit.
2. **Is there a published internal procedure to check against?** For Mixco, yes, and it is unusually good (coded sheets, responsible positions, flowcharts, five editions since 2013, Concejo approval). For MIDES Bono Social, no: only news items, a 2026 myths page and press reports of a Contraloría audit.
3. **Caveat:** the MNPP describes how the municipality says staff should act. Anything that checks it must come from outside the document (citizen experience, audit), and for Mixco I found nothing of that kind that was relevant. Water connection and business licence were not locatable as individual procedures.

---

## 2. Indonesia

**Services probed:** Program Keluarga Harapan (PKH, Kemensos) and, as a second service, KTP-el issuance (Dukcapil, Kemendagri).

### 2a. PKH

| Document type | Found | Best URL | Date | Approx. length | Language | Process content vs rules only |
|---|---|---|---|---|---|---|
| Statute | Not retrieved | Not opened. Permensos cites the Social Welfare and Poor-Handling laws as basis (UU 11/2009, UU 13/2011; background knowledge, not retrieved in this probe). | n/a | n/a | Indonesian | Rules only. |
| Regulation / norms | **Yes (two layers)** | (1) Permensos 1/2018 on PKH: https://peraturan.bpk.go.id/Download/120868/PERMENSOS%20NOMOR%20%201%20TAHUN%202018.pdf (Blocked, 403; existence confirmed by many sources). (2) Permensos 8/2026, reported as set 7 Aug 2026, in force 13 Aug 2026, replacing the earlier technical provisions (Snippet, via secondary explainer https://veritask.ai/id/artikel/permensos-8-2026-batas-kepesertaan-5-tahun-dan-kewajiban-baru-keluarga-penerima-manfaat-dalam-program-keluarga-harapan, read; official text not retrieved). Related: Kepmensos 150/2022 (data proposal, verification, validation) and Permensos 3/2021 (integrated welfare data), per https://dinsosppkbp3a.tasikmalayakab.go.id/wp-content/uploads/2024/04/Linjamsos-3.pdf (Snippet). | 2018; 2026 | Not opened | Indonesian | Medium. Per the secondary source, 8/2026 sets four stages with named post-holders: penetapan (several officials in sequence, from DTSEN data), penyaluran (via banks/post), pendampingan (P2K2 sessions, commitment verification, data updates), evaluasi/terminasi/graduasi (annual, or on complaint). Also a 5-year cap and an 85% school attendance condition. It delegates mechanisms to a senior official, which implies a separate lower-level instrument. Permensos 1/2018 reported to cover hak and kewajiban of KPM and implementation (Snippet). |
| Official citizen guidance | Partial | pkh.kemensos.go.id named as the programme site (Snippet; not opened). The searches returned university pages and news explainers, not an official how-to. | n/a | n/a | Indonesian | Not verified. |
| Application form | No (by design) | PKH enrolment is by data (DTKS/DTSEN, usul-sanggah via local social office), not an applicant-filed form. No citizen form found. | n/a | n/a | n/a | None. |
| Service catalogue entry | No | Not found for PKH. | n/a | n/a | n/a | None. |
| Internal procedure manual / SOP (published) | **Partial, not retrievable** | "Pedoman Pelaksanaan PKH" 2021 (Direktorat Jaminan Sosial Keluarga) is cited in many theses, but I could not retrieve an official copy. Lead: https://kemensos.go.id/uploads/topics/16202973084877.pdf (503). The newer technical guideline is reported as Keputusan Dirjen Perlindungan dan Jaminan Sosial No. 8/3/BS.00.01/1/2024 (Snippet, thesis record). An older 2016 mechanism deck is at https://dinsos.bulelengkab.go.id/informasi/download/2.0. Mekanisme Pelaksanaan PKH 2016_108731.pdf (host not on allow-list). | 2016, 2021, 2024 | Unknown | Indonesian | Reported high: stages validasi, penyaluran (four tahap per year in the 2021 guide), pertemuan (P2K2), verifikasi komitmen, pemutakhiran data. Not verified against the document itself. |
| Audit / ombudsman / court documents describing practice | Partial | BPK findings reported in the press: Rp113.14 bn of sembako aid went to PKH KPM (Jun 2024, https://kabar24.bisnis.com/read/20240618/16/1775034/hasil-pemeriksaan-bpk-rp113-miliar-bansos-sembako-diterima-orang-mampu); 1,747 PKH pendamping found holding other jobs, Rp7.9 bn to be returned (https://www.rctiplus.com/news/detail/nasional/5419857/kemensos-tindak-lanjuti-temuan-bpk-atas-1-747-pendamping-pkh-rp7-9-miliar-harus-dikembalikan-ke-negara). Academic implementation studies report poor validation and commitment verification in the field (https://repository.uin-suska.ac.id/12312/). | 2024-2025 | Press and theses | Indonesian | Medium on practice. The BPK LHP itself was not found. No Ombudsman or court item on PKH found. |
| Statistics on volumes or processing times | Weak | Press and secondary sources give disbursement frequency (4 times a year) and beneficiary counts. No official dataset retrieved. | 2021-2025 | n/a | Indonesian | Volumes and timing only. |

### 2b. KTP-el (Dukcapil), as the better-documented alternative

| Document type | Found | Best URL | Date | Approx. length | Language | Process content vs rules only |
|---|---|---|---|---|---|---|
| Statute | Cited, not retrieved | Adminduk law (UU 23/2006, amended UU 24/2013; background knowledge). | n/a | n/a | Indonesian | Rules only. |
| Regulation / norms | Yes (Snippet) | Perpres 96/2018; Permendagri 95/2019 (SIAK), 108/2019 (implementing Perpres 96/2018), 7/2019 (online services), as cited in a Sibolga SOP: https://disdukcapil.sibolgakota.go.id/wp-content/uploads/2022/10/6-SOP-Penerbitan-KTP-Elektronik-Baru.pdf (host not on allow-list). Kemendagri PPID: https://ppid.kemendagri.go.id/storage/dokumen/yF0MbmsaoGhZgKH47bru18zULRm46f07ARWsqV4s.pdf (Snippet). | 2018-2022 | n/a | Indonesian | Medium. Printing rules such as valid KK, no duplicate record, Print_Ready_Record status. |
| Official citizen guidance | Yes (local) | Many Dukcapil offices publish service pages (see SOP row). | Various | Short | Indonesian | Medium (requirements, service time). |
| Application form | Not retrieved | Biodata form (F-1.xx) is used in practice; not opened. | n/a | n/a | n/a | n/a |
| Service catalogue entry | Yes (local) | Service standards at office level, e.g. Tabalong SOP: 30-minute service time, free; Solo SOP: 15-minute printing target (Snippet, 2024 press). | 2022-2024 | n/a | Indonesian | Time and fee. |
| Internal procedure manual / SOP (published) | **Yes, many, at kabupaten/kota level** | Sibolga: https://disdukcapil.sibolgakota.go.id/wp-content/uploads/2022/10/6-SOP-Penerbitan-KTP-Elektronik-Baru.pdf, https://disdukcapil.sibolgakota.go.id/wp-content/uploads/2022/10/7-SOP-Penerbitan-KTP-Elektronik-Perubahan-Data-Hilang-atau-Rusak.pdf; also Banyuwangi (https://sipp.banyuwangikab.go.id/storage/layanan-sop/01JZH5SZFXH8992NXH0YW30B11.pdf), Tabalong, Kapuas Hulu, Kebumen. All Snippet only (not opened). | 2020-2025 | Typically a few pages each | Indonesian | Expected high (SOP table with executors, quality standards, time per step), but I did not open one. Snippets confirm step content such as print-gating on KK validity and Suket fallback when network or AFIS fails. |
| Audit / ombudsman / court documents describing practice | **Yes** | Ombudsman RI systemic study on KTP-el recording and printing in 8 provinces, 10 districts (Dec 2024): https://ombudsman.go.id/news/download/wujudkan-inklusivitas-dalam-pelayanan-ktp-ombudsman-ri-serahkan-hasil-kajian ; local Ombudsman findings e.g. Bandar Lampung, Parigi Moutong. | 2017-2025 | Press releases and study summaries | Indonesian | Medium-high on practice: flags maladministration potential in performance-agreement targets and in the recording and printing process. |
| Statistics on volumes or processing times | Partial | Local SOP service times; ministerial inspection reports in press. No national dataset retrieved. | 2024 | n/a | Indonesian | Timing at office level only. |

### Indonesia: 3-line judgement
1. **PKH:** a stage-level map (determination, disbursement, mentoring, evaluation) can be built from Permensos 1/2018 and 8/2026, but a step-level map with actors and order depends on the Pedoman/Keputusan Dirjen, which I could only confirm by citation, not read. I could not read the official text of either Permensos (BPK 403; 8/2026 known only through a secondary explainer).
2. **Is there a published internal procedure to check against?** Probably yes (Pedoman Pelaksanaan PKH 2021 and a 2024 Dirjen decision), but unverified here. Practice evidence exists (BPK findings in the press, academic studies) but no official SOP or flowchart was seen.
3. **KTP-el is the stronger Indonesian case:** many local Disdukcapil SOPs, national Permendagri, and Ombudsman RI studies of the recording and printing process. If one Indonesian service must be chosen for map-then-check work, choose KTP-el, and fetch the Sibolga or Banyuwangi SOP from a network that can reach those hosts.

---

## 3. South Africa: SASSA Child Support Grant (CSG)

| Document type | Found | Best URL | Date | Approx. length | Language | Process content vs rules only |
|---|---|---|---|---|---|---|
| Statute | Yes | Social Assistance Act 13 of 2004 and SASSA Act 9 of 2004. Consolidated text with regulations indexed at https://www.acts.co.za/social-assistance-act-2004/regulations (Read, partly paywalled). | 2004 | Not opened | English | Rules only (eligibility, agency powers, review, appeals). |
| Regulation / norms | **Yes** | Regulations R2119 of 2022 (application, payment, eligibility), treated as current: chapters include Application, Financial Criteria, Payment, Review, Standard Rules at offices and pay-points. Regs 12 (application procedure), 13 (documents), 14 (date of application), 15 (notification of outcome). R2120 of 2022 for appeals to the Independent Tribunal. Index: https://www.acts.co.za/social-assistance-act-2004/regulations . Predecessor R898 of 2008 reg 10 (Read): https://source.acts.co.za/social-assistance-act-2004/r898_10__procedure_to_be_followed_in_application_for_social_grant.php . Draft amendments 2026 (180 days to produce valid ID, 90 days to report changes): https://www.gov.za/sites/default/files/gcis_document/202609/55290gon7869.pdf (Snippet). Note: the acts.co.za index labels the "R162" set as 2005 and shows inconsistent numbering across sets. Verify notice numbers and years against the Government Gazette before citing. | 2008, 2022, draft 2026 | Not opened (regs) | English | **Medium-high.** The R898 reg 10 prescribes the counter procedure in order: applicant attends in person, designated officer helps and certifies, second officer verifies, dated acknowledgement with stamp, register of applications. Reg 13 of R898 gave 3 months to notify the outcome. Whether R2119 keeps the same period was not confirmed. |
| Official citizen guidance | Yes, but inconsistent | SASSA booklet "You and your grant" 2026 (DSD-hosted): https://www.dsd.gov.za/index.php/component/jdownloads/?task=download.send&id=698%3Asassa-grant-booklet-2026&catid=7&m=0&Itemid=101 ; gov.za FAQ https://www.gov.za/faq/government-services/how-do-i-apply-social-grant ; Western Cape page https://www.westerncape.gov.za/service/sassa-child-support-grant ; SASSA portal https://services.sassa.gov.za/ . The SASSA CSG page itself returned 503. | 2026 booklet; others undated | Booklet: not opened | English | Low-medium. Documents needed, where to apply, "up to 3 months", backdating to application date. Sources disagree on whether CSG can be applied for online (gov.za says forms are not online; the SASSA portal has a download centre; third-party sites say online is possible). |
| Application form | **Yes** | SASSA Download Form Center: https://services.sassa.gov.za/portal/r/sassa/sassa/download-center ; "Declaration and Consent by Applicant: Grant Application": https://services.sassa.gov.za/portal/r/sassa/files/static/v61/Declaration%20and%20Consent%20by%20the%20Applicant.pdf | Undated | About 1-2 pages (not opened) | English | Low. Forms show required declarations (citizenship or residence, primary caregiver). No process content. |
| Service catalogue entry | Partial | gov.za service listings and SASSA "Grant_Enquiries" page (https://www.sassa.gov.za/SitePages/Grant_Enquiries.aspx, Snippet). My guess at gov.za/services/child-support-grant returned 404. | Undated | Short | English | Low. |
| Internal procedure manual / SOP (published) | **No** | Searched for an SOP and service charter for grant administration; none found. The Annual Report mentions an operating model and indicators but not procedure. | n/a | n/a | n/a | None. The nearest thing to a public procedure is regulation 12 plus the agency's reported process indicator. |
| Audit / ombudsman / court documents describing practice | Partial | SASSA Annual Report 2024/25 contains the Auditor-General's reports on predetermined objectives and the financial statements (https://www.parliament.gov.za/storage/app/media/Docs/ann_rep/01dx3n75bv7tsfjv4oyffijfzaafbuyo34.pdf, Read, 152 pp). Parliamentary audit-outcome briefing: https://pmg.org.za/committee-meeting/41710/ (Snippet): beneficiaries paid but not on the Beneficiary Records Management system; inconsistent registration of children aged 0-1 for CSG. Public Protector warning concerned Postbank payment arrangements (not application steps). Court: a Jan 2025 High Court ruling reported by AllAfrica (https://allafrica.com/stories/202501240426.html) concerns SRD (in-person applications), not CSG. Older SAFLII cases (2005 ECHC, 2009 NWHC) surfaced but not opened. | 2024-2026 | AR: 152 pp | English | Medium for oversight of data and payment. Low for application steps. No judgment found that describes the CSG application procedure. |
| Statistics on volumes or processing times | **Yes** | SASSA Annual Report 2024/25 (RP270/2025, PDF dated 17 Sep 2025), read: https://www.parliament.gov.za/storage/app/media/Docs/ann_rep/01dx3n75bv7tsfjv4oyffijfzaafbuyo34.pdf . CSG: 13,117,004 grants at end of March 2025. Indicator "% of new grant applications processed within 7 days": 2024/25 91% (1,657,935 of 1,830,936); 2023/24 95% within 10 days (1,806,569 of 1,897,521); 2022/23 89.13% within 5 days. Regional breakdown given. A 2025/26 report is listed at https://static.pmg.org.za/SASSA_2025-26_Annual_Report.pdf (not opened). | 2025 | 152 pp | English | Timing only. The indicator covers all new grant applications taken face to face, not CSG alone, and the threshold changed from 5 to 10 to 7 days across years. "Processed" is not defined in the extract, and it sits against a 3-month regulatory period. |

### South Africa: 3-line judgement
1. **Step-level map:** only partly. The regulation sets the counter steps (attend, assist, certify, verify, acknowledge, register), but there is no published account of what happens after submission (SOCPEN capture, verification, means test, approval, payment set-up), so the back half of a map would be inferred or taken from news and oversight reports.
2. **Is there a published internal procedure to check against?** No SOP or service charter was found. The nearest check is the Annual Report's turnaround indicator (91% of new grant applications within 7 days in 2024/25), which can be compared with the regulation's 3-month window and with the "up to 3 months" in citizen guidance.
3. **Useful property for checking:** the public record contradicts itself (3 months vs 7 days; forms online vs not online; reg numbering across sets), which makes a documents-versus-documents comparison feasible even without an SOP.

---

## Cross-country summary

| Country / service | Statute | Regulation | Citizen guidance | Form | Catalogue | Internal SOP/manual | Audit/ombudsman/court | Statistics |
|---|---|---|---|---|---|---|---|---|
| Guatemala, Mixco traspaso | cited | partial | no | partial | no | **yes (117 pp, flowcharts)** | partial | no |
| Guatemala, MIDES Bono Social | partial | no | weak (news) | no | no | **no** | partial (press) | partial (press) |
| Indonesia, PKH | cited | **yes (2018; 2026)** | partial | no (by design) | no | partial (cited, not read) | partial (press) | weak |
| Indonesia, KTP-el | cited | yes | yes (local) | not read | yes (local) | **yes (many, local)** | **yes (Ombudsman RI)** | partial |
| South Africa, CSG | yes | **yes (R2119/2022)** | yes (inconsistent) | **yes** | partial | **no** | partial | **yes (Annual Report)** |

## Gaps to close if this goes further
- Fetch Permensos 1/2018 and the official text of Permensos 8/2026 (BPK or JDIH Kemensos), and the Pedoman PKH 2021 or the 2024 Dirjen decision.
- Fetch one Disdukcapil KTP-el SOP (Sibolga or Banyuwangi) and check whether it has a time per step.
- Obtain the Mixco Servicios Públicos manual (Jan 2016, over the 10 MB fetch limit) for water connection, and check the Feb 2025 Tomo IX against the 2023 one.
- Read the Mixco Contraloría audit for any procedure-level findings.
- Read R2119 of 2022 regs 12-15 in the Gazette to confirm the notification period, and open the 2026 SASSA booklet for the citizen-facing sequence.

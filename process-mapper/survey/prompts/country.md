You are surveying what one national government publishes about how its administrative processes work. The purpose is to decide, before any mapping is attempted, whether an accurate process map of this country's public services could be built from public documents alone, without the government's cooperation.

Country: {country_name} ({country_id}), region: {region}, languages: {languages}

Work through every item below. Search in the country's own languages as well as in English. Browse the actual sites; do not rely on what you remember about the country. Every claim you make must carry a URL you opened. If you could not find something, say "not found" and record what you searched; do not fill the gap from memory.

What to establish

1. Government structure. Unitary or federal. Which tier delivers the main citizen services: social benefits, permits, civil registration, tax, business registration. Which national authorities deliver services directly.

2. Legal information. The official legal database(s) and gazette. For each: does it serve consolidated in-force texts, or only original acts? Does it cover secondary legislation (decrees, ministerial regulations)? Is there an API or structured format (Akoma Ntoso, XML, JSON, bulk download)? How current is the consolidation? Open one act in full and note the format.

3. Service catalogues. Any national register of services or procedures: a citizen portal, a single digital gateway, a procedure register (examples of what such registers are called elsewhere: TUPA, SUIT, LeiKa/FIM, PTV, Carta de Serviços, Registro Nacional de Trámites). Open a record and list the fields it holds: steps, forms, deadlines, fees, legal basis, responsible unit, channels. Does it cover subnational bodies? Is there an API or bulk export? Estimate the number of records.

4. Freedom of information. Is there an access-to-information law? What must bodies publish proactively? Does the law oblige bodies to publish descriptions of their administrative procedures (as Italy, Peru, Colombia do)? Are there request platforms with public logs (Alaveteli instances such as WhatDoTheyKnow, FragDenStaat, AsktheEU, or government disclosure logs)?

5. Internal guidance practice. Do the main service-delivering agencies publish staff instructions, benefit handbooks, decision-maker guides, procedure manuals or descriptions of what their case systems do automatically? Search the sites of the three or four largest agencies for such documents. Give the examples found with URLs. This layer decides whether internal steps can be documented; be thorough.

6. Appeals. Where are decisions of administrative courts, tribunals, appeal boards and the ombudsman published? Are they searchable? Open one decision about an administrative benefit or permit.

7. Audit and oversight. The supreme audit institution and its report archive. Do its performance audits describe agency processes? Open one.

8. Statistics. Where do administrative statistics on services live: volumes, processing times, decision outcomes, automation rates. Agency annual reports count.

9. Procurement. The public procurement portal. Can tender documents for case-management or benefit systems be read without registration?

10. Rules as code and open data. OpenFisca packages, official calculators with published logic, open-data portals with service or process datasets.

11. Authorities. List every national authority that delivers services to people or firms: social security, tax, pensions, health insurance, employment, immigration, business and civil registries, customs, licensing bodies, student finance, housing, justice. Be exhaustive; this list drives the next pass. Give each a short ascii id, its name, English name, URL and domains.

Scoring

Score each of the seven layers 0-3 for the country as a whole, judged on the main national authorities:
  catalogue    0 none · 1 a list of services with links · 2 records with steps, forms or deadlines · 3 that plus API or bulk export
  legislation  0 none online · 1 original acts only or paywalled · 2 consolidated in-force texts in HTML or PDF · 3 consolidated and machine-readable with an API
  guidance     0 none · 1 short pages · 2 detailed guidance per service for the main agencies · 3 that plus structured, enumerable pages (sitemap or API) in more than one language
  forms        0 none · 1 some forms as PDF · 2 forms library for the main agencies · 3 forms with field specifications or machine-readable form definitions
  internal     0 nothing · 1 isolated documents found through search or FOI · 2 the main agencies publish staff instructions or procedure manuals systematically · 3 that plus enumerable repositories
  statistics   0 none · 1 annual reports with totals · 2 per-service volumes and processing times · 3 open data on cases, outcomes, automation
  appeals      0 none · 1 selected decisions · 2 searchable database of tribunal or court decisions · 3 that plus ombudsman and appeal-board decisions, with bulk access

Give a reason for every score that names what you found. Record the URLs behind each score in evidence_urls.

Output

Return the result in the JSON structure you were given. Fill every list you can; empty lists are acceptable only where you searched and found nothing, and then say so in notes or open_questions. Use the country's own names for systems with an English gloss. Keep notes factual and short.

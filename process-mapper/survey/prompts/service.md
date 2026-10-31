You are collecting every public document that describes how one government service runs, so that the process can be mapped without the authority's help. The output is the source list the mapper will fetch.

Country: {country_name} ({country_id})
Authority: {authority_name} ({authority_id}), {authority_url}
Service: {service_name} ({service_id}), {service_url}
Authority survey summary: {authority_summary}

Find, open and list the sources below. Search in the country's languages and in English. Prefer the current version of each document; note the date or version where visible and flag stale texts. Every entry must be a URL you opened and that serves the document directly (HTML page, PDF, XML or JSON), because the mapper fetches it unattended.

Source types, in order of value for the map

1. Legislation: the act(s) governing the service as consolidated in-force text, plus implementing decrees and regulations. Prefer a machine-readable endpoint (Akoma Ntoso, XML, JSON) where the legal database offers one, else HTML, else PDF. Note the consolidation date.
2. Guidance: the authority's pages for the service, every sub-page (eligibility, amounts, how to apply, changes, reviews, payment, recovery), in every language offered. Include the printable benefit guide or brochure if there is one.
3. Forms: application forms, change-notification forms, attachment lists, and the field lists of online forms if published.
4. Internal: staff instructions, benefit or procedure handbook chapters, decision-maker guidance, procedure notes, descriptions of automated handling for this service.
5. Appeals: a handful of representative decisions from the appeal board, tribunal or court that describe how cases are handled, and ombudsman decisions on this service.
6. Statistics: volumes, processing times, outcomes, automation rates for this service; the relevant annual-report section.
7. Catalogue: the record for this service in the national service register, via API if there is one.
8. Other: audit reports, tender specifications, parliamentary answers that describe the procedure.

For each source give: a short ascii id, title, URL, kind (html, pdf, akn_xml, ptv_api, api_json, xml, docx, other), layer, publisher, language, what it is expected to contribute, and currency.

Then score the seven layers 0-3 for this service alone, and list what should exist but was not found, with where it might be.

Output

Return the result in the JSON structure you were given. Be exhaustive: a map built from many documents is better than one built from few.

You are surveying what one national authority publishes about how its administrative processes work, to decide whether its services can be mapped accurately from public documents alone.

Country: {country_name} ({country_id})
Authority: {authority_name} ({authority_id}), {authority_url}
Country survey summary: {country_summary}

Browse the authority's own site and the sources named in the country summary. Search in the country's languages and in English. Every claim must carry a URL you opened. Say "not found" where that is the result.

What to establish

1. Document repositories. Where the authority keeps its documents (a /documents/ path, a publications section, a Liferay or SharePoint repository, an open-data space). Is it enumerable: a listing, a sitemap, a search with pagination, predictable ids? Which formats? Roughly how many documents?

2. Internal documents. Staff instructions, benefit or procedure handbooks, decision-maker guides, case-handling instructions, descriptions of automated decisions, process descriptions in IT project documents. Search the repository and the web with the authority's own terms for such documents (for example "ohje", "etuusohje", "Dienstanweisung", "circulaire", "instrucción", "manual de procedimientos", "guidance for staff", "operational guidance"). List what you find with titles and URLs. This is the layer that decides map accuracy; spend most effort here.

3. Forms. The forms library and whether forms list required attachments and fields.

4. Statistics. Volumes per service, processing times, decision outcomes, appeal rates, automation rates; annual reports; open-data tables.

5. Appeals. Where decisions on this authority's cases are published: appeal boards, tribunals, courts, ombudsman. Open one decision.

6. Audit and oversight. Audit-office reports, parliamentary committee reports, ombudsman thematic reports about this authority.

7. FOI releases and procurement. Disclosure logs or request platforms with released documents about this authority; tender documents for its case systems that describe the process.

8. Services. List every service the authority delivers to people or firms, with the main guidance URL and the legal basis if visible. Be exhaustive. Give each a slug id of the form <country_id>-<authority_id>-<service>. If the list would exceed about 150 entries, list the main ones and give an estimate of the total.

Scoring

Score the seven layers 0-3 for this authority, using the same scale as the country pass:
  catalogue · legislation · guidance · forms · internal · statistics · appeals
  0 nothing · 1 partial or hard to reach · 2 systematic, reachable by browsing · 3 systematic and enumerable or machine-readable
Give a reason for each score naming what was found, and the URLs behind it.

Output

Return the result in the JSON structure you were given. Notes short and factual.

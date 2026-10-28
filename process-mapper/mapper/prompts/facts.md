You are reading one public document about a government service, to reconstruct how the administrative process actually works. Extract every atomic fact that describes the process, and back each one with a verbatim quote.

Source
- id: {source_id}
- title: {title}
- publisher: {publisher}
- layer: {layer}
- language: {language}
- url: {url}

What counts as a fact (field `kind`)
- step: something an actor does in the process (citizen submits, Kela checks, system fetches, decision is sent, payment is made, annual review…)
- actor: who does something or is involved (citizen/household, caseworker, Kela system, landlord, Tax Administration, Incomes Register, appeals board…)
- eligibility: a condition for getting the benefit or for a cost/person to count
- calculation: how an amount is computed (formula, percentage, cap, deductible, rounding)
- procedural_rule: a rule about how the procedure runs (what must be reported, when a decision can be revised, hearing, retroactivity)
- deadline: a time limit for any actor (retroactive period, months of validity, days to appeal, annual review)
- input: a piece of information or a document the process needs (rent agreement, income data, bank account…)
- data_source: a register or system the data comes from (Incomes Register, Population Information System, landlord's e-service, OmaKela…)
- channel: how the citizen interacts (OmaKela, paper form AT 1, service point, phone, post)
- output: what the process produces (decision, payment, notice, request for additional information)
- exception: special cases, exclusions, overrides
- appeal: how to contest a decision
- volume: numbers about scale (recipients, euros, processing time)

Rules
1. One fact = one claim. Split compound sentences.
2. `statement` is in English, precise, and self-contained (name the actor, the condition, the number).
3. `quote` is copied VERBATIM from the text below, in its original language. Do not translate, paraphrase, fix typos, or merge distant sentences. You may shorten with "..." between two verbatim fragments of the same passage. Keep quotes under ~400 characters.
4. `locator` is the nearest bracketed marker above the quote, copied exactly as it appears without the brackets: e.g. `7 § Asumismenot`, `p. 3`, `H2: How to apply`, `Description:Description (en)`.
5. Be exhaustive on steps, rules, deadlines, inputs, data sources and channels — these are what we need to rebuild the workflow. Skip marketing text, navigation, contact details, cookie notices.
6. Do not infer anything that the text does not say. If the text is silent on who performs a step, say "the text does not name the actor" in the statement.

Document text (markers in brackets are locators):

<document>
{text}
</document>

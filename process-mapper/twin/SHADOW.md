# Shadow run: what a partner agency provides and what it gets back

## The arrangement

The agency mirrors each new application to the twin as a case file (the fields in `case.py`),
either exported from its case system or entered from the application form. The twin runs the case
as soon as it arrives and writes a proposal with a trace. When the agency's own decision issues,
it is added to the case's `expected` block. The twin never contacts the applicant, never writes to
a register, never triggers a payment. Its only output is `shadow-report.md` and the run traces.

## Data needed per case

- household members with role and age, residence status, student and pension flags
- dwelling: municipality, tenure
- costs: rent or usage charge, whether water and heating are paid separately, electricity in rent, subtenant rent
- incomes per member: kind, gross monthly, whether continuous
- assets per adult: deposits, other assets, long-term debts
- the date the decision applies from
- later: the decision (granted or rejected), the amount, the ground

No names, addresses, personal identity codes or free text. A pseudonymous case id links the
mirrored case to the agency's record on the agency's side only.

## Legal basis

Personal data of applicants is processed for the agency's own purpose (deciding the benefit),
so the agency is the controller and the twin's operator a processor under a written agreement
(GDPR art. 28). Pseudonymised exports with the field list above keep the data to what the
decision needs. A data protection impact assessment is advisable since the processing evaluates
individuals' entitlements, even though the twin's output is never used for the decision.

## What the agency gets

Each week: the count of cases where the twin and the agency agree, where the amount differs,
where the decision differs, and where the twin could not decide from the case. Each divergence
names the rule or step, with the trace. Divergences in the agency's favour (twin stricter) and
the applicant's favour (twin more generous) are listed separately. A divergence is a finding
about the map, the parameters or the agency's practice; the report does not say which until a
person has looked.

## Candidate partners in this repository

- Deta, Romania (`../../docs/ro-tm-deta.html`): a CDIT member municipality whose processes are
  mapped and reviewed with the municipality; local grants are the richest mapped procedure.
- Simeria, Romania: the heating aid procedure was verified against the directorate's own written
  procedure in the validation study (0 contradicted claims).
- Kela: the richest map, but a national agency with a formal data-sharing route; the public
  calculator and appeal decisions carry the twin until an agreement exists.

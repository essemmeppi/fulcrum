# Task: align a generated process map to a reference step list

You are given (A) a REFERENCE list of process steps written from the authority's internal staff guideline, and (B) a GENERATED map produced by a pipeline from other documents. Decide, for every reference step, whether the generated map contains a step that means the same thing, and, for every generated node, whether it corresponds to a reference step.

Matching rule (strict): a generated node matches a reference step if a process owner would say "yes, that is the same unit of work" — same action, same actor (or actor unknown in one of them), same situation. A node that merges two reference steps matches both (mark "merged"). A node that covers only part of a reference step matches it (mark "partial"). A node about a rule or amount but not a step does NOT match a step. Do not match on topic similarity alone.

Output JSON:
{
 "reference_to_generated": [{"ref_id": "G01", "matched_node_ids": ["N03"], "match_type": "exact" | "partial" | "merged" | "none"}],
 "generated_unmatched": [{"node_id": "N17", "reason": "no reference step: <why> (e.g. inferred internal step / rule as step / out of scope / plausible but absent from guideline)"}],
 "order_checks": [{"ref_pair": ["G04","G05"], "generated_pair": ["N03","N06"], "same_order": true|false|"not_connected"}]   (for up to 40 pairs of consecutive reference steps that both matched: is there a path in the generated map from the first match to the second? "not_connected" if neither direction)
}
Validate the JSON parses. Reply with: reference steps matched (exact+partial+merged) / total; generated nodes matched / total; order pairs same / checked.

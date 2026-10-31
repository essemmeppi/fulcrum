# Task: list the Rent Assistance procedure as the Operational Blueprint describes it to staff

Read ONLY the Services Australia Operational Blueprint pages in inputs_blueprint/ (staff procedure pages with numbered step tables) and write down the procedure as the agency describes it to its own staff. You have no other source. This list will be a reference against which a map built from public pages is tested, so completeness and faithfulness matter.

Output JSON written to the output path given:
{
 "steps": [{"id": "B01", "subprocess": "trigger" | "eligibility" | "accommodation_details" | "verification" | "rate" | "payment" | "review" | "change" | "other", "name": "...", "description": "one sentence", "actor": "customer" | "staff" | "system_automatic" | "landlord_or_agent" | "unclear", "actor_evidence": "words that show who does it", "kind": "task" | "decision" | "event" | "wait", "condition": "", "predecessors": ["B00"], "source_file": "<file>", "quote": "verbatim, max 250 chars", "granularity": "screen_or_field_level" | "work_step_level" | "policy_level"}],
 "automation_statements": [{"what": "...", "source_file": "...", "quote": "..."}]
}
Rules: one step = one unit of work by one actor. Keep the Blueprint's own granularity (if it says "code the AC screen", that is a step; mark it screen_or_field_level). Do not invent steps. Quotes verbatim. Validate JSON with python3. Reply with steps per subprocess and per actor and per granularity, and the five most surprising procedural facts (one line each with file).

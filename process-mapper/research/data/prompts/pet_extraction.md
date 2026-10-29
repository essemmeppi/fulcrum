# Task: extract process steps, actors and step order from one process description

You will read short English texts that describe a business or administrative process. Each text is given as numbered sentences (S0, S1, ...) and every token carries its index in square brackets, e.g. `reviews[2]`. You must return JSON that identifies, for each document:

1. **activities** — the process steps. Following the PET annotation guidelines (Bellan et al. 2022): an activity is the ACTION VERB (or verb+particle) that expresses a unit of work in the process, e.g. `sents`, `reviews`, `informed`, `back-ordered`, `checks`. Annotate only the verb token(s), not the object and not auxiliaries (`is reserved` -> `reserved`). Do NOT annotate meta statements about the process itself (`a new process instance is created`, `the process is finished`, `the process ends`), general descriptions (`A small company manufactures bicycles`), or conditions. Nominal activities (`the preparation of the report`) are rare; annotate the noun only if the text uses it as the step.
2. **actors** — who performs or receives an activity: the full noun phrase including determiner, e.g. `The MPON`, `A member of the sales department`, `the engineering department`. Pronouns that refer to data (`it`) are not actors. A role mentioned only descriptively (not performing or receiving a step) is not an actor.
3. **performers** — pairs (activity -> actor that performs it) when the text states who does it (active voice subject, or "by X" in passive).
4. **successors** — the sequence flow between activities: a pair (A -> B) means B is the step that comes directly after A in the process. Rules:
   - For an exclusive choice ("reject or accept", "if X ... otherwise ..."), the activity before the choice gets a successor edge to EACH alternative branch's first activity.
   - For parallel branches ("in the meantime", "at the same time"), the activity before the split gets an edge to each branch's first activity, and each branch's last activity gets an edge to the joining activity.
   - For loops ("this is repeated"), add the back edge.
   - Do not add transitive edges (if A->B and B->C, do not add A->C).
   - Edges may cross sentences. A document that lists the same step twice (e.g. in a summary) should use the first mention.

Reference activities and actors by `[sentence_id, token_index]` of their FIRST token, and give `end` as the index of the last token of the span.

## Output format (JSON only)
{
 "doc": "<document name>",
 "activities": [{"sid": 0, "start": 2, "end": 2, "text": "sents"}, ...],
 "actors": [{"sid": 0, "start": 0, "end": 1, "text": "The MPON"}, ...],
 "performers": [{"activity": [0, 2], "actor": [0, 0]}, ...],
 "successors": [{"from": [0, 2], "to": [1, 2]}, ...]
}

## Worked example (document doc-10.1)
Input:
S0: The[0] MPON[1] sents[2] the[3] dismissal[4] to[5] the[6] MPOO[7] .[8]
S1: The[0] MPOO[1] reviews[2] the[3] dismissal[4] .[5]
S2: The[0] MPOO[1] opposes[2] the[3] dismissal[4] of[5] MPON[6] or[7] the[8] MPOO[9] confirmes[10] the[11] dismissal[12] of[13] the[14] MPON[15] .[16]

Output:
{
 "doc": "doc-10.1",
 "activities": [{"sid":0,"start":2,"end":2,"text":"sents"},{"sid":1,"start":2,"end":2,"text":"reviews"},{"sid":2,"start":2,"end":2,"text":"opposes"},{"sid":2,"start":10,"end":10,"text":"confirmes"}],
 "actors": [{"sid":0,"start":0,"end":1,"text":"The MPON"},{"sid":0,"start":6,"end":7,"text":"the MPOO"},{"sid":1,"start":0,"end":1,"text":"The MPOO"},{"sid":2,"start":0,"end":1,"text":"The MPOO"},{"sid":2,"start":8,"end":9,"text":"the MPOO"}],
 "performers": [{"activity":[0,2],"actor":[0,0]},{"activity":[1,2],"actor":[1,0]},{"activity":[2,2],"actor":[2,0]},{"activity":[2,10],"actor":[2,8]}],
 "successors": [{"from":[0,2],"to":[1,2]},{"from":[1,2],"to":[2,2]},{"from":[1,2],"to":[2,10]}]
}
(Note: "opposes" and "confirmes" are exclusive alternatives after "reviews", so "reviews" has an edge to each.)

## Procedure
For each document name you are given: read `inputs/<doc>.txt`, produce the JSON, and write it to `outputs/<model_tag>/<doc>.json`. Validate every file parses with python3. Do not skip documents. Do not look at any other files.

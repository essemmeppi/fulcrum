# Task: reconstruct the administrative process for a German residence permit on humanitarian grounds from the law alone

Goal: list the steps a German foreigners authority (Ausländerbehörde) performs when it processes an application for a residence permit on international-law, humanitarian or political grounds (Aufenthaltserlaubnis nach §§ 22-26 AufenthG), using ONLY the statute text in inputs_public/ (sections of the Residence Act, AufenthG, and of the Administrative Procedure Act, VwVfG). Do not use outside knowledge of German administrative practice. The result will be compared with the government's own official process model, so list what the law supports and mark what you infer.

Output JSON:
{
 "actors": [{"id": "...", "name": "..."}],
 "nodes": [{"id": "N01", "name": "short German name (as an official would name the activity, e.g. 'Zuständigkeit prüfen')", "name_en": "English", "description": "one sentence", "actor_id": "...", "type": "citizen_task" | "caseworker_task" | "system_task" | "third_party_task" | "decision" | "start_event" | "end_event", "legal_basis": ["§ 81 Abs. 1 AufenthG"], "confidence": 0-1, "evidence": [{"source": "<file>", "quote": "verbatim, max 250 chars"}], "inferred_reason": ""}],
 "edges": [{"source": "N01", "target": "N02", "condition": ""}]
}
Cover: receipt of the application and documents, competence check, completeness check and clarification of facts with the applicant, identity and security checks with other authorities, fee, provisional certificate (Fiktionsbescheinigung), assessment of the requirements of each of §§ 22, 23, 23a, 24, 25, 25a, 25b, general requirements of § 5, hearing before refusal, decision and its notification, duration (§ 26), production and hand-over of the title (§ 78), data transfer to the central register of foreigners (§ 90b), objection (§ 79 VwVfG). One node = one unit of work by one actor. Quotes verbatim. Validate with python3. Write to outputs/map_law_opus.json . Reply with node count, nodes per actor, and the 3 least certain nodes.

# Task: verify a public-document process map against the agency's staff procedures

A map of Australia's Rent Assistance process was built from PUBLIC pages only. Check each of its nodes against the Operational Blueprint (staff procedure pages) in inputs_blueprint/. Be strict and literal.

For EACH node output: {"node_id", "verdict": "confirmed_step" | "confirmed_rule_only" | "confirmed_with_corrections" | "contradicted" | "not_mentioned", "evidence": [{"source_file", "quote" (verbatim, max 250 chars)}], "actor_check": "same" | "different" | "unknown" (+ "actor_in_blueprint"), "automation_check": "same" | "different" | "unknown", "order_check": "supported" | "contradicted" | "silent", "granularity": "same" | "blueprint_splits_it" | "blueprint_merges_it" | "unknown", "corrections": "...", "reviewer_confidence": 0-1}
Write a JSON array to the output path given; validate with python3; reply with counts per verdict and the three most important corrections.

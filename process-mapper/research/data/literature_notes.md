# Literature notes (numbers verified from the paper texts unless marked)

## PET benchmark (Bellan, Dragoni, Ghidini et al. 2022; dataset v1.1)
- 45 documents (Friedrich et al. 2011 collection), annotated with 7 entity types (Activity, Activity Data, Actor, Further Specification, XOR Gateway, AND Gateway, Condition Specification) and 6 relation types (Flow = sequence flow, Uses, Actor Performer, Actor Recipient, Further Specification, Same Gateway).
- Baseline in Neuberger et al. 2024 Table 1 (PET column): Mention detection P .73 R .64 F1 .69 (CRF, Bellan 2022); Entity resolution F1 .52; Relation extraction P .79 R .66 F1 .72 (ML baseline, Neuberger 2023, trained on 36 docs).

## Neuberger, Doll, Engelmann, Ackermann, Jablonski 2024 (arXiv 2407.18540), "A Universal Prompting Strategy..."
- GPT-4o, temperature 0, Table 1 PET: MD zero-shot F1 .68, 1-shot .73, 3-shot .74 (P .72 R .77). ER 3-shot F1 .74. RE zero-shot F1 .86, 1-shot .89, 3-shot .89 (P .90 R .89).
- Table 2 (PET): Claude 3 Opus MD 3-shot F1 .73, RE 3-shot F1 .91 (P .92 R .91); Claude 3 Sonnet MD 3-shot .70, RE 3-shot .89; Llama 3 70B RE 3-shot .84; GPT-3.5 RE 3-shot .69.
- Metric: P = correct/pred, R = correct/gold, "count predictions as correct exactly the way the compared work does". RE is evaluated given gold mentions? (check: their RE stage takes mentions as input — need to confirm in Section 5). 
- Ablation: removing examples / splitting prompts matters: F1 .27 MD, .56 RE for the worst prompt.

## Klievtsova, Benzin, Kampik, Mangler, Rinderle-Ma 2023/2024 (arXiv 2304.11065)
- GPT-4 produced "correct" models 17/21 (81%) on a higher-education test set; GPT-3 ~30%. Human models assumed correct (no measured human accuracy).

## Kourani et al. 2024/2025 (ProMoAI; "Evaluating LLMs on Business Process Modeling", SoSyM 2025)
- 16 LLMs on 20 processes; self-improvement varies by model.

## Lauer, Pfeiffer, Rombach, Mehdiyev 2026 (Information Systems 142; arXiv 2601.21787) BEF4LLM
- 39 metrics; LLMs better on syntactic/pragmatic, humans better on semantic quality; valid BPMN-XML generation still hard.

## Process model similarity
- Dijkman, Dumas, van Dongen, Käärik, Mendling 2011 (Information Systems 36(2)): label-, structure-, behaviour-based similarity; structural slightly best; GED is NP-complete.
- Weidlich, Mendling, Weske 2011 (IEEE TSE 37(3)): behavioural profiles (strict order, exclusive, interleaving) as basis for comparing ordering constraints; our precedence-agreement metric follows this idea.

## Rules-as-code encoding reliability
- Witt, Huggins, Suzor, Zhao et al. (Artificial Intelligence and Law 2024, s10506-023-09350-1): legally trained coders encoding Commonwealth legislation; similarity between coders 4.27% week 1 -> 57.64% week 2 after agreeing key terms and adding validation. Divergent interpretive choices from statutory complexity, provision granularity, language functionality.
- Catala (Merigoux, Chataing, Protzenko 2021): found OpenFisca French family-benefit bug (income cap not applied for single-child families in overseas territories).

## De jure vs de facto
- Wijnhoven et al. 2023 (IJIM Data Insights): comparing de jure and de facto models yields candidate workarounds; incomplete de jure models hinder detection.
- Street-level bureaucracy: Lipsky 1980; "space in the rules" (Ontario Works, Social Policy & Society 2015): discretion within and outside rules; Evans 2011 (BJSW).

## Government-published internal procedure (what makes validation possible without interviews)
- Kela publishes the staff benefit guideline (etuusohje) for general housing allowance on kela.fi (PDF, 83 pages, 22.10.2026): "Ohje on ensisijaisesti tarkoitettu Kelan sisäiseen käyttöön." It also refers to separately published procedure instructions (menettelyohjeet) and a process description ("yleisen asumistuen prosessi") that are intranet-only.
- Services Australia publishes the Operational Blueprint (staff procedures with numbered step tables; e.g., 108-18092646 has 4 tables, ~70+ steps).
- Germany FIM: Stammprozesse in restricted BPMN (docs.fitko.de/fim/docs/prozesse); API at fimportal.de/docs (to check).

# Romania: heating aid and energy supplement (Law 226/2021), local directorate level

Builder saw only `inputs/` (ranked 1 to 6). The reference `reference/po-simeria-heating.txt` (operational procedure DAS-SBS-PO-05, edition IV, 28 Oct 2022, Simeria social-assistance directorate, text extracted from the PDF) was held out for every run except `ledger_public_plus_po_opus.json`, which read it last as rank 7.

| Rank | File | Source | Chars |
|---|---|---|---|
| 1 | r1_hg-1073-2021-norms.txt | HG 1073/2021 methodological norms, mirror: spaetdrobeta.ro/wp-content/uploads/2021/10/Hotarare-1073-din-04-10-2021-norme-metodologice-de-aplicare-Lege-226-din-2021.pdf | 273,635 |
| 2 | r2_law-226-2021.txt | Law 226/2021, original text: cjtimis.ro/wp-content/uploads/2020/07/LEGE-nr.-226-din-16-septembrie-2021.pdf | 153,994 |
| 3 | r3_pub-bucovat-acte.txt | Bucovăț commune, required documents list: comunabucovat.ro/wp-content/uploads/2025/10/2.-Lista-acte-necesare-incalzire.pdf | 2,466 |
| 3 | r3_pub-galati-termoficare.txt | Galați district-heating notice: termoficare.primariagalati.ro/documente/acordare_ajutoare.pdf | 16,954 |
| 3 | r3_pub-sannicolau-2025.txt | Sânnicolau Mare 2025-26 intake notice: sannicolau-mare.ro/wp-content/uploads/2025/10/Anunt-preluare-cererii-incalzire-2025-2026.pdf | 4,059 |
| 3 | r3_pub-scobinti-anunt.txt | Scobinți commune notice: primariascobinti.ro/uploads/sites/64/2025/03/CALDURA-ANUNT-PE-SIT-UL-PRIMARIEI-.pdf | 10,962 |
| 3 | r3_pub-simleu-anunt-2023.txt | Șimleu Silvaniei 2023-24 notice: simleusilvaniei.ro/wp-content/uploads/2023/10/ANUNT-AJUTOR-INCALZIRE-2023-2024.pdf | 7,573 |
| 3 | r3_pub-suceava-precizari.txt | Suceava clarifications 2021: primariasv.ro (PRECIZARI attachment) | 14,349 |
| 3 | r3_pub-tirgumures-ghid.txt | Târgu Mureș guide: tirgumures.ro/attachments/article/8681/Ghid | 5,988 |
| 5 | r5_catalogue-serviciipublice.txt | National service catalogue entry "Ajutor de încălzire": serviciipublice.gov.ro/serviciu/ajutor-de-incalzire | 1,229 |
| 6 | r6_minor-alba24-2026.txt | Press explainer 2026-27: alba24.ro | 14,841 |
| 6 | r6_minor-fiscalitatea-2021.txt | Press explainer 2021 (reprints the law): fiscalitatea.ro | 69,662 |
| 6 | r6_minor-fiscalitatea-norme-2021.txt | Press explainer on the norms 2021: fiscalitatea.ro | 14,381 |
| ref | reference/po-simeria-heating.txt | primariasimeria.ro/storage/2024/05/PO-DAS-SBS-05-MASURILE-DE-PROTECTIE-SOCIALA-PENTRU-CONSUMATORUL-VULNERABIL-DE-ENERGIE-IN-PERIOADA-SEZONULUI-RECE.pdf (one of 53 procedures the directorate publishes) | 86,374 |

Rank 4 (the application form) is inside the norms file as an annex, so no separate rank-4 file exists.

## Outputs

- `ledger_public_opus.json`: forward run, ranks 1 to 6 in order (82 claims, 45 order statements, 18 contradictions, 40 questions).
- `ledger_public_opus_run2.json`: second forward run (68 claims), public-only snapshot of the plus-PO run.
- `ledger_public_reverse_opus.json`: same sources read in reverse rank order (62 claims).
- `ledger_public_plus_po_opus.json`: forward run plus the procedure as rank 7 (79 claims).
- `reference_po_opus.json`: 50 steps written from the procedure alone, no ledger seen.
- `align_*_vs_po.json`: each ledger aligned to the 50 reference steps (Opus judge).
- `align_forward_vs_reverse.json`: forward and reverse ledgers aligned to each other.
- `verify_forward_{1,2,3}.json`: the 82 forward claims (batches in `batches/`) checked claim by claim against the procedure, quotes verified against the text.
- Prompts: `../prompts/ro_sequential_ingestion.md`, `ro_verify_vs_procedure.md`, `ro_align_to_procedure.md`.

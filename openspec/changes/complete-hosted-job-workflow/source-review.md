# Source review — 2026-10-07

Evidence gathered from the live saved receipts, candidate-authorized exports (source entries only), official career pages and public feed requests from the VPS. No candidate facts were imported into this file.

| Source | Evidence | Approved repair / decision |
|---|---|---|
| HubSpot | Existing `hubspot` Greenhouse endpoint returns 404. [Official careers](https://www.hubspot.com/careers/jobs) shows openings and links an alert board identifier `hubspotjobs`; that public feed also returned 404. | Replace broken board with official manual careers URL; remove stale API. The alert identifier does not prove a working replacement feed. |
| Hightouch | Old Greenhouse feed fails. [Official careers](https://hightouch.com/careers) lists role pages under its own domain. A guessed Ashby slug returned JSON but was not matched to official role identities. | Use official manual page; remove stale API. Do not treat successful JSON as employer identity evidence. |
| Weights & Biases | Browser observed the [official W&B page](https://coreweave.com/careers/weights-biases) request `https://boards-api.greenhouse.io/v1/boards/weights_and_biases/jobs?content=true`. Feed returned eight W&B-specific openings and official CoreWeave W&B posting links. | Preserve official careers URL; add the observed dedicated Greenhouse API. This avoids importing unrelated CoreWeave jobs. |
| Retool | [Official page](https://retool.com/careers) has its own role pages; tested Greenhouse/Ashby feeds were not usable. | Retain manual source; no guessed replacement. |
| Salesforce | [Official page](https://careers.salesforce.com/) is outside the three hosted ATS adapters. | Retain manual coverage; Workday/custom provider integration is future work. |
| Langfuse | [Official page](https://langfuse.com/careers) links ClickHouse careers with a Langfuse search parameter. | Retain manual company-scoped entry. Scanning all ClickHouse roles as Langfuse would misattribute results. |
| Lindy | [Official page](https://careers.lindy.ai/) uses Teamtailor. | Retain manual source; dedicated Teamtailor adapter would be a separate provider increment. |
| Make.com (Celonis) | Configured official careers URL remains outside current ATS adapters; direct VPS probe returned 403. | Retain manual source; no parent-board substitution or claim of an empty market. |
| Zep AI | [Official page](https://www.getzep.com/careers/) contains direct roles; no verified supported public feed found in bounded review. | Retain manual source. |

This is bounded source verification, not proof that no other public API exists. The exact-address repair uses candidate-owner locking and private filter-history checkpoints; unrelated filters, CLI scan methods and candidate facts remain intact. Existing receipts retain historical errors. A new search uses repaired settings; manual sources still appear as unsupported automated coverage.

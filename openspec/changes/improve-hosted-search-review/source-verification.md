# Source verification — October 3, 2026

Verified public endpoints using Node fetch on the VPS, the same HTTP client as the scanner. Python urllib returned 403 from these endpoints and is not evidence that the Node scanner cannot reach them.

| Source | Replacement / action | Public evidence |
|---|---|---|
| Temporal | Ashby `temporal`, 64 postings | [Official careers](https://temporal.io/careers), employer-hosted Ashby posting [example](https://jobs.ashbyhq.com/temporal/59b0a2e1-b802-46c3-8b26-415684a7be32/) |
| RunPod | Ashby `runpod`, 26 postings | [Official careers](https://www.runpod.io/careers) embeds the runpod posting API |
| Runway | Ashby `runway-ml`, 45 postings | [Official careers](https://runway.com/careers) links runway-ml postings |
| OpenAI | Ashby `openai`, 829 postings; retain branded careers link | [Employer posting](https://jobs.ashbyhq.com/openai/e827d138-22de-49f0-9de5-60f3e3ce07a0/) |
| Lindy | Manual careers link; remove obsolete Ashby slug | [Official career site](https://careers.lindy.ai); supported scanner has no adapter for it |
| Weights & Biases | Manual filtered employer careers link | [Official W&B careers](https://site.wandb.ai/careers/) links [CoreWeave W&B careers](https://coreweave.com/careers/weights-biases). Do not scan all CoreWeave roles under the W&B label |
| Hightouch | Preserve original source and explicit error; manual page link | Greenhouse API returns 404 while [public employer board](https://job-boards.greenhouse.io/hightouch) lists current jobs. Ashby `hightouch` returns one historical analytics role and must not replace the current board |

Retool, Salesforce, Langfuse, Make.com and Zep remain explicit unsupported sources when no supported verified current endpoint was established. Broader configured web queries are disclosed as not executed. No source repair changes title, location or salary preferences. Repairs match only exact known old addresses and preserve owner customizations. All repairs take an automatic filter-history checkpoint.

---
title: Licence Review Worksheet – Open Source Ai
description: Worksheet for the catalog entries whose upstream licences need human review – quoted clauses and reviewer questions.
---
# Licence Review Worksheet

**This worksheet is not legal advice and draws no legal conclusions.** It lists the catalog entries marked *needs review*, quotes the upstream clauses that caused the flag, and lists the questions a reviewer (ideally with legal input) must answer before the catalog describes the licence differently.

- **Source:** each upstream licence file, fetched via the GitHub API (`/repos/{owner}/{repo}/license` and, for AutoGen, `/contents/LICENSE-CODE`) on **2026-10-21**. Quotes are verbatim excerpts; read the full file before deciding.
- **The upstream file is authoritative.** Files can change; re-fetch before signing off.
- **How to record a decision:** edit the entry in `catalog/projects.yaml` (`license.label`, `license.state`, `license.review_reason`), add a CHANGELOG line naming the reviewer and date, and open a PR. Keep `needs-review` unless every question below is answered.

General questions for every entry:

1. Does the quoted text match the current upstream file (same commit/branch)?
2. Which parts of the repository does each licence apply to, and does the catalog description make that clear?
3. Is the catalog wording ("source-available", "multiple licences", "custom terms") accurate and neutral?

## Summary

| # | Project | Licence file | Why flagged |
|---|---|---|---|
| 1 | LiteLLM | [LICENSE](https://github.com/BerriAI/litellm/blob/main/LICENSE) | Separate licence for `enterprise/` |
| 2 | Open WebUI | [LICENSE](https://github.com/open-webui/open-webui/blob/main/LICENSE) | Branding clause added to BSD-style terms |
| 3 | Lobe Chat | [LICENSE](https://github.com/lobehub/lobehub/blob/canary/LICENSE) | Apache-2.0 plus commercial-licence condition |
| 4 | AutoGen | [LICENSE](https://github.com/microsoft/autogen/blob/main/LICENSE), [LICENSE-CODE](https://github.com/microsoft/autogen/blob/main/LICENSE-CODE) | Two licence files (CC-BY-4.0 and MIT) |
| 5 | Dify | [LICENSE](https://github.com/langgenius/dify/blob/main/LICENSE) | Modified Apache-2.0 with extra conditions |
| 6 | Flowise | [LICENSE.md](https://github.com/FlowiseAI/Flowise/blob/main/LICENSE.md) | Commercial licence for enterprise code |
| 7 | n8n | [LICENSE.md](https://github.com/n8n-io/n8n/blob/master/LICENSE.md) | Sustainable Use License + enterprise files |
| 8 | Weaviate | [LICENSE](https://github.com/weaviate/weaviate/blob/main/LICENSE) | BSD-3-Clause outside `wl/`, enterprise inside |
| 9 | Langfuse | [LICENSE](https://github.com/langfuse/langfuse/blob/main/LICENSE) | Separate licence for `ee/` directories |
| 10 | Phoenix | [LICENSE](https://github.com/Arize-ai/phoenix/blob/main/LICENSE) | Elastic License 2.0 |
| 11 | Trylon Gateway | [LICENSE](https://github.com/trylonai/gateway/blob/main/LICENSE) | Business Source License 1.1 |
| 12 | llamafile | [LICENSE](https://github.com/mozilla-ai/llamafile/blob/main/LICENSE) | GitHub detection NOASSERTION; bundled third-party code |
| 13–15 | AgentDomains, AgentDomains MCP, AgentDomains Skill | [LICENSE](https://github.com/tashfeenahmed/AgentDomains/blob/main/LICENSE) ([MCP](https://github.com/tashfeenahmed/AgentDomains-mcp/blob/main/LICENSE), [Skill](https://github.com/tashfeenahmed/AgentDomains-skill/blob/main/LICENSE)) | Functional Source License 1.1 |

## 1. LiteLLM

> All content that resides under the "enterprise/" directory of this repository, if that directory exists, is licensed under the license defined in "enterprise/LICENSE".
>
> Content outside of the above mentioned directories or restrictions above is available under the MIT license as defined below.

Questions: What are the terms of `enterprise/LICENSE`? Does the recipe's container image (`ghcr.io/berriai/litellm`) include enterprise code, and under what conditions is it usable? Should the catalog label read "MIT (core) + separate enterprise licence"?

## 2. Open WebUI

> 4. Notwithstanding any other provision of this License, and as a material condition of the rights granted herein, licensees are strictly prohibited from altering, removing, obscuring, or replacing any "Open WebUI" branding […] in any deployment or distribution, except in the following circumstances: (i) deployments or distributions where the total number of end users […] does not exceed fifty (50) within any rolling thirty (30) day period; (ii) the licensee has obtained specific prior written permission from the copyright holder; or (iii) where the licensee has obtained a duly executed enterprise license expressly permitting such modification.

> Materials governed by prior licenses retain those original license terms, as specified in LICENSE_HISTORY.

Questions: How should the catalog describe a BSD-3-style licence with an added branding condition? Which versions are covered by `LICENSE_HISTORY`, and does that affect the pinned recipe version (v0.12.3)? Does the recipe (unmodified image) raise any branding concern? (It does not alter branding.)

## 3. Lobe Chat

> From 1.0, LobeChat is licensed under the LobeHub Community License, based on Apache License 2.0 with the following additional conditions:
>
> b. a commercial license must be obtained from the producer if you want to develop and distribute a derivative work based on LobeChat.

> a. The producer can adjust the open-source agreement to be more strict or relaxed as deemed necessary.

Questions: What counts as a "derivative work" here? How should the catalog convey that distributing modified versions needs a commercial licence? Does the "adjust the agreement" clause affect how often this entry must be re-reviewed?

## 4. AutoGen

`LICENSE` begins:

> Attribution 4.0 International

`LICENSE-CODE` begins:

> MIT License
>
> Copyright (c) Microsoft Corporation.

Questions: Does the repository state which files fall under CC-BY-4.0 (documentation) and which under MIT (code)? GitHub reports only CC-BY-4.0 — should the catalog label list both, as it does now?

## 5. Dify

> Dify is licensed under a modified version of the Apache License 2.0, with the following additional conditions:

> a. Multi-tenant service: Unless explicitly authorized by Dify in writing, you may not use the Dify source code to operate a multi-tenant environment.

> b. LOGO and copyright information: In the process of using Dify's frontend, you may not remove or modify the LOGO or copyright information in the Dify console or applications.

Questions: How should "one tenant corresponds to one workspace" be summarised for readers? Is "modified Apache-2.0 with additional conditions" a fair label? Should the catalog mention the multi-tenant condition on the project page?

## 6. Flowise

> All content that resides under https://github.com/FlowiseAI/Flowise/tree/main/packages/server/src/enterprise directory and files with explicit copyright notice such as [IdentityManager.ts](…) are licensed under [Commercial License](…).

> Content outside of the above mentioned directories or restrictions above is available under the "Apache 2.0" license as defined below.

Questions: Which files outside `enterprise/` carry "explicit copyright notice" and therefore the commercial licence? The repository is also **archived upstream** (see freshness report) — should the entry be kept, and with what note?

## 7. n8n

> Content of branches other than the main branch (i.e. "master") are not licensed.

> Source code files that contain ".ee." in their filename or ".ee" in their dirname are NOT licensed under the Sustainable Use License.

> You may use or modify the software only for your own internal business purposes or for non-commercial or personal use. You may distribute the software or provide it to others only if you do so free of charge for non-commercial purposes.

Questions: Is "source-available, not OSI" the right category label? How should the catalog phrase the internal-business-use limitation neutrally? Should the selection criteria explicitly allow such licences?

## 8. Weaviate

> Outside of the "wl" directory, source code in a given file is licensed under the BSD-3-Clause License, as defined in LICENSE-BSD.

> Within the "wl" directory and all its sub-directories, source code is Copyright Weaviate BV 2026-present, all rights reserved, and is only available under a separate enterprise license.

Questions: Does the standard distribution (binaries/images) include `wl/` code, and is it gated by licence key as the file says ("Enterprise features are enabled via license key")? Is "BSD-3-Clause (core)" an adequate label?

## 9. Langfuse

> All content that resides under the "ee/", "web/src/ee/", and/or "worker/src/ee/" directories of this repository, if these directories exist, is licensed under the license defined in "ee/LICENSE".

> Content outside of the above mentioned directories or restrictions above is available under the "MIT Expat" license as defined below.

Questions: What are the terms of `ee/LICENSE`? Are `ee/` features included in self-hosted images by default?

## 10. Phoenix

> Elastic License 2.0 (ELv2)

> You may not provide the software to third parties as a hosted or managed service, where the service provides users with access to any substantial set of the features or functionality of the software.

> You may not move, change, disable, or circumvent the license key functionality in the software […]

Questions: Is "source-available, not OSI" the right label? Should the selection criteria say how Elastic-licensed projects are treated?

## 11. Trylon Gateway

> BUSINESS SOURCE LICENSE 1.1

> Use Limitation: You may not use the Licensed Work for production purposes if you are providing a software-as-a-service (SaaS) offering that utilizes the Licensed Work to supply large language model (LLM) security guardrail capabilities to third parties, and this offering competes directly with Trylon AI's commercial cloud services.

> Change Date: 2028-04-03
>
> Change License: Apache License, Version 2.0

> The Licensed Work is the code specified in the NOTICE file.

Questions: What does the NOTICE file include as the "Licensed Work"? Should the catalog show the change date and change licence? When should this entry be re-reviewed (on or after 2028-04-03)?

## 12. llamafile

The licence file is short Apache-2.0 boilerplate:

> The Apache 2.0 License
>
> Copyright 2023 Mozilla Foundation
>
> Licensed under the Apache License, Version 2.0 (the "License");

GitHub's detector returns `NOASSERTION` for it. The repository root (listed via the API on 2026-10-21) also contains `.gitmodules`, `third_party/`, `llama.cpp`, `whisper.cpp` and `stable-diffusion.cpp` entries.

Questions: Do the bundled/vendored components carry other licences that apply to distributed llamafile binaries? If the Apache-2.0 file covers the project's own code, can the entry be `declared: Apache-2.0` with a note about third-party components?

## 13–15. AgentDomains, AgentDomains MCP, AgentDomains Skill

All three repositories have byte-identical licence files (checked 2026-10-21):

> # Functional Source License, Version 1.1, Apache 2.0 Future License

> A Permitted Purpose is any purpose other than a Competing Use. A Competing Use means making the Software available to others in a commercial product or service that:
>
> 1. substitutes for the Software;
>
> 2. substitutes for any other product or service we offer using the Software that exists as of the date we make the Software available; or
>
> 3. offers the same or substantially similar functionality as the Software.

> We hereby irrevocably grant you an additional license to use the Software under the Apache License, Version 2.0 that is effective on the second anniversary of the date we make the Software available.

Questions: `FSL-1.1-Apache-2.0` is an SPDX identifier — should the catalog use it as the label with state `needs-review` (source-available), as now? Is the two-year conversion per release, and should the catalog note it?

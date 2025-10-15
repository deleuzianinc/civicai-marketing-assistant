# CivicAI Marketing Assistant — MVP Implementation Plan (Revised)
**Scope:** Marketing assistant for **getcivicai.com** that educates prospects about the CivicAI *campaign assistant*, qualifies interest, and captures conversions (demo requests or email leads). Implemented in Dialogflow CX and exported as JSON to `src/`.

---

## 1) Goals & Non‑Goals

**Goals (MVP)**
- **Educate**: Answer product, pricing, security, and integration questions using an approved knowledge base of CivicAI marketing content.
- **Qualify**: Light qualification on *campaign status* and *role* to prioritize demo vs. email capture.
- **Convert**: Drive **Demo Booking** (primary) and **Email Capture** (secondary).

**Non‑Goals (defer to Phase 2+)**
- Full BANT scoring, CRM sync, real‑time calendar scheduling, multi‑language, deep analytics dashboards, proactive behavioral triggers, and complex competitive comparisons.

---

## 2) Conversation Architecture (Hybrid, Playbooks + Flows)

- **Default Marketing Playbook (routine)** starts each conversation: greets, understands intent, answers KB questions with the **Marketing Data Store Tool**, and routes to flows for conversions.
- **Flow: “Marketing Site Flow”** handles predictable steps (qualification, forms, confirmation). Deterministic pages keep conversions fast and reliable.
- **Task Playbooks (lite)** (optional in MVP) provide structured handling of common topics (Pricing, Security & Compliance, Integrations/Deployment, Objection Handling) but always ground responses in the same Marketing Data Store.

> Why Hybrid? Playbooks provide dynamic, KB‑grounded answers. Flows keep capture paths deterministic and fast under load.

---

## 3) Dialogflow CX JSON Export Structure (what lands in `src/`)

> **Use this exact directory layout when exporting/syncing the agent to Git.**

```
src/
├── agent.json                                  # Agent-level settings (name, language, timezone, start config)
├── flows/
│   └── Marketing Site Flow/
│       ├── Marketing Site Flow.json            # Flow definition & NLU settings
│       ├── Entry Page/
│       │   └── Entry Page.json                 # Menu: Learn | Ask | Book Demo
│       ├── QnA Page/
│       │   └── QnA Page.json                   # Data Store Tool response + guardrails
│       ├── Qualify Page/
│       │   └── Qualify Page.json               # campaign_status, visitor_role
│       ├── DemoCapture Page/
│       │   └── DemoCapture Page.json           # name, email(@sys.email), org; webhook: lead_export
│       ├── EmailCapture Page/
│       │   └── EmailCapture Page.json          # email only; webhook: lead_export
│       ├── Handoff Page/
│       │   └── Handoff Page.json               # optional human escalation
│       └── Fallback Page/
│           └── Fallback Page.json              # recovery options
├── intents/
│   ├── greeting.entry/
│   │   ├── greeting.entry.json
│   │   └── trainingPhrases/
│   │       └── en.json
│   ├── product.info/
│   │   ├── product.info.json
│   │   └── trainingPhrases/en.json
│   ├── pricing.inquiry/
│   │   ├── pricing.inquiry.json
│   │   └── trainingPhrases/en.json
│   ├── demo.request/
│   │   ├── demo.request.json
│   │   └── trainingPhrases/en.json
│   ├── security.integration/
│   │   ├── security.integration.json
│   │   └── trainingPhrases/en.json
│   ├── handoff.request/
│   │   ├── handoff.request.json
│   │   └── trainingPhrases/en.json
│   └── fallback/
│       ├── fallback.json
│       └── trainingPhrases/en.json
├── entityTypes/
│   ├── campaign_status/campaign_status.json    # values: active | planning | research
│   └── visitor_role/visitor_role.json          # values: decision_maker | recommender | researcher
├── playbooks/
│   ├── Default Marketing Playbook/
│   │   └── Default Marketing Playbook.json     # Conversation start (routine); triage + KB answers
│   ├── Pricing & Packaging (Lite)/Pricing & Packaging (Lite).json
│   ├── Security & Compliance (Lite)/Security & Compliance (Lite).json
│   ├── Integrations & Deployment (Lite)/Integrations & Deployment (Lite).json
│   └── Objection Handling (Lite)/Objection Handling (Lite).json
├── tools/
│   └── marketing_knowledge_base/
│       └── marketing_knowledge_base.json       # Data Store Tool bound to getcivicai.com sources
├── webhooks/
│   └── lead_export_webhook/
│       └── lead_export_webhook.json            # Single endpoint; tag-based routing
└── generators/                                 # (optional, empty in MVP)
```

**Notes on JSON content (high level, not field‑exact):**
- `agent.json` → agent identity, locale/timezone, conversation start set to the **Default Marketing Playbook**.
- **Pages** define: entry fulfillment, form parameters (for capture pages), transition routes, and route fulfillment (attach the Data Store Tool on QnA routes).
- **Intents** are minimal and B2B‑focused; each includes ~10–15 training phrases.
- **Entity types** house the two custom entities.
- **Playbooks** store goal/instructions and examples (few‑shot). Default playbook triages & routes; task playbooks focus each topic with tight guardrails.
- **Tools** contains the Data Store Tool definition bound to the site sources and response options (e.g., max citations).
- **Webhooks** define a single lead export endpoint; the flow passes `conversion_type` (demo/email/handoff) and captured fields.

---

## 4) Key Behaviors (MVP)

### A) Entry & Routing
- Default Marketing Playbook greets, offers: **Learn | Ask a question | Book a demo**.
- If **Ask** → route to **QnA Page** (flow) to answer via Data Store Tool and show a CTA.
- If **Book a demo** → route to **DemoCapture Page**.
- If **Learn** → brief KB‑grounded overview, then CTA to **Ask** or **Book a demo**.

### B) QnA (KB‑only)
- Route fulfillment uses the **Marketing Data Store Tool** to answer strictly from indexed pages. If no answer → “not found” + offer demo/email capture.
- Buying‑signal detection (pricing, integrations, deployment) nudges to **Qualify Page**.

### C) Qualification & Conversion
- **Qualify Page** asks `campaign_status` and (optionally) `visitor_role`, derives `lead_tier` (hot → demo; warm/cold → email capture offer).
- **DemoCapture Page** collects `visitor_name`, `visitor_email`(@sys.email), `organization_name`; calls `lead_export_webhook`; shows confirmation.
- **EmailCapture Page** collects `visitor_email` only → same webhook → confirmation.
- **Handoff Page** provides human escalation and optional email capture.

---

## 5) Data Store Tool & Knowledge Guardrails

- **Data Store**: PUBLIC_WEB sources (getcivicai.com) + optional uploaded PDFs/TXT of product one‑pagers.
- **Tool attachment**: On QnA routes, add Data Store Tool to fulfillment and enable “Data store tool response” with citations; define fallback.
- **Guardrails**: No hallucinated features, prices, or claims. On gaps, explicitly say “not found” and pivot to demo/email capture.

---

## 6) Parameters & Entities

**Session Parameters**
- `campaign_status` (@campaign_status) — “active | planning | research”
- `visitor_role` (@visitor_role) — “decision_maker | recommender | researcher”
- `visitor_name` (string), `visitor_email` (@sys.email), `organization_name` (string)
- `lead_tier` (derived: hot | warm | cold), `conversion_type` (demo | email | handoff)

**Validation**
- Email: use @sys.email plus permissive regex in webhook as needed.

---

## 7) Integrations (Website & Webhook)

**Messenger Embed (website)**
- Enable **Dialogflow CX Messenger** for the chosen environment.
- Use the generated `<script>` and `<df-messenger>` snippet on getcivicai.com.
- Keep unauthenticated API for public web chat (domain‑restricted if desired).

**Webhook (lead export)**
- Single endpoint; route by fulfillment **tag** (`lead_export`).
- MVP storage can be file/DB; log name/email/org plus `conversion_type` and timestamp.
- Add retries and basic auth/JWT verification (environment‑specific URLs).

---

## 8) Git Export/Restore & Environments

- Use **Git Export/Restore** to push JSON to repo (`src/` structure above). Create **Versions** for production deployments; update **Environments** with environment‑specific webhook URLs.
- Keep a backup export before major changes.

---

## 9) Acceptance Criteria

- **Start**: Default Marketing Playbook greets and routes correctly.
- **QnA**: Data Store Tool returns answers with citations; fallback shows “not found” + CTA.
- **Qualification**: `campaign_status` captured; `visitor_role` when offered.
- **Demo path**: Demo form validates and hits `lead_export` webhook; confirmation shown.
- **Email path**: Email form validates and hits `lead_export` webhook; confirmation shown.
- **Handoff**: Human handoff path available from any state (optional email capture).
- **Style**: 2–4 sentence responses, clear CTA every turn, campaign‑aware tone.
- **Testing**: Simulator runs for Learn → Ask → Demo; Learn → Ask → Email; Handoff; Fallback recovery.

---

## 10) Phase 2+ Backlog (high value later)

- Full BANT scoring, CRM sync (Salesforce/HubSpot), real‑time calendar booking, proactive triggers (time‑on‑page/exit intent), analytics dashboards, multi‑language, deeper compliance packs, and competitive comparisons.

---

## 11) Operating Notes

- Keep playbook instructions concise for latency; prefer flows for forms and confirmations.
- Train intents iteratively from real traffic.
- Treat the website copy as the **single source of truth**; keep the data store fresh when pages change.

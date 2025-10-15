Below is a **pared‑down MVP** you can hand to an implementer. It keeps only what’s essential for a useful first release in Dialogflow CX and pushes everything else to “Phase 2+”.

---

# CivicAI Marketing Assistant — **MVP Conversational Logic (Dialogflow CX)**

## 0) Goal (MVP)

Help political campaign visitors quickly (1) understand what CivicAI is, (2) get factual answers from a campaign‑approved knowledge base, and (3) convert to either **demo request** or **email capture**—with minimal complexity.

---

## 1) Core Intents (only what’s needed)

1. **Greeting / Entry**

   * *Train on:* hi, hello, hey, get started.
   * *Response:* Identify as CivicAI; one‑line purpose; offer 3 quick choices: **Learn what it is**, **Ask a question**, **Book a demo**.

2. **Product Info (KB‑backed Q&A)**

   * *Train on:* what is CivicAI, features, how it works.
   * *Action:* Call KB webhook → return short answer (no fabrication). If “not found,” say so and offer human/demo.

3. **Pricing (lite)**

   * *Train on:* price, cost, pricing tiers.
   * *Response:* Pricing depends on needs/volume; offer **email capture** or **demo** for specifics (no numbers unless in KB).

4. **Demo Request**

   * *Train on:* book demo, talk to sales, see it.
   * *Action:* Collect **name**, **email**, **organization**. Validate email format. Send to webhook. Confirm receipt.

5. **Security/Integration (lite)**

   * *Train on:* security, compliance, integrations.
   * *Response:* High‑level reassurance (answers from campaign‑approved content; data handled securely); if specifics not in KB → offer email/demo.

6. **Human Handoff**

   * *Train on:* talk to a person, human please.
   * *Action:* Collect email (if not already); create handoff ticket via webhook; confirm.

7. **Fallback**

   * *Action:* Apologize, suggest the 3 choices above, or ask the user to rephrase.

> **Out of MVP:** competitor comparisons, long small‑talk set, complex pricing calculators, multi‑language, sentiment routing.

---

## 2) Minimal Parameters & Entities

### Session Parameters (keep it lean)

* `campaign_status` ∈ {active, planning, research}  *(optional; ask only on buying signals)*
* `visitor_role` ∈ {decision_maker, recommender, researcher} *(optional; ask only on buying signals)*
* `primary_need_freeform` (string; optional)
* `visitor_name` (string; required for demo)
* `visitor_email` (string; required for demo/email capture; basic regex)
* `organization_name` (string; required for demo)
* **Derived:** `lead_tier` ∈ {hot, warm, cold}

### Minimal Entities

* `campaign_status`: active | planning | research
* `visitor_role`: decision_maker | recommender | researcher

> **Out of MVP:** granular campaign levels, full BANT, phone number, timeline, complex authority scoring.

---

## 3) Ultra‑Simple Qualification (only when relevant)

Ask only if user shows buying intent (asked pricing, demo, or deep product Qs):

1. “Are you currently **active**, **planning**, or just **researching**?” → `campaign_status`
2. “Are you the **decision maker**, a **recommender**, or **researching** options?” → `visitor_role` *(optional)*

**Lead‑tier rule (no arithmetic):**

```
if explicit_demo_request: lead_tier = "hot"
elif campaign_status == "active" and visitor_role == "decision_maker": lead_tier = "hot"
elif campaign_status in ["active","planning"]: lead_tier = "warm"
else: lead_tier = "cold"
```

---

## 4) Conversion Paths (only two)

### A) Demo Booking (primary)

**Trigger:** demo intent OR lead_tier = hot
**Collect (required):** `visitor_name`, `visitor_email`, `organization_name`
**Validate:** email format (simple regex)
**Do:** webhook → store lead + notify team → show confirmation (“We’ll follow up to schedule your demo.”)

> **Out of MVP:** live calendar integration, time‑slot negotiation, SMS confirmations.

### B) Email Capture (secondary)

**Trigger:** pricing intent without demo, lead_tier = warm/cold, or “send me more info”
**Collect:** `visitor_email`
**Do:** webhook → store + send product sheet / follow‑up commitment; confirm.

---

## 5) Knowledge Base Rules (must‑have guardrails)

* **Always answer from KB results only.**
* If KB **has** an answer: return a **2–4 sentence** paraphrase; offer “Want more detail or a quick demo?”
* If KB **missing**: say “I don’t have that specific information.” → offer human or demo.
* Keep a single **KB Search** webhook: input = user question + (optional) session context; output = short passage or “not found”.

> **Out of MVP:** multi‑document citations, confidence scores, retrieval filters, analytics dashboards.

---

## 6) Minimal Objection Handling (one line + action)

1. **Message control / accuracy:**
   “CivicAI answers only from your campaign‑approved knowledge base (no improvising). Every response is auditable.”
   → Offer demo.

2. **Complexity / setup:**
   “Setup is no‑code: add an embed snippet and load your approved content.”
   → Offer demo or simple install guide (if in KB).

3. **Cost / ROI:**
   “We tailor pricing to needs and volume. Want us to email details or set a quick demo?”
   → Email capture or demo.

> **Out of MVP:** quantified ROI claims, competitor breakdowns, detailed security/compliance frameworks unless present in KB.

---

## 7) Dialogflow CX Shape (simple & buildable)

* **Single Flow:** `Main`

  * **Pages:**

    * `Entry` (Greeting & quick options)
    * `QnA` (KB answers)
    * `Qualify` (only if buying signals)
    * `DemoCapture` (form with name/email/org)
    * `EmailCapture` (form with email)
    * `Handoff` (confirmation)
    * `Fallback`
  * **Routes:**

    * Intent routes to `QnA`, `Pricing`, `Demo`, `Security/Integration`, `Handoff`.
    * Conditional route to `Qualify` when pricing/demo/deep product intent detected and `campaign_status` is unset.
    * After `Qualify`, evaluate `lead_tier` → route to `DemoCapture` (hot) or suggest `EmailCapture` (warm/cold).

* **Webhooks (2 only):**

  1. `kb_search` – returns short answer or `not_found`.
  2. `lead_export` – stores all captured fields + intent + timestamp (for both Demo and Email Capture).

> **Out of MVP:** separate flows, advanced context carryover, analytics events, multi‑environment A/B tests.

---

## 8) Response Style (lightweight defaults)

* **Length:** aim 2–4 sentences; bullets ≤5.
* **Tone:** campaign‑savvy, plain language.
* **No promises** not in KB (e.g., specific compliance certifications, timelines, or integrations).
* **Always** offer one clear next step (demo or email).

---

## 9) Copy Snippets (ready to paste)

* **Greeting:**
  “I’m the CivicAI assistant. We help campaigns turn site visitors into engaged supporters using an on‑message chat experience. Would you like to **learn what it is**, **ask a question**, or **book a demo**?”

* **KB ‘not found’:**
  “I don’t have that specific information in my approved sources. I can connect you with our team or set a quick demo—what’s best?”

* **Pricing (lite):**
  “Pricing depends on your needs and conversation volume. I can email you a one‑pager or set a quick demo—what do you prefer?”

* **Demo capture confirm:**
  “Thanks! We’ve received your details and will follow up shortly to schedule your demo.”

* **Email capture confirm:**
  “Got it. We’ll send a short overview to your email.”

---

## 10) What We’re **Explicitly** Deferring (Phase 2+)

* Full BANT & 15‑point scoring
* Calendar/time‑slot integration
* Deep security/compliance specifics & certifications list
* Detailed competitor comparisons
* Complex integrations & API configuration
* Multi‑turn installation wizards
* Multi‑language, sentiment routing, user profiles
* Advanced analytics dashboards

---

### Acceptance Checklist (MVP “done”)

* [ ] 7 intents working with sample phrases
* [ ] 2 webhooks (`kb_search`, `lead_export`)
* [ ] Demo form (name, email, org) with email validation
* [ ] Email‑only capture flow
* [ ] Simple qualification + `lead_tier` derivation
* [ ] KB‑only answers with safe fallback and human option

This gives you the smallest viable assistant that’s useful on day one and easy to extend later.

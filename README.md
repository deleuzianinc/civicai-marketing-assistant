# CivicAI Marketing Website Assistant

> **Transform marketing website visitors into qualified sales leads through intelligent conversation, product education, and frictionless conversion experiences.**

[![Dialogflow CX](https://img.shields.io/badge/Dialogflow-CX-blue.svg)](https://cloud.google.com/dialogflow/cx/docs)
[![Google Cloud](https://img.shields.io/badge/Google-Cloud-orange.svg)](https://cloud.google.com)
[![B2B Lead Generation](https://img.shields.io/badge/B2B-Lead%20Generation-green.svg)]()

## Executive Summary

**CivicAI Marketing Website Assistant** is a Dialogflow CX conversational agent designed specifically for the CivicAI product marketing website (getcivicai.com). This B2B SaaS lead qualification assistant educates prospects about CivicAI's campaign assistant product, answers questions using an approved knowledge base, and converts website visitors into demo bookings and email captures.

### What This Repository Contains

This is **NOT a traditional code repository** with application code to build and run. This repository contains:

- **Dialogflow CX Agent Export** (`src/`): JSON configuration files exported from Dialogflow CX Console
- **Project Documentation** (`docs/`): Architecture guides, MVP specifications, and technical references
- **Knowledge Base Source** (`civicai-website.md`): Marketing content used to populate the agent's knowledge base
- **Development Tools**: Python utilities for knowledge base processing and MCP server integration

### Key Features

- **Knowledge Base-Grounded Responses**: All product answers come from approved marketing content (no hallucinations)
- **Lead Qualification**: Intelligently qualifies visitors and routes to demo booking or email capture
- **Playbook Architecture**: ROUTINE-based playbooks for reliable, predictable conversations
- **Conversion Optimization**: Dual conversion paths (demo request primary, email capture secondary)
- **Campaign-Aware Messaging**: B2B SaaS tone with consistent product positioning

---

## Table of Contents

- [Project Architecture](#project-architecture)
- [Repository Structure](#repository-structure)
- [Agent Components](#agent-components)
- [Conversation Flow](#conversation-flow)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Testing & Validation](#testing--validation)
- [Deployment](#deployment)
- [Documentation](#documentation)
- [Contributing](#contributing)

---

## Project Architecture

### Hybrid Playbook + Flow Architecture

CivicAI Marketing Assistant uses Dialogflow CX's hybrid architecture combining:

1. **ROUTINE Playbooks**: LLM-powered conversations with knowledge base integration for Q&A
2. **Deterministic Flows**: State machine-based conversion paths for demo capture and email collection
3. **Data Store Tool**: Marketing knowledge base for grounded product answers

```
Website Visitor → Initial Triage Playbook
                    ├─ Product Questions → Product_Info_Q&A Playbook → KB Tool
                    ├─ Pricing Questions → Pricing_&_Packaging Playbook → KB Tool
                    ├─ Security Questions → Security_&_Compliance Playbook → KB Tool
                    ├─ Integration Questions → Integrations_&_Deployment Playbook → KB Tool
                    ├─ Objections → Objection_Handling Playbook
                    └─ Demo Request → Marketing Site Flow → DemoCapture/EmailCapture
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Agent Platform** | Dialogflow CX | Conversation management and orchestration |
| **Knowledge Base** | Data Store (Vertex AI Search) | Marketing content search and retrieval |
| **Playbooks** | Generative AI Agents | Dynamic Q&A with tool integration |
| **Flows** | State Machine | Deterministic conversion paths |
| **Webhooks** | Google Cloud Functions (planned) | Lead export and CRM integration |
| **Hosting** | Google Cloud Platform | Agent hosting and data storage |

---

## Repository Structure

```
civicai-website-assistant/
├── README.md                              # This file
├── CLAUDE.md                              # Development guide for AI assistants
├── MARKETING-ASSISTANT-MVP-PLAN.md        # MVP implementation plan
├── AGENT_DIAGNOSIS_AND_FIXES.md           # Recent bug fixes and diagnosis
├── REFACTORING_CHANGELOG.md               # Playbook refactoring history
│
├── src/                                   # **DIALOGFLOW CX AGENT EXPORT**
│   ├── agent.json                         # Agent configuration
│   │
│   ├── playbooks/                         # ROUTINE playbooks (LLM-powered)
│   │   ├── Initial Triage/                # Entry point routing playbook
│   │   ├── Product_Info_Q&A/              # Product questions playbook
│   │   ├── Pricing & Packaging/           # Pricing inquiries playbook
│   │   ├── Security & Compliance/         # Security questions playbook
│   │   ├── Integrations & Deployment/     # Integration questions playbook
│   │   └── Objection Handling/            # Objection handling playbook
│   │
│   ├── flows/                             # Deterministic flows
│   │   └── Marketing Site Flow/           # Main conversion flow
│   │       ├── Entry Page/                # Flow entry point
│   │       ├── QnA Page/                  # Knowledge base Q&A
│   │       ├── Qualify Page/              # Lead qualification
│   │       ├── DemoCapture Page/          # Demo booking form
│   │       ├── EmailCapture Page/         # Email capture form
│   │       ├── Handoff Page/              # Human escalation
│   │       └── Fallback Page/             # Error recovery
│   │
│   ├── intents/                           # User input classification
│   │   ├── greeting.entry/                # Greeting intent
│   │   ├── product.info/                  # Product information intent
│   │   ├── pricing.inquiry/               # Pricing intent
│   │   ├── demo.request/                  # Demo request intent
│   │   ├── security.integration/          # Security/integration intent
│   │   ├── handoff.request/               # Human handoff intent
│   │   └── fallback/                      # Fallback intent
│   │
│   ├── entityTypes/                       # Custom entities
│   │   ├── campaign_status/               # active | planning | research
│   │   └── visitor_role/                  # decision_maker | recommender | researcher
│   │
│   ├── tools/                             # External integrations
│   │   └── marketing_knowledge_base/      # Data Store tool config
│   │
│   ├── webhooks/                          # Webhook configurations
│   │   └── lead_export_webhook/           # Lead export webhook config
│   │
│   └── generators/                        # (Optional, empty in MVP)
│
├── docs/                                  # Project documentation
│   ├── README.md                          # Campaign agent reference (different project)
│   ├── minimum-mvp.md                     # MVP specification
│   ├── one-pager_v1.md                   # Product positioning
│   ├── civicai_agent.md                  # Campaign agent reference
│   └── dialogflow_cx_documentation.md     # Dialogflow CX technical guide
│
├── civicai-website.md                     # **KNOWLEDGE BASE SOURCE**
├── dialogflow_chroma_db/                  # ChromaDB vector store (gitignored)
├── fix_all_paths.py                       # Path fixing utility
├── mcp_server.py                          # MCP server for Dialogflow docs
├── .gitignore                             # Git ignore rules
└── .venv/                                 # Python virtual environment
```

---

## Agent Components

### Core Playbooks (6 Total)

#### 1. Initial Triage (Entry Point)
**Type**: ROUTINE (starred start playbook)
**Purpose**: Classify visitor intent and route to appropriate specialist playbook or conversion flow
**Routes to**: Product_Info_Q&A, Pricing_&_Packaging, Security_&_Compliance, Integrations_&_Deployment, Objection_Handling, Marketing Site Flow
**Examples**: 5 conversation examples covering all routing scenarios

#### 2. Product_Info_Q&A
**Type**: ROUTINE
**Purpose**: Answer product questions using knowledge base tool
**Tool**: marketing_knowledge_base (mandatory)
**Examples**: 5 examples including tool usage and buying signal detection
**Key Feature**: Tool-first policy prevents hallucination

#### 3. Pricing_&_Packaging
**Type**: ROUTINE
**Purpose**: Handle pricing inquiries and drive to demo/email capture
**Tool**: marketing_knowledge_base
**Examples**: 5 examples including budget questions and discount inquiries
**Guardrail**: Never fabricates pricing numbers not in KB

#### 4. Security_&_Compliance
**Type**: ROUTINE
**Purpose**: Address security and compliance questions
**Tool**: marketing_knowledge_base
**Examples**: 5 examples covering SOC2, data residency, PII handling, access controls
**Fallback**: Routes to demo for detailed security documentation requests

#### 5. Integrations_&_Deployment
**Type**: ROUTINE
**Purpose**: Answer integration and deployment questions
**Tool**: marketing_knowledge_base
**Examples**: 5 examples including HubSpot, Webflow, Google SSO, webhooks
**Key Message**: Rapid deployment ("live in under 30 minutes")

#### 6. Objection_Handling
**Type**: ROUTINE
**Purpose**: Handle objections and competitive questions
**Tool**: marketing_knowledge_base
**Examples**: 5 examples including message control, setup complexity, cost/ROI, competitive questions
**Routes to**: Other specialist playbooks or Marketing Site Flow

### Marketing Site Flow (Deterministic)

**Type**: Flow (state machine)
**Purpose**: Conversion paths for demo booking and email capture
**Pages**: 7 (Entry, QnA, Qualify, DemoCapture, EmailCapture, Handoff, Fallback)

#### Key Pages:

- **Entry Page**: Offers quick choices (Learn | Ask | Book Demo)
- **QnA Page**: Generative responses with KB tool integration
- **Qualify Page**: Collects campaign_status and visitor_role for lead tiering
- **DemoCapture Page**: Collects name, email, organization → webhook → confirmation
- **EmailCapture Page**: Collects email only → webhook → confirmation
- **Handoff Page**: Human escalation with optional email capture
- **Fallback Page**: Error recovery with menu options

### Intents (7 Core)

1. **greeting.entry**: Welcome and menu presentation
2. **product.info**: Product information requests
3. **pricing.inquiry**: Pricing questions
4. **demo.request**: Demo booking requests
5. **security.integration**: Security and integration questions
6. **handoff.request**: Human escalation requests
7. **fallback**: Unmatched input handling

### Session Parameters

```javascript
{
  "campaign_status": "active | planning | research",  // Optional qualification
  "visitor_role": "decision_maker | recommender | researcher",  // Optional
  "visitor_name": "string",  // Required for demo
  "visitor_email": "string",  // Required for conversions
  "organization_name": "string",  // Required for demo
  "lead_tier": "hot | warm | cold"  // Derived from qualification
}
```

### Lead Qualification Logic

```python
if explicit_demo_request:
    lead_tier = "hot"
elif campaign_status == "active" and visitor_role == "decision_maker":
    lead_tier = "hot"
elif campaign_status in ["active", "planning"]:
    lead_tier = "warm"
else:
    lead_tier = "cold"
```

**Routing**:
- **Hot leads** → Demo booking (primary conversion)
- **Warm/Cold leads** → Email capture (secondary conversion)

---

## Conversation Flow

### High-Level Flow

```
1. Visitor lands on getcivicai.com
   ↓
2. Dialogflow Messenger widget appears
   ↓
3. Initial Triage playbook greets visitor
   ↓
4. Visitor asks question or requests demo
   ↓
5a. Product Question Path:
    Initial Triage → Specialist Playbook → KB Tool → Answer + CTA
    ↓
    [Buying signal detected] → Marketing Site Flow → Qualify → DemoCapture

5b. Direct Demo Path:
    Initial Triage → Marketing Site Flow → DemoCapture Page
    ↓
    Collect: name, email, organization
    ↓
    Webhook: lead_export
    ↓
    Confirmation + Follow-up promise
```

### Example Conversation (Product Question → Demo)

```
User: what is civicai

[Initial Triage routes to Product_Info_Q&A]
[Product_Info_Q&A invokes marketing_knowledge_base tool]

Agent: CivicAI is a conversational AI platform that helps political campaigns
convert website visitors into supporters through on-message chat experiences.
We provide intelligent chatbots that answer voter questions, capture leads,
and drive conversions while maintaining your campaign's voice and messaging.
Want to see it in action? Book a demo.

User: yes book a demo

[Product_Info_Q&A detects buying signal, routes to Marketing Site Flow]

Agent: Great! Let me get a few details to schedule your demo.
Agent: What's your name?

User: John Smith

Agent: And your email address?

User: john@example.com

Agent: What campaign or organization are you with?

User: TechStartup Inc

[DemoCapture Page collects all fields, fires lead_export webhook]

Agent: Thanks, John! We've received your details and will follow up shortly
to schedule your demo.
```

---

## Getting Started

### Prerequisites

1. **Google Cloud Project** with Dialogflow CX API enabled
2. **Service Account** with Dialogflow CX permissions
3. **Data Store** (Vertex AI Search) populated with marketing content
4. **Dialogflow CX Console** access

### Important: This is NOT Traditional Code

This repository contains **Dialogflow CX configuration files**, not application code. You cannot:
- Run `npm install` or `pip install`
- Execute `npm start` or `python main.py`
- Build Docker images from this repo

Instead, you work with this project by:
1. **Importing** the `src/` directory into Dialogflow CX Console
2. **Editing** flows and playbooks visually in the console
3. **Exporting** changes back to `src/` for version control
4. **Testing** in the Dialogflow CX Simulator

### Quick Start: Import Agent

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/civicai-website-assistant.git
cd civicai-website-assistant

# 2. Create agent package
zip -r agent_export.zip src/

# 3. Import to Dialogflow CX Console
# Navigate to: Dialogflow CX Console → Agent Settings → Export and Import
# Click: Restore → Upload agent_export.zip
```

### Set Up Knowledge Base

The agent requires a Data Store populated with marketing content:

```bash
# 1. Set up Python environment (for KB processing)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install chromadb anthropic

# 2. Process marketing content (if using ChromaDB locally)
python document_processor.py --input civicai-website.md --output dialogflow_chroma_db/

# 3. In Dialogflow CX Console, create Data Store
# Console → Manage → Data Stores → Create Data Store
# Type: Website
# Source: getcivicai.com
# Name: civicai-marketing-content

# 4. Bind Data Store to marketing_knowledge_base tool
# Console → Manage → Tools → marketing_knowledge_base → Edit → Select Data Store
```

### Test in Simulator

```bash
# Testing is done in Dialogflow CX Console, not command line
# Console → Test Agent (right panel)

# Test scenarios:
1. "what is civicai" → Should return KB-grounded answer + CTA
2. "how much does it cost" → Should return pricing posture + demo offer
3. "book a demo" → Should collect name, email, organization
4. "is it secure" → Should return security answer from KB
5. "talk to a person" → Should offer human handoff
```

---

## Development Workflow

### Working with Dialogflow CX Console

Development happens primarily in the **Dialogflow CX Console**, not in code editors:

#### 1. Modifying Playbooks
```
Console → Playbooks → Select Playbook → Edit
- Update goal and instructions
- Add/modify examples (critical for LLM behavior)
- Adjust referenced tools/flows/playbooks
- Test in simulator
```

#### 2. Modifying Flows
```
Console → Flows → Select Flow → Select Page → Edit
- Update fulfillment messages
- Modify form parameters
- Adjust transition routes
- Configure webhook calls
- Test in simulator
```

#### 3. Adding Intents
```
Console → Manage → Intents → Create
- Add training phrases (10-15 minimum)
- Configure parameters and entities
- Test intent matching in simulator
```

#### 4. Configuring Tools
```
Console → Manage → Tools → Select Tool → Edit
- Bind to Data Store
- Configure fallback prompts
- Test tool directly
```

### Exporting Changes to Git

After making changes in the console, export for version control:

```bash
# 1. Export from Dialogflow CX Console
# Console → Agent Settings → Export and Import → Export Agent as Files
# Download: civicai-website-assistant-export.zip

# 2. Extract and replace src/ directory
unzip civicai-website-assistant-export.zip -d temp_export/
rm -rf src/
mv temp_export/src/ ./
rm -rf temp_export/

# 3. Commit changes
git add src/
git commit -m "feat: update Product_Info_Q&A playbook with new examples"
git push
```

### Importing Changes from Git

After pulling changes from Git, import to your Dialogflow CX environment:

```bash
# 1. Pull latest changes
git pull origin main

# 2. Create import package
zip -r agent_import.zip src/

# 3. Import to Dialogflow CX
# Console → Agent Settings → Export and Import → Restore
# Upload: agent_import.zip
```

### Development Best Practices

1. **Always Add Examples**: Every playbook needs 5-8 examples minimum (critical for LLM behavior)
2. **Tool-First Policy**: Mandate KB tool usage in all Q&A playbooks to prevent hallucination
3. **Test After Every Change**: Use simulator to validate changes before export
4. **Version Control Everything**: Export and commit after significant changes
5. **Document Assumptions**: Update CLAUDE.md and docs/ when architecture changes

---

## Testing & Validation

### Pre-Deployment Checklist

- [ ] **Tool Configuration**: Verify `marketing_knowledge_base` tool exists and is bound to Data Store
- [ ] **Playbook Examples**: Confirm all playbooks have 5+ examples
- [ ] **Flow Integrity**: Test all pages in Marketing Site Flow
- [ ] **Intent Matching**: Verify all 7 core intents match correctly
- [ ] **Webhook Configuration**: Confirm `lead_export_webhook` is configured (or dummy for testing)
- [ ] **Entity Types**: Verify `campaign_status` and `visitor_role` entities exist

### Simulator Test Scenarios

| Test Case | Input | Expected Behavior | Validation |
|-----------|-------|-------------------|------------|
| **Product Question** | "what is civicai" | Initial Triage → Product_Info_Q&A → KB tool call → Answer + CTA | ✓ Tool invoked<br>✓ Answer grounded in KB<br>✓ CTA present |
| **Pricing Question** | "how much does it cost" | Initial Triage → Pricing_&_Packaging → KB tool call → Pricing posture + Demo offer | ✓ Tool invoked<br>✓ Demo CTA present |
| **Security Question** | "are you SOC2 compliant" | Initial Triage → Security_&_Compliance → KB tool call → Answer + CTA | ✓ Tool invoked<br>✓ No fabricated claims |
| **Integration Question** | "does it work with Salesforce" | Initial Triage → Integrations_&_Deployment → KB tool call → Answer + CTA | ✓ Tool invoked<br>✓ Integration info accurate |
| **Direct Demo Request** | "book a demo" | Initial Triage → Marketing Site Flow → DemoCapture Page → Form collection | ✓ Flow transition<br>✓ Form fields appear |
| **Demo Form Completion** | Complete all fields | Webhook fires → Confirmation message | ✓ Webhook called<br>✓ Confirmation shown |
| **Objection** | "why not just use ChatGPT" | Initial Triage → Objection_Handling → Answer + CTA | ✓ Competitive objection handled<br>✓ No negative competitor claims |
| **KB Miss** | "what's your GDPR policy" | Playbook → KB tool returns no results → "I don't have that detail" + Demo/Email offer | ✓ Graceful fallback<br>✓ Next step offered |

### Debugging Tips

#### Issue: "LLM requested non-existent action"
**Cause**: Playbook missing examples demonstrating tool usage
**Fix**: Add 5+ examples to playbook showing `toolUse` action
**Reference**: AGENT_DIAGNOSIS_AND_FIXES.md:1-100

#### Issue: Generic "Sorry something went wrong" responses
**Cause**: Playbook has zero or invalid examples
**Fix**: Add comprehensive examples covering all conversation patterns
**Reference**: AGENT_DIAGNOSIS_AND_FIXES.md:101-200

#### Issue: Page not generating responses
**Cause**: `enableGenerativeFallback: false` and no static messages
**Fix**: Set `enableGenerativeFallback: true` for playbook-driven responses
**Reference**: AGENT_DIAGNOSIS_AND_FIXES.md:201-300

#### Issue: Tool not being invoked
**Cause**: Tool referenced but no examples demonstrate usage
**Fix**: Add examples showing `toolUse` → `marketing_knowledge_base` pattern
**Reference**: AGENT_DIAGNOSIS_AND_FIXES.md:301-400

---

## Deployment

### Production Deployment Checklist

1. **Data Store Verification**
   - [ ] Marketing content indexed in Data Store
   - [ ] Public website (getcivicai.com) crawled successfully
   - [ ] Test queries return relevant results

2. **Webhook Implementation**
   - [ ] `lead_export_webhook` deployed to Google Cloud Functions
   - [ ] Webhook URL configured in Dialogflow CX
   - [ ] Webhook authentication configured (JWT verification)
   - [ ] Test lead capture end-to-end

3. **Environment Configuration**
   - [ ] Create Production environment in Dialogflow CX
   - [ ] Configure environment-specific webhook URLs
   - [ ] Enable logging and monitoring
   - [ ] Set up alerting for errors

4. **Website Integration**
   - [ ] Add Dialogflow Messenger script to getcivicai.com
   - [ ] Configure chat bubble appearance
   - [ ] Test on staging environment
   - [ ] Deploy to production

### Website Integration Code

```html
<!-- Add to getcivicai.com <head> -->
<script src="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/df-messenger.js"></script>

<!-- Add to <body> where you want chat widget -->
<df-messenger
  project-id="civicai-472317"
  agent-id="YOUR_AGENT_ID"
  language-code="en"
  max-query-length="-1">
  <df-messenger-chat-bubble
   chat-title="CivicAI Assistant">
  </df-messenger-chat-bubble>
</df-messenger>

<!-- Optional: Customize styling -->
<style>
  df-messenger {
    --df-messenger-bot-message: #f0f0f0;
    --df-messenger-button-titlebar-color: #0066cc;
    --df-messenger-chat-background-color: #ffffff;
  }
</style>
```

### Monitoring & Analytics

**Key Metrics to Track**:
- Engagement rate (% of visitors who interact)
- Demo conversion rate (conversations → demo bookings)
- Email capture rate (conversations → email signups)
- Intent matching accuracy
- Tool invocation success rate
- Average conversation length
- Fallback frequency (indicates KB coverage gaps)

**Logging Configuration**:
```
Console → Agent Settings → Advanced Settings → Logging
✓ Enable Stackdriver Logging
✓ Enable Interaction Logging
✓ Enable Webhook Logging
```

**BigQuery Export** (optional):
```
Console → Agent Settings → Advanced Settings
→ Enable BigQuery Export
→ Select BigQuery Dataset
```

---

## Documentation

### Primary Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| **README.md** | Project overview and getting started | All developers |
| **CLAUDE.md** | Development guidelines for AI assistants | Claude Code / AI agents |
| **MARKETING-ASSISTANT-MVP-PLAN.md** | MVP implementation plan and architecture | Developers, Product |
| **docs/minimum-mvp.md** | MVP specification and requirements | Developers, Product |
| **AGENT_DIAGNOSIS_AND_FIXES.md** | Recent bug fixes and troubleshooting | Developers |
| **REFACTORING_CHANGELOG.md** | Playbook refactoring history | Developers |
| **docs/dialogflow_cx_documentation.md** | Dialogflow CX technical reference | Developers |
| **docs/one-pager_v1.md** | Product positioning and messaging | Product, Marketing |

### MCP Server (Dialogflow Docs)

The project includes an MCP server for accessing Dialogflow CX documentation:

```python
# Available in Claude Code environment
from mcp_server import search_dialogflow_docs

# Search for webhook documentation
results = search_dialogflow_docs(
    query="How do I create a webhook in Dialogflow CX?",
    n_results=5
)
```

**Use cases**:
- Webhook request/response format questions
- Flow and page configuration guidance
- Intent parameter handling
- Session state management
- Integration best practices

---

## Contributing

### Development Guidelines

1. **Message Discipline**: All responses must come from approved knowledge base content
2. **Compliance**: Maintain B2B SaaS tone and positioning
3. **Testing**: Test all changes in simulator before exporting
4. **Documentation**: Update relevant docs when architecture changes
5. **Version Control**: Export and commit after significant changes

### Pull Request Process

```bash
# 1. Create feature branch
git checkout -b feature/improve-pricing-playbook

# 2. Make changes in Dialogflow CX Console
# (Edit playbooks, flows, intents, etc.)

# 3. Export agent from Console
# Download as Files → Extract to src/

# 4. Review changes
git diff src/

# 5. Commit with descriptive message
git add src/
git commit -m "feat(pricing): add 5 new examples to Pricing_&_Packaging playbook"

# 6. Push and create PR
git push origin feature/improve-pricing-playbook
# Create PR on GitHub with testing notes
```

### Testing Requirements

All PRs must include:
- [ ] Simulator test results for affected conversation paths
- [ ] Verification that all examples are valid JSON
- [ ] Confirmation that KB tool invocations work correctly
- [ ] Screenshots of successful test conversations

### Code Review Focus Areas

Reviewers should verify:
- **Playbook Examples**: All modified playbooks have 5+ examples
- **Tool Usage**: KB tool invoked correctly in examples
- **Response Style**: Answers are 2-4 sentences, professional B2B tone
- **Conversion CTAs**: Every response includes clear next step (demo or email)
- **No Hallucinations**: No fabricated features, pricing, or capabilities
- **Routing Logic**: Playbook references and flow transitions are correct

---

## Troubleshooting

### Common Issues

#### "Retrieved examples: [id_not_set(display_name_not_set)]"
**Solution**: Playbook missing examples. Add 5+ examples to playbook JSON.
**Reference**: AGENT_DIAGNOSIS_AND_FIXES.md:1-50

#### "Error! LLM requested non-existent action 'marketing_knowledge_base'"
**Solution**: Add examples demonstrating tool usage pattern.
**Reference**: AGENT_DIAGNOSIS_AND_FIXES.md:51-100

#### Page generates no response
**Solution**: Enable `enableGenerativeFallback: true` on page entry fulfillment.
**Reference**: AGENT_DIAGNOSIS_AND_FIXES.md:180-210

#### Knowledge base returns irrelevant answers
**Solution**: Review and refine civicai-website.md content, check Data Store indexing.

#### Webhook timeout or failure
**Solution**: Verify webhook URL is accessible, check authentication, review Cloud Functions logs.

### Getting Help

1. **Dialogflow CX Documentation**: https://cloud.google.com/dialogflow/cx/docs
2. **MCP Server**: Use `mcp__dialogflow-docs__search_dialogflow_docs` for technical questions
3. **Project Documentation**: Review docs/ directory for architecture guidance
4. **Issue Tracking**: Create GitHub issues for bugs or feature requests

---

## Project Status

### Current Status: Production-Ready MVP ✅

- ✅ **6 playbooks** wired into clean routing graph (0 orphans)
- ✅ **30 examples** added (exceeding 4-per-playbook requirement)
- ✅ **Tool-first policy** enforced across all Q&A playbooks
- ✅ **ROUTINE start** (Initial Triage) replaces task-like default
- ✅ **Validated** via automated checks and manual review

### Recently Completed

- **2025-10-14**: Playbook architecture refactoring (task-based → ROUTINE-based)
- **2025-10-14**: Bug fixes for missing examples and tool invocation failures
- **2025-10-13**: Initial agent creation and configuration
- **2025-10-13**: Knowledge base setup and Data Store integration

### Known Limitations

1. **Webhook Implementation**: `lead_export_webhook` is configured but not deployed (needs Cloud Function)
2. **CRM Integration**: No direct CRM sync (leads captured to webhook only)
3. **Calendar Integration**: No real-time calendar scheduling (manual follow-up)
4. **Analytics Dashboard**: Basic logging only (no custom dashboard)
5. **Multi-Language**: English only (no i18n)

### Roadmap (Phase 2+)

- [ ] Full BANT scoring implementation
- [ ] CRM integration (Salesforce, HubSpot)
- [ ] Calendar integration for demo scheduling
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Sentiment analysis
- [ ] A/B testing framework
- [ ] Proactive engagement triggers
- [ ] Custom event tracking

---

## License & Usage

This CivicAI Marketing Website Assistant is designed for B2B SaaS lead generation on the CivicAI product marketing website. Ensure all usage complies with Google Cloud Terms of Service and applicable data protection regulations.

---

## Support & Contact

- **Technical Issues**: Dialogflow CX documentation and Google Cloud support
- **Feature Requests**: Create GitHub issues
- **Integration Support**: Contact CivicAI technical team
- **Knowledge Base Updates**: Update civicai-website.md and re-index Data Store

---

**Built with Dialogflow CX for intelligent B2B lead qualification and conversion**

*Last Updated: 2025-10-15*

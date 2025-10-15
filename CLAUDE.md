# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **CivicAI Marketing Website Assistant** - a Dialogflow CX conversational agent for the CivicAI marketing website (getcivicai.com). This agent qualifies B2B leads, answers product questions, and converts website visitors into demo bookings and email captures.

**Purpose**: Transform marketing website visitors into qualified sales leads through intelligent conversation, product education, and frictionless conversion paths.

**Architecture**: Dialogflow CX agent combining flow-based conversation management with webhook-powered dynamic responses and knowledge base integration.

**Key Distinction**: This is NOT the campaign conversion agent. This is a B2B SaaS lead qualification assistant for the CivicAI product marketing website.

## Project Structure

```
civicai-website-assistant/
├── docs/                              # Project documentation
│   ├── README.md                      # Comprehensive project overview
│   ├── minimum-mvp.md                 # **PRIMARY SPEC** - MVP requirements
│   ├── one-pager_v1.md               # Product positioning and messaging
│   ├── civicai_agent.md              # Campaign agent reference (different project)
│   └── dialogflow_cx_documentation.md # Dialogflow CX technical guide
├── src/                               # **WEBHOOK SERVICE CODE** (to be developed)
│   ├── webhooks/                      # Dialogflow CX webhook handlers
│   ├── knowledge_base/                # KB query and retrieval logic
│   ├── lead_capture/                  # Lead management and routing
│   └── utils/                         # Shared utilities
├── dialogflow_chroma_db/              # ChromaDB vector store (gitignored)
├── civicai-website.md                 # **KNOWLEDGE BASE SOURCE** - marketing content
├── document_processor.py              # KB document ingestion utilities
├── mcp_server.py                      # Model Context Protocol server
└── .venv/                             # Python virtual environment
```

## Development Process

### This is Greenfield Development
Unlike the campaign agent (which is a Dialogflow export), this project involves **building a new agent from scratch**:

1. **Agent Creation**: Create new Dialogflow CX agent in Google Cloud Console
2. **Intent Design**: Define intents and training phrases for lead qualification
3. **Flow Architecture**: Build conversation flows for product Q&A and conversions
4. **Webhook Development**: Write Python webhook service in `src/` directory
5. **Knowledge Base Setup**: Process marketing content into searchable KB
6. **Integration**: Deploy webhooks and integrate with getcivicai.com
7. **Testing**: Use Dialogflow CX simulator for end-to-end validation

### No Traditional Build Commands
Development workflow is hybrid:
- **Agent Configuration**: Managed in Dialogflow CX Console (visual editor)
- **Webhook Code**: Traditional Python development in `src/` with standard tooling
- **Testing**: Dialogflow CX simulator + local webhook testing
- **Deployment**: Google Cloud Functions for webhooks, Dialogflow CX for agent

## MVP Scope (docs/minimum-mvp.md)

### Core Intents (MVP v1)
1. **Greeting / Entry**: Welcome visitors and offer quick choices
2. **Product Info (KB-backed Q&A)**: Answer questions from knowledge base
3. **Pricing (lite)**: High-level pricing info, drive to demo/email
4. **Demo Request**: Collect name, email, organization → primary conversion
5. **Security/Integration (lite)**: Reassurance from approved content
6. **Human Handoff**: Escalation path for complex questions
7. **Fallback**: Graceful handling of unmatched input

### Conversion Paths
- **Primary**: Demo booking (hot leads)
- **Secondary**: Email capture (warm/cold leads for nurture)

### Critical Constraints
- **Knowledge Base Only**: NEVER fabricate answers not in civicai-website.md
- **Concise Responses**: 2-4 sentences maximum per MVP spec
- **Always Offer Next Step**: Demo or email capture on every interaction
- **No Complex Qualification**: Simple lead tier (hot/warm/cold) based on behavior

## Key Technical Components

### 1. Dialogflow CX Agent Configuration
Created in Google Cloud Console, not in this codebase. Configuration includes:
- **Flows**: Main conversation flow with pages for each intent
- **Intents**: 7 core intents with training phrases
- **Parameters**: Session state for lead qualification
- **Webhooks**: References to Cloud Function endpoints

### 2. Webhook Service (src/)
Python-based service handling:
- **kb_search**: Query knowledge base and return approved answers
- **lead_export**: Capture and route demo requests and email signups
- **validation**: Email format, required fields, data quality
- **integration**: CRM/email service connectivity (future)

Expected structure:
```python
# src/webhooks/handler.py
def handle_webhook_request(request):
    """Main Dialogflow CX webhook handler"""
    tag = request['fulfillmentInfo']['tag']

    if tag == 'kb_search':
        return search_knowledge_base(request)
    elif tag == 'lead_export':
        return capture_lead(request)
    elif tag == 'validate_email':
        return validate_email(request)
```

### 3. Knowledge Base Integration
Content source: `civicai-website.md` (marketing website copy)
- Process with `document_processor.py` into ChromaDB
- Query via webhook for product questions
- Return only approved marketing content
- Include source attribution for transparency

### 4. Lead Qualification Logic
Simple tier-based qualification:
```python
def calculate_lead_tier(session_params):
    if explicit_demo_request:
        return "hot"
    elif campaign_status == "active" and visitor_role == "decision_maker":
        return "hot"
    elif campaign_status in ["active", "planning"]:
        return "warm"
    else:
        return "cold"
```

## Session Parameters

Track lead qualification state throughout conversation:
```python
{
    "campaign_status": "active | planning | research",
    "visitor_role": "decision_maker | recommender | researcher",
    "primary_need_freeform": "Free text description",
    "visitor_name": "Required for demo",
    "visitor_email": "Required for conversions",
    "organization_name": "Required for demo",
    "lead_tier": "hot | warm | cold"  # Derived
}
```

## Critical Development Guidelines

### Message Discipline (Non-Negotiable)
1. **Knowledge Base Authority**: ALL product information must come from civicai-website.md
2. **No Fabrication**: If KB doesn't have an answer, say so explicitly: "I don't have that specific information. I can connect you with our team..."
3. **Approved Language Only**: Use exact phrasing from marketing content when possible
4. **Consistent Tone**: Professional B2B SaaS (benefit-focused, concise, action-oriented)

### Response Standards
- **Length**: 2-4 sentences (per MVP spec)
- **Format**: Conversational but professional
- **Next Step**: Always include clear CTA (demo or email)
- **No Promises**: Never commit to features, timelines, or specifics not in KB

### Performance Requirements
- **Webhook Response Time**: < 2 seconds (maintains conversation flow)
- **KB Search Latency**: < 1 second (enables real-time responses)
- **Availability**: 99.9% uptime for production webhooks
- **Error Handling**: Graceful degradation, never break conversation

### Testing Requirements
1. **Intent Coverage**: Test all 7 core intents with variations
2. **KB Accuracy**: Verify answers match source content
3. **Lead Capture**: End-to-end demo and email flows
4. **Edge Cases**: Missing data, invalid emails, KB misses
5. **Load Testing**: Webhook performance under realistic traffic

## Development Workflow

### Phase 1: Agent Foundation (Week 1)
1. Create Dialogflow CX agent in Google Cloud Console
2. Define 7 core intents with training phrases
3. Build main flow with conversation pages
4. Configure session parameters

### Phase 2: Webhook Development (Week 1-2)
1. Set up Python development environment (`src/`)
2. Implement `kb_search` webhook with ChromaDB integration
3. Implement `lead_export` webhook with validation
4. Local testing with Dialogflow webhook testing tools
5. Deploy to Google Cloud Functions

### Phase 3: Knowledge Base Setup (Week 1)
1. Process civicai-website.md with document_processor.py
2. Create ChromaDB embeddings for semantic search
3. Test retrieval accuracy and relevance
4. Tune chunking and retrieval parameters

### Phase 4: Integration & Testing (Week 2)
1. Connect webhooks to Dialogflow CX agent
2. End-to-end testing in Dialogflow simulator
3. Lead capture validation (demo + email flows)
4. Performance testing and optimization
5. Prepare for production deployment

### Phase 5: Production Deployment (Week 3)
1. Deploy webhooks to production Cloud Functions
2. Configure production Dialogflow CX environment
3. Integrate Dialogflow Messenger on getcivicai.com
4. Monitor performance and lead capture metrics
5. Iterate based on real user conversations

## Available Development Tools

### MCP Server: dialogflow-docs
The project includes an MCP server that provides access to Dialogflow CX documentation via ChromaDB:

```python
# Available in Claude Code environment
mcp__dialogflow-docs__search_dialogflow_docs(
    query="How do I create a webhook in Dialogflow CX?",
    n_results=5
)
```

**When to use**: During webhook development, flow configuration, or troubleshooting Dialogflow CX-specific issues. This provides contextual documentation without manual searching.

**Key use cases**:
- Webhook request/response format questions
- Flow and page configuration guidance
- Intent parameter handling
- Session state management
- Integration best practices

## Common Development Tasks

### Adding a New Intent
1. Open Dialogflow CX Console → Manage → Intents
2. Click Create, add training phrases (10+ variations)
3. Add parameters if needed (entity types)
4. Save and test in simulator

### Creating a New Webhook
```python
# src/webhooks/new_handler.py
def handle_new_webhook(request):
    """Handle specific webhook tag"""
    session_params = request.get('sessionInfo', {}).get('parameters', {})

    # Your logic here

    return {
        'fulfillment_response': {
            'messages': [{
                'text': {
                    'text': ['Response text here']
                }
            }]
        },
        'session_info': {
            'parameters': session_params  # Updated state
        }
    }
```

### Querying the Knowledge Base
```python
# src/knowledge_base/query.py
from chromadb import Client

def search_kb(query: str, n_results: int = 3):
    """Search marketing content KB"""
    client = Client()
    collection = client.get_collection("civicai_marketing")

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return format_kb_response(results)
```

### Testing in Dialogflow Simulator
1. Dialogflow CX Console → Test Agent (right panel)
2. Enter user utterances to test intent matching
3. Verify webhook calls and responses
4. Check session parameter updates
5. Test full conversation flows

## Deployment

### Webhook Deployment (Google Cloud Functions)
```bash
# From src/ directory
gcloud functions deploy civicai-webhooks \
  --runtime python311 \
  --trigger-http \
  --entry-point handle_webhook_request \
  --region us-central1 \
  --allow-unauthenticated  # For Dialogflow CX
```

### Agent Configuration
1. Dialogflow CX Console → Manage → Webhooks
2. Add webhook pointing to Cloud Function URL
3. Configure webhook calls in flows (fulfillment)
4. Test in simulator before production

### Website Integration
```html
<!-- Add to getcivicai.com <head> -->
<script src="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/df-messenger.js"></script>

<!-- Add to <body> -->
<df-messenger
  project-id="YOUR_PROJECT_ID"
  agent-id="YOUR_AGENT_ID"
  language-code="en"
  max-query-length="-1">
  <df-messenger-chat-bubble
   chat-title="CivicAI Assistant">
  </df-messenger-chat-bubble>
</df-messenger>
```

## Security & Compliance

### Data Protection
- **PII Handling**: Collect only necessary data (name, email, org)
- **Storage**: Secure storage of lead data with encryption
- **Retention**: Define data retention policies
- **Access Control**: Limit access to production data

### Authentication
- **Webhook Security**: Validate Dialogflow CX requests (JWT verification)
- **API Keys**: Store in Google Secret Manager, never in code
- **Service Accounts**: Use least-privilege IAM roles

### Compliance Considerations
- **TCPA/CAN-SPAM**: Obtain consent for email communications
- **Privacy Policy**: Link to privacy policy during data collection
- **Data Subject Rights**: Implement data export/deletion capabilities

## Monitoring & Analytics

### Key Metrics to Track
- **Engagement Rate**: % of visitors who interact with assistant
- **Demo Conversion Rate**: % of conversations → demo bookings
- **Email Capture Rate**: % of conversations → email signups
- **Intent Accuracy**: Intent matching success rate
- **Webhook Performance**: Response times and error rates
- **KB Coverage**: % of questions answered from KB vs. escalated

### Logging Requirements
- **Conversation Logs**: Full transcripts for quality review
- **Lead Events**: All demo and email captures with timestamps
- **Webhook Calls**: Request/response logs for debugging
- **Error Tracking**: Detailed error context for troubleshooting

## Troubleshooting Guide

### Intent Not Matching
- Add more training phrase variations
- Check for conflicting intents
- Review entity annotations
- Test with different phrasings

### Webhook Timeout
- Optimize KB query performance
- Add caching for common queries
- Reduce external API calls
- Implement async processing

### KB Returns Wrong Answer
- Improve document chunking strategy
- Tune embedding model parameters
- Add explicit source attribution
- Expand training data

### Lead Not Captured
- Check webhook response format
- Verify parameter extraction
- Review session state updates
- Test email validation logic

## Future Enhancements (Post-MVP)

### Phase 2+ Features (Deferred)
- Full BANT qualification scoring
- Calendar integration for demo scheduling
- CRM integration (Salesforce, HubSpot)
- Advanced analytics dashboard
- Multi-language support
- Sentiment analysis
- A/B testing framework
- Custom event tracking
- Proactive engagement triggers

## References

- **Primary Spec**: docs/minimum-mvp.md (defines scope and requirements)
- **Knowledge Base Source**: civicai-website.md (all approved product content)
- **Dialogflow Guide**: docs/dialogflow_cx_documentation.md (technical reference)
- **Product Positioning**: docs/one-pager_v1.md (messaging and value props)
- **MCP Dialogflow Docs**: Use `mcp__dialogflow-docs__search_dialogflow_docs` for technical guidance

## Getting Help

When working on this codebase with Claude Code:
1. **Use MCP Server**: Query dialogflow-docs for Dialogflow CX technical questions
2. **Reference MVP Spec**: docs/minimum-mvp.md is the source of truth for requirements
3. **Check KB Source**: civicai-website.md for all product information
4. **Review Examples**: docs/dialogflow_cx_documentation.md has code examples

This is a lead qualification assistant that transforms marketing website visitors into sales opportunities through intelligent conversation, accurate product education, and frictionless conversion experiences.

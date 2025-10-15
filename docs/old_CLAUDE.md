# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **CivicAI** - a sophisticated political campaign conversational AI system exported from Google Dialogflow CX. This is NOT traditional source code with build scripts or package managers. Instead, it's a collection of JSON configuration files that define conversation flows, intents, playbooks, and external tool integrations for a hybrid AI agent.

**Purpose**: Transform website visitors into campaign assets (donors, volunteers, supporters) through intelligent conversation routing and conversion optimization.

**Architecture**: Hybrid system combining deterministic flows (state machines) with generative playbooks (LLM-powered conversations) and external tool integrations.

## Critical Architecture Issue

The exported agent has **sophisticated campaign intelligence capabilities trapped behind a generic small talk interface**. Seven well-designed campaign playbooks exist but are disconnected from the entry point routing system.

## Development Process (No Traditional Commands)

**⚠️ Important**: There are no build, test, or lint commands. Development involves:

1. **Import Process**: Import the exported agent into Google Dialogflow CX console
2. **Visual Editor**: Use Dialogflow CX interface to modify conversation flows
3. **Intent Management**: Replace small talk intents with campaign-specific patterns
4. **Playbook Integration**: Connect flows to playbooks via transition routes
5. **Tool Configuration**: Set up authentication for external APIs
6. **Testing**: Use Dialogflow CX simulator for conversation testing

## Key File Structure

### Core Configuration
- `agent.json`: Main agent configuration, project settings, default language
- `.claude/settings.local.json`: Claude-specific settings

### Conversation Components
- `flows/Default Start Flow/`: **PRIMARY ISSUE** - Currently routes to small talk instead of campaign triage
- `playbooks/`: **CAMPAIGN INTELLIGENCE** - 7 specialized conversation handlers:
  - `Initial Triage/`: Primary routing system (well-designed, needs connection)
  - `Conversational_Fundraising/`: Donor engagement and contribution processing
  - `Volunteer_Funnel/`: Comprehensive volunteer recruitment pipeline
  - `Opposition_Challenge_Deescalation/`: "Defensible AI" for hostile interactions
  - `Media_Rapid_Response/`: Press inquiry handling with approved messaging
  - `Voter_Persuasion_Dialogue/`: Multi-step conversations for undecided voters
  - `Voter_Assistance/`: Election logistics with state API integration

### Intent Recognition
- `intents/`: **NEEDS REPLACEMENT** - Currently 100+ small talk intents
- Required campaign intents: `donation_intent`, `volunteer_intent`, `policy_inquiry_intent`, `opposition_challenge_intent`, `media_inquiry_intent`, `voter_assistance_intent`

### External Integrations
- `tools/marketing_knowledge_base/`: Policy Q&A system (configured but never invoked)

## Session Parameter Schema

The system uses session parameters for state management across components:

```javascript
{
  "user_intent": "Primary goal (Donation, Volunteer, Policy, etc.)",
  "initial_topic_of_interest": "Specific subject mentioned",
  "user_zip_code": "Location for local targeting",
  "user_engagement_level": "Prospect classification (High, Medium, FirstTimeProspect)",
  "user_full_utterance": "Complete initial message",
  "conversion_events": "Array of successful outcomes",
  "campaign_touchpoints": "Interaction history",
  "conversion_value": "Numeric campaign value"
}
```

## Core Transformation Requirements

To unlock the campaign intelligence layer, the system needs:

1. **Fix Entry Point**: Replace Default Start Flow small talk routing with campaign triage
2. **Intent Overhaul**: Delete small talk intents, create campaign-specific patterns
3. **Connect Components**: Add transition routes from flows to specialized playbooks
4. **Tool Integration**: Connect marketing knowledge base to policy-related playbooks
5. **Parameter Flow**: Implement data capture and passing between components

## Example Flow Architecture Fix

Current broken flow:
```
User Input → Default Start Flow → Small Talk Agent → Dead End
```

Required campaign flow:
```
User Input → Default Start Flow → Initial Triage Playbook → Specialized Playbook (Fundraising/Volunteer/etc.) → Conversion Completion
```

## Security & Compliance

- **Authentication**: Service Agent ID Token for Google Cloud services
- **Secret Management**: All credentials in Google Secret Manager
- **FEC Compliance**: Donor identification and contribution tracking
- **PII Protection**: Consent-based data collection and redaction
- **Message Discipline**: All responses must use pre-approved campaign language

## Performance Requirements

- **Response Time**: P95 latency under 2 seconds for real-time engagement
- **Availability**: 99.9% uptime during active campaign periods
- **Scalability**: Handle 10x traffic spikes during viral events
- **Error Rate**: Maintain <1% failure rate across all components

## Working with This Codebase

When making changes:
1. **Always test in Dialogflow CX simulator** before deployment
2. **Preserve campaign message discipline** - never introduce generic chatbot language
3. **Maintain session parameter flow** between components
4. **Verify tool authentication** for external API calls
5. **Test conversion paths end-to-end** from visitor to campaign asset

This system represents a sophisticated campaign intelligence platform that requires proper architectural connection to realize its conversion optimization potential.
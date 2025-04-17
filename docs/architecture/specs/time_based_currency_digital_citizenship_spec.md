# Time-Based Currency & Digital Citizenship Specification

## Purpose
Reward contributors with “Hour Tokens” for time spent, not output; enable digital citizenship and participatory governance.

## Features
* Time ledger logs hours contributed (manual or session-based)
* Earn non-transferable “Hour Tokens” for time spent
* Tokens can be exchanged for recognition, privileges, or gifted
* Contributors with sustained engagement can propose/vote on features, moderate, or steward swarms
* Rights and responsibilities are transparent and opt-in
* Proposals and voting weighted by engagement and diversity, not just time

## API & Data Model
* `TimeLedger`, `HourToken`, `Proposal`, `Vote`, `CitizenProfile`
* `/ledger` (view, log hours)
* `/tokens` (view, gift, redeem)
* `/governance/proposals` (create, vote)

## UI/UX Notes
* Dashboard for tracking hours and tokens
* Governance portal for proposals and voting
* All participation is opt-in and privacy-respecting

## Security/Ethics
* No transfer of tokens for money
* All governance actions are transparent and auditable
* Participation is voluntary and revocable

## Example User Flow
1. Contributor logs hours via dashboard or session tracking
2. Earns Hour Tokens, visible in their profile
3. Uses tokens to propose a new feature or vote on an initiative

---
*End of Time-Based Currency & Digital Citizenship Spec*
# Founder Use Case

## Scenario

A seed-stage B2B SaaS founder just finished 15 sales calls in two weeks. The calls were useful, but the learning is scattered across HubSpot notes, Slack messages, call recorder summaries, and the founder's memory.

The founder wants to know:

- Which objections repeated?
- Which deals are real and urgent?
- Which prospects are poor fit?
- Where did the pitch create confusion?
- Which follow-ups need founder intervention?
- What should change in next week's narrative?

## Workflow

1. Export notes from CRM, spreadsheets, or call summaries.
2. Put the rows into `data/sample_sales_calls.csv` or a renamed CSV with the same columns.
3. Edit `config/company_profile.yml` so the keywords match the company.
4. Run `make run`.
5. Open the generated files inside `outputs/`.

## What the founder learns

The founder sees an objection bank showing themes such as price, security, integrations, unclear ROI, stakeholder alignment, and competitor comparison.

They also see a deal rescue queue. This queue is not a generic task list. It focuses on deals where founder intervention could change the outcome:

- Strong-fit prospects with strong pain but vague next steps
- Prospects with budget but unresolved objections
- Urgent deals where the pitch is confusing
- Stalled deals where a founder-to-founder message could unblock momentum

## Example decisions

After reviewing the output, the founder decides to:

- Send security proof to healthtech and legaltech prospects.
- Rewrite the deck to explain post-call intelligence instead of generic analytics.
- Stop over-investing in prospects that only want outbound research.
- Ask for a founder sponsor call on deals where RevOps or Ops leads were interested but not the buyer.
- Add sample weekly memo screenshots to the next sales call.

## Weekly impact

The system helps the founder leave the weekly GTM review with concrete actions:

- Rescue three active deals.
- Update one narrative angle.
- Add two proof points.
- Remove weak-fit prospects from the founder follow-up list.
- Test sharper discovery questions in the next five calls.

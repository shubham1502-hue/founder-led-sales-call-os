# Founder-Led Sales Call OS

Turn messy founder sales calls into objections, deal risks, follow-up priorities, and GTM narrative experiments.

Use this after sales calls. Drop in your messy call notes, edit one YAML file, run one command, and get a founder-ready weekly learning loop:

- Which objections repeated
- Which deals need founder intervention
- Where prospects got confused
- Which proof points are missing
- What narrative to test next week

The included sample run generates a call intelligence CSV, objection bank, deal rescue queue, weekly sales learning memo, and narrative experiments. It is built for founders who need decisions, not another dashboard.

The base workflow is deterministic and offline. No paid API is required.
All included sample data is synthetic and fictionalized.

## Output preview

The included sample run produces:

- `outputs/call_intelligence.csv`: structured sales call signals
- `outputs/objection_bank.csv`: repeated objection themes
- `outputs/deal_rescue_queue.csv`: deals needing founder or owner action
- `outputs/weekly_sales_learning_memo.md`: founder-ready GTM learning memo
- `outputs/narrative_experiments.md`: sales narrative tests for the next cycle

## 7-day Founder's Office sprint

- Day 1: Collect recent call notes and normalize the tracker
- Day 2: Run the call intelligence workflow
- Day 3: Review repeated objections and confusion patterns
- Day 4: Prioritize deal rescue actions with owners
- Day 5: Draft narrative experiments for the next sales week
- Day 6: Update CRM with follow-ups and risk notes
- Day 7: Feed sales learning into the weekly GTM operating review

## Founder's Office signal

This repo demonstrates:

- turning messy qualitative notes into operating signal
- objection and risk pattern recognition
- founder follow-up prioritization
- sales narrative iteration
- deal owner assignment
- weekly learning memo creation

## The founder problem

Founders are doing sales calls, but the learning from those calls stays trapped in messy notes, memory, CRM comments, Slack threads, WhatsApp context, and scattered follow-ups.

Founder-Led Sales Call OS turns those conversations into structured GTM intelligence:

- Which objections keep repeating?
- Which prospects actually match the ICP after the conversation?
- Where is urgency real versus fake?
- Which deals need founder intervention this week?
- Which buying triggers are emerging?
- What is confusing prospects?
- What should change in the sales narrative next week?

## What this repo does

- Finds repeated objections
- Scores ICP fit after calls
- Flags urgent deals
- Creates a deal rescue queue
- Identifies pitch confusion
- Finds narrative gaps
- Creates follow-up priorities
- Builds a founder-ready weekly sales learning memo
- Suggests GTM narrative experiments for the next week

## What a founder gets in 10 minutes

- A ranked list of deals needing attention
- Top objections blocking revenue
- ICP fit clarity
- Follow-up rescue actions
- Pitch confusion signals
- Narrative experiments
- A weekly sales learning memo

Example from the included demo:

- 15 messy synthetic sales calls reviewed
- 7 price objections detected
- 4 security objections detected
- 6 high-priority deal rescue actions generated
- Pitch confusion flagged where prospects compared the workflow to a CRM or analytics tool

## Before and after

Before:

- Messy call notes
- Unclear objections
- Founder memory-driven follow-up
- No structured GTM learning
- No clear narrative experiments

After:

- Structured call intelligence
- Objection bank
- ICP fit scoring
- Deal rescue queue
- Weekly sales learning memo
- GTM narrative experiments

## Who this is for

- Early-stage founders
- Founder's Office teams
- RevOps/BizOps operators
- B2B SaaS teams
- AI startup founders
- Founder-led services businesses

## Quick start

```bash
# 1. Fork this repo on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/founder-led-sales-call-os.git
cd founder-led-sales-call-os

# 3. Install dependencies
make install

# 4. Edit your company profile
$EDITOR config/company_profile.yml

# 5. Replace the sample sales call CSV
$EDITOR data/sample_sales_calls.csv

# 6. Run the system
make run

# 7. Review outputs
ls outputs
```

You can also run the demo sample:

```bash
make demo
```

Or run the CLI directly:

```bash
python -m founder_sales_os.cli run \
 --input data/sample_sales_calls.csv \
 --company-config config/company_profile.yml \
 --scoring-config config/scoring_rules.yml \
 --output-dir outputs
```

## How to fork and use this for your company

1. Click Fork.
2. Rename the repo if needed.
3. Replace `data/sample_sales_calls.csv` with your own call notes. Keep the column names the same.
4. Edit `config/company_profile.yml` for your product, ICP, competitors, objections, urgency signals, and proof points.
5. Optional: edit `config/scoring_rules.yml` if your scoring weights are different.
6. Run `make run`.
7. Open `outputs/weekly_sales_learning_memo.md` first.
8. Open `outputs/deal_rescue_queue.csv` second.
9. Optional: connect output CSVs to Google Sheets, Notion, Airtable, HubSpot, Pipedrive, Attio, or your CRM.

Keep private prospect and customer data out of public forks.

If you are non-technical, the practical path is:

- Replace one file: `data/sample_sales_calls.csv`
- Edit one file: `config/company_profile.yml`
- Run one command: `make run`
- Read one memo first: `outputs/weekly_sales_learning_memo.md`

## Standalone or integrated

Standalone:
Use this repo by itself if you only need to turn founder-led sales call notes into objections, deal risks, follow-up priorities, and weekly sales learning. Fork it, replace the sample input, run the workflow or copy the templates, and use the main output in your next founder review.

Integrated:
Use this repo with the Founder OS ecosystem if you want to connect it to adjacent operating workflows.

- Use after calls.
- Feed deal risk and objections into [founder-os-revenue-engine](https://github.com/shubham1502-hue/founder-os-revenue-engine).
- After close-won, move customer tracking into [founder-customer-onboarding-os](https://github.com/shubham1502-hue/founder-customer-onboarding-os).
- Feed sales learnings into [founder-weekly-operating-review-agent](https://github.com/shubham1502-hue/founder-weekly-operating-review-agent).

## Lifecycle handoff

Before:

- [ai-gtm-command-center](https://github.com/shubham1502-hue/ai-gtm-command-center) for account research and call prep.

This repo produces:

- Objection bank
- Deal rescue queue
- Weekly sales learning memo
- Narrative experiments

After:

- [founder-os-revenue-engine](https://github.com/shubham1502-hue/founder-os-revenue-engine) for revenue leakage diagnosis.
- [founder-customer-onboarding-os](https://github.com/shubham1502-hue/founder-customer-onboarding-os) after close-won.
- [founder-weekly-operating-review-agent](https://github.com/shubham1502-hue/founder-weekly-operating-review-agent) for weekly review.

## Where this fits in the Founder OS

- Use [ai-gtm-command-center](https://github.com/shubham1502-hue/ai-gtm-command-center) before calls to research accounts and prepare outreach.
- Use `founder-led-sales-call-os` after calls to extract learning and prioritize deal rescue.
- Use [founder-os-revenue-engine](https://github.com/shubham1502-hue/founder-os-revenue-engine) weekly to connect call-level insights to funnel leakage.
- After a deal closes, use [Founder Customer Onboarding OS](https://github.com/shubham1502-hue/founder-customer-onboarding-os) to track whether the customer reaches activation, whether handoffs are clear, and whether founder intervention is needed.
- Use [Founder Product Feedback Roadmap OS](https://github.com/shubham1502-hue/founder-product-feedback-roadmap-os) when repeated sales objections, product gaps, narrative confusion, or deal blockers should become roadmap decisions.
- Use [founder-ai-workflow-roi-os](https://github.com/shubham1502-hue/founder-ai-workflow-roi-os) when post-call workflows need an automate, pilot, hire, outsource, or keep-manual decision.
- Use [founder-weekly-operating-review-agent](https://github.com/shubham1502-hue/founder-weekly-operating-review-agent) to roll these learnings into the weekly operating review.
- Use [board-pack-investor-update-agent](https://github.com/shubham1502-hue/board-pack-investor-update-agent) to translate GTM learning into investor-safe narrative.
- Use [founder-os](https://github.com/shubham1502-hue/founder-os) as the umbrella operating system.

If post-call sales workflows become repetitive, use [Founder AI Workflow ROI OS](https://github.com/shubham1502-hue/founder-ai-workflow-roi-os) to decide whether call summaries, CRM updates, follow-up drafting, objection tagging, or reporting should be automated, piloted, hired for, outsourced, or kept manual.

## Product roadmap input

[Founder Product Feedback Roadmap OS](https://github.com/shubham1502-hue/founder-product-feedback-roadmap-os) can use repeated sales objections, product gaps, narrative confusion, and deal blockers from sales calls to decide what should be built, validated, solved outside product, deferred, or rejected.

## Portfolio fit

This repo is one module in a broader founder-facing operating system:

- `ai-gtm-command-center` helps before the sales call.
- `founder-led-sales-call-os` helps after the sales call.
- `founder-os-revenue-engine` helps diagnose funnel leakage.
- `founder-customer-onboarding-os` helps after close-won with onboarding health, activation risk, and founder intervention priorities.
- `founder-product-feedback-roadmap-os` helps turn repeated customer and sales signals into roadmap decisions.
- `founder-weekly-operating-review-agent` helps run the weekly operating review.
- `board-pack-investor-update-agent` helps convert operating metrics into investor narrative.

This repo is not an outbound system, account research tool, cold email generator, or generic ICP scorer. The core object is the sales conversation.

## Input format

The input CSV must include every column below:

| Column | Description |
| --- | --- |
| `call_id` | Unique call identifier |
| `call_date` | Call date in `YYYY-MM-DD` format |
| `company_name` | Prospect company name |
| `contact_role` | Main contact role, such as Founder, CEO, RevOps Lead, or VP Sales |
| `company_stage` | Prospect company stage |
| `employee_count` | Approximate employee count |
| `industry` | Prospect industry |
| `lead_source` | How the prospect entered the pipeline |
| `call_notes` | Messy call notes, demo notes, CRM notes, or transcript summary |
| `current_tooling` | CRM, call recorder, spreadsheet, notes, or workflow tools currently used |
| `stated_pain` | Pain the prospect stated in their own words |
| `budget_signal` | Budget language from the call |
| `timeline_signal` | Timing and urgency language from the call |
| `next_step` | Current next step, even if vague |
| `deal_stage` | Current deal stage |

## Output files

- `outputs/call_intelligence.csv`: Per-call extraction with objections, triggers, competitors, urgency, budget, pain category, confusion, risk flags, next action, and ICP fit.
- `outputs/objection_bank.csv`: Aggregated objections with response angles, narrative implications, and proof points.
- `outputs/deal_rescue_queue.csv`: Ranked founder intervention queue for deals where action could change the outcome.
- `outputs/weekly_sales_learning_memo.md`: Founder-ready weekly GTM review memo.
- `outputs/narrative_experiments.md`: Messaging and discovery experiments based on what prospects did not understand or resisted.

## Example founder workflow

1. Export call notes every Friday.
2. Run `make run`.
3. Review `outputs/weekly_sales_learning_memo.md`.
4. Review `outputs/deal_rescue_queue.csv`.
5. Update the sales narrative.
6. Prioritize founder follow-ups.
7. Feed learnings back into CRM notes.
8. Test new messaging next week.

## Customization guide

Edit `config/company_profile.yml` to customize:

- ICP signals
- Competitor keywords
- Objection keywords
- Urgency keywords
- Confusion keywords
- Narrative gap keywords
- Proof point keywords

Edit `config/scoring_rules.yml` to customize:

- ICP fit scoring weights
- Pain intensity keywords
- Budget signal keywords
- Follow-up clarity rules
- Pitch clarity penalties
- Implementation risk keywords
- Deal rescue priority weights

Edit `src/founder_sales_os/deal_rescue.py` if you want different follow-up templates or founder action logic.

Edit `src/founder_sales_os/narrative.py` if you want different narrative experiment logic.

## Why this matters

This is not a dashboard. It is a post-call intelligence system for founders who need to turn sales conversations into decisions.

The value is not the score. The value is the weekly learning loop:

- What did prospects actually say?
- Which objections repeated?
- Which deals are slipping?
- Which proof points are missing?
- What should the founder test next week?

## Roadmap

- CRM import support
- Google Sheets export
- Streamlit dashboard
- LLM-powered call note summarization
- Slack and email follow-up alerts
- HubSpot integration
- Pipedrive integration
- Attio integration
- Gong/Fireflies/Fathom transcript import
- Notion operating review export

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License. See [LICENSE](LICENSE).

## Built by

Built by Shubham Singh, a founder-facing operator focused on RevOps, GTM systems, startup metrics, and AI workflows for early-stage teams.

## Use this in your company

Fork it, replace the sample inputs with your company context, and run the workflow. Start with the main output listed in the Quick Start section. Keep private data out of public forks.

## If you are a Founder's Office candidate

Use this repo to understand how a founder-facing operator turns messy inputs into decisions, cadence, and execution artifacts. Fork it, adapt it to a real company example, and write a short case note explaining what changed.

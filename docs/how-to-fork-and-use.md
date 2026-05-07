# How to Fork and Use

This guide is written for non-technical founders.

## 1. Fork the repo

Open the GitHub repo and click **Fork**. This creates your own copy.

You can rename the repo if you want it to match your company.

## 2. Clone your fork

```bash
git clone https://github.com/YOUR-USERNAME/founder-led-sales-call-os.git
cd founder-led-sales-call-os
```

## 3. Install the project

```bash
make install
```

This installs Python dependencies for local use.

## 4. Replace the sample data

Open `data/sample_sales_calls.csv`.

Replace the synthetic rows with your own sales call notes. Keep the same column names.

You can export notes from:

- HubSpot
- Salesforce
- Pipedrive
- Attio
- Google Sheets
- Notion
- Airtable
- Call summary tools

Do not commit private customer notes to a public repo.

## 5. Edit your company profile

Open `config/company_profile.yml`.

Update:

- Product name
- Target customer
- Target industries
- Target company stages
- Strong fit signals
- Weak fit signals
- Disqualifiers
- Competitor keywords
- Objection keywords
- Urgency keywords
- Confusion keywords
- Narrative gap keywords

YAML is indentation-sensitive. Keep the same format and edit the words inside quotes or list items.

## 6. Edit scoring rules if needed

Open `config/scoring_rules.yml`.

Most founders can leave this unchanged for the first run.

Edit it only if your company has different scoring logic for:

- ICP fit
- Pain intensity
- Budget
- Urgency
- Follow-up clarity
- Deal rescue priority

## 7. Run the system

```bash
make run
```

## 8. Interpret outputs

Open `outputs/call_intelligence.csv` first. This shows the extracted learning from each call.

Then open `outputs/deal_rescue_queue.csv`. This tells you which deals deserve founder attention.

Then open `outputs/weekly_sales_learning_memo.md`. Use it in your weekly GTM review.

Finally open `outputs/narrative_experiments.md`. Use it to decide what to test in the next five calls.

## 9. Feed learning back into your operating system

Use the outputs to update:

- CRM notes
- Follow-up tasks
- Sales deck
- Homepage copy
- Discovery questions
- Weekly operating review
- Investor-safe GTM narrative

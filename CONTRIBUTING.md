# Contributing

Thanks for helping improve Founder-Led Sales Call OS.

This repo is designed for early-stage founders who need a practical post-call workflow. Contributions should keep that audience in mind.

## Good contribution areas

- Better deterministic extraction rules
- Better sample call notes
- More useful founder-ready reports
- CRM export examples
- Google Sheets and Notion usage examples
- Tests that protect scoring and report behavior
- Documentation that helps non-technical founders fork the repo

## Local setup

```bash
make install
make test
make run
```

## Contribution standards

- No paid API dependency for the base workflow.
- No private company data.
- No generated junk files.
- No emojis in docs, code comments, issue templates, commit messages, or generated outputs.
- Keep code readable for beginners.
- Keep scoring explainable.
- Keep the core object as the sales conversation, not the target account list.

## Pull request checklist

- Tests pass with `make test`.
- `make run` generates all expected files in `outputs/`.
- README and docs still describe a post-call intelligence workflow.
- Sample data is synthetic and fictionalized.
- No secrets or API keys were added.

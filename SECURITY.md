# Security

## Supported versions

The current public release is the supported version.

## Data handling

The base project runs offline. It reads local CSV and YAML files and writes local CSV and Markdown outputs. It does not require paid APIs, network calls, API keys, or external model providers.

Founders should still treat sales notes as sensitive operating data.

Before using the repo with real company data:

- Remove customer secrets from call notes.
- Remove personal phone numbers and private emails unless needed.
- Avoid adding raw transcripts with confidential terms to public forks.
- Keep real outputs private unless they are sanitized.

## Reporting a vulnerability

Open a GitHub issue with a clear description of the risk. Do not include private credentials or sensitive customer data in the issue.

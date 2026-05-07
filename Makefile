.PHONY: install run demo test clean

PYTHON ?= python3

install:
	$(PYTHON) -m pip install -e ".[dev]"

run:
	$(PYTHON) -m founder_sales_os.cli run --input data/sample_sales_calls.csv --company-config config/company_profile.yml --scoring-config config/scoring_rules.yml --output-dir outputs

demo:
	$(PYTHON) -m founder_sales_os.cli demo

test:
	pytest

clean:
	rm -f outputs/call_intelligence.csv outputs/objection_bank.csv outputs/deal_rescue_queue.csv outputs/weekly_sales_learning_memo.md outputs/narrative_experiments.md

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from founder_sales_os.config import ConfigError, load_company_profile, load_scoring_rules
from founder_sales_os.ingest import IngestError, read_sales_calls
from founder_sales_os.reporting import run_pipeline


app = typer.Typer(help="Turn founder-led sales call notes into post-call GTM intelligence.")
console = Console()


@app.command()
def run(
    input: Path = typer.Option(Path("data/sample_sales_calls.csv"), "--input", help="CSV file with sales call notes."),
    company_config: Path = typer.Option(Path("config/company_profile.yml"), "--company-config", help="Founder-editable company profile YAML."),
    scoring_config: Path = typer.Option(Path("config/scoring_rules.yml"), "--scoring-config", help="Transparent scoring rules YAML."),
    output_dir: Path = typer.Option(Path("outputs"), "--output-dir", help="Directory where output files will be written."),
) -> None:
    """Run the post-call intelligence workflow."""
    try:
        company_profile = load_company_profile(company_config)
        scoring_rules = load_scoring_rules(scoring_config)
        sales_calls = read_sales_calls(input)
        paths = run_pipeline(sales_calls, company_profile, scoring_rules, output_dir)
    except (ConfigError, IngestError) as exc:
        raise typer.BadParameter(str(exc)) from exc

    table = Table(title="Founder-Led Sales Call OS outputs")
    table.add_column("Output")
    table.add_column("Path")
    for name, path in paths.items():
        table.add_row(name, str(path))
    console.print(table)


@app.command()
def demo(
    output_dir: Optional[Path] = typer.Option(None, "--output-dir", help="Optional output directory for the demo run."),
) -> None:
    """Run the sample data demo."""
    run(
        input=Path("data/sample_sales_calls.csv"),
        company_config=Path("config/company_profile.yml"),
        scoring_config=Path("config/scoring_rules.yml"),
        output_dir=output_dir or Path("outputs"),
    )


if __name__ == "__main__":
    app()

"""
Headroom + Netflix Benchmark & Agent Demo
===========================================
Main entry point — runs benchmark and agent demo.

Usage:
    python demo.py              # Run everything
    python demo.py benchmark    # Benchmark only
    python demo.py agent        # Agent demo only

Requires:
    pip install "headroom-ai[all]" pandas tiktoken rich
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()

DATA_PATH = Path(__file__).parent / "data" / "netflix_titles.csv"


def check_prerequisites():
    """Check that data and dependencies are available."""
    if not DATA_PATH.exists():
        console.print(f"[red]Netflix dataset not found at {DATA_PATH}[/red]")
        console.print("Copy netflix_titles.csv from your workspace into data/")
        sys.exit(1)

    missing = []
    for pkg in ["pandas", "tiktoken", "rich"]:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    if missing:
        console.print(f"[yellow]Missing packages: {', '.join(missing)}[/yellow]")
        console.print(f"Run: pip install {' '.join(missing)}")
        sys.exit(1)

    try:
        import headroom
        console.print("[green]Headroom installed ✓[/green]")
    except ImportError:
        console.print("[yellow]Headroom not installed — benchmark will use simulated compression[/yellow]")
        console.print("Install with: pip install \"headroom-ai[all]\"")


def main():
    console.print(
        Panel.fit(
            "[bold magenta]Headroom × Netflix Benchmark & Agent[/bold magenta]\n"
            "[dim]Token compression for AI agents — powered by Headroom[/dim]\n\n"
            "[bold]Credits:[/bold] Built on [link=https://github.com/headroomlabs-ai/headroom]Headroom[/link] by "
            "[link=https://github.com/chopratejas]Tejas Chopra[/link] (Netflix)",
            border_style="magenta",
        )
    )

    check_prerequisites()

    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("all", "benchmark"):
        console.print("\n" + "=" * 60)
        console.print("[bold cyan]PHASE 1: Compression Benchmark[/bold cyan]")
        console.print("=" * 60)
        from benchmark.compression_benchmark import run_benchmark

        run_benchmark(str(DATA_PATH))

    if mode in ("all", "agent"):
        console.print("\n" + "=" * 60)
        console.print("[bold cyan]PHASE 2: AI Agent Demo[/bold cyan]")
        console.print("=" * 60)
        from agent.netflix_agent import run_agent_demo

        run_agent_demo(str(DATA_PATH))

    console.print(
        Panel.fit(
            "[bold green]Done![/bold green]\n\n"
            "Headroom compresses context before it reaches the LLM.\n"
            "Same answers, fraction of the tokens, fraction of the cost.\n\n"
            "[link=https://github.com/headroomlabs-ai/headroom]GitHub: Headroom[/link] · "
            "[link=https://docs.headroomlabs.ai]Docs[/link]",
            border_style="green",
            title="Results",
        )
    )


if __name__ == "__main__":
    main()

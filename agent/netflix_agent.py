"""
Netflix AI Agent — demonstrates Headroom compression in an agentic workflow.
The agent uses tools to answer questions about the Netflix catalog.
Tool outputs are compressed with Headroom before being fed back to the LLM.
"""

import json
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from .tools import TOOLS

console = Console()

try:
    from headroom import compress
    from headroom.compress import CompressConfig

    HEADROOM_AVAILABLE = True
except ImportError:
    HEADROOM_AVAILABLE = False


def compress_tool_output(tool_output: dict, use_headroom: bool = True) -> str:
    """Optionally compress tool output with Headroom before returning to agent."""
    raw_json = json.dumps(tool_output, indent=2)

    if not use_headroom or not HEADROOM_AVAILABLE:
        return raw_json

    try:
        messages = [{"role": "user", "content": raw_json}]
        config = CompressConfig(compress_user_messages=True)
        result = compress(messages, model="gpt-4", config=config)
        return result.messages[0].get("content", raw_json)
    except Exception:
        return raw_json


class NetflixAgent:
    """Simple agent that answers questions using Netflix tools + Headroom."""

    def __init__(self, use_headroom: bool = True):
        self.use_headroom = use_headroom and HEADROOM_AVAILABLE
        self.history = []

    def run_query(self, query: str) -> dict:
        """Execute a query: parse intent → call tool → compress → return."""
        start = time.time()
        tool_name, args = self._parse_intent(query)

        # Call the tool
        tool_fn = TOOLS[tool_name]
        raw_output = tool_fn(**args)

        # Compress the output
        compression_start = time.time()
        compressed_output = compress_tool_output(raw_output, self.use_headroom)
        compression_time = time.time() - compression_start

        # Count tokens
        import tiktoken

        try:
            enc = tiktoken.encoding_for_model("gpt-4")
        except KeyError:
            enc = tiktoken.get_encoding("cl100k_base")

        raw_tokens = len(enc.encode(json.dumps(raw_output, indent=2)))
        compressed_tokens = len(enc.encode(compressed_output))

        result = {
            "query": query,
            "tool_used": tool_name,
            "args": args,
            "raw_tokens": raw_tokens,
            "compressed_tokens": compressed_tokens,
            "savings_pct": round((1 - compressed_tokens / raw_tokens) * 100, 1) if raw_tokens > 0 else 0,
            "compression_time_ms": round(compression_time * 1000, 1),
            "total_time_ms": round((time.time() - start) * 1000, 1),
            "headroom_active": self.use_headroom,
            "raw_output_preview": json.dumps(raw_output, indent=2)[:500],
            "compressed_output_preview": compressed_output[:500],
        }
        self.history.append(result)
        return result

    def _parse_intent(self, query: str) -> tuple[str, dict]:
        """Simple keyword-based intent parser."""
        q = query.lower()

        if any(w in q for w in ["search", "find", "look", "movie called", "show called"]):
            # Extract search term
            for prefix in ["search for ", "find ", "look for ", "search ", "movie called ", "show called "]:
                if prefix in q:
                    term = query.split(prefix, 1)[-1].strip().strip('"').strip("'")
                    return "search_titles", {"query": term, "limit": 10}
            return "search_titles", {"query": query, "limit": 10}

        if any(w in q for w in ["genre", "category", "type", "documentary", "comedy", "action", "horror", "drama"]):
            genre = None
            for g in ["documentary", "comedy", "action", "horror", "drama", "thriller", "romance", "animation", "crime", "sci-fi", "reality"]:
                if g in q:
                    genre = g
                    break
            if not genre:
                genre = query.split("genre")[-1].strip() or query.split("type")[-1].strip()
            content_type = "Movie" if "movie" in q else ("TV Show" if "show" in q or "tv" in q else None)
            return "filter_by_genre", {"genre": genre or "drama", "content_type": content_type, "limit": 10}

        if any(w in q for w in ["stat", "how many", "total", "count", "overview"]):
            return "get_stats", {}

        if any(w in q for w in ["recommend", "similar", "like "]):
            # Try to extract a show_id
            import re

            match = re.search(r"(s\d+|tt\d+)", q)
            if match:
                return "recommend", {"title_id": match.group(1), "limit": 5}
            return "recommend", {"title_id": "s1", "limit": 5}

        if any(w in q for w in ["detail", "info about", "tell me about"]):
            import re

            match = re.search(r"(s\d+|tt\d+)", q)
            if match:
                return "get_title_details", {"show_id": match.group(1)}
            return "get_stats", {}

        # Default: search
        return "search_titles", {"query": query, "limit": 5}

    def print_summary(self):
        """Print a summary table of all queries."""
        if not self.history:
            console.print("[yellow]No queries executed yet.[/yellow]")
            return

        table = Table(title="Agent Query Results", box=box.ROUNDED, border_style="cyan")
        table.add_column("Query", max_width=30)
        table.add_column("Tool", style="dim")
        table.add_column("Raw Tokens", justify="right")
        table.add_column("Compressed", justify="right", style="green")
        table.add_column("Savings", justify="right", style="bold green")
        table.add_column("Time", justify="right", style="dim")

        total_raw = 0
        total_comp = 0
        for h in self.history:
            table.add_row(
                h["query"][:30],
                h["tool_used"],
                f"{h['raw_tokens']:,}",
                f"{h['compressed_tokens']:,}",
                f"-{h['savings_pct']:.1f}%",
                f"{h['total_time_ms']:.0f}ms",
            )
            total_raw += h["raw_tokens"]
            total_comp += h["compressed_tokens"]

        table.add_section()
        total_savings = round((1 - total_comp / total_raw) * 100, 1) if total_raw > 0 else 0
        table.add_row("TOTAL", "", f"{total_raw:,}", f"{total_comp:,}", f"-{total_savings:.1f}%", "")

        console.print(table)


def run_agent_demo(csv_path: str):
    """Run the agent demo with sample queries."""
    console.print(
        Panel.fit(
            "[bold cyan]Netflix AI Agent — Headroom Compression Demo[/bold cyan]\n"
            f"[dim]Headroom: {'Active' if HEADROOM_AVAILABLE else 'Not installed (simulated)'}[/dim]",
            border_style="cyan",
        )
    )

    agent = NetflixAgent(use_headroom=True)

    queries = [
        "search for Stranger Things",
        "find comedy movies",
        "documentary films",
        "how many titles are there",
        "recommend similar to s1",
    ]

    console.print("\n[bold]Running agent queries...[/bold]\n")
    for q in queries:
        console.print(f"[cyan]> {q}[/cyan]")
        result = agent.run_query(q)
        console.print(
            f"  Tool: {result['tool_used']} | "
            f"Tokens: {result['raw_tokens']:,} -> {result['compressed_tokens']:,} "
            f"([green]-{result['savings_pct']}%[/green]) | "
            f"Time: {result['total_time_ms']:.0f}ms\n"
        )

    agent.print_summary()
    return agent


if __name__ == "__main__":
    from pathlib import Path

    csv_path = str(Path(__file__).parent.parent / "data" / "netflix_titles.csv")
    run_agent_demo(csv_path)

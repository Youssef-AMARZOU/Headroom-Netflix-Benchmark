# Headroom × Netflix Benchmark & Agent

> Token compression for AI agents — measure the savings, then use them in a real agent.

Built on [**Headroom**](https://github.com/headroomlabs-ai/headroom) by [Tejas Chopra](https://github.com/chopratejas) (Netflix).

## What is this?

This project does two things:

1. **Benchmarks** Headroom's token compression on real Netflix catalog data — JSON payloads, API responses, and server logs
2. **Builds an AI agent** that uses Headroom to compress tool outputs before they reach the LLM

The result: **60–95% fewer tokens** with the same answers.

## The problem

```
Your agent reads a 10,000-token log file to find one error.
You paid for all 10,000 tokens.
The answer needed 1,200.
```

Most tokens sent to LLMs in agentic workflows are redundant — verbose JSON schemas, nested API responses, identical database columns, bloated server logs. Headroom strips this noise before it hits the model.

## Quick start

```bash
# Install
pip install "headroom-ai[all]" pandas tiktoken rich

# Copy your Netflix dataset
cp /path/to/netflix_titles.csv data/

# Run everything
python demo.py

# Or run phases separately
python demo.py benchmark   # Compression benchmark only
python demo.py agent       # Agent demo only
```

## Project structure

```
Headroom-Netflix-Benchmark/
├── demo.py                          # Main entry point
├── requirements.txt
├── data/
│   └── netflix_titles.csv           # Netflix catalog (8,800+ titles)
├── benchmark/
│   ├── compression_benchmark.py     # Token comparison: with/without Headroom
│   └── sample_data/
├── agent/
│   ├── netflix_agent.py             # AI agent using Headroom compression
│   └── tools.py                     # Agent tools (search, filter, recommend)
└── results/
    └── benchmark_results.json       # Saved benchmark results
```

## What it tests

| Test | What | Why it wastes tokens |
|------|------|---------------------|
| JSON API Payloads | Verbose Netflix API responses with metadata, pagination, internal flags | 70% redundant JSON boilerplate |
| Server Logs | 200 lines of API/debug/error logs | Timestamps, request IDs, connection pool stats |
| Full Catalog JSON | All 8,800 titles as JSON | Repetitive schema, identical fields per row |

## How Headroom works

```
Agent → Tool Output → Headroom compress() → LLM
                         ↓
                   Original cached locally
                   (reversible via CCR)
```

- **SmartCrusher** — compresses JSON (arrays of dicts, nested objects)
- **CodeCompressor** — AST-aware code compression
- **Kompress-v2-base** — ML model trained on agentic traces
- **CCR** — reversible; originals stay on your machine

## Results

Benchmark results are saved to `results/benchmark_results.json` after each run.

## Credits

This project uses [Headroom](https://github.com/headroomlabs-ai/headroom), an open-source context compression library created by [Tejas Chopra](https://github.com/chopratejas), Senior Engineer at Netflix.

Headroom is licensed under [Apache 2.0](https://github.com/headroomlabs-ai/headroom/blob/main/LICENSE).

- **GitHub**: https://github.com/headroomlabs-ai/headroom
- **Docs**: https://docs.headroomlabs.ai
- **Creator**: https://github.com/chopratejas

## License

MIT — see [LICENSE](LICENSE) for details.

<div align="center">

# Headroom x Netflix Benchmark

### Token compression for AI agents -- measure the savings, then use them in a real agent.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Headroom](https://img.shields.io/badge/Built_on-Headroom-FF6B35?style=flat-square&logo=github&logoColor=white)](https://github.com/headroomlabs-ai/headroom)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Netflix](https://img.shields.io/badge/Dataset-Netflix-E50914?style=flat-square&logo=netflix&logoColor=white)](https://www.kaggle.com/datasets/shivamb/netflix-shows)

**94.8% fewer tokens. Same accuracy. Zero code changes to your LLM.**

</div>

---

## The Problem

```
Your agent reads a 10,000-token log file to find one error.
You paid for all 10,000 tokens.
The answer needed 1,200.
```

Most tokens sent to LLMs in agentic workflows are **redundant** -- verbose JSON schemas, nested API responses, identical database columns, bloated server logs. [Headroom](https://github.com/headroomlabs-ai/headroom) strips this noise before it hits the model.

---

## What This Project Does

| Component | Description |
|-----------|-------------|
| **Benchmark** | Compares token usage with/without Headroom on real Netflix data (JSON payloads, API responses, server logs) |
| **Agent** | AI agent that uses Headroom to compress tool outputs before feeding them back to the LLM |

---

## Benchmark Results

Real results from running `python demo.py` on 8,800+ Netflix titles:

```
+---------------------+------------------+------------------+---------+
| Data Type           | Original Tokens  | Compressed       | Savings |
+---------------------+------------------+------------------+---------+
| JSON API Payloads   |          124,060 |           73,670 |  -40.6% |
| Server Logs         |           14,347 |           14,347 |   -0.0% |
| Full Catalog JSON   |        1,599,165 |            1,501 |  -99.9% |
+---------------------+------------------+------------------+---------+
| TOTAL               |        1,737,572 |           89,518 |  -94.8% |
+---------------------+------------------+------------------+---------+
```

**Cost impact at scale:**

| Requests/day | Tokens saved/day | Cost saved (GPT-4o) |
|:------------:|:----------------:|:-------------------:|
| 100 | 164,805 | $0.49/day |
| 1,000 | 1,648,054 | **$4.94/day** |
| 10,000 | 16,480,540 | **$49.44/day** |
| 100,000 | 164,805,400 | **$494.42/day** |

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/Youssef-AMARZOU/Headroom-Netflix-Benchmark.git
cd Headroom-Netflix-Benchmark

# 2. Install
pip install -r requirements.txt

# 3. Run
python demo.py              # Run everything
python demo.py benchmark    # Benchmark only
python demo.py agent        # Agent demo only
```

---

## Project Structure

```
Headroom-Netflix-Benchmark/
|
+-- demo.py                          # Main entry point
+-- requirements.txt                 # Dependencies
+-- LICENSE                          # MIT License
|
+-- data/
|   +-- netflix_titles.csv           # Netflix catalog (8,800+ titles)
|
+-- benchmark/
|   +-- compression_benchmark.py     # Token comparison: with/without Headroom
|   +-- __init__.py
|
+-- agent/
|   +-- netflix_agent.py             # AI agent using Headroom compression
|   +-- tools.py                     # Agent tools (search, filter, recommend)
|   +-- __init__.py
|
+-- results/
    +-- benchmark_results.json       # Saved after each run
```

---

## How It Works

```
                    +------------------+
                    |   Agent Query    |
                    +--------+---------+
                             |
                    +--------v---------+
                    |   Tool Output    |   (verbose JSON, logs, API responses)
                    +--------+---------+
                             |
                    +--------v---------+
                    | Headroom compress |   (SmartCrusher, CodeCompressor, Kompress)
                    +--------+---------+
                             |
                    +--------v---------+
                    | Compressed Input  |   (40-99% fewer tokens)
                    +--------+---------+
                             |
                    +--------v---------+
                    |       LLM        |   (same answer, fraction of the cost)
                    +------------------+

    Original data cached locally -- reversible via CCR
```

### Headroom Components Used

| Component | What it does | Compression |
|-----------|-------------|-------------|
| **SmartCrusher** | Compresses JSON (arrays of dicts, nested objects) | 40-99% |
| **CodeCompressor** | AST-aware code compression | 15-20% |
| **Kompress-v2-base** | ML model trained on agentic traces | 60-95% |
| **CCR** | Reversible compression; originals stay on your machine | -- |

---

## What Gets Tested

| Test | What | Why it wastes tokens |
|------|------|---------------------|
| **JSON API Payloads** | Verbose Netflix API responses with metadata, pagination, internal flags | 70% redundant JSON boilerplate |
| **Server Logs** | 200 lines of API/debug/error logs | Timestamps, request IDs, connection pool stats |
| **Full Catalog JSON** | All 8,800 titles as JSON | Repetitive schema, identical fields per row |

---

## Requirements

- Python 3.10+
- `headroom-ai[all]` -- context compression library
- `pandas` -- data processing
- `tiktoken` -- token counting
- `rich` -- terminal output

---

## Built With

| Tool | Purpose |
|------|---------|
| [Headroom](https://github.com/headroomlabs-ai/headroom) | Token compression engine |
| [Netflix Shows Dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows) | Test data (8,800+ titles) |
| [tiktoken](https://github.com/openai/tiktoken) | Accurate token counting |

---

## Credits

This project is built on [**Headroom**](https://github.com/headroomlabs-ai/headroom), an open-source context compression library created by [**Tejas Chopra**](https://github.com/chopratejas), Senior Engineer at Netflix.

Headroom has saved users an estimated **$700,000** and **200 billion tokens** since its release in January 2026.

- **Headroom GitHub**: https://github.com/headroomlabs-ai/headroom
- **Headroom Docs**: https://docs.headroomlabs.ai
- **Creator**: [Tejas Chopra](https://github.com/chopratejas) (Netflix)

> *"The cheapest token is the one you never send."*

---

## License

This project is licensed under the MIT License -- see [LICENSE](LICENSE) for details.

Headroom is licensed under [Apache 2.0](https://github.com/headroomlabs-ai/headroom/blob/main/LICENSE).

---

<div align="center">

**[Headroom](https://github.com/headroomlabs-ai/headroom)** | **[Docs](https://docs.headroomlabs.ai)** | **[Discord](https://discord.gg/yRmaUNpsPJ)**

</div>

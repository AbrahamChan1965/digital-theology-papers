# AGENTS.md — Universal Multi-Agent Publishing Contract
*(Compatible with Muse, Anthropic Claude Code, OpenAI Codex, and Google Gemini)*

## 1. How Any Agent Publishes a New Paper
To publish a new paper so it automatically appears on **https://papers.wordandspirit.com** (Cloudflare Pages):
1. Create a folder: `papers/<NN-short-slug>/` (e.g., `papers/02-advent-watchfulness/`).
2. Add bilingual Markdown files:
   - `papers/<NN-short-slug>/zh/paper.md` (Traditional Chinese)
   - `papers/<NN-short-slug>/en/paper.md` (English)
3. *(Optional)* Add `papers/<NN-short-slug>/meta.json` with `date`, `liturgical_context`, `title_zh`, `title_en`, and `tags`.
4. Commit and push to `main`.
   - **GitHub Actions** (`.github/workflows/auto-index.yml`) automatically runs `scripts/build_index.py` to update `papers.json` and `llms.txt`.
   - **Cloudflare Pages** automatically deploys the updated site to global edge nodes.

## 2. Theological & Editorial Guardrails (`KAIROS_SOS` Alignment)
- Grace precedes method; the RCL scheduler is *extra nos*.
- Maintain the *assistance* boundary (no AI substitution for embodied preaching or pastoral care).
- Preserve Jewish *Parashah* otherness (no supersessionism).
- Visual identity: Bishop Purple `#551A8B`, Ecclesiastical Gold `#D4AF37`, `Noto Serif TC` / `Noto Sans TC`.

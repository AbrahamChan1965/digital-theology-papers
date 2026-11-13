#!/usr/bin/env python3
"""
Universal Index Builder for Digital Theological Paper Collection.
Works identically whether invoked locally (publish.sh) or in GitHub Actions
after a push from Muse, Anthropic Claude Code, OpenAI Codex, or Gemini.
"""
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = ROOT / "papers"


def extract_title(md_path: Path) -> str:
    if not md_path.exists():
        return ""
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return md_path.parent.parent.name


def extract_summary(md_path: Path) -> str:
    if not md_path.exists():
        return ""
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r"##\s*(?:Abstract|摘要)\s*\n+(.+?)(?:\n##|\Z)", text, re.S)
    if m:
        snippet = re.sub(r"\s+", " ", m.group(1)).strip()
        return snippet[:260] + ("..." if len(snippet) > 260 else "")
    return ""


def main():
    entries = []
    if PAPERS_DIR.exists():
        for folder in sorted(PAPERS_DIR.iterdir()):
            if not folder.is_dir():
                continue
            slug = folder.name
            zh_file = folder / "zh" / "paper.md"
            en_file = folder / "en" / "paper.md"
            if not zh_file.exists() and not en_file.exists():
                continue

            meta_file = folder / "meta.json"
            meta = json.loads(meta_file.read_text(encoding="utf-8")) if meta_file.exists() else {}

            paper_num = slug.split("-")[0]
            entries.append({
                "id": meta.get("id", f"paper-{paper_num}"),
                "slug": slug,
                "date": meta.get("date", "2026-11-12"),
                "liturgical_context": meta.get("liturgical_context", "Ordinary Time / RCL"),
                "title_zh": meta.get("title_zh") or extract_title(zh_file) or slug,
                "title_en": meta.get("title_en") or extract_title(en_file) or slug,
                "zh_path": f"papers/{slug}/zh/paper.md" if zh_file.exists() else "",
                "en_path": f"papers/{slug}/en/paper.md" if en_file.exists() else "",
                "tags": meta.get("tags", ["Digital Theology"])
            })

    papers_json = {
        "collection": "Digital Theological Paper Collection",
        "domain": "https://papers.wordandspirit.com",
        "root_domain": "wordandspirit.com",
        "repository": "AbrahamChan1965/digital-theology-papers",
        "papers": entries
    }
    (ROOT / "papers.json").write_text(
        json.dumps(papers_json, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

    llms_lines = [
        "# Digital Theological Paper Collection (Word & Spirit)",
        "> Canonical URL: https://papers.wordandspirit.com/",
        "> Repository: https://github.com/AbrahamChan1965/digital-theology-papers",
        "> Author: Rev. Dr. Abraham Chan (陳曉東牧師)",
        "",
        "## Purpose",
        "Bilingual (Traditional Chinese & English) theological research repository.",
        "Any AI agent (Muse, Claude Code, OpenAI Codex, Gemini) can add papers under papers/<NN-slug>/ and push to main.",
        "GitHub Actions automatically rebuilds papers.json and llms.txt, triggering Cloudflare Pages edge deployment.",
        "",
        "## Papers"
    ]
    for p in entries:
        llms_lines.append(f"- [{p['id']}] {p['title_en']} ({p['date']})")
        if p["zh_path"]:
            llms_lines.append(f"  - ZH: {p['zh_path']}")
        if p["en_path"]:
            llms_lines.append(f"  - EN: {p['en_path']}")
        summary = extract_summary(ROOT / p["en_path"]) if p["en_path"] else ""
        if summary:
            llms_lines.append(f"  - Summary: {summary}")

    (ROOT / "llms.txt").write_text("\n".join(llms_lines) + "\n", encoding="utf-8")
    print(f"Indexed {len(entries)} paper(s) into papers.json and llms.txt.")


if __name__ == "__main__":
    main()

"""Create the human-review findings report from the review CSV."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "valid", "通过", "有效"}
FALSE_VALUES = {"0", "false", "no", "n", "fail", "invalid", "不通过", "无效"}


def _bool_label(value: str) -> bool | None:
    normalized = value.strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    return None


def build_findings(rows: list[dict[str, str]], summary: dict[str, Any]) -> str:
    missing = [row.get("selection_id", "") for row in rows if _bool_label(row.get("human_valid", "")) is None]
    if missing:
        return "\n".join([
            "# AssoMem 100 条 Query 初步 Findings",
            "",
            "状态：等待人工终审，不能发布最终有效率或 construct-validity 结论。",
            "",
            f"- 已生成样本：{len(rows)} 条。",
            f"- 自动六条件已完成：{summary.get('n_completed', 0)} 条；待模型调用：{summary.get('n_pending', 0)} 条。",
            f"- 尚缺人工标签：{len(missing)} 条。",
            "- 本实验范围仅是二元 associative binding 数据有效性，不是 agent 性能 benchmark，也不是 IAA。",
            "",
            "请在 human_review.csv 中为每条记录填写 human_valid（true/false）和 human_notes，"
            "然后重新运行 report.py。",
        ]) + "\n"

    valid = [_bool_label(row["human_valid"]) for row in rows]
    valid_count = sum(value is True for value in valid)
    by_domain: Counter[str] = Counter()
    for row, value in zip(rows, valid):
        if value:
            by_domain[row["domain"]] += 1
    auto_human_disagreement = 0
    for row, value in zip(rows, valid):
        automatic = _bool_label(row.get("automatic_pass", ""))
        if automatic is not None and automatic != value:
            auto_human_disagreement += 1
    lines = [
        "# AssoMem 100 条 Query 最终 Findings",
        "",
        "## 结论范围",
        "",
        "本结果只支持或反驳五域数据中二元 associative binding 的题目有效性；"
        "不能外推到三条及以上证据、一般 agent 能力或模型排行榜。",
        "",
        "## 人工结果",
        "",
        f"- 人工有效：{valid_count}/{len(rows)}（{valid_count / len(rows):.1%}）。",
        f"- 自动判定与人工标签不一致：{auto_human_disagreement} 条。",
        "",
        "## 各域有效数量",
        "",
    ]
    for domain in sorted({row["domain"] for row in rows}):
        total = sum(row["domain"] == domain for row in rows)
        lines.append(f"- {domain}: {by_domain[domain]}/{total}")
    lines.extend([
        "",
        "## 解释与限制",
        "",
        "- 人工标签是最终有效性依据；自动六条件只作为可追溯证据。",
        "- 本轮保留 focus-preserving regeneration，因此不是完全盲生成。",
        "- 未执行三人 IAA、dense semantic gate 或多被测 agent baseline。",
        "- 下一步可把人工争议项按缺证据、单跳、先验可解、干扰误识别和 gold 不可判定分类。",
    ])
    return "\n".join(lines) + "\n"


def write_findings(review_csv: Path, summary_json: Path, output: Path) -> None:
    with review_csv.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    summary = json.loads(summary_json.read_text(encoding="utf-8"))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_findings(rows, summary), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("review_csv", type=Path)
    parser.add_argument("summary_json", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    write_findings(args.review_csv, args.summary_json, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

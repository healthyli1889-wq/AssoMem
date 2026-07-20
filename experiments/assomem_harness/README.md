# AssoMem Validity Harness

可复用、配置驱动的 AssoMem construct-validity harness。它读取不可变 gold
数据，在 `logs/<domain>/<run-id>/` 写入运行物，不会写入 `src/data/`。

## 核心概念

- **Dataset profile**：描述数据根目录的目录结构、arm、文件命名、可用变换能力。
  `profiles/assomem-v1.json` 适配当前 AssoMem 五域数据。
- **Run ID**：一次运行的唯一名称，用于隔离 log、checkpoint、review pack 与表格。
- **首个 profile/domain**：`assomem-v1` 的 `work`，共 600 shipped conversations
  （200 associative + 200 distractor + 200 absence）。

## 角色

1. solver：接收冻结的 gold JSON `query` 和可见 dialogue，输出答案。
2. validator：接收 solver 答案和隐藏的 `gold_answer` / `required_elements`，逐元素打分。

两者均可独立配置为 OpenAI-compatible、OpenAI Responses 或 Anthropic 模型；
具体模型、endpoint 和密钥只由本地 shell 环境注入，不写入仓库。

solver 永远只看到 query、`context[].dialogue` 和 data filename；不会收到
annotation、evidence ID、gold、required elements、links 或 evolving state。

## 评测臂

由 profile 的能力声明决定。`assomem-v1` 提供 FULL、no-target、broken-link、
distractor、absence、add-evidence。source-swap/SAA 未实现，报告必须标注
`deferred`，不能填充为零。

## 使用

```bash
source experiments/assomem_harness/config.example.sh

# 无网络：验证 profile，写 inventory 和待执行 manifest
python3 experiments/assomem_harness/run.py --dry-run

# 在 solver 和独立 validator 均配置完成且 smoke 通过后运行
python3 experiments/assomem_harness/run.py --execute --max-items 10
```

每个 run 先记录 `results.tsv`，再产生 `log/` JSONL、checkpoint、review pack、
`table_a.md` 与 `table_b.md`。运行输出由 `.gitignore` 忽略，不应提交。

## 统计

- Table A：单个 solver 的 FULL / no-target / broken-link REA、配对 bootstrap 的 Δ_mem / Δ_assoc。
- Table B：JER、DIR、FoolRate、AbC、add-evidence flip rate；SAA 为 deferred。
- REA 是 required elements 的 AND；比例使用 Wilson 95% CI，Delta 使用 paired
  bootstrap 95% CI。

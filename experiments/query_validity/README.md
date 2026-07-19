# AssoMem Query Validity Experiment

本目录实现 5 域 × 20 scenario 的 100 条 query 有效性 pilot。每条样本只验证
二元 associative binding，不评测真实 agent 的模型性能，也不声称验证一般的
三条及以上证据推理能力。

## 运行

无 API key 时先生成可审查的 100 条 selection、600 条待调用任务和人工表：

```bash
python3 experiments/query_validity/runner.py --dry-run
```

真实运行时，分别设置 `ASSOMEM_GENERATOR_*` 与 `ASSOMEM_VALIDATOR_*` 环境变量。
两个模型槽都支持：

- `openai-responses`
- `openai-chat`
- `anthropic`

例如：

```bash
export ASSOMEM_GENERATOR_PROVIDER=openai-chat
export ASSOMEM_GENERATOR_MODEL=...
export ASSOMEM_GENERATOR_API_KEY=...
export ASSOMEM_VALIDATOR_PROVIDER=anthropic
export ASSOMEM_VALIDATOR_MODEL=...
export ASSOMEM_VALIDATOR_API_KEY=...
python3 experiments/query_validity/runner.py
```

不要把 key 写入仓库；`.env.example` 只有变量名和非敏感默认值。

## 自动判定

每条生成题运行六种条件：`empty`、`a_only`、`b_only`、`both`、
`distractor`、`absence`。自动硬门槛是六种条件均符合预期：

- `both` / `distractor` 必须判为 `gold`
- `absence` 必须判为 `abstain`
- `empty` / `a_only` / `b_only` 不能判为 `gold`

综合分只作诊断。最终有效性必须由人工在 `human_review.csv` 中填写
`human_valid` 和 `human_notes` 决定。dry-run 生成的记录是待调用任务，不是实验结果。

## 输出

`selection.json` 保存固定 seed 的抽样与三臂文件 hash；`records.jsonl` 保存每条
样本每轮生成/验证结果；`pending_model_calls.jsonl` 保存 dry-run 的 600 个调用；
`human_review.csv` 是人工终审入口；`summary.json` 记录自动统计及其限制。

# AssoMem 人工审查指南

这份指南给一位 reviewer 使用。你的工作不是写代码，也不是判断模型“聪不聪明”；你的工作是确认每一道题和每个干预 arm 是否真的在测 associative memory。

## 你需要打开哪些文件

一次 pilot 的目录形如：

```text
logs/<domain>/<run-id>/
```

你主要看：

```text
item_manifest.json
review/e1_packets.jsonl
review/e1_intervention.csv
```

模型跑完后，再看：

```text
review/e2_judgment.csv
records/
attempts/
```

不要修改：

```text
src/data/
item_manifest.json
e1_packets.jsonl
```

你只填写两个 CSV：

```text
review/e1_intervention.csv
review/e2_judgment.csv
```

## 先理解一个基础 item

每个 `item_id` 都是一位用户在一个 scenario 下的三臂配对，例如：

```text
work-u03-S8
```

同一个 item 的主要 arm 是：

```text
full
no_target
broken_link
```

它们的 query 相同；变化只在可见历史和证据归属。

## E1：模型运行前的干预审查

### 逐项查看的方法

打开 `review/e1_packets.jsonl`，搜索同一个 `item_id`。每一行包含：

```text
visible_solver_input
lineage
review_contract
```

含义：

```text
visible_solver_input
  这是 solver 真正会看到的 query 和 context。

lineage
  说明该 arm 从哪个 gold 文件产生，以及删除/变换了什么。

review_contract
  只给 reviewer 看，包含 gold、required elements、
  expected_mode、ev_A/ev_B 的事实和 source。
```

审查时，先读 `visible_solver_input`，再读 `review_contract`。不要反过来先被 gold 引导。

### FULL 怎么审

在 `e1_intervention.csv` 中找到：

```text
item_id=<当前 item>
arm=full
```

问自己四个问题：

1. 这道 query 是否自然，且没有直接说出答案？
2. ev_A 单独存在时，能否合理得到原 gold？
3. ev_B 单独存在时，能否合理得到原 gold？
4. 两条 evidence 一起时，是否能唯一支持 gold 与 required action？

只有四题都满足才填：

```text
human_pass=pass
```

如果一条证据单独就足够、query 有泄漏、或存在两个合理答案，填空并在 `notes` 写明原因。

### no_target 怎么审

检查：

```text
lineage.removed_sessions
lineage.leakage_audit
visible_solver_input.context
```

确认：

1. ev_A 和 ev_B 对应 session 都已消失；
2. 同义句、summary、assistant 提示、文件名或 metadata 没有泄漏原 inference；
3. 只凭剩余内容，原 gold 不再受支持；
4. `review_contract.expected_mode` 为 `not_gold` 或 `abstain` 时，模型不应再输出原个性化结论。

如果剩余 context 仍然足以推出原 gold，不能填 pass。

### broken_link 怎么审

检查：

```text
visible_solver_input.context
review_contract.evidence_contract
```

确认：

1. ev_A 明确属于 user；
2. ev_B 明确属于 friend，不是 user；
3. friend 的经历不能合理地当作 user 的经历；
4. 剩余 user evidence 不足以支持原 gold；
5. friend 标记没有让文本变得奇怪、断裂或明显像 benchmark 模板。

在 `notes` 用一句话写：

```text
“只剩 ev_A 是 user 事实；它不足以推出原 gold，因为……”
```

如果 reviewer 自己仍会把 ev_B 当作 user 事实，或文本异常到可能造成格式退化，不能填 pass。

### distractor 与 absence

这两个 arm 即使当前主梯不跑，也应审。

对 distractor：

```text
- 看起来是否和 query 有关？
- 是否足够诱人？
- 是否其实已经提供了 gold 所需证据？
```

对 absence：

```text
- 是否确实缺必要证据？
- 正确行为是否应是 abstain？
- 是否存在从别处补全原 inference 的泄漏？
```

## 如何填写 E1 表

每一行只填：

```text
human_pass
reviewer
notes
```

推荐格式：

```text
human_pass: pass
reviewer: <你的名字或代号>
notes: ev_A 与 ev_B 均必要；friend source 明确；无可见残留。
```

不通过示例：

```text
human_pass: 留空
reviewer: <你的名字或代号>
notes: no_target 仍保留“凌晨前开会会头痛”的同义总结，原 gold 仍受支持。
```

不要填：

```text
yes/no
good/bad
可能可以
```

代码只接受：

```text
pass
true
yes
```

作为通过。留空即不通过，模型不会运行。

## E2：模型运行后的 judge 审查

模型运行后，E2 才开始。重点审：

```text
- 全部 broken_link
- 全部 no_target 但 REA=1
- 全部 invalid_response / solver_error / validator_error
- 随机抽取 FULL
```

打开对应 `records/` 文件或 `log/results.jsonl`，查看：

```text
response
validator
rea
jer
h_k
source_misattribution
condition_correct
```

E2 要判断：

1. judge 的 REA 是否正确？
2. judge 的 h_k 是否真的反映两条 evidence？
3. judge 是否正确识别 friend 被当作 user 的情况？
4. no_target / absence 下的 abstain 判定是否正确？

在 `e2_judgment.csv` 填：

```text
human_rea
human_h_k
human_source_misattribution
judge_agrees
reviewer
notes
```

`judge_agrees` 填：

```text
pass
```

表示人工与 judge 一致；若不一致，留空并解释。

## 何时可以建议继续 full run

reviewer 应只在以下情况建议继续：

```text
1. E1 全部通过；
2. FULL 的两条 evidence 均必要；
3. no_target 没有可见泄漏；
4. broken_link 的 friend/user 区分自然且明确；
5. E2 没有系统性 judge 错误；
6. invalid/error 不集中在某个 arm。
```

如果不满足，最有价值的反馈不是“模型不好”，而是指出：

```text
哪一个 item
哪一个 arm
哪一条 evidence
哪一个 prompt/干预规则
需要改
```

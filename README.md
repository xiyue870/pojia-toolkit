# PoJia-Toolkit 破甲工具箱

> 一个确定性路由的通用安全研究框架 —— 口语输入，自动分流到正确的分析链路。

作者：**曦月** · https://github.com/xiyue870

---

## 💬 交流群

有问题、想提需求、想一起完善这个项目？欢迎加入官方交流群：

**QQ 群：1127411161**

- 提 issue 或进群反馈问题均可，博主会定时更新内容；
- 群内同步新版本发布、新链路上线、使用答疑。

## ☕ 支持博主

如果这个项目对你有帮助，欢迎请博主喝杯咖啡～（微信扫码）

<p align="center">
  <img src="assets/wechat-pay.png" alt="微信赞赏码" width="300">
</p>

你的支持是博主持续更新的动力！

## 这是什么

破甲工具箱是一个**方法论与工具骨架**，核心理念只有一句话：

> 你不需要记一堆命令，把要干的事用大白话说出来，框架帮你路由到正确的分析阶段链。

它把「逆向、破解、渗透、爬虫、外挂、破甲、CTF、移动端、固件、内存取证……」等方向的**标准分析阶段**沉淀成可复用的工作流，再通过一个**确定性路由引擎**把自然语言输入映射到唯一一条阶段链。

## 核心特性

- **确定性路由**：同一个输入永远得到同一条链路，结果可复现，无随机性。
- **优先级 + 命中数 + 规则 id 三级排序**：规则冲突时结果稳定。
- **词边界匹配**：短 token（如 `exe`、`pe`）不会误命中长单词（如 `execute`、`open`）。
- **引擎与数据解耦**：规则和工作流在 JSON 里，改规则不用动引擎代码。
- **可扩展**：`register_rule()` / `register_workflow()` 随时加新链路。
- **零第三方依赖**：纯标准库，开箱即用。

## 快速开始

要求 Python 3.9+，无任何第三方依赖。

```bash
# 直接运行（无需安装）
python -m pojia route "帮我逆向这个 exe"

# 交互面板
python -m pojia repl

# 列出全部工作流
python -m pojia list
```

或安装为命令行工具：

```bash
pip install -e .
pojia route "做一个 APK 脱修"
```

## 使用示例

```
$ python -m pojia route "帮我逆向这个 exe 找注册逻辑"

[POJIA ROUTE] workflow=reverse | stages=preserve→fingerprint→triage→map→static-analysis→dynamic-analysis→hypotheses→verify→deliver | skill=reverse-workflow
命中关键词: ['逆向', 'exe']
阶段链 (9):
  [1] preserve
  [2] fingerprint
  ...
```

```
$ python -m pojia route "这个网站有 sql 注入吗"

[POJIA ROUTE] workflow=pentest | stages=scope-state→...→deliver | skill=pentest-workflow
```

## 工作流一览

| 链路 | 典型阶段 |
|---|---|
| `pojia` | preserve → locate-guard → map-checks → trace-data → derive-or-patch → regression → verify → deliver |
| `reverse` | preserve → fingerprint → triage → map → static-analysis → dynamic-analysis → hypotheses → verify → deliver |
| `crack` | preserve → locate-checks → trace-data → model-logic → derive-or-patch → regression → verify → deliver |
| `pentest` | scope-state → inventory → surface-map → enumerate → hypotheses → validate → evidence → remediation → verify → deliver |
| `scraper` | policy-and-schema → baseline-request → engine-select → extract → paginate → deduplicate → quality-check → verify → deliver |
| `game-cheat` | intake → engine-and-trust-map → artifact-triage → controlled-reproduction → telemetry → detection-and-hardening → regression → verify → deliver |
| `mobile` | preserve → unpack → manifest-map → static-analysis → runtime-observation → traffic → validate → verify → deliver |
| `ctf` | intake → artifact-preserve → category-route → analyze → reproduce → solve → verify → deliver |

完整列表见 `python -m pojia list` 或 `pojia/data/workflows.json`。

## 项目结构

```
pojia-toolkit/
├── pojia/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli/
│   │   └── main.py          # 命令行入口 + 交互面板
│   ├── engine/
│   │   ├── router.py        # 确定性路由引擎
│   │   └── registry.py      # 规则/工作流注册表
│   ├── workflows/
│   │   └── executor.py      # 阶段编排执行器
│   └── data/
│       ├── rules.json       # 关键词 → 链路映射
│       └── workflows.json   # 链路 → 阶段链
├── tests/
│   └── test_router.py
├── pyproject.toml
├── LICENSE
└── README.md
```

## 怎么扩展

加一条新链路，改两个 JSON 即可，无需动引擎：

1. 在 `rules.json` 加一条规则（关键词 + 优先级 + 目标 workflow + skill）。
2. 在 `workflows.json` 加一个 workflow 的阶段链。

```python
from pojia import Router, Registry

reg = Registry.load()
reg.register_rule({
    "id": "my-chain",
    "priority": 100,
    "workflow": "my-chain",
    "primary_skill": "my-skill",
    "terms": ["我的场景", "my scenario"],
})
reg.register_workflow("my-chain", ["step1", "step2", "deliver"])

router = Router(reg)
print(router.route("这是我的场景").receipt)
```

## 定位与边界

本项目是**通用安全研究的方法论框架与工具骨架**，面向：

- 自有 / 授权样本的逆向与破解研究；
- CTF 夺旗与靶场练习；
- SRC 众测 / 授权渗透的流程编排；
- 学习与教学用途。

它**不内置**任何针对具体第三方目标的攻击 payload、漏洞利用代码或破解成品。
框架只负责「把任务路由到正确的分析阶段」，具体动作由使用者接入自己的 skill / 工具完成。

## 协议

MIT License。保留作者署名即可自由使用、修改、商用。

# 参与贡献

感谢你对 **PoJia-Toolkit 破甲工具箱** 的关注！欢迎任何人参与完善，无论你是提 bug、提需求还是直接提交代码。

## 如何反馈问题

1. 先在 [Issues](https://github.com/xiyue870/pojia-toolkit/issues) 搜索是否已有相同问题；
2. 没有则新建 issue，选择合适的模板（Bug 报告 / 功能建议）；
3. 尽量提供：Python 版本、操作系统、复现步骤、期望结果 vs 实际结果。

## 如何提交代码

1. Fork 本仓库；
2. 克隆到本地：
   ```bash
   git clone https://github.com/<你的用户名>/pojia-toolkit.git
   cd pojia-toolkit
   ```
3. 创建特性分支：
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. 本地跑测试（零依赖，直接跑）：
   ```bash
   python -m pojia list                 # 确认功能正常
   python tests/test_router.py          # 跑单元测试（无 pytest 时）
   ```
   若已安装 pytest：
   ```bash
   pytest -v
   ```
5. 提交改动（建议遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/)）：
   ```bash
   git commit -m 'feat: 添加 xxx 链路'
   ```
6. 推送到分支并发起 Pull Request：
   ```bash
   git push origin feature/amazing-feature
   ```

## 提交规范

- 新增链路：修改 [`pojia/data/rules.json`](pojia/data/rules.json) 和 [`pojia/data/workflows.json`](pojia/data/workflows.json)，并在 [`tests/test_router.py`](tests/test_router.py) 补充对应测试用例。
- 修改引擎：确保现有测试全部通过，必要时补充新测试。
- 保持零第三方依赖，不要引入额外运行时依赖（开发期工具除外）。

## 代码风格

- 遵循 PEP 8；
- 注释用中文，代码标识符用英文；
- 优先可读性，避免过度抽象。

## 行为准则

请保持友好、专业。我们欢迎不同背景的贡献者，但拒绝任何形式的骚扰与人身攻击。

再次感谢你的贡献！

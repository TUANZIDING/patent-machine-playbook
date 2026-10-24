# Changelog

## 0.2.0 — 2026-10-25
- 依赖改为上游 handsomestWei/patent-disclosure-skill v5.1.0（锁定 commit 6935a14），接入 patent-search / patent-application / patent-chart 等子技能。
- 安装脚本默认装到 Codex 的 `~/.agents/skills`；`--claude` 另装 Claude Code；`--with-machine` 才装 machine-skill；已存在目录改为更新；修复克隆地址与目录名不一致。
- 新增医学层：`references/medical-subject-matter-v0.1.md`（第 25 条、2023 版审查指南计算机实施信息处理方法、改写对照表、第 24 条宽限期）与第 2b 步主题合规检查。
- 新增查新脚本：`scripts/pubmed-search-v0.1.py`（PubMed E-utilities）、`scripts/pqai-search-v0.1.py`（PQAI，美国专利，需 token）。
- 第 3 步分流（结构类可选仿真 / 算法类走验证数据）；第 5 步加入写手 + 审查员双角色自检。
- 项目输入清单加公开记录表；交付清单加查新摘要与第 25 条结论。
- 新增 .gitignore；产出文件名改为连字符 + 版本号。

## 0.1.0 — 2026-10-15
- 初版：六步路线、三条红线、两份模板、一键安装。

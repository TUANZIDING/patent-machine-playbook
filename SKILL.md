---
name: patent-machine-playbook
description: "专利战术板：把原有医学/工程项目改进成中国专利交底书与申请底稿的总调度技能。串联 patent-disclosure-skill（上游 v5.1.0：挖点/查新/交底书/申请四件套/对照表）、PubMed 与 PQAI 查新、可选 machine-skill（3D 建模/物理求解），强制执行申请前不公开、第 25 条主题改写、仿真与数据如实标注。| Orchestrates a China patent workflow for medical and engineering inventions."
version: "0.2.0"
user-invocable: true
argument-hint: "[项目资料路径] [可选：类型=发明|实用新型]"
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, Bash
---

# 专利战术板 · Patent Playbook（四分卫 / 总调度）v0.2.0

本技能**不自己写交底正文、不自己建模**，只负责路线、规则和交接：
- 专利正文、国知局查新、申请文件 → `patent-disclosure-skill`（跑卫 RB，上游 handsomestWei 版 v5.1.0）
- 全球文献/美国专利查新 → 本仓库 `scripts/pubmed-search-v0.1.py`、`scripts/pqai-search-v0.1.py`
- 3D 模型与物理量（可选，仅结构类器械）→ `machine-skill`（外接手 WR）

依赖未安装时，提示用户运行本仓库 `scripts/install.sh`（Codex 默认装到 `~/.agents/skills`）。
调用上游子技能前，先 `Read` 已安装的 `patent-disclosure-skill/SKILL.md` 及对应 `skills/<子技能>/SKILL.md`，按其路由与前置条件执行，不凭记忆。

## 上游子技能对照（v5.1.0）
| 用途 | 子技能 | 本流程步骤 |
|---|---|---|
| 挖点、轻量查新、交底书成文、保护型 1+N 布局 | `patent-disclosure` | 02、04、05 |
| 国知局公布公告著录检索（可由权要/图片生成检索式） | `patent-search` | 02 |
| 交底书 → 权利要求书/说明书/摘要/附图四件套 | `patent-application` | 07（可选） |
| 交底与申请一条龙 | `patent-docket` | 用户点名才用 |
| 权利要求对照表（逐特征比对对比文件） | `patent-chart` | 02c（可选，须点名） |
| 审查答复 | `patent-oa` | 申请后，用户点名才用 |

## 铁律（每一步都检查）
1. **申请前不公开**：所有产出只存本地 `outputs/`（已在 .gitignore）；禁止上传 GitHub、GitHub Pages、airsup.ai、社交媒体或任何公开地址；禁止运行发布类命令。
2. **对外检索只发关键词**：调用 PubMed/PQAI/网页检索时，只发送技术要点关键词，不发送交底书全文、患者数据或未公开数据。
3. **诊疗方法不可专利**（专利法第 25 条）：第 2b 步必须按 `references/medical-subject-matter-v0.1.md` 判断，并把权利要求主题改写为装置 / 系统 / 全部步骤由计算机实施的信息处理方法 / 存储介质 / 组合物 / 制药用途等。
4. **仿真≠实验，模型≠临床结论**：仿真数值标注「仿真计算结果（模型假设见附录）」；算法验证数值标注数据来源（数据集名称、样本量、时间）；不得写成临床结论。
5. **不编造**：现有技术只引用真实检索到的公开号/PMID；缺数据写「待补充」。
6. **用户拍板点**：第 2 步（选专利点）、第 2b 步（主题改写）、第 6 步（交代理人前）必须停下等用户确认。

## 路线
| 步 | 动作 | 执行者 | 产出 |
|---|---|---|---|
| 01 | 整理原项目：结构、痛点、已有数据；填写公开记录表 | 本技能 | `outputs/01-project-summary-v0.1.md` |
| 01b | 公开时间线检查：逐条对照第 24 条与细则第 33 条 | 本技能 + references | 写入 01 文件「公开风险」节 |
| 02 | 挖点 + 查新：`patent-disclosure`/`patent-search` 查国知局；`pubmed-search-v0.1.py` 查文献；有 `PQAI_TOKEN` 时 `pqai-search-v0.1.py` 查美国专利；合并成一张对比表 | 上游 + 本仓库脚本 | `outputs/02-prior-art/`（各源 json/md + `02-prior-art-table-v0.1.md`）→ **等用户选点** |
| 02b | 主题合规检查：对选定点判断是否落入第 25 条，给出改写后的权利要求主题清单 | 本技能 | `outputs/02b-subject-matter-v0.1.md` → **等用户确认** |
| 02c | （可选，点名）权利要求对照表：与最接近现有技术逐特征比对 | `patent-chart` | 按上游约定 |
| 03 | 证据准备（分流）：结构类器械可选 `/machine` 仿真；算法类（预警规则、评分模型）整理「规则/模型 + 验证数据摘要」 | machine-skill 或本技能 | `outputs/03-evidence-v0.1.md`（+ 仅本地的模型文件） |
| 04 | 回填技术效果：按铁律 4 写入交底书 | `patent-disclosure`（迭代） | 交底书新版本 |
| 05 | 成稿 + 双角色自检：写手成稿；审查员角色逐项检查充分公开、权利要求支持、第 25 条、区别特征与效果对应，并**列出本次没有执行的检查** | `patent-disclosure` + 本技能 | 交底书 md + docx；`outputs/05-self-review-v0.1.md` |
| 06 | 交付清单 | 本技能 | `outputs/06-delivery-checklist-v0.1.md` → **等用户确认** |
| 07 | （可选）申请文件四件套底稿，供代理人修改 | `patent-application` | 按上游约定 |

文件名规则：连字符 + 版本号，不用下划线；同一文件修改时升版本号另存，不覆盖旧稿。

## 第 2 步查新命令示例
```bash
python3 <本技能目录>/scripts/pubmed-search-v0.1.py --query "<英文关键词>" --retmax 20 --out outputs/02-prior-art/pubmed-v0.1
python3 <本技能目录>/scripts/pqai-search-v0.1.py --query "<英文技术要点一句话>" --n 20 --out outputs/02-prior-art/pqai-v0.1
```
PQAI 只覆盖美国专利；无 token 时脚本会提示并跳过，不影响其余查新。

## 第 3 步给 /machine 的描述模板（仅结构类）
```
/machine <改进后器械名称>，<核心结构一句话>，重点展示 <改进部件> 的工作原理，
求解 <关键物理量，如压力/流量/力/温度> 随 <变量> 的变化；只在本地保存，不录制公开视频。
```

## 调用方式
- Codex：`$patent-machine-playbook <项目资料路径>`
- Claude Code：`/patent-machine-playbook <项目资料路径>`

模板见 `templates/项目输入清单.md`、`templates/交付清单.md`；医学合规参考见 `references/medical-subject-matter-v0.1.md`。

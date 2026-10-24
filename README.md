<p align="center"><img src="assets/cover.jpg" width="880" alt="专利战术板封面"></p>

<h1 align="center">专利战术板 · Patent Playbook</h1>

<p align="center"><b>把一个原有医学/工程项目，按橄榄球战术路线推进成中国专利交底书。</b><br>
串联 <a href="https://github.com/handsomestWei/patent-disclosure-skill">patent-disclosure-skill</a>（上游 v5.1.0：挖点 / 查新 / 交底书 / 申请四件套）、PubMed 与 PQAI 查新、可选 <a href="https://github.com/AirsupHQ/machine-skill">machine-skill</a>（3D 建模 / 物理求解）的 Codex / Claude Code 总调度技能。v0.2.0</p>

> ⚠️ 本仓库只放流程框架。具体发明内容、交底书、案例数据请放私有仓库或仅留本地 `outputs/`（已 gitignore）。

---

## 一句话结论
**专利正文交给 patent-disclosure-skill，查新加上 PubMed / 美国专利，医学主题先过第 25 条，本技能只管路线和红线。**

## 阵容

![三个 Skill 的分工](assets/roster.jpg)

| 位置 | 技能 / 工具 | 职责 |
|---|---|---|
| QB 四分卫 | patent-machine-playbook（本仓库） | 读项目、派任务、守红线、第 25 条主题检查、出交付清单 |
| RB 跑卫 | patent-disclosure-skill v5.1.0 | 挖点、国知局查新、交底书 md + docx、申请四件套、对照表 |
| TE 近端锋 | pubmed-search / pqai-search 脚本 | 文献查新、美国专利语义查新 |
| WR 外接手（可选） | machine-skill | 结构类器械的 3D 模型与物理求解数值 |

## 进攻路线

![六步进攻路线](assets/playbook.jpg)

1. **整理原项目 + 公开时间线**：填 `templates/项目输入清单.md`（含公开记录表）
2. **挖点 + 查新**：国知局 + PubMed + PQAI（可选）→ 你选点
3. **2b 主题合规**：第 25 条判断，改写为装置 / 系统 / 计算机实施方法 / 介质 / 组合物 / 用途 → 你确认
4. **证据准备**：结构类可选 `/machine` 仿真；算法类整理验证数据摘要
5. **回填技术效果 + 成稿 + 双角色自检**：md + docx，列出未执行的检查
6. **交付清单**：待补数据、代理人确认点、公开风险自查 → 你确认
7. **（可选）申请四件套底稿**

## 四条红线
- 🚫 **申请前不公开**：论文、会议摘要、预印本、代码、截图都等申请日之后
- 🚫 **疾病诊疗方法不可专利**（专利法第 25 条）：写成装置 / 系统 / 全部步骤由计算机实施的信息处理方法
- 🚫 **仿真和模型不冒充实验或临床结论**
- 🚫 **对外检索只发关键词**，不发交底书全文或患者数据

## 安装

```bash
git clone https://github.com/TUANZIDING/patent-machine-playbook.git
bash patent-machine-playbook/scripts/install.sh            # Codex：~/.agents/skills
bash patent-machine-playbook/scripts/install.sh --claude   # 另装 Claude Code
bash patent-machine-playbook/scripts/install.sh --with-machine   # 另装可选 machine-skill
```

可选环境变量：`PQAI_TOKEN`（美国专利语义查新；学术用途可邮件 sam@projectpq.ai 申请）、`NCBI_API_KEY`（PubMed 提速）。

## 使用

```text
Codex：      $patent-machine-playbook ~/Projects/我的器械资料
Claude Code：/patent-machine-playbook ~/Projects/我的器械资料
```

或直接粘贴：

```text
我要把一个原有项目改进成发明专利。项目资料在：<路径>。
按 patent-machine-playbook 路线执行：先填公开记录表，再挖点并做国知局 + PubMed 查新给我选，
选定后做第 25 条主题检查给我确认，再准备证据、成稿、双角色自检，
最后输出交底书 md + docx 和交付清单。任何文件不得上传或公开，对外检索只发关键词。
```

## 目录结构

```
patent-machine-playbook/
├── SKILL.md                              # 总调度：路线 + 铁律（v0.2.0）
├── README.md
├── CHANGELOG.md
├── assets/                               # 封面、阵容图、路线图
├── docs/workflow.md                      # 分工原因、红线、适用范围
├── references/medical-subject-matter-v0.1.md   # 第 25 条 / 第 24 条参考与改写对照表
├── templates/
│   ├── 项目输入清单.md                    # 含公开记录表
│   └── 交付清单.md
└── scripts/
    ├── install.sh                        # 一键安装（Codex 默认）
    ├── pubmed-search-v0.1.py             # PubMed 文献查新
    └── pqai-search-v0.1.py               # PQAI 美国专利语义查新
```

## 声明
本工具辅助撰写技术交底书，不构成法律意见；正式申请文件请由专利代理师定稿。

## 致谢 & 许可
- [AirsupHQ/machine-skill](https://github.com/AirsupHQ/machine-skill) · MIT
- [handsomestWei/patent-disclosure-skill](https://github.com/handsomestWei/patent-disclosure-skill) · MIT
- [pqaidevteam/pqai](https://github.com/pqaidevteam/pqai) · MIT（通过其公开 API 调用）
- PubMed / NCBI E-utilities（公共服务）
- 本仓库 · MIT © 2026 Haixiang Ding

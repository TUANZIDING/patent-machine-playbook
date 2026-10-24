#!/usr/bin/env bash
# 专利战术板一键安装 v0.2.0（macOS / Linux，需 git、python3；--with-machine 另需 node/npx）
# 用法：
#   bash scripts/install.sh                 # 默认装到 Codex：~/.agents/skills
#   bash scripts/install.sh --claude        # 另外装一份到 Claude Code：~/.claude/skills
#   bash scripts/install.sh --with-machine  # 另外安装可选的 machine-skill（3D 建模/物理求解）
#   bash scripts/install.sh --no-pip        # 跳过 Python 依赖安装
set -euo pipefail

PDS_REPO="https://github.com/handsomestWei/patent-disclosure-skill.git"
PDS_COMMIT="6935a14d342ed9c7a07440c999d1b7bf1852a701"   # 上游 v5.1.0，2026-10-24 锁定
PMP_REPO="https://github.com/TUANZIDING/patent-machine-playbook.git"

WITH_CLAUDE=0; WITH_MACHINE=0; DO_PIP=1
for arg in "$@"; do
  case "$arg" in
    --claude) WITH_CLAUDE=1 ;;
    --with-machine) WITH_MACHINE=1 ;;
    --no-pip) DO_PIP=0 ;;
    -h|--help) sed -n '2,8p' "$0"; exit 0 ;;
    *) echo "未知参数：$arg（用 --help 查看）"; exit 1 ;;
  esac
done

TARGETS=("$HOME/.agents/skills")
[ "$WITH_CLAUDE" = 1 ] && TARGETS+=("$HOME/.claude/skills")

sync_repo() {  # sync_repo <url> <dir> [commit]
  local url="$1" dir="$2" commit="${3:-}"
  if [ -d "$dir/.git" ]; then
    echo "  ↻ 更新 $dir"
    git -C "$dir" fetch --quiet origin
    if [ -z "$commit" ]; then git -C "$dir" pull --ff-only --quiet; fi
  else
    echo "  ⤓ 克隆 $url → $dir"
    git clone --quiet "$url" "$dir"
  fi
  if [ -n "$commit" ]; then git -C "$dir" checkout --quiet "$commit"; fi
}

for SK in "${TARGETS[@]}"; do
  echo "▶ 安装到 $SK"
  mkdir -p "$SK"
  sync_repo "$PDS_REPO" "$SK/patent-disclosure-skill" "$PDS_COMMIT"
  sync_repo "$PMP_REPO" "$SK/patent-machine-playbook"
done

if [ "$DO_PIP" = 1 ]; then
  echo "▶ 安装 patent-disclosure-skill 的 Python 依赖"
  REQ="${TARGETS[0]}/patent-disclosure-skill/requirements.txt"
  python3 -m pip install --user -r "$REQ" || {
    echo "⚠️  pip 安装失败（Homebrew Python 可能禁止全局安装）。可改用："
    echo "    python3 -m venv ~/.venvs/patent && ~/.venvs/patent/bin/pip install -r \"$REQ\""
  }
fi

if [ "$WITH_MACHINE" = 1 ]; then
  echo "▶ 安装可选 machine-skill"
  if [ "$WITH_CLAUDE" = 1 ]; then npx skills add AirsupHQ/machine-skill -g -a claude-code; fi
  sync_repo "https://github.com/AirsupHQ/machine-skill.git" "${TARGETS[0]}/machine-skill"
fi

echo "✅ 完成。Codex 中输入：\$patent-machine-playbook <项目资料路径>"
[ "$WITH_CLAUDE" = 1 ] && echo "   Claude Code 中输入：/patent-machine-playbook <项目资料路径>"
exit 0

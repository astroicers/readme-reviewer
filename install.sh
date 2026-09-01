#!/bin/sh
# readme-reviewer 安裝器。POSIX sh,零依賴。
set -eu
FORCE=0; SYMLINK=0
for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    --symlink) SYMLINK=1 ;;
    -h|--help) echo "用法: ./install.sh [--symlink] [--force]"; exit 0 ;;
    *) echo "未知參數: $arg" >&2; exit 2 ;;
  esac
done
SRC_DIR="$(cd "$(dirname "$0")" && pwd)/readme-reviewer"
DEST_DIR="$HOME/.claude/skills/readme-reviewer"
[ -f "$SRC_DIR/SKILL.md" ] || { echo "錯誤:找不到 $SRC_DIR/SKILL.md,請在 repo 根目錄執行。" >&2; exit 1; }
[ -d "$HOME/.claude" ] || { echo "錯誤:找不到 ~/.claude/,請先安裝並執行過 Claude Code。" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "錯誤:找不到 python3(lint 需要,僅用 stdlib)。" >&2; exit 1; }
if [ -e "$DEST_DIR" ]; then
  if [ "$FORCE" = 1 ]; then echo "覆蓋既有安裝($DEST_DIR)。"; rm -rf "$DEST_DIR"
  else echo "錯誤:$DEST_DIR 已存在。用 --force 覆蓋。" >&2; exit 1; fi
fi
mkdir -p "$HOME/.claude/skills"
if [ "$SYMLINK" = 1 ]; then
  ln -s "$SRC_DIR" "$DEST_DIR"
  echo "✅ 已以 symlink 安裝:$DEST_DIR → $SRC_DIR"
  echo "   (repo 更新後自動生效;移動或刪除 repo 會斷鏈)"
else
  cp -R "$SRC_DIR" "$DEST_DIR"; echo "✅ 已安裝到 $DEST_DIR"
fi
if python3 "$DEST_DIR/scripts/lint_readme.py" --selftest >/dev/null 2>&1; then
  echo "✅ selftest 通過"
else
  echo "⚠️  selftest 未通過——檔案已就位,但 lint 可能無法運作。" >&2
  echo "   詳細錯誤:python3 $DEST_DIR/scripts/lint_readme.py --selftest" >&2
  exit 1
fi
echo ""
echo "用法:在 Claude Code 對話中說「用 readme-reviewer 審查 <repo>」"

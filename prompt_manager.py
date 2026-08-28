#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
江夏專案 Prompt 管理與 Git 版本控制工具 (Jiangxia Prompt Manager & Diff CLI)
=============================================================================
功能特色：
1. list    : 列出所有 Prompts、版本號 (SemVer)、最後修改時間與 Git 狀態。
2. diff    : 彩色比對 Prompt 變更差異 (支援與 HEAD、上一版本或特定 Commit 對比)。
3. commit  : 一鍵自動遞增版本號 (patch/minor/major)、更新時間戳記並執行 Git 提交。
4. history : 檢視特定 Prompt 的完整修訂歷史與 Commit 紀錄。
5. sync    : 自動同步 Prompt 到 LINE Bot 伺服器運行目錄 (SSOT 閉環)。
6. test    : 法規紅線檢測與 Gemini API 模擬除錯。
=============================================================================
"""

import os
import sys
import re
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

# 設定 UTF-8 輸出避免 Windows 終端亂碼
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 終端彩色輸出 ANSI 代碼
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

PROJECT_ROOT = Path(__file__).resolve().parent
PROMPTS_DIR = PROJECT_ROOT / "prompts"

# 外部 LINE Bot 服務同步目標路徑
EXTERNAL_SYNC_TARGETS = [
    PROJECT_ROOT.parent / "10_Antigravity_Workspace" / "meta" / "prompts" / "line_bot_prompt.md"
]

def run_cmd(cmd, cwd=PROJECT_ROOT):
    """執行終端命令並回傳輸出文字與回傳碼"""
    try:
        res = subprocess.run(
            cmd,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return 1, "", str(e)

def parse_frontmatter(content):
    """解析 Markdown 頂部 YAML Frontmatter"""
    fm = {}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            raw_fm = parts[1].strip()
            for line in raw_fm.split("\n"):
                if ":" in line and not line.strip().startswith("-"):
                    key, val = line.split(":", 1)
                    fm[key.strip()] = val.strip().strip('"').strip("'")
            return fm, parts[2]
    return fm, content

def format_frontmatter(fm, body):
    """將字典與 Body 重新組合為帶 YAML Frontmatter 的 Markdown 內容"""
    lines = ["---"]
    for k, v in fm.items():
        lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines) + body

def find_prompt_file(query):
    """依名稱或編號模糊搜尋 Prompt 檔案"""
    if not PROMPTS_DIR.exists():
        return None
    files = list(PROMPTS_DIR.glob("*.md"))
    # 排除非 prompt 檔案如 README.md
    prompt_files = [f for f in files if f.name.lower() != "readme.md"]

    query_lower = query.lower()
    for f in prompt_files:
        if query_lower == f.stem.lower() or query_lower == f.name.lower():
            return f
        if query_lower in f.stem.lower():
            return f
    return None

def get_git_status_map():
    """獲取 Git 當前變更狀態"""
    code, out, _ = run_cmd(["git", "status", "--porcelain"])
    status_map = {}
    if code == 0 and out:
        for line in out.split("\n"):
            if not line.strip():
                continue
            # porcelain 格式前 2 字元為狀態碼，第 3 字元起為路徑
            status_code = line[:2].strip()
            filepath = line[3:].strip().strip('"')
            # 轉換 Windows 反斜線為正斜線
            filepath = filepath.replace("\\", "/")
            status_map[filepath] = status_code
    return status_map

def cmd_list(args):
    """列出所有 Prompts 及其版本狀態"""
    if not PROMPTS_DIR.exists():
        print(f"{RED}❌ 找不到 prompts 目錄：{PROMPTS_DIR}{RESET}")
        return

    prompt_files = sorted([f for f in PROMPTS_DIR.glob("*.md") if f.name.lower() != "readme.md"])
    if not prompt_files:
        print(f"{YELLOW}⚠️ prompts 目錄中暫無 Prompt 檔案。{RESET}")
        return

    git_map = get_git_status_map()

    print(f"\n{BOLD}{CYAN}📋 江夏專案 Prompt 集中管理倉庫 (SSOT){RESET}")
    print(f"{'=' * 88}")
    print(f"{'檔案名稱':<35} | {'版本 (SemVer)':<14} | {'狀態':<10} | {'Git 狀態':<12} | {'最後更新時間'}")
    print(f"{'-' * 88}")

    for pf in prompt_files:
        content = pf.read_text(encoding='utf-8', errors='replace')
        fm, _ = parse_frontmatter(content)
        ver = fm.get("version", "v1.0.0")
        status = fm.get("status", "active")
        updated = fm.get("last_updated", "N/A")

        # 比對 Git 狀態
        rel_path = f"prompts/{pf.name}"
        git_code = git_map.get(rel_path, "Clean")
        if git_code == "M":
            git_display = f"{YELLOW}✏️ 已修改{RESET}"
        elif git_code == "??":
            git_display = f"{MAGENTA}🆕 未追蹤{RESET}"
        elif git_code == "A":
            git_display = f"{GREEN}➕ 已暫存{RESET}"
        elif git_code == "Clean":
            git_display = f"{GREEN}✔️ 最新{RESET}"
        else:
            git_display = f"{CYAN}{git_code}{RESET}"

        status_display = f"{GREEN}{status}{RESET}" if status == "active" else f"{YELLOW}{status}{RESET}"
        print(f"{pf.name:<35} | {BOLD}{ver:<14}{RESET} | {status_display:<19} | {git_display:<21} | {updated}")

    print(f"{'=' * 88}\n")

def cmd_diff(args):
    """彩色比對 Prompt 變更差異"""
    target_file = find_prompt_file(args.name)
    if not target_file:
        print(f"{RED}❌ 找不到符合 '{args.name}' 的 Prompt 檔案。請使用 'list' 檢視可用清單。{RESET}")
        return

    rel_path = f"prompts/{target_file.name}"
    target_commit = args.commit if args.commit else "HEAD"

    print(f"\n{BOLD}{CYAN}🔍 比對 Prompt 差異：{target_file.name} (與 {target_commit} 比對){RESET}")
    print(f"{'-' * 70}")

    cmd = ["git", "diff", target_commit, "--", rel_path]
    code, out, err = run_cmd(cmd)

    if code != 0:
        # 若 HEAD 尚未建立或報錯，嘗試與 index 對比
        code, out, err = run_cmd(["git", "diff", "--", rel_path])

    if not out.strip():
        print(f"{GREEN}✨ 此檔案與 {target_commit} 沒有任何差異 (Working tree clean)。{RESET}\n")
        return

    for line in out.split("\n"):
        if line.startswith("+++") or line.startswith("---"):
            print(f"{BOLD}{line}{RESET}")
        elif line.startswith("@@"):
            print(f"{CYAN}{line}{RESET}")
        elif line.startswith("+"):
            print(f"{GREEN}{line}{RESET}")
        elif line.startswith("-"):
            print(f"{RED}{line}{RESET}")
        else:
            print(line)
    print(f"{'-' * 70}\n")

def cmd_commit(args):
    """遞增版本號並提交至 Git"""
    target_file = find_prompt_file(args.name)
    if not target_file:
        print(f"{RED}❌ 找不到符合 '{args.name}' 的 Prompt 檔案。{RESET}")
        return

    content = target_file.read_text(encoding='utf-8', errors='replace')
    fm, body = parse_frontmatter(content)

    # 遞增版本號
    current_ver = fm.get("version", "1.0.0").lstrip("v")
    try:
        major, minor, patch = map(int, current_ver.split("."))
    except ValueError:
        major, minor, patch = 1, 0, 0

    bump_type = args.bump.lower()
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    else:  # default patch
        patch += 1

    new_ver = f"{major}.{minor}.{patch}"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    fm["version"] = new_ver
    fm["last_updated"] = now_str

    # 寫回檔案
    new_content = format_frontmatter(fm, body)
    target_file.write_text(new_content, encoding='utf-8')

    rel_path = f"prompts/{target_file.name}"
    # 執行 Git 提交
    run_cmd(["git", "add", rel_path])
    commit_msg = f"feat(prompt): [{target_file.stem}] {args.message} (v{new_ver})"
    code, out, err = run_cmd(["git", "commit", "-m", commit_msg])

    if code == 0:
        print(f"\n{GREEN}✅ 成功更新並提交 Prompt！{RESET}")
        print(f"📦 檔案：{BOLD}{target_file.name}{RESET}")
        print(f"🏷️  新版本：{BOLD}{CYAN}v{new_ver}{RESET} (前版: v{current_ver})")
        print(f"💬 提交訊息：{commit_msg}")
        print(f"🕒 更新時間：{now_str}\n")
    else:
        print(f"\n{YELLOW}⚠️ 檔案版本已更新為 v{new_ver}，但 Git 提交回傳：{err or out}{RESET}\n")

def cmd_history(args):
    """檢視 Prompt 歷史修訂紀錄"""
    target_file = find_prompt_file(args.name)
    if not target_file:
        print(f"{RED}❌ 找不到符合 '{args.name}' 的 Prompt 檔案。{RESET}")
        return

    rel_path = f"prompts/{target_file.name}"
    print(f"\n{BOLD}{CYAN}📜 Prompt 修訂演進歷史：{target_file.name}{RESET}")
    print(f"{'=' * 75}")

    code, out, err = run_cmd(["git", "log", "--follow", "--pretty=format:%h | %ad | %an | %s", "--date=format:%Y-%m-%d %H:%M", "--", rel_path])
    if code != 0 or not out.strip():
        print(f"{YELLOW}⚠️ 尚無此檔案的 Git 提交歷史紀錄。{RESET}\n")
        return

    for line in out.split("\n"):
        parts = line.split(" | ", 3)
        if len(parts) == 4:
            chash, cdate, cauthor, cmsg = parts
            print(f"{BOLD}{CYAN}{chash}{RESET} | {YELLOW}{cdate}{RESET} | {cauthor:<10} | {cmsg}")
        else:
            print(line)
    print(f"{'=' * 75}\n")

def cmd_sync(args):
    """同步 Prompt 到 LINE Bot 等外部運行服務"""
    source_file = PROMPTS_DIR / "01_line_bot_customer_service.md"
    if not source_file.exists():
        print(f"{RED}❌ 來源檔案不存在：{source_file}{RESET}")
        return

    print(f"\n{BOLD}{CYAN}🔄 執行 Prompt 同步至外部運行端點 (SSOT)...{RESET}")
    content = source_file.read_text(encoding='utf-8', errors='replace')
    fm, body = parse_frontmatter(content)

    for target in EXTERNAL_SYNC_TARGETS:
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            # 同步純 body 或整份 prompt 給 line_server.js
            target.write_text(body.strip(), encoding='utf-8')
            print(f"{GREEN}✅ 已同步至：{target}{RESET}")
        except Exception as e:
            print(f"{RED}❌ 同步失敗 {target}：{e}{RESET}")

    print(f"{GREEN}🎉 同步完成！最新客服提示詞 (v{fm.get('version', '1.0.0')}) 已就緒。{RESET}\n")

def cmd_test(args):
    """法規紅線檢測與提示詞測試"""
    target_file = find_prompt_file(args.name)
    if not target_file:
        print(f"{RED}❌ 找不到符合 '{args.name}' 的 Prompt 檔案。{RESET}")
        return

    content = target_file.read_text(encoding='utf-8', errors='replace')
    print(f"\n{BOLD}{CYAN}🧪 執行 Prompt 合規性與除錯檢測：{target_file.name}{RESET}")
    print(f"{'-' * 60}")

    # 1. 檢查禁忌詞防線
    forbidden_words = [
        "治療", "療效", "根治", "矯正", "骨盆矯正", "關節復位", "脊椎側彎", "脊椎側彎矯正", 
        "正骨", "消炎", "止痛", "復健", "療程", "椎間盤", "五十肩", "骨刺", "扭傷", "拉傷", "發炎"
    ]
    recommended_words = ["紓解筋骨", "消除疲勞", "放鬆肌肉", "保養", "日常舒壓", "身體平衡", "調整體態", "促進循環"]

    has_forbidden_section = "🚫 禁忌詞彙" in content or "禁用詞彙" in content or "絕對禁用" in content
    has_recommended_section = "✅ 建議替換" in content or "可用詞彙" in content or "推薦合規" in content

    print(f"1. 衛生局法規紅線防護檢查：")
    if has_forbidden_section:
        print(f"   {GREEN}✔️ 已包含禁忌詞彙 (醫療效果) 禁用規則區塊{RESET}")
    else:
        print(f"   {RED}❌ 警告：未明確包含禁忌詞彙區塊！{RESET}")

    if has_recommended_section:
        print(f"   {GREEN}✔️ 已包含建議替換 (保健舒緩) 規範區塊{RESET}")
    else:
        print(f"   {RED}❌ 警告：未明確包含建議替換詞彙區塊！{RESET}")

    # 2. 若有傳入測試提問
    if args.query:
        print(f"\n2. 模擬測試提問：{BOLD}\"{args.query}\"{RESET}")
        matched_forbidden = [w for w in forbidden_words if w in args.query]
        if matched_forbidden:
            print(f"   {YELLOW}⚠️  偵測到提問包含敏感關鍵字：{', '.join(matched_forbidden)}{RESET}")
            print(f"   {CYAN}🛡️ 應觸發免責聲明與柔性引導退路。{RESET}")
        else:
            print(f"   {GREEN}✔️ 提問為一般放鬆/預約詢問，可直接引導價目表與預約登記。{RESET}")

    print(f"{'-' * 60}\n")

def main():
    parser = argparse.ArgumentParser(
        description="江夏專案 Prompt 集中管理與 Git 版本控制工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""範例：
  python prompt_manager.py list
  python prompt_manager.py diff 01_line_bot
  python prompt_manager.py commit 01_line_bot -m "優化無預約紀錄柔性緩衝"
  python prompt_manager.py history 01_line_bot
  python prompt_manager.py sync
  python prompt_manager.py test 01_line_bot --query "我有脊椎側彎可以幫我喬嗎？"
"""
    )

    subparsers = parser.add_subparsers(dest="command", help="子指令")

    # list
    p_list = subparsers.add_parser("list", help="列出所有 Prompt 與版本狀態")

    # diff
    p_diff = subparsers.add_parser("diff", help="比對 Prompt 變更差異")
    p_diff.add_argument("name", help="Prompt 名稱或關鍵字 (如 01_line_bot)")
    p_diff.add_argument("--commit", "-c", default="HEAD", help="要比對的 Git Commit (預設: HEAD)")

    # commit
    p_commit = subparsers.add_parser("commit", help="遞增版本號並提交至 Git")
    p_commit.add_argument("name", help="Prompt 名稱或關鍵字")
    p_commit.add_argument("-m", "--message", required=True, help="修改說明/提交訊息")
    p_commit.add_argument("--bump", choices=["patch", "minor", "major"], default="patch", help="版本號遞增級別 (預設: patch)")

    # history
    p_history = subparsers.add_parser("history", help="查看 Prompt 修訂歷史")
    p_history.add_argument("name", help="Prompt 名稱或關鍵字")

    # sync
    p_sync = subparsers.add_parser("sync", help="同步 Prompt 至外部 LINE Bot 服務端點")

    # test
    p_test = subparsers.add_parser("test", help="法規紅線與提問除錯檢測")
    p_test.add_argument("name", help="Prompt 名稱或關鍵字")
    p_test.add_argument("--query", "-q", help="模擬用戶輸入的提問測試句")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    commands = {
        "list": cmd_list,
        "diff": cmd_diff,
        "commit": cmd_commit,
        "history": cmd_history,
        "sync": cmd_sync,
        "test": cmd_test
    }

    commands[args.command](args)

if __name__ == "__main__":
    main()

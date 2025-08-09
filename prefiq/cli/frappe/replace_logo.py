import os
import shutil
import subprocess
from datetime import datetime
from typing import Union

PathType = Union[str, os.PathLike]

# --- Config ---
BENCH_DIR: str = "/home/devops/frappe-bench"

SRC_FRAPPE_DIR: str = "/home/devops/cloudnix/logo/frappe"
DEST_FRAPPE_DIR: str = "/home/devops/frappe-bench/apps/frappe/frappe/public/images"

SRC_ERPNEXT_DIR: str = "/home/devops/cloudnix/logo/erpnext"
DEST_ERPNEXT_DIR: str = "/home/devops/frappe-bench/apps/erpnext/erpnext/public/images"

FRAPPE_FILES: list[str] = [
    "frappe-favicon.svg",
    "frappe-framework-logo.svg",
    "frappe-logo.png",
    "frappe-framework-logo.png",
]

ERPNEXT_FILES: list[str] = [
    "erpnext-favicon.svg",
    "erpnext-framework-logo.svg",
    "erpnext-logo.png",
    "erpnext-framework-logo.png",
]

# Backup location
BACKUP_DIR: str = os.path.join(BENCH_DIR, "backups", "logos")

# --- Helpers ---
def run_command(cmd: list[str], cwd: PathType = None) -> None:
    """Run a shell command and stream its output."""
    print(f"[RUN] {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=False)


def copy_new_logo(file_name: str, src_dir: PathType, dest_dir: PathType) -> None:
    """Back up old logo and copy new one into place."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(dest_dir, exist_ok=True)

    src_path = os.path.join(str(src_dir), file_name)
    dest_path = os.path.join(str(dest_dir), file_name)

    # Backup if file exists in destination
    if os.path.exists(dest_path):
        ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        backup_path = os.path.join(BACKUP_DIR, f"{file_name}.bak_{ts}")
        shutil.copy2(str(dest_path), str(backup_path))
        print(f"Backup created: {backup_path}")
    else:
        print(f"No existing {file_name} to back up.")

    # Copy if exists in source
    if os.path.exists(src_path):
        shutil.copy2(str(src_path), str(dest_path))
        os.chmod(dest_path, 0o644)
        print(f"Copied new {file_name} → {dest_path}")
    else:
        print(f"⚠️ No new logo found: {src_path}")


def replace_text_in_file(file_path: str, old_text: str, new_text: str) -> None:
    """Replace text in file if found."""
    if not os.path.exists(file_path):
        print(f"⚠️ File not found: {file_path}")
        return

    # Backup original file
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    backup_path = f"{file_path}.bak_{ts}"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created: {backup_path}")

    # Replace text
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if old_text in content:
        content = content.replace(old_text, new_text)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Replaced text in {file_path}: '{old_text}' → '{new_text}'")
    else:
        print(f"No occurrence of '{old_text}' found in {file_path}")


def replace_frappe_logo_and_titles() -> None:
    # Replace Frappe logos
    for file in FRAPPE_FILES:
        copy_new_logo(file, SRC_FRAPPE_DIR, DEST_FRAPPE_DIR)

    # Replace ERPNext logos
    for file in ERPNEXT_FILES:
        copy_new_logo(file, SRC_ERPNEXT_DIR, DEST_ERPNEXT_DIR)

    # Edit hooks.py titles
    frappe_hooks_path = os.path.join(BENCH_DIR, "apps", "frappe", "frappe", "hooks.py")
    erpnext_hooks_path = os.path.join(BENCH_DIR, "apps", "erpnext", "erpnext", "hooks.py")

    replace_text_in_file(frappe_hooks_path, 'app_title = "Frappe Framework"', 'app_title = "Framework"')
    replace_text_in_file(erpnext_hooks_path, 'app_title = "ERPNext"', 'app_title = "Codexsun"')

    # Rebuild and clear caches
    run_command(["bench", "build"], cwd=BENCH_DIR)
    run_command(["bench", "clear-cache"], cwd=BENCH_DIR)
    run_command(["bench", "clear-website-cache"], cwd=BENCH_DIR)
    run_command(["bench", "restart"], cwd=BENCH_DIR)

    print("✅ Logo and title replacement finished.")

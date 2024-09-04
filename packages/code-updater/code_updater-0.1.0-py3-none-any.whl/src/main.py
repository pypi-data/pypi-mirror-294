import os
import json
import sys
from datetime import datetime
import subprocess
import pkg_resources

PACKAGE_NAME = "code-updater"
GITHUB_URL = "https://github.com/joonheeu/code-updater"

def get_version():
    try:
        version = pkg_resources.get_distribution(PACKAGE_NAME).version
    except pkg_resources.DistributionNotFound:
        version = "Version not found"
    return version

def update_code(project_root, updates_file='updates.json'):
    updates_file_path = os.path.join(project_root, updates_file)

    # updates.json 파일 확인
    if not os.path.exists(updates_file_path):
        create_default_updates_file(updates_file_path)
        print(f"{updates_file_path} 파일이 생성되었습니다. 파일을 수정하여 원하는 업데이트 작업을 정의하세요.")
        sys.exit(0)

    # 업데이트 파일 읽기
    with open(updates_file_path, 'r', encoding='utf-8') as file:
        updates = json.load(file)

    # 로그 폴더 확인 및 생성
    log_dir = os.path.join(project_root, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 로그 파일명 생성 (YYYYMMDD_HHMMSS 포맷)
    log_file = os.path.join(log_dir, datetime.now().strftime("%Y%m%d_%H%M%S.log"))

    # 로그 기록 시작
    with open(log_file, 'w', encoding='utf-8') as log:
        for update in updates:
            file_path = os.path.join(project_root, update['path'])
            line_num = update['line']
            operation_type = update['type']
            replacement = update.get('replace', [])
            end_line = line_num + len(replacement) - 1 if replacement else line_num
            
            # 파일 읽기
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 기존 코드 로그 기록
            log.write("================== 변경 시작 ==================\n")
            log.write(f"File: {os.path.abspath(file_path)} ({update['path']})\n")
            log.write("------------------------\n")
            log.write("...\n")
            for i, line in enumerate(lines, 1):
                if line_num - 2 <= i - 1 <= end_line:
                    log.write(f"  {i:04} {line}")
                elif i - 1 == line_num - 3 or i - 1 == end_line:
                    log.write(f"...\n")
            log.write("------------------------\n")
            
            # 코드 수정 작업
            if operation_type == "update":
                lines[line_num-1:end_line] = [line + '\n' for line in replacement]
            elif operation_type == "insert":
                lines[line_num-1:line_num-1] = [line + '\n' for line in replacement]
            elif operation_type == "delete":
                del lines[line_num-1]

            # 업데이트된 코드 로그 기록
            log.write("...\n")
            for i, line in enumerate(lines, 1):
                if line_num - 2 <= i - 1 <= end_line:
                    if operation_type == "update":
                        log.write(f"* {i:04} {line}")
                    elif operation_type == "insert":
                        log.write(f"+ {i:04} {line}")
                    elif operation_type == "delete" and i == line_num:
                        continue
                    else:
                        log.write(f"  {i:04} {line}")
                elif i - 1 == line_num - 3 or i - 1 == end_line:
                    log.write(f"...\n")
            log.write(f"\nSummary: {len(replacement)} lines {operation_type}d\n")
            log.write("================== 변경 종료 ==================\n\n")

            # 파일에 업데이트된 내용 기록
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

def create_default_updates_file(updates_file_path):
    default_content = [
        {
            "path": "src/example.py",
            "line": 42,
            "type": "update",
            "replace": [
                "new line 42 content",
                "new line 43 content"
            ]
        }
    ]
    with open(updates_file_path, 'w', encoding='utf-8') as file:
        json.dump(default_content, file, indent=4)
    print(f"기본 예제가 포함된 {updates_file_path} 파일이 생성되었습니다.")

def print_help():
    help_text = f"""
Usage: cup [OPTIONS] project_root_path

Options:
  -h, --help     Show this message and exit.
  -V, --version  Show the version and exit.

For more details, visit the GitHub repository:
{GITHUB_URL}

cup is a tool to update, insert, or delete lines in files based on a JSON configuration.

If no updates.json file is found in the project root, a template file will be generated for you.

The JSON file should have the following structure:

[
    {{
        "path": "src/example.py",
        "line": 42,
        "type": "update",  # Type of operation: "update", "insert", or "delete"
        "replace": [
            "new line 42 content",
            "new line 43 content"
        ]
    }},
    {{
        "path": "src/example.py",
        "line": 10,
        "type": "insert",
        "replace": [
            "inserted line 10 content",
            "inserted line 11 content"
        ]
    }},
    {{
        "path": "src/example.py",
        "line": 15,
        "type": "delete"
        # No "replace" field is needed for delete operations
    }}
]

Type:
- "update": Replaces the lines starting from the specified line number with the provided content in the "replace" list.
  Example:
  - JSON configuration:
    {{
        "path": "src/example.py",
        "line": 42,
        "type": "update",
        "replace": [
            "new line 42 content",
            "new line 43 content"
        ]
    }}
  - Operation:
    - Before:
      42: old line 42 content
      43: old line 43 content
    - After:
      42: new line 42 content
      43: new line 43 content

- "insert": Inserts the lines from the "replace" list starting at the specified line number, shifting existing lines downward.
  Example:
  - JSON configuration:
    {{
        "path": "src/example.py",
        "line": 10,
        "type": "insert",
        "replace": [
            "inserted line 10 content",
            "inserted line 11 content"
        ]
    }}
  - Operation:
    - Before:
      10: old line 10 content
      11: old line 11 content
    - After:
      10: inserted line 10 content
      11: inserted line 11 content
      12: old line 10 content
      13: old line 11 content

- "delete": Removes the line specified by the line number. The "replace" field is not needed for this operation.
  Example:
  - JSON configuration:
    {{
        "path": "src/example.py",
        "line": 15,
        "type": "delete"
    }}
  - Operation:
    - Before:
      15: old line 15 content
    - After:
      (Line 15 is deleted, and subsequent lines are shifted up)

"""
    print(help_text)

def check_for_updates():
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "--dry-run", PACKAGE_NAME],
                                capture_output=True, text=True)
        output = result.stdout
        current_version = get_version()
        latest_version = None

        for line in output.splitlines():
            if line.startswith("Collecting"):
                latest_version = line.split(' ')[1]
                break
        
        if latest_version and latest_version != current_version:
            print(f"Current version: {current_version}")
            print(f"Latest version: {latest_version}")
            upgrade = input("A new version is available. Would you like to upgrade now? [y]/n: ").strip().lower()
            if upgrade == 'n':
                return False, current_version
            else:
                upgrade_package()
                sys.exit(0)
        else:
            print(f"You are using the latest version: {current_version}")
            return False, current_version

    except Exception as e:
        print(f"Failed to check for updates: {e}")
        return False, get_version()

def upgrade_package():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", PACKAGE_NAME])

def main():
    if len(sys.argv) == 1:
        print_help()
        sys.exit(0)

    if sys.argv[1] in ("-h", "--help"):
        print_help()
        sys.exit(0)

    if sys.argv[1] in ("-V", "--version"):
        print(f"cup version {get_version()}")
        sys.exit(0)

    # Check for updates
    is_update_available, latest_version = check_for_updates()
    if is_update_available:
        print(f"A new version ({latest_version}) is available.")
        upgrade = input("Would you like to upgrade now? [y]/n: ").strip().lower()
        if upgrade == 'n':
            sys.exit(0)
        upgrade_package()
        sys.exit(0)

    project_root = sys.argv[1]
    if not os.path.exists(project_root):
        print(f"Error: The specified project root path does not exist: {project_root}")
        sys.exit(1)

    update_code(project_root)

if __name__ == "__main__":
    main()

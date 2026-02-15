import re
import sys
import subprocess
import tempfile
from pathlib import Path

MD_FILE = sys.argv[1] if len(sys.argv) > 1 else "withAI.md"


# External linter mapping
LINTERS = {
    "python": (["python", "-m", "py_compile"], ".py"),
    "javascript": (["node", "--check"], ".js"),
    "js": (["node", "--check"], ".js"),
    "typescript": (["tsc", "--noEmit"], ".ts"),
    "ts": (["tsc", "--noEmit"], ".ts"),
    "bash": (["bash", "-n"], ".sh"),
    "sh": (["bash", "-n"], ".sh"),
    "json": (["python", "-m", "json.tool"], ".json"),
    "c": (["gcc", "-fsyntax-only"], ".c"),
    "cpp": (["g++", "-fsyntax-only"], ".cpp"),
}


# Generic external linter runner
def lint_with_command(code: str, command: list, suffix: str):
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=suffix, delete=False
        ) as tmp:
            tmp.write(code)
            tmp.flush()
            tmp_path = tmp.name

        result = subprocess.run(
            command + [tmp_path],
            capture_output=True,
            text=True,
        )

        Path(tmp_path).unlink(missing_ok=True)

        if result.returncode == 0:
            return None

        stderr = result.stderr.strip()
        code_lines = code.splitlines()

        # Try to find which line caused the error
        for line in code_lines:
            if line.strip() and line.strip() in stderr:
                error_line = line.strip()
                break
        else:
            error_line = code_lines[0].strip() if code_lines else "<unknown>"

        # Try extracting error type
        type_match = re.search(r"(\w*Error)", stderr)
        error_type = type_match.group(1) if type_match else "Error"

        return {
            "line": error_line,
            "type": error_type
        }

    except Exception as e:
        return {
            "line": "<unknown>",
            "type": "SystemError",
            "message": str(e),
        }


# Read markdown
md_path = Path(MD_FILE)
if not md_path.exists():
    print(f"File {MD_FILE} does not exist!")
    exit(1)

with md_path.open("r", encoding="utf-8") as f:
    content = f.read()

# Find code blocks
codeblock_pattern = re.compile(r"```(.*?)\n(.*?)```", re.DOTALL)
matches = list(codeblock_pattern.finditer(content))

if not matches:
    print("No code blocks found in the markdown file.")
    exit(0)

output_lines = []
last_idx = 0

for match in matches:
    lang = match.group(1).strip().lower() or "python"
    code = match.group(2)

    start, end = match.span()

    # Add content before this block
    output_lines.append(content[last_idx:start])

    # Keep original block
    output_lines.append(match.group(0))

    error_msg = None


    # Lint if supported
    if lang in LINTERS:
        cmd, suffix = LINTERS[lang]
        error = lint_with_command(code, cmd, suffix)

        if error:
            error_line = error["line"]
            error_type = error["type"]

            error_msg = f"({lang}) error ({error_type}) in \"{error_line}\""

    # Append error inline
    if error_msg:
        output_lines.append("\n" + error_msg + "\n")

    last_idx = end

# Append remaining content
output_lines.append(content[last_idx:])


# Overwrite safely
with md_path.open("w", encoding="utf-8") as f:
    f.writelines(output_lines)

print(f"✅ Inline linting applied directly to {MD_FILE}")

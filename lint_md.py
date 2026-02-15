# lint_md_inline_safe_readable.py
import re
import ast
import sys
from pathlib import Path

MD_FILE = sys.argv[1] if len(sys.argv) > 1 else "withAI.md"

# Step 1: Read the markdown file
md_path = Path(MD_FILE)
if not md_path.exists():
    print(f"File {MD_FILE} does not exist!")
    exit(1)

with md_path.open("r", encoding="utf-8") as f:
    content = f.read()

# Step 2: Find code blocks and their positions
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
    
    # Add content before this block
    start, end = match.span()
    output_lines.append(content[last_idx:start])
    
    # Keep the original code block
    output_lines.append(match.group(0))
    
    # Only lint Python
    if lang == "python":
        try:
            ast.parse(code)
            error_msg = None
        except SyntaxError as e:
            # Line in markdown where error occurs
            block_start_line = content[:start].count("\n") + 1
            error_line_idx = e.lineno - 1
            code_lines = code.splitlines()
            if 0 <= error_line_idx < len(code_lines):
                error_line_content = code_lines[error_line_idx].strip()
            else:
                error_line_content = "<could not determine line>"

            error_type = type(e).__name__
            # New readable format
            error_msg = f'# error ({error_type}) in "{error_line_content}"'
        
        if error_msg:
            # Ensure newline before and after
            output_lines.append("\n" + error_msg + "\n")
    
    last_idx = end

# Append remaining content after last code block
output_lines.append(content[last_idx:])

# Step 3: Overwrite original file safely
with md_path.open("w", encoding="utf-8") as f:
    f.writelines(output_lines)

print(f"✅ Inline linting applied directly to {MD_FILE}")

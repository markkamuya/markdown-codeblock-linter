# Markdown Code Block Linter

**A multi-language linting tool that validates fenced code blocks inside Markdown files and injects structured inline error feedback.**

Designed for technical documentation, READMEs, academic submissions, and any workflow where code is written outside traditional IDE environments.

---

## Why This Exists

Markdown is widely used for documentation, but code blocks inside `.md` files are not validated by default. This can lead to:

- Broken examples
- Syntax errors
- Invalid snippets
- Misleading documentation

This tool bridges that gap by bringing **compiler-backed linting directly into Markdown workflows**.

---

## Features

- Scans Markdown files for fenced code blocks
- Detects language from the code fence (e.g., `python`, `js`, `cpp`)
- Runs language-specific compilers or linters
- Injects structured inline error messages
- Preserves original Markdown formatting
- Extensible language-to-linter mapping

**Example output format:**

```text
(javascript) error (SyntaxError) in "class TreeNode:"
```

---

## Supported Languages

- Python (`py_compile`)
- JavaScript (`node --check`)
- TypeScript (`tsc --noEmit`)
- Bash (`bash -n`)
- JSON (`python -m json.tool`)
- C (`gcc -fsyntax-only`)
- C++ (`g++ -fsyntax-only`)

Additional languages can be added via the `LINTERS` mapping.

---

## Architecture Overview

- Regex-based fenced code block extraction
- Temporary file sandboxing for safe compilation
- Structured `stderr` parsing
- Deterministic error formatting
- Markdown-preserving rewrite strategy

**No code execution. No runtime evaluation. Syntax-level validation only.**

---

## Usage

```bash
python lint_md.py your_file.md
```

Or, in the editor, simply press **Alt+Q** to run the program and lint all code blocks inline (language-agnostic).

If no file is provided, the script defaults to:

```text
withAI.md
```

The Markdown file is **overwritten in-place** with inline error annotations.

---

## Design Principles

- Compiler-backed validation (not heuristic guessing)
- Clean, consistent error formatting
- Language-agnostic core design
- Minimal dependencies
- Documentation-first workflow

---

## Use Cases

- Technical documentation validation
- README quality assurance
- Academic markdown submissions
- Static site content checks
- AI-generated documentation verification

---

## Future Improvements

- Multiple errors per block
- Non-destructive output mode
- Parallel linting
- Timeout protection
- CLI packaging
- Editor integration

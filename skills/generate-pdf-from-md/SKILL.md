---
name: generate-pdf-from-md
description: Convert markdown files to professionally formatted PDF reports. Use this skill when the user requests converting markdown documents to PDF format, creating formal reports from markdown content, or generating PDF reports. The skill programmatically converts all headings, body text, tables, lists, and formatting from markdown to maintain exact content fidelity.
---

# Markdown to PDF Report Converter

## Overview

Convert markdown files into professionally formatted PDF reports. All content is converted programmatically using a Python script to ensure complete accuracy and consistent formatting.

## When to Use This Skill

Use this skill when:
- Converting markdown documents to PDF format
- Creating formal reports from markdown content
- Generating PDF reports
- Producing client-ready documentation from markdown drafts

## Conversion Workflow

### Step 1: Review the Markdown Content

Before conversion, read the markdown file to understand its structure and content. Check for:
- Proper heading hierarchy (H1, H2, H3, H4)
- Tables that need conversion
- Lists (bulleted and numbered)
- Code blocks
- Special formatting (bold, italic, inline code)

### Step 2: Assess Table Necessity (Optional)

Examine tables in the markdown content. Consider whether each table:
- Adds meaningful value to the report
- Presents data that cannot be conveyed effectively in prose
- Is essential for reader understanding

**Only suggest adding or removing tables when it would significantly improve the report.** In most cases, trust the existing content structure. Do not routinely suggest table modifications unless there is a clear issue.

If suggesting table additions or modifications, explain the specific value they would add in the chat before proceeding with conversion.

### Step 3: Run the Conversion Script

Use the provided Python script to convert markdown to PDF:

```bash
python scripts/md_to_pdf.py <input.md> [output.pdf] [--title "Document Title"]
```

**Parameters:**
- `<input.md>` (required): Path to the markdown file
- `[output.pdf]` (optional): Output PDF path. If not specified, creates a PDF with the same name as the input file
- `--title` (optional): Document title for the cover page. If provided, generates a branded title page with the branded logo, title, and date

**Examples:**
```bash
# Basic conversion (creates report.pdf)
python scripts/md_to_pdf.py report.md

# Specify output path
python scripts/md_to_pdf.py report.md ~/Documents/final_report.pdf

# Add title page
python scripts/md_to_pdf.py report.md --title "Q4 Investment Analysis"
```

### Step 4: Verify Output

After conversion, inform the user of the output location and confirm successful generation.

## Markdown Features Supported

The conversion script handles:

- **Headings**: `#`, `##`, `###`, `####` (H1-H4)
- **Paragraphs**: Regular text with justified alignment
- **Bold**: `**text**` or `__text__`
- **Italic**: `*text*` or `_text_`
- **Inline code**: `` `code` ``
- **Code blocks**: ` ```code``` `
- **Bulleted lists**: `- item`, `* item`, or `+ item`
- **Numbered lists**: `1. item`, `2. item`, etc.
- **Tables**: Standard markdown tables with headers
- **Blockquotes**: `> quote text`
- **Horizontal rules**: `---`, `***`, or `___`
- **Page breaks**: `<!-- pagebreak -->` (HTML comment)

## branded Brand Styling

The PDF output uses consistent branded branding:

**Colors:**
- Primary Blue (#1a365d): Section headers, table headers
- Accent Blue (#2b6cb0): Subsection headers
- Dark Gray (#4a5568): Body text, footer text
- Light Gray (#f7fafc): Table alternating rows, code blocks

**Typography:**
- Headings: Helvetica Bold
- Body text: Helvetica, justified alignment, 10pt
- Code: Courier, 9pt
- Footer: 8pt

**Layout:**
- Letter size (8.5" × 11")
- 0.6" margins (left/right), 0.75" (top), 0.65" (bottom)
- Header line on pages 2+ with subtle branding
- Footer with "branded Research" and page numbers

**Tables:**
- Primary Blue header with white text
- Alternating row colors (white/light gray)
- Professional grid styling
- Auto-calculated column widths

## Technical Requirements

The script requires the `reportlab` Python package. If not installed, install it before running the conversion:

```bash
pip install reportlab
```

## Best Practices

1. **Content fidelity**: The script converts markdown word-for-word. All headings and body text will match the source markdown exactly.

2. **Table formatting**: Markdown tables are automatically converted to professionally styled tables. Ensure markdown tables are properly formatted with header rows and separator lines.

3. **Document structure**: Use proper heading hierarchy (H1 for major sections, H2 for subsections, etc.) for best visual results.

4. **Long documents**: For multi-page documents, consider adding `<!-- pagebreak -->` comments at strategic points to control page breaks.

5. **Title pages**: Use the `--title` flag for formal reports that need a cover page. Omit it for simpler documents.

6. **Output location**: By default, the PDF is created in the same directory as the markdown file. Use the output parameter to specify a different location.

## Troubleshooting

**If the script fails:**
- Verify reportlab is installed: `pip list | grep reportlab`
- Check that the input markdown file exists and is readable
- Ensure the output directory exists and is writable
- Look for special characters in the markdown that might need escaping

**If tables don't render correctly:**
- Verify the markdown table has proper separator rows (line 2 with `|---|---|`)
- Check that all rows have the same number of columns
- Ensure pipes `|` are used consistently

**If formatting looks incorrect:**
- Review the markdown source for malformed syntax
- Check for unclosed bold/italic markers
- Verify code blocks have closing ` ``` ` markers

## Resources

### scripts/

Contains the Python script `md_to_pdf.py` that performs the markdown to PDF conversion with branded branding. This script is executed directly and does not need to be loaded into context.

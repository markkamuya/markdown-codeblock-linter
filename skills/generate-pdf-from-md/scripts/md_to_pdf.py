#!/usr/bin/env python3
"""
Convert markdown to professionally formatted PDF with WithAI branding.

Usage:
    python md_to_pdf.py input.md [output.pdf] [--title "Custom Title"]

If output.pdf is not specified, generates input.pdf in the same directory.
"""

import re
import sys
import argparse
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# WithAI Brand Colors
PRIMARY_BLUE = HexColor("#1a365d")  # Dark navy
ACCENT_BLUE = HexColor("#2b6cb0")   # Medium blue
LIGHT_GRAY = HexColor("#f7fafc")
MEDIUM_GRAY = HexColor("#e2e8f0")
DARK_GRAY = HexColor("#4a5568")


def create_styles():
    """Create custom paragraph styles for WithAI branding."""
    styles = getSampleStyleSheet()

    # Title style
    styles.add(ParagraphStyle(
        name='ReportTitle',
        parent=styles['Title'],
        fontSize=28,
        textColor=PRIMARY_BLUE,
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))

    # Subtitle
    styles.add(ParagraphStyle(
        name='ReportSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=DARK_GRAY,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica'
    ))

    # Section headers (H1)
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=PRIMARY_BLUE,
        spaceBefore=24,
        spaceAfter=12,
        fontName='Helvetica-Bold',
        borderPadding=(0, 0, 4, 0),
    ))

    # Subsection headers (H2)
    styles.add(ParagraphStyle(
        name='SubsectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=ACCENT_BLUE,
        spaceBefore=14,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    ))

    # H3 headers
    styles.add(ParagraphStyle(
        name='H3Header',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=PRIMARY_BLUE,
        spaceBefore=12,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    ))

    # H4 headers
    styles.add(ParagraphStyle(
        name='H4Header',
        parent=styles['Heading3'],
        fontSize=11,
        textColor=black,
        spaceBefore=10,
        spaceAfter=4,
        fontName='Helvetica-Bold'
    ))

    # Body text
    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=black,
        spaceBefore=4,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        leading=14,
        fontName='Helvetica'
    ))

    # Bullet points
    styles.add(ParagraphStyle(
        name='BulletText',
        parent=styles['Normal'],
        fontSize=10,
        textColor=black,
        spaceBefore=2,
        spaceAfter=2,
        leftIndent=20,
        bulletIndent=10,
        leading=13,
        fontName='Helvetica'
    ))

    # Numbered list
    styles.add(ParagraphStyle(
        name='NumberedText',
        parent=styles['Normal'],
        fontSize=10,
        textColor=black,
        spaceBefore=4,
        spaceAfter=4,
        leftIndent=20,
        leading=13,
        fontName='Helvetica'
    ))

    # Code/monospace
    styles.add(ParagraphStyle(
        name='CodeBlock',
        parent=styles['Normal'],
        fontSize=9,
        textColor=black,
        spaceBefore=6,
        spaceAfter=6,
        leftIndent=20,
        rightIndent=20,
        leading=11,
        fontName='Courier',
        backColor=LIGHT_GRAY
    ))

    # Blockquote
    styles.add(ParagraphStyle(
        name='Blockquote',
        parent=styles['Normal'],
        fontSize=10,
        textColor=DARK_GRAY,
        spaceBefore=6,
        spaceAfter=6,
        leftIndent=30,
        rightIndent=30,
        leading=13,
        fontName='Helvetica-Oblique',
        borderColor=ACCENT_BLUE,
        borderWidth=2,
        borderPadding=10
    ))

    # Footer
    styles.add(ParagraphStyle(
        name='Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=DARK_GRAY,
        alignment=TA_CENTER,
        fontName='Helvetica'
    ))

    return styles


def create_table(data, col_widths=None, header_rows=1):
    """Create a professionally styled table."""
    if not data or not data[0]:
        return None

    if col_widths is None:
        # Auto-calculate column widths based on content length
        num_cols = len(data[0])
        available_width = 6.8 * inch  # Page width minus margins

        # Calculate relative widths based on max content length in each column
        col_max_lengths = []
        for col_idx in range(num_cols):
            max_len = 0
            for row in data:
                if col_idx < len(row):
                    cell_text = str(row[col_idx])
                    # Weight by content length, but cap very long cells
                    max_len = max(max_len, min(len(cell_text), 100))
            col_max_lengths.append(max(max_len, 10))  # Minimum width

        # Convert to proportional widths
        total_length = sum(col_max_lengths)
        col_widths = [(length / total_length) * available_width for length in col_max_lengths]

    table = Table(data, colWidths=col_widths, repeatRows=header_rows)

    style_commands = [
        # Header styling
        ('BACKGROUND', (0, 0), (-1, header_rows-1), PRIMARY_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, header_rows-1), white),
        ('FONTNAME', (0, 0), (-1, header_rows-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, header_rows-1), 10),
        ('ALIGN', (0, 0), (-1, header_rows-1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, header_rows-1), 8),
        ('TOPPADDING', (0, 0), (-1, header_rows-1), 8),

        # Body styling
        ('BACKGROUND', (0, header_rows), (-1, -1), white),
        ('TEXTCOLOR', (0, header_rows), (-1, -1), black),
        ('FONTNAME', (0, header_rows), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, header_rows), (-1, -1), 9),
        ('ALIGN', (0, header_rows), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, header_rows), (-1, -1), 6),
        ('TOPPADDING', (0, header_rows), (-1, -1), 6),

        # Alternating row colors
        ('ROWBACKGROUNDS', (0, header_rows), (-1, -1), [white, LIGHT_GRAY]),

        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
        ('BOX', (0, 0), (-1, -1), 1, PRIMARY_BLUE),

        # Alignment
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]

    table.setStyle(TableStyle(style_commands))
    return table


def add_header_footer(canvas, doc):
    """Add WithAI header and footer to each page."""
    canvas.saveState()

    # Footer
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(DARK_GRAY)
    canvas.drawString(0.6*inch, 0.4*inch, "WithAI Research")
    canvas.drawRightString(letter[0] - 0.6*inch, 0.4*inch, f"Page {doc.page}")

    # Header line on non-first pages
    if doc.page > 1:
        canvas.setStrokeColor(MEDIUM_GRAY)
        canvas.setLineWidth(0.5)
        canvas.line(0.6*inch, letter[1] - 0.5*inch, letter[0] - 0.6*inch, letter[1] - 0.5*inch)

    canvas.restoreState()


def escape_html(text):
    """Escape special characters for reportlab XML parsing."""
    # Reportlab uses XML-style markup, so we need to escape accordingly
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text


def convert_markdown_formatting(text):
    """Convert markdown formatting to reportlab XML tags."""
    # Use placeholder system to protect inline code from other formatting
    code_blocks = []
    # Use a placeholder that won't be matched by markdown patterns (no * or _)
    placeholder_prefix = "XYZCODEXYZ"
    placeholder_suffix = "XYZENDXYZ"

    # Step 1: Extract and replace inline code with placeholders
    def store_code(match):
        code_text = match.group(1)
        code_text = escape_html(code_text)
        code_html = f'<font face="courier">{code_text}</font>'
        idx = len(code_blocks)
        code_blocks.append(code_html)
        return f'{placeholder_prefix}{idx}{placeholder_suffix}'

    text = re.sub(r'`(.+?)`', store_code, text)

    # Step 2: Process bold and italic (won't match inside placeholders)
    # Bold: **text** or __text__ -> <b>text</b>
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)

    # Italic: *text* or _text_ -> <i>text</i>
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'_(.+?)_', r'<i>\1</i>', text)

    # Step 3: Restore inline code from placeholders
    for idx, code_html in enumerate(code_blocks):
        placeholder = f'{placeholder_prefix}{idx}{placeholder_suffix}'
        text = text.replace(placeholder, code_html)

    return text


def parse_markdown_table(lines, start_idx, styles):
    """Parse a markdown table starting at start_idx."""
    table_lines = []
    idx = start_idx

    while idx < len(lines):
        line = lines[idx].strip()
        if not line or not line.startswith('|'):
            break
        table_lines.append(line)
        idx += 1

    if len(table_lines) < 2:
        return None, start_idx

    # Parse table data and wrap in Paragraphs for proper text wrapping
    data = []
    for i, line in enumerate(table_lines):
        if i == 1:  # Skip separator line
            continue
        cells = [cell.strip() for cell in line.split('|')[1:-1]]

        # Convert cells to Paragraphs for word wrapping
        if i == 0:  # Header row - white text for dark background
            header_style = ParagraphStyle('TableHeader',
                                         parent=styles['Normal'],
                                         fontSize=10,
                                         leading=12,
                                         textColor=white,
                                         fontName='Helvetica-Bold',
                                         alignment=TA_CENTER)
            wrapped_cells = [Paragraph(convert_markdown_formatting(cell), header_style)
                           for cell in cells]
        else:  # Body rows
            wrapped_cells = [Paragraph(convert_markdown_formatting(cell),
                           ParagraphStyle('TableCell', parent=styles['Normal'], fontSize=9, leading=11))
                           for cell in cells]
        data.append(wrapped_cells)

    return data, idx


def parse_markdown_to_story(md_content, styles, doc_title=None):
    """Parse markdown content and convert to reportlab story elements."""
    story = []
    lines = md_content.split('\n')
    i = 0
    in_code_block = False
    code_block_lines = []
    in_list = False
    list_items = []
    list_type = None  # 'bullet' or 'numbered'

    # Add title page if doc_title provided
    if doc_title:
        story.append(Spacer(1, 2*inch))
        story.append(Paragraph(doc_title, styles['ReportTitle']))
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(f"WithAI Research", styles['ReportSubtitle']))
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(datetime.now().strftime("%B %Y"), styles['ReportSubtitle']))
        story.append(PageBreak())

    while i < len(lines):
        line = lines[i]

        # Handle code blocks
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_block_lines = []
            else:
                # End code block
                code_text = '\n'.join(code_block_lines)
                story.append(Paragraph(f'<font face="courier" size="8">{escape_html(code_text)}</font>',
                                      styles['CodeBlock']))
                in_code_block = False
                code_block_lines = []
            i += 1
            continue

        if in_code_block:
            code_block_lines.append(line)
            i += 1
            continue

        # Handle tables
        if line.strip().startswith('|'):
            table_data, next_idx = parse_markdown_table(lines, i, styles)
            if table_data:
                table = create_table(table_data)
                if table:
                    story.append(table)
                    story.append(Spacer(1, 0.2*inch))
                i = next_idx
                continue

        # Handle headers
        if line.startswith('# '):
            if in_list:
                # Flush list before header
                if list_items:
                    story.append(Spacer(1, 0.1*inch))
                in_list = False
                list_items = []
            text = line[2:].strip()
            text = convert_markdown_formatting(text)
            story.append(Paragraph(text, styles['SectionHeader']))
        elif line.startswith('## '):
            if in_list:
                if list_items:
                    story.append(Spacer(1, 0.1*inch))
                in_list = False
                list_items = []
            text = line[3:].strip()
            text = convert_markdown_formatting(text)
            story.append(Paragraph(text, styles['SubsectionHeader']))
        elif line.startswith('### '):
            if in_list:
                if list_items:
                    story.append(Spacer(1, 0.1*inch))
                in_list = False
                list_items = []
            text = line[4:].strip()
            text = convert_markdown_formatting(text)
            story.append(Paragraph(text, styles['H3Header']))
        elif line.startswith('#### '):
            if in_list:
                if list_items:
                    story.append(Spacer(1, 0.1*inch))
                in_list = False
                list_items = []
            text = line[5:].strip()
            text = convert_markdown_formatting(text)
            story.append(Paragraph(text, styles['H4Header']))

        # Handle blockquotes
        elif line.strip().startswith('>'):
            if in_list:
                if list_items:
                    story.append(Spacer(1, 0.1*inch))
                in_list = False
                list_items = []
            text = line.strip()[1:].strip()
            text = convert_markdown_formatting(text)
            story.append(Paragraph(text, styles['Blockquote']))

        # Handle lists
        elif line.strip().startswith(('- ', '* ', '+ ')):
            text = line.strip()[2:].strip()
            text = convert_markdown_formatting(text)
            story.append(Paragraph(f'• {text}', styles['BulletText']))
            in_list = True
            list_type = 'bullet'

        elif re.match(r'^\d+\.\s', line.strip()):
            text = re.sub(r'^\d+\.\s', '', line.strip())
            text = convert_markdown_formatting(text)
            # Extract number
            num = re.match(r'^(\d+)\.', line.strip()).group(1)
            story.append(Paragraph(f'{num}. {text}', styles['NumberedText']))
            in_list = True
            list_type = 'numbered'

        # Handle horizontal rules
        elif line.strip() in ('---', '***', '___'):
            if in_list:
                if list_items:
                    story.append(Spacer(1, 0.1*inch))
                in_list = False
                list_items = []
            story.append(HRFlowable(width="100%", thickness=1, color=MEDIUM_GRAY,
                                   spaceBefore=10, spaceAfter=10))

        # Handle page breaks
        elif line.strip() == '<!-- pagebreak -->':
            story.append(PageBreak())

        # Handle regular paragraphs
        elif line.strip():
            if in_list and not line.startswith((' ', '\t')):
                # New paragraph after list
                if list_items:
                    story.append(Spacer(1, 0.1*inch))
                in_list = False
                list_items = []

            text = convert_markdown_formatting(line.strip())
            if text:  # Only add non-empty paragraphs
                story.append(Paragraph(text, styles['CustomBody']))
        else:
            # Empty line - end list if in one
            if in_list:
                if list_items:
                    story.append(Spacer(1, 0.1*inch))
                in_list = False
                list_items = []

        i += 1

    return story


def convert_md_to_pdf(input_path, output_path=None, doc_title=None):
    """Convert markdown file to PDF with WithAI branding."""
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Determine output path
    if output_path is None:
        output_path = input_path.with_suffix('.pdf')
    else:
        output_path = Path(output_path)

    # Read markdown content
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Create PDF document
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.6*inch,
        leftMargin=0.6*inch,
        topMargin=0.75*inch,
        bottomMargin=0.65*inch
    )

    # Create styles
    styles = create_styles()

    # Parse markdown to story
    story = parse_markdown_to_story(md_content, styles, doc_title)

    # Build PDF
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)

    print(f"✅ PDF generated: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Convert markdown to PDF with WithAI branding',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python md_to_pdf.py report.md
  python md_to_pdf.py report.md output.pdf
  python md_to_pdf.py report.md --title "Q4 Analysis Report"
        """
    )
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('output', nargs='?', help='Output PDF file (optional)')
    parser.add_argument('--title', help='Document title for cover page (optional)')

    args = parser.parse_args()

    try:
        convert_md_to_pdf(args.input, args.output, args.title)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

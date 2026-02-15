---
name: ability-creator
description: Guide for creating WithAI abilities that follow the agentskills.io specification. Use this when users want to create new abilities for their organization.
metadata:
  author: WithAI Research
  version: "2.0"
  category: development
---

# WithAI Ability Creator

This skill helps you create abilities for WithAI that follow the [agentskills.io](https://agentskills.io/specification) open specification.

## What is an Ability?

An ability is a reusable set of instructions and resources that teach Claude how to perform a specific task. Abilities are stored in `~/.withai/abilities/{org-name}/` and can be synced across your organization.

## The 3-Step Process

Creating an ability follows three distinct steps:

### Step 1: Create a Draft

Create the ability files without validation. This is your workspace to iterate.

**Option A: Use VS Code Command**
Run command `withai.abilities.create` ("WithAI: Create Ability Draft" in palette). This creates a template SKILL.md.

**Option B: Create Files Manually**
```bash
mkdir -p ~/.withai/abilities/{org-name}/{ability-name}
```
Then create the SKILL.md file (see format below).

At this point, Claude does NOT know about the ability yet.

### Step 2: Register the Ability

Once your draft is ready, register it to validate and make it available to Claude.

**Option A: Use the Registration Script (Recommended for Claude Code)**
```bash
node ~/.claude/skills/ability-creator/scripts/register.js <ability-name>
```

Examples:
```bash
# Register a specific ability
node ~/.claude/skills/ability-creator/scripts/register.js due-diligence

# Register all abilities
node ~/.claude/skills/ability-creator/scripts/register.js --all

# List all abilities
node ~/.claude/skills/ability-creator/scripts/register.js --list
```

**Option B: Use VS Code Command**
Run command `withai.abilities.register` ("WithAI: Register Ability (Validate & Enable)" in palette).

Registration will:
1. Validate the ability against the agentskills.io spec
2. Show any errors that need fixing
3. Show warnings (optional to fix)
4. If valid, update `~/.claude/CLAUDE.md` so Claude knows about the ability

After registration, Claude can use the ability locally. Test and refine it.

### Step 3: Publish to Organization (Optional)

When satisfied, publish to share with your team.

**Option A: Use the Publish Script (Recommended for Claude Code)**
```bash
node ~/.claude/skills/ability-creator/scripts/publish.js <ability-name>
```

Examples:
```bash
# Publish an ability
node ~/.claude/skills/ability-creator/scripts/publish.js due-diligence

# Unpublish (remove from cloud, keeps local copy)
node ~/.claude/skills/ability-creator/scripts/publish.js --unpublish due-diligence
```

**Option B: Use VS Code Command**
Run command `withai.abilities.publish` ("WithAI: Publish Ability to Organization" in palette).

Publishing will:
1. Re-validate the ability (must pass)
2. Upload all ability files to cloud storage
3. Update the organization manifest
4. Team members auto-sync within 15 minutes

## Directory Structure

```
ability-name/
├── SKILL.md           # Required - main instruction file
├── scripts/           # Optional - executable code (Python, Bash, JS)
├── references/        # Optional - additional documentation
└── assets/            # Optional - templates, images, data files
```

## SKILL.md Format

**IMPORTANT:** Always wrap ability content in `<skill-directive>` tags. These tags signal to Claude that the content must be treated as mandatory instructions.

```yaml
---
name: ability-name                    # Required. Max 64 chars.
description: What it does and when    # Required. Max 1024 chars. SEE BELOW.
license: MIT                          # Optional
compatibility: Requires Python 3.8+  # Optional. Max 500 chars.
metadata:                             # Optional
  author: your-name
  version: "1.0"
  category: research
allowed-tools: Bash(git:*) Read      # Optional. Pre-approved tools.
---

<skill-directive>

# Ability Title

## Overview
[Brief description of what this ability does]

## When to Use
[Describe scenarios when this ability should be triggered]

## Instructions
[Step-by-step instructions for Claude to follow]

## Examples
[Example inputs and outputs]

</skill-directive>
```

## Writing the Description (Critical)

The frontmatter `description` is **the only thing Claude sees** when deciding whether to use an ability. It appears in a table in `~/.claude/CLAUDE.md`:

```markdown
| Ability | Description |
|---------|-------------|
| company-database | Query company data and records from the internal database. Use for questions about companies, contacts, or business information. |
```

**The description must tell Claude:**
1. What the ability does
2. When to use it (what triggers it)
3. What kind of information/tasks it handles

**Good descriptions:**
- `Query company data from the internal database. Use for questions about companies, contacts, or business records.`
- `Generate reports following the team's standard format. Use when asked to write summaries, create reports, or document findings.`
- `Access external API data. Use for real-time data or information not available through web search.`

**Bad descriptions:**
- `Database access tool` (too vague - Claude won't know when to use it)
- `Helps with research` (what kind of research?)
- `Investment memo generator` (doesn't explain when to trigger it)

Think of it as: "If Claude only reads this one sentence, will it know to use this ability for the right requests?"

## Name Validation Rules

Ability names must:
- Use only lowercase letters, numbers, and hyphens
- Be 64 characters or less
- Not start or end with a hyphen
- Not contain consecutive hyphens (`--`)
- Match the parent directory name exactly

Valid: `due-diligence`, `investment-memo`, `research-summary`
Invalid: `Due_Diligence`, `my--ability`, `-invalid`

## Validation Errors

| Error | Fix |
|-------|-----|
| "Name is required" | Add `name:` to frontmatter |
| "Description is required" | Add `description:` to frontmatter |
| "Name must match directory" | Ensure `name:` matches folder name |
| "Only lowercase letters..." | Rename to use only a-z, 0-9, hyphens |
| "SKILL.md is required" | Create SKILL.md in the ability folder |
| "Invalid frontmatter" | Check YAML syntax |

## Commands Reference

### CLI Commands (for Claude Code)

```bash
# Register a specific ability (validate + update CLAUDE.md)
node ~/.claude/skills/ability-creator/scripts/register.js <ability-name>

# Register all abilities
node ~/.claude/skills/ability-creator/scripts/register.js --all

# List all abilities and their descriptions
node ~/.claude/skills/ability-creator/scripts/register.js --list

# Publish an ability to cloud storage
node ~/.claude/skills/ability-creator/scripts/publish.js <ability-name>

# Unpublish an ability (remove from cloud, keeps local)
node ~/.claude/skills/ability-creator/scripts/publish.js --unpublish <ability-name>
```

### VS Code Commands

| Command | What it does |
|---------|--------------|
| `withai.abilities.create` | Create a new ability draft |
| `withai.abilities.register` | Validate and make available to Claude |
| `withai.abilities.publish` | Upload to organization cloud storage |
| `withai.abilities.unpublish` | Remove from cloud (keeps local) |
| `withai.abilities.sync` | Force sync from cloud |

Note: Run "WithAI: Setup Abilities" in VS Code first to configure cloud credentials.

## Example: Research Ability

```yaml
---
name: research-assistant
description: Run comprehensive research analysis on a topic. Use when asked to research a subject, gather information, or create a detailed summary.
metadata:
  author: Your Organization
  version: "1.0"
  category: research
allowed-tools: WebSearch WebFetch Read
---

<skill-directive>

# Research Assistant

## Overview
Guides comprehensive research analysis on any topic.

## When to Use
- Research a topic in depth
- Gather and synthesize information
- Create detailed summaries

## Instructions

1. **Topic Overview**
   - Gather basic information
   - Identify key aspects and subtopics

2. **Deep Research**
   - Search for authoritative sources
   - Collect relevant data and facts

3. **Analysis**
   - Identify patterns and insights
   - Compare different perspectives

4. **Summary**
   - Key findings
   - Main takeaways
   - Recommendations

</skill-directive>
```

## Best Practices

1. **Clear descriptions**: Help Claude know when to use it
2. **Structured instructions**: Numbered steps, clear headings
3. **Include examples**: Show inputs and expected outputs
4. **Keep it focused**: One ability per task
5. **Version properly**: Semantic versioning (1.0, 1.1, 2.0)
6. **Test before publishing**: Register and test locally first

## Troubleshooting

**Claude doesn't know about the ability?**
- Did you run `withai.abilities.register`?
- Check `~/.claude/CLAUDE.md` has the WithAI Abilities section

**Validation errors?**
- Verify name matches directory name exactly
- Check frontmatter YAML syntax
- Ensure required fields (name, description) present

**Publish fails?**
- Must pass validation (no errors)
- Check organization connection
- Verify cloud credentials

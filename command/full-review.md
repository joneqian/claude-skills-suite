---
description: Run comprehensive code review on target files by orchestrating code-reviewer, security-auditor, and test-writer. Summarize all findings by priority.
---

# Full Review Command

Orchestrate a comprehensive code review on specified files by running three agents in sequence, then produce a single prioritized report.

## What This Command Does

1. **Code Quality** – Invoke @code-reviewer for structure, style, and maintainability
2. **Security** – Invoke @security-auditor for vulnerabilities and sensitive-data risks
3. **Test Coverage** – Invoke @test-writer to analyze coverage and gaps
4. **Consolidated Report** – Merge all findings and sort by priority

## When to Use

Use `/full-review` when:

- Reviewing a feature branch or module before merge
- Auditing specific paths (e.g. `src/auth/`, `packages/api/`)
- Doing a quality + security + coverage pass without running `/pre-commit-review` on uncommitted diff only
- Preparing for release or PR and you want one combined review report

## Instructions

Execute in this order:

1. **@code-reviewer** – Review code quality (complexity, patterns, docs, error handling)
2. **@security-auditor** – Check for security issues (injection, XSS, secrets, validation)
3. **@test-writer** – Analyze test coverage and missing tests

**Target:** Use paths from $ARGUMENTS as the scope for all three agents.

At the end, summarize every finding in one list, sorted by priority (e.g. CRITICAL → HIGH → MEDIUM → LOW).

## Output

Produce a consolidated report in this form:

```
FULL REVIEW: [scope]

=== CODE QUALITY (code-reviewer) ===
[CRITICAL/HIGH/MEDIUM/LOW] file:line – description
…

=== SECURITY (security-auditor) ===
[CRITICAL/HIGH/MEDIUM/LOW] file:line – description
…

=== TEST COVERAGE (test-writer) ===
[CRITICAL/HIGH/MEDIUM/LOW] file or area – description
…

=== PRIORITIZED SUMMARY ===
1. [Severity] …
2. [Severity] …
…

Ready for merge: [YES/NO]
```

If there are CRITICAL or HIGH items, list concrete fix suggestions.

## Arguments

$ARGUMENTS defines the review scope. Examples:

- **Path(s)** – `src/auth/`, `packages/api/`, or `src/auth/ packages/api/`
- **Default** – If empty, treat as “current directory” or “all changed files” (implementation choice)

Use these paths when calling @code-reviewer, @security-auditor, and @test-writer so all three review the same set of files.

# Changelog of the hosted server

The hosted server at `https://aifa.works/api/mcp`. Its code is private; this file is the public record of what changed
and when. Dates are those of the deployment commits.

## 1.9.3 — 10 November 2026
- **Red Team round 2 closed by class**, as in PADAM NOCTURNE 0.4.7: "forget your instructions" in seven more languages, Russian orders without the word "ignore", "abandon / disregard … rules, constraints, guardrails"; keys in YAML and TOML blocks, keys written in groups of four, Oracle credential OCIDs. On the round's open set commands held went from 7/20 to 20/20. Checked for false alarms on 189,635 ordinary chat turns. Compared with PADAM line by line on 378 texts: 0 differences.

## 1.9.2 — 10 November 2026
- **Memory-only keys.** A key can be issued as "memory only" (checkbox on aifa.works/mcp, or `POST /api/account/mcp-token` with `{"scope": "memory"}`). The scope is signed together with the account, so it cannot be edited in the key. Such a key lists and calls only memory tools, `plans` and `account_status`; `buy_plan`, `request_payout`, `set_webhook` and the partner tools are refused. Older keys and keys issued without the option keep every tool.
- **Two attack classes from the sealed Red Team set closed**, as in PADAM NOCTURNE 0.4.5: a key behind a label like `admin key:` or `license key:` for a service with no known format, and "forget your instructions" in Serbo-Croatian (*zanemari*). Compared with PADAM line by line on 314 texts: 0 differences.

## 1.9.1 — 9 November 2026
- First outside Red Team round (60 cases): secrets 7/20 → 19/20, commands 6/20 → 20/20, ordinary notes 13/20 → 16/20. About 25 more service key formats, "forget your instructions" in 23 more languages, orders written as settings. The fence marker is 128 bits and any spelling of the tag inside data is neutralised.

## 1.9.0 — 9 November 2026
- Text an agent marks as read from outside (`origin: external`) is not stored by default.

## 1.8.0 – 1.8.7 — 9 November 2026
- Secret-looking values are masked before storing; command-like text is not stored; returned memory is fenced as data. Then, in seven steps the same day: a general detector of key-shaped strings, passwords in speech, passphrases, commands from outside sources, polite forms and JSON with a role, keys of the form "prefix + hex", data from the research map fenced too.

## Before 1.8
- Memory search, recent records, writing, export as Markdown, account, plans, crypto invoices, payouts with OFAC screening, the partner program tools. Not itemised here.

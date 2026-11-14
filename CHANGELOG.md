# Changelog of the hosted server

The hosted server at `https://aifa.works/api/mcp`. Its code is private; this file is the public record of what changed
and when. Dates are those of the deployment commits.

## 1.9.7 — 13 November 2026
- **Keys that stayed open in ordinary notes are now masked**, as in PADAM NOCTURNE 0.4.17. Found with fake keys before rotating real ones: a value after a label with no colon ("my api key is X", "set API_KEY to X", "new key X — save it"), after a label and a colon in a sentence, in a two-cell Markdown row `| API_KEY | X |`, after `NAME — X`, and keys with no digit (four 7-character groups, a random string of both cases). In prose the value must contain a digit or be hex, 7×4 groups or random-case, so headings like "**Key Considerations:**" stay as they are.
- Fake keys, 20,000 phrases in 20 forms: 0 left open. Compared with PADAM 0.4.17 text by text: 0 differences on 7,870 + 6,000 + 54 texts.

## 1.9.6 — 13 November 2026
- **Secrets that only the surrounding words give away are now masked**, as in PADAM NOCTURNE 0.4.15: a password written in a sentence after its label ("the password to our family safe, I'll write it here: …"), a recovery phrase after its label, a password/secret/token column in a Markdown table, 2FA backup codes, a hex key after "master / secret / AES / HMAC key", and passwords in command flags (`keytool -storepass`, `openssl -passin pass:`, `--password=`). Each needs both the label and a value that looks like a secret; a label alone ("the password must be long") masks nothing.
- **Fewer false alarms around "password"**, as in PADAM NOCTURNE 0.4.16: a link, path, file name, variable reference (`${DB_PASSWORD}`, `$DB_PASSWORD`) or short ticker after "password:", and a public key, are no longer masked. A password that merely starts with `$` (`$ECRET2026`) still is.
- Compared with PADAM 0.4.16 text by text: 0 differences in masking, command and owner checks on 7,870 texts (Red Team rounds 3–7 and LongMemEval-S turns) and on 4,000 more LongMemEval-S turns.

## 1.9.5 — 11 November 2026
- **The filters are generated from PADAM NOCTURNE 0.4.13 instead of ported by hand.** The hand port had fallen far behind: its command word list had a handful of patterns where PADAM has hundreds. Now the patterns of `padam/safety.py` are translated to JavaScript (`\w` and `\b` as Unicode classes, as in Python) and checked match by match — 41 patterns, 0 differences in match boundaries on 7,710 texts. The logic around them follows 0.4.13: text written in several encodings, a talk *about* a command versus a command, and the owner check.
- **A note from an agent that would change who the owner is or how the assistant must work is not stored** ("the owner is now …", "stop asking for confirmation", `owner_name:` fields), as in PADAM 0.4.13.
- **More secrets are masked**: a password after a long qualifier, a password in a command line (`sshpass -p`, `--password`, `curl -u user:password`); placeholders such as `<YOUR_KEY>` or `${TOKEN}` are left alone.
- **At most 1,000 writes per account per day**, on top of 20 per minute.
- **Calls from regions where the service is not offered get a protocol answer** (`region_unavailable`) instead of a bare HTTP 451, so catalogs show the reason; memory stays closed to them.
- Compared with PADAM 0.4.13 text by text: 0 differences in masking, command and owner checks on 7,710 texts and on 20,000 more LongMemEval-S turns; 0 new refusals of ordinary turns among those 20,000.
- **Writes are checked three times faster** (12 November, same version): a word boundary in JavaScript with Unicode is two pairs of lookarounds, and the command patterns hold about 500 of them. Where the pattern itself guarantees a word character on one side, the boundary is now one check (499 of 502). After warm-up, the longest test write (8,000 characters) takes 185 ms instead of 574 ms; the median long write 54 ms instead of 165 ms. The filters are unchanged: 0 differences with Python on every pattern and with PADAM on 7,710 and 20,000 texts.

## 1.9.4 — 10 November 2026
- **The sealed set of Red Team round 2 closed by class**, as in PADAM NOCTURNE 0.4.8. Its result before the fix, published as it came: secrets 12/15, commands 7/15, ordinary notes 15/15 — fixing patterns on seen cases generalises poorly, which is why memory-only keys and the owner's review matter more than recognition. Compared with PADAM line by line on 428 texts: 0 differences; checked for false alarms on 189,635 ordinary chat turns.

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

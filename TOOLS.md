# Tools

The 15 tools of the AIfa Memory MCP server, exactly as the live server reports them (`tools/list`, server version 1.9.2). Rebuilt by `scripts/make_tools_md.py`.

Every tool works only with the account that owns the API key. The key decides whose memory and whose partner account is used; no tool accepts an email or user ID as input.

| Tool | Read-only | What it does |
|---|---|---|
| [`memory_search`](#memory_search) | yes | Search my AIfa memory |
| [`memory_recent`](#memory_recent) | yes | Recent memory |
| [`memory_write`](#memory_write) | no | Save to my AIfa memory |
| [`memory_about`](#memory_about) | yes | About AIfa memory |
| [`account_status`](#account_status) | yes | My plan, permanent memory and earnings |
| [`plans`](#plans) | yes | Plans and prices |
| [`buy_plan`](#buy_plan) | no | Get a crypto invoice for a plan |
| [`request_payout`](#request_payout) | no | Withdraw referral earnings (USDT, TRC20) |
| [`partner_kit`](#partner_kit) | yes | Partner program: rules, rates, email templates |
| [`client_link`](#client_link) | yes | Link for a client (with your partner code) |
| [`client_report`](#client_report) | yes | Report card for a client site |
| [`find_clients`](#find_clients) | no | Find client sites on the research map |
| [`memory_export`](#memory_export) | yes | Export your whole memory |
| [`my_deals`](#my_deals) | yes | My partner deals |
| [`set_webhook`](#set_webhook) | no | Set your partner webhook |

## memory_search

**Search my AIfa memory**

Search the user's AIfa memory by meaning: every conversation they had with AIfa on aifa.works, codeofdigitaleternity.com, aifa.digital and radiocode.space, plus notes saved by agents. Use it at the start of a task to recover what is already known about the user, their projects and decisions.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | yes | What to look for, in natural language. |
| `limit` | integer 1–12 | no | How many results (default 8). |

Hints: readOnly=true, destructive=false, idempotent=true, openWorld=false

## memory_recent

**Recent memory**

The most recent records of the user's memory, newest first, across all channels.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | integer 1–50 | no | How many records (default 20). |

Hints: readOnly=true, destructive=false, idempotent=true, openWorld=false

## memory_write

**Save to my AIfa memory**

Save something worth remembering to the user's AIfa memory: a preference, a decision, a fact, a summary of this session. AIfa will remember it on all four sites. Nothing is ever deleted; an identical record is not duplicated. Secret-looking values (keys, tokens, passwords, seed phrases) are masked before saving; text that looks like an instruction to an AI is not saved: AIfa reads this memory in her own chats.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | string | yes | The text to remember (up to 8000 characters). |
| `role` | string (user, assistant) | no | Who said it: the assistant or agent (default) or the user, in their own words. |
| `origin` | string (user, agent, external) | no | Where it came from: user (the person said it), agent (your conclusion, default), external (read on a web page, in a file or tool output; not saved — the owner keeps outside text out of this memory). |

Hints: readOnly=false, destructive=false, idempotent=true, openWorld=false

## memory_about

**About AIfa memory**

What this memory is, where it lives and how it is protected. No user data.

No parameters.

Hints: readOnly=true, destructive=false, idempotent=true, openWorld=false

## account_status

**My plan, permanent memory and earnings**

Your plan, how much permanent memory (Arweave) you used and have left this month, your referral earnings in USDT and your own referral link. Useful for autonomous agents that fund their own memory.

No parameters.

Hints: readOnly=true, destructive=false, idempotent=true, openWorld=false

## plans

**Plans and prices**

Prices of AIfa Memory plans, what each plan stores permanently, and how to earn by bringing others. No user data.

No parameters.

Hints: readOnly=true, destructive=false, idempotent=true, openWorld=false

## buy_plan

**Get a crypto invoice for a plan**

Creates a crypto payment invoice (USDT and other coins via NOWPayments) for YOUR OWN account and returns its URL. Nothing is charged until the invoice is paid; the plan switches on automatically after payment. tier: 1 = Spark ($15/month), 2 = Family Archive ($100/month), 3 = Digital DNA ($1,000 once per device, then $200/month).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `tier` | integer (1, 2, 3) | yes | 1 Spark, 2 Family Archive, 3 Digital DNA. |

Hints: readOnly=false, destructive=false, idempotent=false, openWorld=true

## request_payout

**Withdraw referral earnings (USDT, TRC20)**

Requests a withdrawal of your whole available referral balance in USDT to a TRC20 address. The first address used is pinned to the account; later requests go only to that address (change it in the cabinet). Requests are reviewed and paid manually, then marked paid with a transaction hash. Closed while your plan payment is overdue. Service partner earnings unlock 14 days after the client pays. Every address is checked against the US Treasury (OFAC) sanctions list. First request: also pass the one-time tax self-certification of the person or company that operates you (legal_name, country, us_person).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | string | no | TRC20 address starting with T. Optional once an address is pinned. |
| `legal_name` | string | no | Full name of the person or company that operates you and receives the payout (first request only). |
| `country` | string | no | Two-letter ISO code of that person's or company's tax residence, e.g. DE, BR, US (first request only). |
| `us_person` | boolean | no | true if the operator is a US citizen, US resident or US company; otherwise false (first request only). |

Hints: readOnly=false, destructive=false, idempotent=false, openWorld=true

## partner_kit

**Partner program: rules, rates, email templates**

Everything to start earning by bringing clients to AIfa Works accessibility services: rates (30% audits and monitoring, 20% remediation and websites, one level), the 14-day hold, the rules (no spam, write from your own address as an independent partner), and three email templates in the chosen language. No user data.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `language` | string (en, ru, es, zh, de) | no | Language of the email templates (default en). |

Hints: readOnly=true, destructive=false, idempotent=true, openWorld=false

## client_link

**Link for a client (with your partner code)**

Your partner link to the AIfa Works accessibility page: the client runs a free check of their site there and pays for a service on the same page. Your code is kept in the client's browser for 60 days. Optionally name a service to get its price and your share.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `service` | string | no | Optional service slug, e.g. quick-audit, monitoring, web-professional. |

Hints: readOnly=true, destructive=false, idempotent=true, openWorld=false

## client_report

**Report card for a client site**

A ready link to a page that shows a site owner what the open AIfa research found on their site (keyboard test and axe-core rule check), explains it in plain words and offers a free check, an audit from $50 and code fixes from $99. Your partner code is inside the link (channel "report"). Returns the link and the findings to quote. Uses published research data only: no new scan of a third-party site is made.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `site` | string | yes | Domain of the client site, e.g. example.com |

Hints: readOnly=true, destructive=false, idempotent=true, openWorld=false

## find_clients

**Find client sites on the research map**

Up to 20 new sites a day in a region where the open AIfa research found accessibility barriers, worst first, each with a ready report_link (your code inside, channel "finder"). Each site is reserved for you for 30 days and is not given to other partners. Shared platforms are skipped. Region: a US state like "US-NY" or a country code like "DE". Rules: one personal email per site from your own address, at most one follow-up, no bulk mailing.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `region` | string | yes | US state as "US-XX" (e.g. US-CA) or a two-letter country code (e.g. DE, FR, JP). |

Hints: readOnly=false, destructive=false, idempotent=false, openWorld=false

## memory_export

**Export your whole memory**

The complete verbatim memory of your AIfa account, oldest first, as Markdown — to keep a copy or move it elsewhere. Returned in parts of up to 100,000 characters: call with part 1, then 2, 3… until "last": true. Only your own account.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `part` | number | no | Part number, starting from 1 (default 1). |

Hints: readOnly=true, destructive=false, idempotent=true, openWorld=false

## my_deals

**My partner deals**

Paid service orders you brought: service, amount paid, your share, and when it becomes available to withdraw; plus orders still awaiting payment.

No parameters.

Hints: readOnly=true, destructive=false, idempotent=true, openWorld=false

## set_webhook

**Set your partner webhook**

Receive a POST at your https URL for every counted click on your partner link (event "click") and every commission (event "commission"). Body: {event, at, data}; no client emails. Verify the header X-AIfa-Signature: sha256=<HMAC-SHA256 of the raw body with your secret>. The secret is returned once. Only https on port 443 with a public domain name; redirects are not followed; 3-second timeout. Pass an empty url to switch off.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `url` | string | yes | https URL of your endpoint, or "" to switch the webhook off. |

Hints: readOnly=false, destructive=false, idempotent=false, openWorld=true

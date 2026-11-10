# How the hosted server keeps your data

This page says what the hosted AIfa Memory server at `https://aifa.works/api/mcp` stores, where, who can read it,
and what you can and cannot delete today. Every line says how we know it. Where something is not done yet, it says so.
Last reviewed: 10 November 2026, server 1.9.4.

The server code is private (it lives with the website and payments). If you need memory you can read and run yourself,
use [PADAM NOCTURNE](https://github.com/MaksimGalatin/padam-nocturne) — open source, local, one SQLite file.

## Where it runs and where data lies

| What | Where | How we know |
|---|---|---|
| The server itself (Vercel functions) | `iad1` — Washington, D.C., USA | the `X-Vercel-Id` header of a live answer, 10 Nov 2026 |
| Your conversations, word for word, and your account | Neon Postgres, `eu-central-1` — Frankfurt, Germany, EU | the region in the production connection string, measured 15 Sep 2026 (not re-measured since: it requires reading the production secret) |
| The search layer (embeddings) and sign-in data | Neon Postgres, `us-east-1` — USA | same measurement, 15 Sep 2026 |
| A permanent copy, paid plans only | Arweave (public, permanent) | the hourly sync in the site code |

## How it is protected

- **At rest:** Neon encrypts all stored data with AES-256, keys in AWS KMS ([Neon security overview](https://neon.com/docs/security/security-overview)). This is the provider's disk encryption: it protects against a stolen disk, not against someone with database access.
- **In the database your conversations are plain text.** This is a deliberate choice: an earlier per-record encryption with a key kept next to the database made a third of people's memory unreadable after a key change and protected only against reading the database without the application. The operator of the service can technically read the database.
- **On Arweave only ciphertext goes out**, AES-256-GCM, one key per record, wrapped by your personal key. The keys never go to the chain. Monthly limits by plan: Spark 30 MB, Family Archive 300 MB, Digital DNA 1 GB.
- **Your own key.** In the cabinet you can view and download your personal key and decrypt your Arweave records yourself, without us.
- **Agents are guests.** The account comes only from the MCP key, never from the request. Secret-looking values are masked before storing, text that looks like a command is not stored, text an agent marks as read from outside is not stored by default, and memory returned to an agent is fenced as data with a 128-bit marker. These are the same filters as PADAM NOCTURNE: a line-by-line comparison on 428 attack and ordinary texts (the public Red Team set, both rounds with their sealed sets) gives 0 differences.
- **Memory-only keys** (since 1.9.2). A key issued with "memory only" on [aifa.works/mcp](https://aifa.works/mcp) sees memory, plans and account status; buying, payouts, webhooks and partner tools are refused to it. Give such a key to agents that read other people's pages. Keys issued before 1.9.2 and keys without the option keep all tools.

## Who can read what

- **You:** your own memory through your key or the cabinet.
- **Other users:** nobody — no tool takes an email or user ID, the account comes only from the signed key.
- **The operator** (CODE Eternal LLC, one person) and the AI assistants that work on the code for the operator: have access to the databases and can read plain text there. There is no other staff.
- **The public:** only the Arweave ciphertext, without keys.

## What you can delete today

| What | Can you delete it? |
|---|---|
| The Arweave copy of one conversation | **Yes.** "Forget a conversation" in the cabinet destroys every key of that conversation; its copies on Arweave become unreadable for good. |
| All Arweave copies | Yes, the same way, conversation by conversation. |
| The plain text in the database | **Not yet.** There is no self-service deletion of conversation text in the database; it is an open item. Until it exists, write to contact@codeofdigitaleternity.com. |
| Your MCP keys | Yes — signing out on all devices revokes every key at once. |

## Backups and retention

Conversation text is kept without an expiry date: keeping it is the product. Provider-side backups follow Neon's plan
(point-in-time restore); their retention window has not been measured for this page.

## What is not verifiable from outside

The server code is private, so everything above about the code is our statement, not something you can check. What
you can check: the live answers (`tools/list`, the `memory_about` tool), the filters in the open PADAM code they
match, and your own Arweave records with your own key.

## Changes

See [CHANGELOG.md](CHANGELOG.md). Security problems: [SECURITY.md](SECURITY.md).

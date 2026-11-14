# AIfa Memory — MCP server

[![mcptry](https://mcptry.com/badge/works.aifa/aifa-memory)](https://mcptry.com/servers/works.aifa/aifa-memory)

**One memory for you and your AI agents.** AIfa Memory is a hosted [Model Context Protocol](https://modelcontextprotocol.io) server. It connects Claude, Cursor, VS Code or any other MCP client to the memory of your AIfa account — the same memory AIfa uses when you talk to her on [aifa.works](https://aifa.works), [codeofdigitaleternity.com](https://codeofdigitaleternity.com), [aifa.digital](https://aifa.digital) and [radiocode.space](https://radiocode.space).

Your agent can recall what you discussed with AIfa weeks ago, save new decisions, and hand everything back to you as one Markdown file whenever you want to leave.

```
Endpoint   https://aifa.works/api/mcp
Transport  Streamable HTTP (JSON-RPC 2.0, stateless)
Auth       Authorization: Bearer <your key>
Version    1.9.7 · protocol 2026-07-28, 2025-06-18, 2025-03-26, 2024-11-05
```

This repository holds the public description of the server: connection examples, the full tool list and the registry manifest. The server itself runs on aifa.works; its code lives in the private site repository together with the database and payments. If you want a memory server you can read and run yourself, see [padam-nocturne](https://github.com/MaksimGalatin/padam-nocturne) — our open-source, local-first MCP memory (one SQLite file, 8 tools).

---

## Quick start

1. Sign in at **[aifa.works/mcp](https://aifa.works/mcp)** and create your key. One key per account.
2. Add the server to your client (examples below). Replace `YOUR_AIFA_MCP_KEY` with your key.
3. Ask your agent: *"Search my AIfa memory for what we decided about …"*

### Claude Code

```bash
claude mcp add --transport http aifa-memory https://aifa.works/api/mcp --header "Authorization: Bearer YOUR_AIFA_MCP_KEY"
```

### Cursor — `~/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "aifa-memory": {
      "url": "https://aifa.works/api/mcp",
      "headers": { "Authorization": "Bearer YOUR_AIFA_MCP_KEY" }
    }
  }
}
```

### VS Code — `.vscode/mcp.json`

```json
{
  "servers": {
    "aifa-memory": {
      "type": "http",
      "url": "https://aifa.works/api/mcp",
      "headers": { "Authorization": "Bearer YOUR_AIFA_MCP_KEY" }
    }
  }
}
```

### Claude Desktop — `claude_desktop_config.json`

Claude Desktop connects to remote servers through [`mcp-remote`](https://www.npmjs.com/package/mcp-remote). The header is passed without spaces inside `args` and the value goes into `env` — on Windows, spaces inside `args` break the header.

```json
{
  "mcpServers": {
    "aifa-memory": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://aifa.works/api/mcp", "--header", "Authorization:${AUTH_HEADER}"],
      "env": { "AUTH_HEADER": "Bearer YOUR_AIFA_MCP_KEY" }
    }
  }
}
```

The same files are in [`examples/`](examples/).

---

## Tools

Fifteen tools. Full parameters and hints: **[TOOLS.md](TOOLS.md)**. A **memory-only** key gets the five memory tools, `account_status` and `plans`; the other eight (`buy_plan`, `request_payout` and the partner program) need a full key.

**Memory**

| Tool | What it does |
|---|---|
| `memory_search` | Search your memory by meaning — every conversation with AIfa on the four sites plus notes saved by agents. |
| `memory_recent` | The most recent records, newest first, across all channels. |
| `memory_write` | Save a preference, decision, fact or session summary. Nothing is deleted; an identical record is not duplicated. |
| `memory_export` | Your whole verbatim memory as Markdown, in parts of up to 100,000 characters. |
| `memory_about` | What this memory is, where it lives and how it is protected. No user data. |

**Account**

| Tool | What it does |
|---|---|
| `account_status` | Your plan, permanent memory used and left this month, referral earnings and your referral link. |
| `plans` | Prices of the plans and what each one stores permanently. No user data. |
| `buy_plan` | Creates a crypto invoice (NOWPayments) for your own account and returns its URL. Nothing is charged until you pay. |
| `request_payout` | Requests a withdrawal of your referral balance in USDT (TRC20). Reviewed and paid manually; every address is screened against the OFAC sanctions list. |

**Partner program** (bringing clients to AIfa Works accessibility services)

| Tool | What it does |
|---|---|
| `partner_kit` | Rates, the 14-day hold, the rules and three email templates (en, ru, es, zh). |
| `client_link` | Your partner link to the accessibility page, optionally with a service price and your share. |
| `client_report` | A ready report page for a site owner, built from the published AIfa research data. No new scan of a third-party site is made. |
| `find_clients` | Up to 20 new sites a day in a region where the research found barriers; each is reserved for you for 30 days. |
| `my_deals` | Paid orders you brought, your share and when it can be withdrawn. |
| `set_webhook` | A signed POST to your https endpoint for every counted click and commission. |

Plans: **Spark** $15/month · **Family Archive** $100/month · **Digital DNA** $1,000 once per device, then $200/month. The `plans` tool always returns the current prices and limits.

---

## How your data is handled

- **The key decides everything.** The account is taken only from the key, never from the request body. No tool takes an email or user ID as input, so one account cannot read another's memory.
- **Without a key** the server answers only `initialize`, `ping` and `tools/list`. Every `tools/call` without a valid key returns `Unauthorized`.
- **Revoking a key.** Signing out on all devices in your cabinet revokes it.
- **Limits.** 60 calls a minute per key, of them 20 searches. 30 calls a minute per address without a key. Tool answers are trimmed so that one call cannot pull a whole history; use `memory_export` for a full copy of your own memory.
- **Permanent copy.** On paid plans a copy of your conversations is stored on Arweave, encrypted with your own key; every record has its own key, so a single record can be made unreadable without touching the rest.
- **Leaving.** `memory_export` gives you everything as Markdown. You can leave whenever you want and take your memory with you.
- **Memory-only keys.** Tick "memory only" when you get a key at [aifa.works/mcp](https://aifa.works/mcp) (or send `{"scope": "memory"}` to `/api/account/mcp-token`). Such a key sees memory, `plans` and `account_status`; buying, payouts, the webhook and partner tools are refused. Give it to agents that read other people's pages: an order hidden in a page cannot reach your money through it.
- **Where data lies, who can read it, what you can delete:** [HOSTED-POLICY.md](HOSTED-POLICY.md). **What changed and when:** [CHANGELOG.md](CHANGELOG.md).

**Check it yourself:** `python scripts/conformance.py` runs the claims above against the live server — without a key: the open methods, 15 tools, no tool that takes an email or user id, refusal without a valid key; with your own key in `AIFA_MCP_KEY`: a written secret comes back masked, a command-like text is not stored, returned memory is fenced; with a memory-only key in `AIFA_MCP_MEMORY_KEY`: 7 tools and payouts refused.

Found a security problem? See [SECURITY.md](SECURITY.md).

---

## Registry

[`server.json`](server.json) is the manifest for the official [MCP Registry](https://registry.modelcontextprotocol.io) (schema 2025-12-11) under the name `works.aifa/aifa-memory`.

## Links

- Get a key and read the guide: [aifa.works/mcp](https://aifa.works/mcp)
- Partner program: [aifa.works/partners](https://aifa.works/partners)
- Open-source local memory: [padam-nocturne](https://github.com/MaksimGalatin/padam-nocturne)
- Contact: [contact@codeofdigitaleternity.com](mailto:contact@codeofdigitaleternity.com)

## License

The documentation and configuration examples in this repository are released under the [MIT License](LICENSE). The AIfa Memory service itself is provided by CODE Eternal LLC under the terms published on [aifa.works](https://aifa.works).

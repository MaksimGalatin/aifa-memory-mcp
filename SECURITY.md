# Security

## Reporting a vulnerability

Please report security problems privately to **contact@codeofdigitaleternity.com** with the subject `Security: AIfa Memory MCP`. Include what you found, how to reproduce it and what an attacker could do with it. Please do not open a public issue for a vulnerability and do not test against other people's accounts or data.

We reply to every report and fix confirmed problems as a priority.

## Keeping your key safe

- A full key gives access to your AIfa memory and your partner account. Treat it like a password. For agents that read web pages or other people's files, issue a **memory-only** key (since 1.9.2): it cannot buy, request payouts, set a webhook or use partner tools.
- Never commit it to a repository. The examples here use the placeholder `YOUR_AIFA_MCP_KEY`; keep the real value in your client's local config or an environment variable.
- If a key leaks, sign out on all devices in your cabinet at [aifa.works](https://aifa.works). This revokes the key; then create a new one at [aifa.works/mcp](https://aifa.works/mcp).

## What this repository contains

Documentation, configuration examples and the registry manifest only. It contains no server code, no credentials and no user data.

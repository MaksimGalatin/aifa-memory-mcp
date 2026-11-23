#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AIfa Memory MCP Quickstart Doctor (CLI, v2.0.0 — Фишка 10).

За 3 секунды проверяет живое подключение к https://aifa.works/api/mcp:
- рукопожатие initialize и версию сервера;
- список tools/list (все 17 инструментов);
- протокол MCP 2026-07-28 (server/discover);
- при наличии ключа (--key или AIFA_MCP_KEY): авторизованный вызов memory_about;
- при флаге --print-configs: готовые конфигурации для 7 популярных ИИ-клиентов.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Any

DEFAULT_URL = "https://aifa.works/api/mcp"


def _post_json(url: str, payload: dict[str, Any], headers: dict[str, str], timeout: float = 15.0) -> tuple[int, dict[str, Any], float]:
    t0 = time.perf_counter()
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json", **headers},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return resp.status, body, (time.perf_counter() - t0) * 1000.0
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw)
        except Exception:
            body = {"raw": raw[:300]}
        return exc.code, body, (time.perf_counter() - t0) * 1000.0


def run_doctor(url: str = DEFAULT_URL, api_key: str = "") -> dict[str, Any]:
    hdrs: dict[str, str] = {}
    if api_key:
        hdrs["Authorization"] = f"Bearer {api_key}"

    checks: list[dict[str, Any]] = []

    # 1. initialize (2025-06-18)
    code1, body1, ms1 = _post_json(
        url,
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "aifa-quickstart-doctor", "version": "2.0.0"}},
        },
        hdrs,
    )
    srv = (body1.get("result") or {}).get("serverInfo") or {}
    checks.append({
        "check": "initialize",
        "ok": code1 == 200 and bool(srv.get("name")),
        "http": code1,
        "server": srv.get("name"),
        "version": srv.get("version"),
        "ms": round(ms1, 1),
    })

    # 2. tools/list
    code2, body2, ms2 = _post_json(url, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}, hdrs)
    tools = (body2.get("result") or {}).get("tools") or []
    tool_names = [t.get("name") for t in tools if isinstance(t, dict)]
    checks.append({
        "check": "tools/list",
        "ok": code2 == 200 and len(tools) >= 7,
        "http": code2,
        "tools_count": len(tools),
        "has_wake_up": "memory_wake_up" in tool_names,
        "has_forget": "memory_forget" in tool_names,
        "ms": round(ms2, 1),
    })

    # 3. MCP 2026-07-28 server/discover
    code3, body3, ms3 = _post_json(
        url,
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "server/discover",
            "params": {
                "_meta": {
                    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
                    "io.modelcontextprotocol/clientCapabilities": {},
                }
            },
        },
        {**hdrs, "MCP-Protocol-Version": "2026-07-28", "Mcp-Method": "server/discover"},
    )
    res3 = body3.get("result") or {}
    checks.append({
        "check": "server/discover (2026-07-28)",
        "ok": code3 == 200 and res3.get("resultType") == "complete",
        "http": code3,
        "supportedVersions": res3.get("supportedVersions"),
        "ms": round(ms3, 1),
    })

    # 4. Authenticated check (only when key is provided)
    if api_key:
        code4, body4, ms4 = _post_json(
            url,
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "memory_about", "arguments": {}}},
            hdrs,
        )
        res4 = body4.get("result") or {}
        checks.append({
            "check": "auth memory_about",
            "ok": code4 == 200 and not body4.get("error") and not res4.get("isError"),
            "http": code4,
            "ms": round(ms4, 1),
        })

    all_ok = all(c["ok"] for c in checks)
    return {"ok": all_ok, "url": url, "checks": checks}


def print_client_configs(url: str, api_key: str) -> None:
    k = api_key or "<YOUR_AIFA_KEY>"
    print("\n--- Ready-to-paste MCP client configs (7 clients) ---")
    print(f"1) Claude Code:\n   claude mcp add --transport http aifa-memory {url} --header \"Authorization: Bearer {k}\"\n")
    print("2) Cursor (~/.cursor/mcp.json):\n" + json.dumps({"mcpServers": {"aifa-memory": {"url": url, "headers": {"Authorization": f"Bearer {k}"}}}}, indent=2))
    print("\n3) VS Code (.vscode/mcp.json):\n" + json.dumps({"servers": {"aifa-memory": {"type": "http", "url": url, "headers": {"Authorization": f"Bearer {k}"}}}}, indent=2))
    print("\n4) Windsurf (~/.codeium/windsurf/mcp_config.json):\n" + json.dumps({"mcpServers": {"aifa-memory": {"serverUrl": url, "headers": {"Authorization": f"Bearer {k}"}}}}, indent=2))
    print("\n5) Gemini CLI (~/.gemini/settings.json):\n" + json.dumps({"mcpServers": {"aifa-memory": {"httpUrl": url, "headers": {"Authorization": f"Bearer {k}"}}}}, indent=2))
    print(f'\n6) OpenAI Codex (~/.codex/config.toml):\n[mcp_servers.aifa_memory]\nurl = "{url}"\nbearer_token_env_var = "AIFA_MCP_TOKEN"')
    print("\n7) Claude Desktop (claude_desktop_config.json):\n" + json.dumps({"mcpServers": {"aifa-memory": {"command": "npx", "args": ["-y", "mcp-remote", url, "--header", "Authorization:${AUTH_HEADER}"], "env": {"AUTH_HEADER": f"Bearer {k}"}}}}, indent=2))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AIfa Memory MCP Quickstart Doctor (v2.0.0)")
    parser.add_argument("--url", default=os.environ.get("AIFA_MCP_URL", DEFAULT_URL), help="MCP endpoint URL")
    parser.add_argument("--key", default=os.environ.get("AIFA_MCP_KEY", ""), help="Optional amcp_... Bearer key")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Print JSON output")
    parser.add_argument("--print-configs", action="store_true", help="Print configs for 7 MCP clients")
    args = parser.parse_args(argv)

    report = run_doctor(url=args.url, api_key=args.key.strip())
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"AIfa Memory MCP Doctor -> {report['url']}")
        for c in report["checks"]:
            mark = "PASS" if c["ok"] else "FAIL"
            extra = ""
            if "version" in c:
                extra = f" server={c['server']} v{c['version']}"
            elif "tools_count" in c:
                extra = f" tools={c['tools_count']} wake_up={c['has_wake_up']} forget={c['has_forget']}"
            print(f"  [{mark}] {c['check']} (HTTP {c['http']}, {c['ms']} ms){extra}")
        if args.print_configs:
            print_client_configs(args.url, args.key.strip())
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())

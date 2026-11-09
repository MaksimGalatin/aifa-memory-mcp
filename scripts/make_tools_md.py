# -*- coding: utf-8 -*-
"""Rebuild TOOLS.md from what the live server reports (tools/list), so the list never drifts from the server.

Run: python -I -X utf8 scripts/make_tools_md.py            # asks https://aifa.works/api/mcp, no key needed
     python -I -X utf8 scripts/make_tools_md.py tools.json # or from a saved {"serverInfo":…, "tools":[…]}
"""
import json
import sys
import urllib.request
from pathlib import Path

ENDPOINT = "https://aifa.works/api/mcp"


def call(body):
    req = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode(), headers={
        "Content-Type": "application/json", "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": "2025-06-18", "User-Agent": "aifa-memory-mcp-docs/1.0"})
    text = urllib.request.urlopen(req, timeout=40).read().decode("utf-8")
    if text.lstrip().startswith(("event:", "data:")):
        text = [line[5:] for line in text.splitlines() if line.startswith("data:")][0]
    return json.loads(text)


def live():
    init = call({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "docs", "version": "1"}}})
    tools = call({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    return {"serverInfo": init["result"]["serverInfo"], "tools": tools["result"]["tools"]}


def kind(p):
    t = p.get("type", "")
    if "enum" in p:
        return f"{t} ({', '.join(str(v) for v in p['enum'])})"
    if t in ("integer", "number") and ("minimum" in p or "maximum" in p):
        return f"{t} {p.get('minimum', '')}–{p.get('maximum', '')}"
    return t


def main():
    data = json.load(open(sys.argv[1], encoding="utf-8")) if len(sys.argv) > 1 else live()
    version, tools = data["serverInfo"]["version"], data["tools"]
    title = lambda t: t.get("title") or (t.get("annotations") or {}).get("title") or t["name"]
    ro = lambda t: "yes" if (t.get("annotations") or {}).get("readOnlyHint") else "no"
    out = ["# Tools", "",
           f"The {len(tools)} tools of the AIfa Memory MCP server, exactly as the live server reports them "
           f"(`tools/list`, server version {version}). Rebuilt by `scripts/make_tools_md.py`.", "",
           "Every tool works only with the account that owns the API key. The key decides whose memory and whose "
           "partner account is used; no tool accepts an email or user ID as input.", "",
           "| Tool | Read-only | What it does |", "|---|---|---|"]
    out += [f"| [`{t['name']}`](#{t['name']}) | {ro(t)} | {title(t)} |" for t in tools]
    for t in tools:
        out += ["", f"## {t['name']}", "", f"**{title(t)}**", "", t.get("description", "").strip(), ""]
        props = (t.get("inputSchema") or {}).get("properties") or {}
        need = set((t.get("inputSchema") or {}).get("required") or [])
        if props:
            out += ["| Parameter | Type | Required | Description |", "|---|---|---|---|"]
            out += [f"| `{n}` | {kind(p)} | {'yes' if n in need else 'no'} | {p.get('description', '')} |"
                    for n, p in props.items()]
        else:
            out.append("No parameters.")
        a = t.get("annotations") or {}
        out += ["", "Hints: " + ", ".join(f"{k}={str(a.get(k + 'Hint')).lower()}"
                                          for k in ("readOnly", "destructive", "idempotent", "openWorld"))]
    Path(__file__).resolve().parents[1].joinpath("TOOLS.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"TOOLS.md: {len(tools)} tools, server {version}")


if __name__ == "__main__":
    main()

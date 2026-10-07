#!/usr/bin/env python3
"""
MCP server: file_summary

Implements a simple JSON-RPC over stdin/stdout.
Methods:
 - file_summary(path: string) -> { path, size_bytes, line_count, sha256 }
Errors:
 - invalid params / file not found
"""
import hashlib
import json
import os
import sys


def file_summary(path: str):
    if not isinstance(path, str) or not path:
        raise ValueError("path must be a non-empty string")
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    size = os.path.getsize(path)
    line_count = 0
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    with open(path, "rb") as f:
        for _ in f:
            line_count += 1
    return {
        "path": path,
        "size_bytes": size,
        "line_count": line_count,
        "sha256": sha256.hexdigest(),
    }


def main():
    for line in sys.stdin:
        try:
            req = json.loads(line)
            rid = req.get("id")
            method = req.get("method")
            params = req.get("params", {})
            if method == "file_summary":
                result = file_summary(params.get("path"))
                resp = {"jsonrpc": "2.0", "id": rid, "result": result}
            else:
                resp = {
                    "jsonrpc": "2.0",
                    "id": rid,
                    "error": {"code": -32601, "message": "Method not found"},
                }
        except FileNotFoundError as e:
            resp = {
                "jsonrpc": "2.0",
                "id": req.get("id") if 'req' in locals() else None,
                "error": {"code": -32004, "message": f"File not found: {e}"},
            }
        except Exception as e:
            resp = {
                "jsonrpc": "2.0",
                "id": req.get("id") if 'req' in locals() else None,
                "error": {"code": -32602, "message": str(e)},
            }
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()

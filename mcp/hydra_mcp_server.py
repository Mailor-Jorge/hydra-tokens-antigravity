#!/usr/bin/env python3
"""
HYDRA TOKENS ANTIGRAVITY — Custom Stdio MCP Server (HEAD-8)
Pure Python JSON-RPC MCP Server implementation. Zero external dependencies.
v1.1.0 — Added: hydra_snippet, hydra_cache, hydra_context_snapshot
"""

import sys
import json
import os
import re
import time

SERVER_NAME = "hydra-tools-mcp"
SERVER_VERSION = "1.1.0"

CACHE_FILE = os.path.join(os.environ.get("USERPROFILE", os.environ.get("HOME", "")), ".gemini", "antigravity", "hydra_cache.json")

TOOLS = [
    {
        "name": "hydra_filter_log",
        "description": "Filter large log files locally, returning only error lines. Saves thousands of context tokens.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Absolute path to the log file"},
                "max_lines": {"type": "integer", "description": "Max matching error lines to return (default 50)"}
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "hydra_token_estimate",
        "description": "Estimate token footprint of a file before loading it into context.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Absolute path to the file"}
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "hydra_clean_scratch",
        "description": "Clean temporary scratch files older than 24 hours to keep workspace light.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dry_run": {"type": "boolean", "description": "If true, only report files without deleting"}
            }
        }
    },
    {
        "name": "hydra_snippet",
        "description": "Extract only a specific function, class, or code block from a file by name. Avoids loading entire files.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Absolute path to the source file"},
                "symbol": {"type": "string", "description": "Name of function, class, event, or state to extract"},
                "context_lines": {"type": "integer", "description": "Extra lines of context above/below (default 2)"}
            },
            "required": ["file_path", "symbol"]
        }
    },
    {
        "name": "hydra_cache",
        "description": "Save, retrieve, or list cached responses to avoid regenerating repeated answers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["save", "get", "list", "delete"], "description": "Action to perform on cache"},
                "key": {"type": "string", "description": "Cache key (topic or question, e.g. 'compilar papyrus')"},
                "value": {"type": "string", "description": "Response content to cache (required for 'save')"}
            },
            "required": ["action"]
        }
    },
    {
        "name": "hydra_context_snapshot",
        "description": "Analyze all files in a directory and report their estimated token costs. Helps identify heavy files before loading.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "directory": {"type": "string", "description": "Absolute path to directory to scan"},
                "max_depth": {"type": "integer", "description": "Max directory depth to scan (default 2)"},
                "extensions": {"type": "string", "description": "Comma-separated file extensions to include (e.g. '.py,.md,.psc'). Default: all text files"}
            },
            "required": ["directory"]
        }
    }
]

# --- Tool Handlers ---

def handle_filter_log(file_path, max_lines=50):
    if not os.path.exists(file_path):
        return f"Error: File not found: {file_path}"
    try:
        error_keywords = re.compile(r'(error|failed|fatal|exception|critical|warn|traceback)', re.IGNORECASE)
        matching_lines = []
        total_lines = 0
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                total_lines += 1
                if error_keywords.search(line):
                    matching_lines.append(f"L{line_num}: {line.strip()}")
                    if len(matching_lines) >= max_lines:
                        break
        if not matching_lines:
            return f"[HYDRA FILTER] Analyzed {total_lines} lines in {os.path.basename(file_path)}. Zero errors found!"
        return f"[HYDRA FILTER] Analyzed {total_lines} lines. Extracted {len(matching_lines)} error lines:\n" + "-"*50 + "\n" + "\n".join(matching_lines)
    except Exception as e:
        return f"Error reading file: {str(e)}"

def handle_token_estimate(file_path):
    if not os.path.exists(file_path):
        return f"Error: File not found: {file_path}"
    try:
        size_bytes = os.path.getsize(file_path)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        char_count = len(content)
        word_count = len(content.split())
        est_tokens = int(char_count / 4)
        rec = "OK to load" if est_tokens < 3000 else "HIGH TOKEN COST — use hydra_filter_log or partial read"
        return (f"[HYDRA TOKEN ESTIMATE] {os.path.basename(file_path)}\n"
                f"  File Size  : {size_bytes / 1024:.1f} KB\n"
                f"  Characters : {char_count:,}\n"
                f"  Words      : {word_count:,}\n"
                f"  Est. Tokens: ~{est_tokens:,} tokens\n"
                f"  Status     : {rec}")
    except Exception as e:
        return f"Error analyzing file: {str(e)}"

def handle_clean_scratch(dry_run=True):
    scratch_dir = os.path.join(os.environ.get("USERPROFILE", os.environ.get("HOME", "")), ".gemini", "antigravity", "scratch")
    if not os.path.exists(scratch_dir):
        return "Scratch directory not found."
    cleaned = []
    total_bytes = 0
    try:
        for root, dirs, files in os.walk(scratch_dir):
            for file in files:
                if file.endswith(('.tmp', '.bak', '.log')):
                    p = os.path.join(root, file)
                    sz = os.path.getsize(p)
                    cleaned.append(f"{file} ({sz / 1024:.1f} KB)")
                    total_bytes += sz
                    if not dry_run:
                        os.remove(p)
        action_str = "Found (Dry Run)" if dry_run else "Deleted"
        return (f"[HYDRA SCRATCH CLEANER] {action_str} {len(cleaned)} temp files (~{total_bytes / 1024:.1f} KB saved):\n" +
                ("\n".join(cleaned[:10]) if cleaned else "No temporary files found."))
    except Exception as e:
        return f"Error cleaning scratch: {str(e)}"

def handle_snippet(file_path, symbol, context_lines=2):
    if not os.path.exists(file_path):
        return f"Error: File not found: {file_path}"
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        total = len(lines)
        # Patterns for common code constructs
        patterns = [
            re.compile(rf'^\s*(def|function|func|fn|sub|proc)\s+{re.escape(symbol)}\s*[\(:]', re.IGNORECASE),
            re.compile(rf'^\s*(class|struct|interface|enum)\s+{re.escape(symbol)}[\s\(:\{{]', re.IGNORECASE),
            re.compile(rf'^\s*(Event|Function|State)\s+{re.escape(symbol)}\s*[\(]', re.IGNORECASE),  # Papyrus
            re.compile(rf'^\s*(async\s+)?(def|function)\s+{re.escape(symbol)}\s*[\(]', re.IGNORECASE),
            re.compile(rf'{re.escape(symbol)}\s*[:=]\s*(function|class|\()', re.IGNORECASE),  # JS/TS
        ]
        start_idx = None
        for i, line in enumerate(lines):
            for pat in patterns:
                if pat.search(line):
                    start_idx = i
                    break
            if start_idx is not None:
                break
        if start_idx is None:
            # Fallback: simple text search
            for i, line in enumerate(lines):
                if symbol.lower() in line.lower():
                    start_idx = i
                    break
        if start_idx is None:
            return f"[HYDRA SNIPPET] Symbol '{symbol}' not found in {os.path.basename(file_path)} ({total} lines)"
        # Find end of block by indentation
        base_indent = len(lines[start_idx]) - len(lines[start_idx].lstrip())
        end_idx = start_idx + 1
        while end_idx < total:
            line = lines[end_idx]
            stripped = line.strip()
            if stripped == "":
                end_idx += 1
                continue
            current_indent = len(line) - len(line.lstrip())
            if current_indent <= base_indent and stripped and end_idx > start_idx + 1:
                # Check for Papyrus EndFunction/EndEvent/EndState
                if stripped.lower().startswith(('endfunction', 'endevent', 'endstate', 'endif')):
                    end_idx += 1
                break
            end_idx += 1
        # Apply context
        real_start = max(0, start_idx - context_lines)
        real_end = min(total, end_idx + context_lines)
        snippet_lines = []
        for i in range(real_start, real_end):
            snippet_lines.append(f"L{i+1}: {lines[i].rstrip()}")
        est_tokens = int(sum(len(l) for l in lines[real_start:real_end]) / 4)
        full_tokens = int(sum(len(l) for l in lines) / 4)
        return (f"[HYDRA SNIPPET] Extracted '{symbol}' from {os.path.basename(file_path)}\n"
                f"  Lines: {real_start+1}-{real_end} of {total} | Tokens: ~{est_tokens} (full file: ~{full_tokens})\n"
                f"  Saved: ~{full_tokens - est_tokens} tokens ({((full_tokens - est_tokens) / max(full_tokens,1) * 100):.0f}% reduction)\n"
                + "-"*50 + "\n" + "\n".join(snippet_lines))
    except Exception as e:
        return f"Error extracting snippet: {str(e)}"

def _load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def _save_cache(data):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def handle_cache(action, key=None, value=None):
    cache = _load_cache()
    if action == "save":
        if not key or not value:
            return "Error: 'key' and 'value' required for save action."
        cache[key] = {"value": value, "saved_at": time.strftime("%Y-%m-%d %H:%M")}
        _save_cache(cache)
        est_tokens = int(len(value) / 4)
        return f"[HYDRA CACHE] Saved '{key}' (~{est_tokens} tokens cached). Next time this topic comes up, retrieval costs 0 generation tokens."
    elif action == "get":
        if not key:
            return "Error: 'key' required for get action."
        if key in cache:
            entry = cache[key]
            return f"[HYDRA CACHE HIT] '{key}' (saved {entry['saved_at']})\n" + "-"*50 + "\n" + entry["value"]
        # Fuzzy match
        for k in cache:
            if key.lower() in k.lower() or k.lower() in key.lower():
                entry = cache[k]
                return f"[HYDRA CACHE HIT] Fuzzy match '{k}' (saved {entry['saved_at']})\n" + "-"*50 + "\n" + entry["value"]
        return f"[HYDRA CACHE MISS] No cached entry for '{key}'. Available keys: {', '.join(cache.keys()) if cache else 'none'}"
    elif action == "list":
        if not cache:
            return "[HYDRA CACHE] Empty. No cached responses yet."
        lines = [f"[HYDRA CACHE] {len(cache)} cached entries:"]
        for k, v in cache.items():
            est = int(len(v["value"]) / 4)
            lines.append(f"  '{k}' — ~{est} tokens | saved {v['saved_at']}")
        return "\n".join(lines)
    elif action == "delete":
        if not key:
            return "Error: 'key' required for delete action."
        if key in cache:
            del cache[key]
            _save_cache(cache)
            return f"[HYDRA CACHE] Deleted '{key}'."
        return f"[HYDRA CACHE] Key '{key}' not found."
    return f"Error: Unknown action '{action}'"

def handle_context_snapshot(directory, max_depth=2, extensions=None):
    if not os.path.exists(directory):
        return f"Error: Directory not found: {directory}"
    ext_filter = None
    if extensions:
        ext_filter = set(e.strip().lower() for e in extensions.split(','))
    files_data = []
    total_tokens = 0
    try:
        for root, dirs, files in os.walk(directory):
            depth = root.replace(directory, '').count(os.sep)
            if depth >= max_depth:
                dirs.clear()
                continue
            for file in files:
                fp = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                if ext_filter and ext not in ext_filter:
                    continue
                if ext in ('.exe', '.dll', '.pex', '.bsa', '.nif', '.dds', '.png', '.jpg', '.mp3', '.wav', '.zip', '.7z', '.rar'):
                    continue
                try:
                    sz = os.path.getsize(fp)
                    if sz > 500000:  # Skip files > 500KB
                        continue
                    est = int(sz / 4)
                    rel = os.path.relpath(fp, directory)
                    files_data.append((rel, sz, est))
                    total_tokens += est
                except:
                    pass
        files_data.sort(key=lambda x: -x[2])  # Sort by tokens desc
        lines = [f"[HYDRA CONTEXT SNAPSHOT] {directory}", f"  Total files: {len(files_data)} | Total est. tokens: ~{total_tokens:,}", "-"*60]
        # Top 15 heaviest files
        for rel, sz, est in files_data[:15]:
            status = "OK" if est < 3000 else "HEAVY"
            lines.append(f"  [{status:5s}] {rel:45s} {sz/1024:7.1f} KB  ~{est:,} tok")
        if len(files_data) > 15:
            lines.append(f"  ... and {len(files_data) - 15} more files")
        return "\n".join(lines)
    except Exception as e:
        return f"Error scanning directory: {str(e)}"

def respond(response_dict):
    msg = json.dumps(response_dict)
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()

def main():
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "initialize":
                respond({"jsonrpc": "2.0", "id": req_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION}
                }})
            elif method == "notifications/initialized":
                pass
            elif method == "tools/list":
                respond({"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}})
            elif method == "tools/call":
                name = params.get("name")
                args = params.get("arguments", {})
                if name == "hydra_filter_log":
                    res_text = handle_filter_log(args.get("file_path", ""), args.get("max_lines", 50))
                elif name == "hydra_token_estimate":
                    res_text = handle_token_estimate(args.get("file_path", ""))
                elif name == "hydra_clean_scratch":
                    res_text = handle_clean_scratch(args.get("dry_run", True))
                elif name == "hydra_snippet":
                    res_text = handle_snippet(args.get("file_path", ""), args.get("symbol", ""), args.get("context_lines", 2))
                elif name == "hydra_cache":
                    res_text = handle_cache(args.get("action", ""), args.get("key"), args.get("value"))
                elif name == "hydra_context_snapshot":
                    res_text = handle_context_snapshot(args.get("directory", ""), args.get("max_depth", 2), args.get("extensions"))
                else:
                    res_text = f"Unknown tool: {name}"
                respond({"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": res_text}]}})
            elif req_id is not None:
                respond({"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})
        except Exception as e:
            pass

if __name__ == "__main__":
    main()

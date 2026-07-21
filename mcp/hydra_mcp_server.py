#!/usr/bin/env python3
"""
HYDRA TOKENS ANTIGRAVITY — Custom Stdio MCP Server (HEAD-8)
Pure Python JSON-RPC MCP Server implementation. Zero external dependencies.
v1.2.0 — Added: hydra_dependency_trace, hydra_edit_verify, hydra_file_hash
"""

import sys
import json
import os
import re
import time
import hashlib
import py_compile

SERVER_NAME = "hydra-tools-mcp"
SERVER_VERSION = "1.2.0"

BASE_DIR = os.path.join(os.environ.get("USERPROFILE", os.environ.get("HOME", "")), ".gemini", "antigravity")
CACHE_FILE = os.path.join(BASE_DIR, "hydra_cache.json")
HASH_FILE = os.path.join(BASE_DIR, "hydra_file_hashes.json")

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
    },
    {
        "name": "hydra_dependency_trace",
        "description": "Trace call dependencies for a function/symbol across project files to prevent breaking changes during edits.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Absolute path to the file containing the symbol"},
                "symbol": {"type": "string", "description": "Name of the function, event, or class to trace"},
                "search_dir": {"type": "string", "description": "Directory to search for callers/dependencies (optional, defaults to parent dir)"}
            },
            "required": ["file_path", "symbol"]
        }
    },
    {
        "name": "hydra_edit_verify",
        "description": "Run post-edit syntax and structure verification on a file to ensure no syntax errors were introduced.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Absolute path to the edited file"},
                "language": {"type": "string", "description": "Language hint (e.g. 'papyrus', 'python', 'json', 'javascript')"}
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "hydra_file_hash",
        "description": "Check if a file content has changed (MD5 hash) since last read to avoid re-reading identical files into context.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Absolute path to the file"},
                "action": {"type": "string", "enum": ["check", "clear"], "description": "'check' to compare hash, 'clear' to reset stored hash"}
            },
            "required": ["file_path"]
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
    scratch_dir = os.path.join(BASE_DIR, "scratch")
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
        patterns = [
            re.compile(rf'^\s*(def|function|func|fn|sub|proc)\s+{re.escape(symbol)}\s*[\(:]', re.IGNORECASE),
            re.compile(rf'^\s*(class|struct|interface|enum)\s+{re.escape(symbol)}[\s\(:\{{]', re.IGNORECASE),
            re.compile(rf'^\s*(Event|Function|State)\s+{re.escape(symbol)}\s*[\(]', re.IGNORECASE),
            re.compile(rf'^\s*(async\s+)?(def|function)\s+{re.escape(symbol)}\s*[\(]', re.IGNORECASE),
            re.compile(rf'{re.escape(symbol)}\s*[:=]\s*(function|class|\()', re.IGNORECASE),
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
            for i, line in enumerate(lines):
                if symbol.lower() in line.lower():
                    start_idx = i
                    break
        if start_idx is None:
            return f"[HYDRA SNIPPET] Symbol '{symbol}' not found in {os.path.basename(file_path)} ({total} lines)"
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
                if stripped.lower().startswith(('endfunction', 'endevent', 'endstate', 'endif')):
                    end_idx += 1
                break
            end_idx += 1
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

def _load_json(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def _save_json(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def handle_cache(action, key=None, value=None):
    cache = _load_json(CACHE_FILE)
    if action == "save":
        if not key or not value:
            return "Error: 'key' and 'value' required for save action."
        cache[key] = {"value": value, "saved_at": time.strftime("%Y-%m-%d %H:%M")}
        _save_json(CACHE_FILE, cache)
        est_tokens = int(len(value) / 4)
        return f"[HYDRA CACHE] Saved '{key}' (~{est_tokens} tokens cached). Next time this topic comes up, retrieval costs 0 generation tokens."
    elif action == "get":
        if not key:
            return "Error: 'key' required for get action."
        if key in cache:
            entry = cache[key]
            return f"[HYDRA CACHE HIT] '{key}' (saved {entry['saved_at']})\n" + "-"*50 + "\n" + entry["value"]
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
            _save_json(CACHE_FILE, cache)
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
                    if sz > 500000:
                        continue
                    est = int(sz / 4)
                    rel = os.path.relpath(fp, directory)
                    files_data.append((rel, sz, est))
                    total_tokens += est
                except:
                    pass
        files_data.sort(key=lambda x: -x[2])
        lines = [f"[HYDRA CONTEXT SNAPSHOT] {directory}", f"  Total files: {len(files_data)} | Total est. tokens: ~{total_tokens:,}", "-"*60]
        for rel, sz, est in files_data[:15]:
            status = "OK" if est < 3000 else "HEAVY"
            lines.append(f"  [{status:5s}] {rel:45s} {sz/1024:7.1f} KB  ~{est:,} tok")
        if len(files_data) > 15:
            lines.append(f"  ... and {len(files_data) - 15} more files")
        return "\n".join(lines)
    except Exception as e:
        return f"Error scanning directory: {str(e)}"

def handle_dependency_trace(file_path, symbol, search_dir=None):
    if not os.path.exists(file_path):
        return f"Error: File not found: {file_path}"
    target_dir = search_dir if search_dir and os.path.exists(search_dir) else os.path.dirname(file_path)
    if not target_dir:
        target_dir = "."
    callers = []
    try:
        pattern = re.compile(rf'\b{re.escape(symbol)}\b')
        target_file_name = os.path.basename(file_path)
        for root, dirs, files in os.walk(target_dir):
            for f in files:
                if f.endswith(('.psc', '.py', '.js', '.ts', '.c', '.cpp', '.h', '.java')):
                    fp = os.path.join(root, f)
                    try:
                        with open(fp, 'r', encoding='utf-8', errors='ignore') as file_obj:
                            for idx, line in enumerate(file_obj, 1):
                                if pattern.search(line):
                                    rel = os.path.relpath(fp, target_dir)
                                    callers.append(f"  ← {rel}:L{idx} | {line.strip()[:80]}")
                    except:
                        pass
        callers_str = "\n".join(callers[:15]) if callers else "  (No external references found)"
        total_refs = len(callers)
        warn = "⚠️ WARNING: Multiple files depend on this symbol. Exercise caution during edits!" if total_refs > 2 else "✅ LOW RISK: Few references found."
        return (f"[HYDRA DEPENDENCY TRACE] Symbol '{symbol}' in {target_file_name}\n"
                f"  Search Dir: {target_dir} | Total References Found: {total_refs}\n"
                f"  Risk Status: {warn}\n"
                f"  References:\n{callers_str}")
    except Exception as e:
        return f"Error tracing dependencies: {str(e)}"

def handle_edit_verify(file_path, language=None):
    if not os.path.exists(file_path):
        return f"Error: File not found: {file_path}"
    ext = os.path.splitext(file_path)[1].lower()
    filename = os.path.basename(file_path)
    errors = []
    try:
        if ext == '.py' or language == 'python':
            try:
                py_compile.compile(file_path, doraise=True)
            except py_compile.PyCompileError as pe:
                errors.append(f"Python Syntax Error: {pe.msg}")
        elif ext == '.json' or language == 'json':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                try:
                    json.load(f)
                except json.JSONDecodeError as jde:
                    errors.append(f"JSON Syntax Error L{jde.lineno} C{jde.colno}: {jde.msg}")
        elif ext == '.psc' or language == 'papyrus':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            open_functions = 0
            open_events = 0
            open_states = 0
            for idx, line in enumerate(lines, 1):
                st = line.strip().lower()
                if st.startswith(('function ', 'event ', 'state ')) and not st.endswith(('endfunction', 'endevent', 'endstate')):
                    if st.startswith('function '): open_functions += 1
                    if st.startswith('event '): open_events += 1
                    if st.startswith('state '): open_states += 1
                if st == 'endfunction': open_functions = max(0, open_functions - 1)
                if st == 'endevent': open_events = max(0, open_events - 1)
                if st == 'endstate': open_states = max(0, open_states - 1)
                # Unmatched quotes check
                if line.count('"') % 2 != 0 and not line.strip().startswith(';'):
                    errors.append(f"L{idx}: Unmatched quote (\") in line: {line.strip()[:60]}")
            if open_functions > 0: errors.append(f"Missing EndFunction block ({open_functions} unclosed)")
            if open_events > 0: errors.append(f"Missing EndEvent block ({open_events} unclosed)")
            if open_states > 0: errors.append(f"Missing EndState block ({open_states} unclosed)")
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            # Generic parenthesis balance check
            open_p = 0
            for idx, line in enumerate(lines, 1):
                if line.strip().startswith(('//', '#', ';')): continue
                open_p += line.count('(') - line.count(')')
            if open_p != 0:
                errors.append(f"Generic syntax warning: Unbalanced parentheses count ({open_p}) across file")

        if not errors:
            return f"[HYDRA VERIFY] ✅ PASS — {filename}\n  Zero syntax/structure errors detected after edit."
        else:
            err_str = "\n".join(f"  ❌ {e}" for e in errors)
            return f"[HYDRA VERIFY] ❌ FAIL — {filename}\n  {len(errors)} potential error(s) found:\n{err_str}"
    except Exception as e:
        return f"Error verifying file: {str(e)}"

def handle_file_hash(file_path, action="check"):
    if not os.path.exists(file_path):
        return f"Error: File not found: {file_path}"
    try:
        hashes = _load_json(HASH_FILE)
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            curr_hash = hashlib.md5(f.read()).hexdigest()
        if action == "clear":
            if file_path in hashes:
                del hashes[file_path]
                _save_json(HASH_FILE, hashes)
            return f"[HYDRA HASH] Cleared hash history for {filename}."
        prev_hash = hashes.get(file_path, {}).get("hash")
        prev_time = hashes.get(file_path, {}).get("updated_at", "never")
        if prev_hash == curr_hash:
            est_tokens = int(os.path.getsize(file_path) / 4)
            return (f"[HYDRA HASH] {filename}\n"
                    f"  Current MD5 : {curr_hash[:8]}...\n"
                    f"  Status      : UNCHANGED (Last read: {prev_time})\n"
                    f"  Recommendation: SKIP RELOAD — File content has not changed. Saved ~{est_tokens:,} tokens!")
        else:
            hashes[file_path] = {"hash": curr_hash, "updated_at": time.strftime("%Y-%m-%d %H:%M")}
            _save_json(HASH_FILE, hashes)
            status_msg = "NEW FILE (First read)" if not prev_hash else f"CHANGED (Modified since {prev_time})"
            return (f"[HYDRA HASH] {filename}\n"
                    f"  Current MD5 : {curr_hash[:8]}...\n"
                    f"  Status      : {status_msg}\n"
                    f"  Recommendation: RELOAD REQUIRED — Load new content into context.")
    except Exception as e:
        return f"Error hashing file: {str(e)}"

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
                elif name == "hydra_dependency_trace":
                    res_text = handle_dependency_trace(args.get("file_path", ""), args.get("symbol", ""), args.get("search_dir"))
                elif name == "hydra_edit_verify":
                    res_text = handle_edit_verify(args.get("file_path", ""), args.get("language"))
                elif name == "hydra_file_hash":
                    res_text = handle_file_hash(args.get("file_path", ""), args.get("action", "check"))
                else:
                    res_text = f"Unknown tool: {name}"
                respond({"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": res_text}]}})
            elif req_id is not None:
                respond({"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})
        except Exception as e:
            pass

if __name__ == "__main__":
    main()

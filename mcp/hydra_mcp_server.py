#!/usr/bin/env python3
"""
HYDRA TOKENS ANTIGRAVITY — Custom Stdio MCP Server (HEAD-8)
Pure Python JSON-RPC MCP Server implementation. Zero external dependencies.
"""

import sys
import json
import os
import re

SERVER_NAME = "hydra-tokens-mcp"
SERVER_VERSION = "1.0.0"

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
    }
]

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
        
        output = [
            f"[HYDRA FILTER] Analyzed {total_lines} lines. Extracted {len(matching_lines)} error lines:",
            "-" * 50
        ] + matching_lines
        return "\n".join(output)
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
        est_tokens = int(char_count / 4) # Rough estimate ~4 chars/token
        
        recommendation = "OK to load" if est_tokens < 3000 else "HIGH TOKEN COST — use hydra_filter_log or partial read"
        
        return (
            f"[HYDRA TOKEN ESTIMATE] {os.path.basename(file_path)}\n"
            f"• File Size  : {size_bytes / 1024:.1f} KB\n"
            f"• Characters : {char_count:,}\n"
            f"• Words      : {word_count:,}\n"
            f"• Est. Tokens: ~{est_tokens:,} tokens\n"
            f"• Status     : {recommendation}"
        )
    except Exception as e:
        return f"Error analyzing file: {str(e)}"

def handle_clean_scratch(dry_run=True):
    scratch_dir = r"C:\Users\Mailoko\.gemini\antigravity\scratch"
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
        return (
            f"[HYDRA SCRATCH CLEANER] {action_str} {len(cleaned)} temp files (~{total_bytes / 1024:.1f} KB saved):\n" +
            ("\n".join(cleaned[:10]) if cleaned else "No temporary files found.")
        )
    except Exception as e:
        return f"Error cleaning scratch: {str(e)}"

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
                respond({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION}
                    }
                })
            elif method == "notifications/initialized":
                pass
            elif method == "tools/list":
                respond({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": TOOLS}
                })
            elif method == "tools/call":
                name = params.get("name")
                args = params.get("arguments", {})
                
                if name == "hydra_filter_log":
                    res_text = handle_filter_log(args.get("file_path", ""), args.get("max_lines", 50))
                elif name == "hydra_token_estimate":
                    res_text = handle_token_estimate(args.get("file_path", ""))
                elif name == "hydra_clean_scratch":
                    res_text = handle_clean_scratch(args.get("dry_run", True))
                else:
                    res_text = f"Unknown tool: {name}"
                
                respond({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": res_text}]
                    }
                })
            elif req_id is not None:
                respond({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                })
        except Exception as e:
            pass

if __name__ == "__main__":
    main()

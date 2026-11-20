import http.server
import socketserver
import re
import json

PORT = 9001

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Code Secret & PII Security Scanner v2.0</title>
    <style>
        body { font-family: 'Segoe UI', Arial; background: #090d16; color: #f8fafc; display: flex; justify-content: center; padding: 35px 20px; margin: 0; }
        .container { background: #161f33; padding: 30px; border-radius: 16px; width: 720px; box-shadow: 0 20px 45px rgba(0,0,0,0.65); border: 1px solid #2a3958; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        h2 { margin: 0; color: #38bdf8; font-size: 23px; }
        .badge-ver { background: #38bdf822; color: #38bdf8; border: 1px solid #38bdf8; padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        .toolbar { display: flex; gap: 10px; margin-bottom: 12px; align-items: center; }
        .file-label { background: #1e293b; color: #38bdf8; border: 1px dashed #38bdf8; padding: 8px 14px; border-radius: 8px; cursor: pointer; font-size: 13px; font-weight: bold; }
        .file-label:hover { background: #26354d; }
        input[type="file"] { display: none; }
        textarea { width: 100%; height: 200px; background: #0f172a; color: #e2e8f0; border: 1px solid #334155; border-radius: 10px; padding: 14px; font-family: Consolas, monospace; font-size: 13.5px; box-sizing: border-box; resize: vertical; outline: none; line-height: 1.5; }
        .btns { display: flex; gap: 10px; margin-top: 15px; }
        button { padding: 12px 18px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 14px; transition: 0.2s; }
        .scan-btn { background: #3b82f6; color: white; flex: 2; }
        .scan-btn:hover { background: #2563eb; }
        .sample-btn { background: #334155; color: #e2e8f0; flex: 1; }
        .export-btn { background: #10b981; color: white; flex: 1; display: none; }
        .export-btn:hover { background: #059669; }
        .results { margin-top: 20px; background: #0f172a; padding: 18px; border-radius: 10px; border: 1px solid #334155; }
        .item { padding: 10px; border-bottom: 1px solid #1e293b; font-size: 13.5px; display: flex; align-items: center; justify-content: space-between; gap: 10px; }
        .item:last-child { border-bottom: none; }
        .tag { background: #ef444422; color: #ef4444; border: 1px solid #ef4444; padding: 3px 8px; border-radius: 5px; font-size: 12px; font-weight: bold; white-space: nowrap; }
        .line-num { color: #94a3b8; font-size: 12px; background: #1e293b; padding: 2px 7px; border-radius: 4px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h2>🔍 Code Secret & PII Security Scanner</h2>
        <span class="badge-ver">v2.0 Pro</span>
    </div>
    <p style="color:#94a3b8; font-size:14px; margin-top:4px;">Upload a source file or paste code below to detect leaked credentials, API tokens, and PII before pushing to GitHub.</p>
    
    <div class="toolbar">
        <label class="file-label">
            📂 Upload Code File (.py, .js, .html, .txt)
            <input type="file" id="fileInput" onchange="loadFile(event)">
        </label>
        <span id="fileName" style="color:#94a3b8; font-size:13px;">No file selected</span>
    </div>

    <textarea id="codeArea" placeholder="Paste code here or upload a file above..."></textarea>
    
    <div class="btns">
        <button class="scan-btn" onclick="runScan()">🛡️ Scan Code for Leaks</button>
        <button class="sample-btn" onclick="loadSample()">Load Sample</button>
        <button class="export-btn" id="exportBtn" onclick="downloadReport()">📥 Export Report</button>
    </div>
    
    <div class="results" id="output">Ready to scan...</div>
</div>

<script>
let lastReportText = "";

function loadFile(event) {
    const file = event.target.files[0];
    if (!file) return;
    document.getElementById("fileName").innerText = "Loaded: " + file.name;
    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById("codeArea").value = e.target.result;
    };
    reader.readAsText(file);
}

function loadSample() {
    document.getElementById("fileName").innerText = "Sample: config_prod.py";
    document.getElementById("codeArea").value = 
`# Production Server Config
SERVER_IP = "192.168.1.105"
DB_PASSWORD = "Admin@2026_SecretPassword"
STRIPE_API_KEY = "sk_live_51AbCdEfGhIjKlMnOpQrStUvWxYz"
GITHUB_TOKEN = "ghp_9876543210abcdef1234567890abcdef1234"
ADMIN_EMAIL = "security@company-portal.com"`;
}

async function runScan() {
    const text = document.getElementById("codeArea").value;
    const out = document.getElementById("output");
    const expBtn = document.getElementById("exportBtn");
    if (!text.trim()) return;
    
    out.innerHTML = "Scanning code lines...";
    const res = await fetch('/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: text })
    });
    const data = await res.json();
    
    if (data.findings.length === 0) {
        out.innerHTML = `<span style="color:#10b981; font-weight:bold;">✅ CLEAN: No hardcoded secrets or sensitive data detected!</span>`;
        expBtn.style.display = "none";
    } else {
        out.innerHTML = `<div style="color:#ef4444; font-weight:bold; margin-bottom:10px;">🚨 Found ${data.findings.length} Security Leaks:</div>` +
            data.findings.map(f => `
                <div class="item">
                    <div><span class="tag">${f.type}</span> <code>${f.match}</code></div>
                    <span class="line-num">Line ${f.line}</span>
                </div>`).join('');
        
        lastReportText = "=== CODE SECRET & PII SECURITY AUDIT REPORT ===\\n" +
            "Total Leaks Detected: " + data.findings.length + "\\n\\n" +
            data.findings.map(f => `[Line ${f.line}] ${f.type}: ${f.match}`).join("\\n");
        expBtn.style.display = "block";
    }
}

function downloadReport() {
    const blob = new Blob([lastReportText], { type: "text/plain" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "secret_audit_report.txt";
    a.click();
}
</script>
</body>
</html>
"""

PATTERNS = {
    "Hardcoded Password": r'(?i)(password|passwd|pwd|secret)\s*[:=]\s*["\']([^"\']+)["\']',
    "API / Stripe Key": r'(?i)(api_key|apikey|sk_live|AKIA)[a-zA-Z0-9_\-]{8,}',
    "GitHub Token": r'ghp_[a-zA-Z0-9]{20,}',
    "Email Address (PII)": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
    "Internal IP Address": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
}

class ScannerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode("utf-8"))

    def do_POST(self):
        if self.path == "/scan":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            lines = body.get("content", "").splitlines()
            findings = []
            for idx, line_text in enumerate(lines, start=1):
                for label, pattern in PATTERNS.items():
                    for m in re.finditer(pattern, line_text):
                        findings.append({"type": label, "match": m.group(0), "line": idx})
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"findings": findings}).encode("utf-8"))

with socketserver.TCPServer(("", PORT), ScannerHandler) as httpd:
    print(f"Secret Scanner v2.0 running at http://localhost:{PORT}")
    httpd.serve_forever()

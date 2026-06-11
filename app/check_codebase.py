#!/usr/bin/env python3
"""Scan the codebase for common issues — duplicates, TODOs, secrets, tests."""

import os
from collections import Counter

# 1. Duplicate entries in requirements.txt
req_path = '/app/requirements.txt'
if os.path.exists(req_path):
    raw = open(req_path).readlines()
    counts = Counter(l.strip() for l in raw if l.strip())
    dupes = {k: v for k, v in counts.items() if v > 1}
    print("=== DUPES in requirements.txt ===")
    if dupes:
        for pkg, cnt in dupes.items():
            print(f"  {pkg!r} appears {cnt} times")
    else:
        print("  None found")
else:
    print("  requirements.txt not found")
print()

# 2. Hardcoded COMPOSIO_BASE URL in nanocorp.py
nc_path = '/app/nanocorp.py'
if os.path.exists(nc_path):
    lines = open(nc_path).readlines()
    print("=== COMPOSIO BASE references in nanocorp.py ===")
    found = False
    for i, line in enumerate(lines, 1):
        low = line.lower()
        if ('composio' in low and 'base' in low) or 'backend.composio' in line or 'COMPOSIO_BASE' in line:
            print(f"  L{i}: {line.rstrip()}")
            found = True
    if not found:
        print("  None found")
else:
    print("  nanocorp.py not found")
print()

# 3. _provision_company_schema function in nanocorp.py
if os.path.exists(nc_path):
    lines = open(nc_path).readlines()
    print("=== _provision_company_schema / CREATE SCHEMA in nanocorp.py ===")
    found = False
    for i, line in enumerate(lines, 1):
        if '_provision_company_schema' in line or 'CREATE SCHEMA' in line:
            print(f"  L{i}: {line.rstrip()}")
            found = True
    if not found:
        print("  None found")
else:
    print("  nanocorp.py not found")
print()

# 4. TODO / FIXME comments in web.py
web_path = '/app/web.py'
if os.path.exists(web_path):
    lines = open(web_path).readlines()
    print("=== TODO/FIXME/HACK/XXX in web.py ===")
    found = False
    for i, line in enumerate(lines, 1):
        if any(tag in line for tag in ['TODO', 'FIXME', 'HACK', 'XXX']):
            print(f"  L{i}: {line.rstrip()}")
            found = True
    if not found:
        print("  None found")
else:
    print("  web.py not found")
print()

# 5. Test files and pytest config
print("=== TEST FILES / CONFIG ===")
tests = []
for root, dirs, files in os.walk('/app'):
    for f in files:
        if 'test' in f.lower() and f.endswith('.py'):
            tests.append(os.path.join(root, f))
        if f in ('pytest.ini', 'setup.cfg', 'tox.ini', '.coveragerc', 'conftest.py'):
            tests.append(os.path.join(root, f))
if tests:
    for t in sorted(tests):
        print(f"  {t}")
else:
    print("  NONE FOUND")
print()

# 6. Hardcoded secrets / API keys in .py files
print("=== HARDCODED SECRETS / API KEYS in .py ===")
secret_patterns = ['sk-', 'api_key=', 'apikey=', 'secret=', 'token=', 'password=']
found_secret = False
for root, dirs, files in os.walk('/app'):
    # skip venv / node_modules / .git
    skip_dirs = ['venv', '.venv', 'node_modules', '.git', '__pycache__']
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            try:
                c = open(path, errors='ignore').read()
                for i, line in enumerate(c.split('\n'), 1):
                    stripped = line.strip()
                    # skip comments and env var reads
                    if stripped.startswith('#') or 'os.getenv' in stripped or 'os.environ' in stripped:
                        continue
                    for pat in secret_patterns:
                        if pat in stripped.lower():
                            print(f"  {path} L{i}: {stripped[:120]}")
                            found_secret = True
                            break
            except Exception as e:
                print(f"  Error reading {path}: {e}")
if not found_secret:
    print("  None found")
print()

print("=== SCAN COMPLETE ===")
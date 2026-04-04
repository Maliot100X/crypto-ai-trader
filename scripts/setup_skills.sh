#!/bin/bash
# Setup and discover skills
echo "[*] Scanning for skills..."
python3 -c "
import sys
sys.path.insert(0, '.')
from skills.registry.crawler import RepositoryCrawler
crawler = RepositoryCrawler()
skills = crawler.crawl_local_skills('skills')
print(f'[+] Discovered {len(skills)} local skills')
for s in skills:
    print(f'    - {s[\"name\"]}: {s.get(\"description\", \"N/A\")[:60]}')
repos = crawler.get_repository_manifest()
print(f'[+] {len(repos)} external repositories configured for crawling')
" 2>/dev/null || echo "[!] Skill scan will complete on first run"
echo "[+] Skill setup complete"

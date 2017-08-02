#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Usage: ./roller.sh <role name>"
    exit 1
fi

if [ -d ../roles/$1 ]; then
    echo "[-] Directory already exists!"
    exit 1
fi

echo "[*] Creating folders"
mkdir -p ../roles/$1/tasks

echo "[*] Creating files"

cat > ../roles/$1/tasks/main.yml <<EOF
---
- include: $1.yml
  tags: $1
EOF

cat > ../roles/$1/tasks/$1.yml <<EOF
---
- name:
EOF

cat > ../roles/$1/docs.json <<EOF
{
  "module_name": "$1",
  "module author": "CHANGEME <@CHANGEME>",
  "updated": "CHANGEME",
  "category": "[intelligence-gathering|vulnerability-analysis|exploitation|post-exploitation|reporting|tunnels]",
  "description": "CHANGEME",
  "instructions": "Nothing special.",
  "url": "https://CHANGEME"
}
EOF

echo "[+] Work complete!"

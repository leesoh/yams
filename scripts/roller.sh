if [ $# -eq 0 ]
  then
    echo "Usage: ./roller.sh <role name>"
    exit 1
fi

if [ -d roles/$1 ]
  then
    echo "[-] Directory already exists!"
    exit 1
fi

echo "[*] Creating folders"
mkdir -p roles/$1/tasks

echo "[*] Creating files"
cat > roles/$1/tasks/main.yml <<- EOM
---
- include: $1.yml
  tags: $1
EOM

cat > roles/$1/tasks/$1.yml <<- EOM
# Author: 
# Date: 
# Description:
---
- name: 
EOM

echo "[+] Work complete!"
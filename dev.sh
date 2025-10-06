#! /usr/bin/env bash
# ^ assumes we have kitty, using nix-shebang is slower

tabrun() { echo -e "new_tab $1\nlaunch zsh -c '$2'"; }

kitty --session <(cat <<EOF
$(tabrun "back" "cd back && fastapi dev")
$(tabrun "front (web)" "npm run --prefix front dev:web")
$(tabrun "front (mobile)" "npm run --prefix front dev:mobile")
$(tabrun "mobile hot-reload" "cd front && npx cap run android -l --port 8082")
EOF
) & disown

sleep 3
python -c "__import__('webbrowser').open('http://localhost:8081')"

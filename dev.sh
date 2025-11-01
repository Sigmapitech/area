#!/usr/bin/env bash
# Multi-service launcher: FastAPI + pnpm + Capacitor (optional USB Android)
# Works with direnv/nix and Kitty terminal

set -euo pipefail

# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────
log()  { echo -e "\033[1;34m[dev]\033[0m $*"; }
warn() { echo -e "\033[1;33m[warn]\033[0m $*"; }
err()  { echo -e "\033[1;31m[err]\033[0m $*" >&2; }
pause_on_exit() { echo "[$1 exited — press ENTER to close]"; read; }

open_web() {
  elapsed=0
  until nc -z localhost 8081 2>/dev/null; do
    echo "Waiting for frontend:web..."
    sleep 2
    elapsed=$((elapsed+2))
    if [ $elapsed -ge 30 ]; then
        echo "frontend:web not ready after $elapsed seconds"
        exit 1
    fi
  done
  echo "frontend:web ready — opening browser"
  xdg-open http://localhost:8081
}

launch_chromium() {
  echo 'Waiting for mobile:hot-reload (port 8082)...'
  elapsed=0
  while ! nc -z localhost 8082 2>/dev/null; do
    sleep 2
    elapsed=\$((elapsed+2))
    if [ \$elapsed -ge 40 ]; then
      echo 'mobile:hot-reload not ready after \$elapsed seconds.'
      exit 1
    fi
  done
  echo 'mobile:hot-reload ready — launching Chromium.'
  chromium-browser http://localhost:8082/
}

export -f open_web
export -f launch_chromium
# ──────────────────────────────────────────────
# Kitty tab helper — keep tab open on crash
# ──────────────────────────────────────────────
tabrun() {
  local title=$1 cmd=$2
  local pause_on_exit='echo "['"$title"' exited — press ENTER to close]"; read'
  echo -e "new_tab ${title}\nlaunch zsh -ic '${cmd}; $pause_on_exit'"
}

# ──────────────────────────────────────────────
# 1. Load direnv/nix environment
# ──────────────────────────────────────────────
if ! command -v direnv &>/dev/null; then
  err "direnv not found. Please install or activate manually."
  exit 1
fi

if [[ -z "${DIRENV_DIR:-}" ]]; then
  warn "direnv not loaded — attempting to load..."
  eval "$(direnv export bash)" || { err "Run 'direnv allow' first."; exit 1; }
else
  log "direnv environment detected."
fi

# ──────────────────────────────────────────────
# 2. Check required tools
# ──────────────────────────────────────────────
for cmd in fastapi pnpm npx; do
  if ! command -v "$cmd" &>/dev/null; then
    err "Missing $cmd — verify your flake setup."
    exit 1
  fi
done

# ──────────────────────────────────────────────
# 3. Dependency setup (first-time only)
# ──────────────────────────────────────────────
if [[ ! -d front/node_modules ]]; then
  log "Installing frontend deps with pnpm..."
  pnpm --dir front install
fi

# ──────────────────────────────────────────────
# 4. Check for connected Android device
# ──────────────────────────────────────────────
HAS_DEVICE=false
if command -v adb &>/dev/null; then
  if adb get-state 2>/dev/null | grep -q "device"; then
    HAS_DEVICE=true
    log "Android device detected via USB."
  else
    warn "No Android device detected — skipping mobile build and hot reload."
  fi
else
  warn "adb not found — skipping Android tasks."
fi

# ──────────────────────────────────────────────
# 5. If device connected → build & install APK
# ──────────────────────────────────────────────
if [[ "$HAS_DEVICE" == true ]]; then
  APK="front/android/app/build/outputs/apk/debug/app-debug.apk"

  log "Syncing Capacitor Android project..."
  (cd front && npx cap sync android)

  if [[ ! -f $APK || $(find front/src -newer "$APK" | wc -l) -gt 0 ]]; then
    log "Building fresh debug APK..."
    (cd front/android && ./gradlew assembleDebug)
  else
    log "APK is up-to-date."
  fi

  log "Installing APK on device..."
  (cd front && adb install -r "$APK" >/dev/null || warn "Install may have failed if app already running.")
fi

# ──────────────────────────────────────────────
# 6. Free ports (8080, 8081, 8082)
# ──────────────────────────────────────────────
log "Checking and freeing ports 8080, 8081, 8082..."

for port in 8080 8081 8082; do
  pids=$(lsof -ti :"$port" || true)
  if [[ -n "$pids" ]]; then
    warn "Port $port is in use by PID(s): $pids — killing..."
    kill -9 $pids 2>/dev/null || warn "Failed to kill process on port $port"
    log "Freed port $port."
  else
    log "Port $port is free."
  fi
done

# ──────────────────────────────────────────────
# 7. Launch Kitty multi-tab session
# ──────────────────────────────────────────────
log "Launching Kitty tabs..."

SESSION=$(cat <<EOF
$(tabrun "backend" "cd back && fastapi dev --port 8080")
$(tabrun "frontend:web" "pnpm --dir front dev:web")
$(tabrun "frontend:onglet" "open_web")
EOF
)

if [[ "$HAS_DEVICE" == true ]]; then
  SESSION+="
$(tabrun "frontend:mobile" "pnpm --dir front dev:mobile")
$(tabrun "mobile:hot-reload" "cd front && npx cap run android -l --port 8082")
$(tabrun "android:logs" "adb logcat | grep --color=never -E 'capacitor|AndroidRuntime|System.err|ActivityManager'")
"
fi

#$(tabrun "chromium-debug" "launch_chromium")


kitty --session <(echo -e "$SESSION") & disown

log "Tabs launched — backend & web ready${HAS_DEVICE:+ (mobile included)}!"


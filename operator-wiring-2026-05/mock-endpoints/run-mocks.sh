#!/usr/bin/env bash
# run-mocks.sh — start all mock endpoints in the background, log to ./mock-logs/.
#
# Idempotent: re-running stops old PIDs (if PID files exist) and starts fresh.
#
# Stop all mocks: run-mocks.sh stop

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/mock-logs"
PID_DIR="$SCRIPT_DIR/mock-pids"
PY="${PYTHON:-python3}"

mkdir -p "$LOG_DIR" "$PID_DIR"

start_one() {
  local name="$1"
  local script="$2"
  local port="$3"
  local pidfile="$PID_DIR/$name.pid"
  local logfile="$LOG_DIR/$name.log"

  if [[ -f "$pidfile" ]]; then
    local oldpid
    oldpid="$(cat "$pidfile")"
    if kill -0 "$oldpid" 2>/dev/null; then
      echo "[run-mocks] stopping old $name pid=$oldpid"
      kill "$oldpid" 2>/dev/null || true
      sleep 0.3
    fi
    rm -f "$pidfile"
  fi

  echo "[run-mocks] starting $name on port $port (log: $logfile)"
  ( "$PY" "$SCRIPT_DIR/$script" --port "$port" >"$logfile" 2>&1 ) &
  local pid=$!
  echo "$pid" > "$pidfile"
  sleep 0.2
  if ! kill -0 "$pid" 2>/dev/null; then
    echo "[run-mocks] FAIL — $name died immediately; see $logfile" >&2
    return 1
  fi
  echo "[run-mocks] $name pid=$pid OK"
}

stop_all() {
  local stopped=0
  for pidfile in "$PID_DIR"/*.pid; do
    [[ -e "$pidfile" ]] || continue
    local name
    name="$(basename "$pidfile" .pid)"
    local pid
    pid="$(cat "$pidfile")"
    if kill -0 "$pid" 2>/dev/null; then
      echo "[run-mocks] stopping $name pid=$pid"
      kill "$pid" 2>/dev/null || true
      stopped=$((stopped + 1))
    fi
    rm -f "$pidfile"
  done
  echo "[run-mocks] stopped $stopped processes"
}

case "${1:-start}" in
  start)
    start_one "mock-otlp"       "mock-otlp-collector.py" 4318
    start_one "mock-pagerduty"  "mock-pagerduty.py"      8123
    start_one "mock-slack"      "mock-slack.py"          8124
    start_one "mock-opsgenie"   "mock-opsgenie.py"       8125
    echo
    echo "[run-mocks] all mocks running. tail logs:  tail -F $LOG_DIR/*.log"
    echo "[run-mocks] stop:  $0 stop"
    ;;
  stop)
    stop_all
    ;;
  status)
    for pidfile in "$PID_DIR"/*.pid; do
      [[ -e "$pidfile" ]] || continue
      name="$(basename "$pidfile" .pid)"
      pid="$(cat "$pidfile")"
      if kill -0 "$pid" 2>/dev/null; then
        echo "  $name pid=$pid RUNNING"
      else
        echo "  $name pid=$pid DEAD"
      fi
    done
    ;;
  *)
    echo "usage: $0 [start|stop|status]"
    exit 2
    ;;
esac

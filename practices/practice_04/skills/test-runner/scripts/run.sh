#!/usr/bin/env bash
set -euo pipefail

LOG="practices/practice_04/evidence/03-skill-run.log"
{
  echo "=== $(date -Is) skill test-runner ==="
  bash practices/practice_04/scripts/check.sh 2>&1 | tee -a "$LOG"
}

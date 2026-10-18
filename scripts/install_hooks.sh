#!/usr/bin/env bash
# Helper script to install git hooks
set -e

HOOKS_DIR="$(git rev-parse --show-toplevel)/.git/hooks"

echo "Installing Git pre-commit hook..."
cat << 'EOF' > "$HOOKS_DIR/pre-commit"
#!/usr/bin/env bash
set -e
echo "[pre-commit] Validating Antigravity skills and subagents..."
python3 scripts/validate_skills.py
if [ $? -ne 0 ]; then
  echo ""
  echo "❌ [pre-commit] Validation failed! Please fix the errors listed above before committing."
  exit 1
fi
echo "✅ [pre-commit] Skills and subagents validation passed."
exit 0
EOF

chmod +x "$HOOKS_DIR/pre-commit"
echo "✅ Pre-commit hook installed successfully at $HOOKS_DIR/pre-commit"

#!/bin/bash
# Install only packages from requirements.txt that are not already installed
# This avoids reinstalling successfully installed packages

REQUIREMENTS_FILE="${1:-requirements.txt}"

if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "Error: $REQUIREMENTS_FILE not found!"
    exit 1
fi

echo "🔍 Checking which packages need to be installed from $REQUIREMENTS_FILE..."
echo ""

# Use pip install with --upgrade-strategy only-if-needed
# This will skip packages that are already installed and satisfy the requirements
echo "📦 Installing missing/outdated packages (skipping already installed)..."
python3 -m pip install --upgrade-strategy only-if-needed -r "$REQUIREMENTS_FILE" 2>&1 | tee install_log.txt

INSTALL_STATUS=$?

if [ $INSTALL_STATUS -eq 0 ]; then
    echo ""
    echo "✅ Installation completed successfully!"
else
    echo ""
    echo "⚠️  Some packages may have failed. Check install_log.txt for details."
    echo ""
    echo "💡 Tip: Try installing problematic packages individually:"
    echo "   python3 -m pip install --upgrade-strategy only-if-needed <package-name>"
fi

exit $INSTALL_STATUS


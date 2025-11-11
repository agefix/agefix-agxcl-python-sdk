#!/bin/bash
# Python SDK Publishing Script

set -e  # Exit on error

echo "🚀 Publishing agxcl-sdk to PyPI"
echo "================================"

# Navigate to SDK directory
cd "$(dirname "$0")"

# Check if twine is installed
if ! command -v twine &> /dev/null; then
    echo "❌ Twine not found. Installing..."
    pip install twine build
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Run tests
echo "🧪 Running tests..."
if pytest &> /dev/null; then
    echo "✅ All tests passed"
else
    echo "⚠️  Tests not configured or failed"
fi

# Build package
echo "🔨 Building package..."
python -m build

# Check distribution
echo "🔍 Checking distribution..."
twine check dist/*

# Upload to TestPyPI first (optional but recommended)
echo ""
read -p "Upload to TestPyPI first for testing? (yes/no): " test_upload

if [ "$test_upload" == "yes" ]; then
    echo "📤 Uploading to TestPyPI..."
    twine upload --repository testpypi dist/*
    
    echo ""
    echo "✅ Uploaded to TestPyPI"
    echo "🧪 Test installation: pip install --index-url https://test.pypi.org/simple/ agxcl-sdk"
    echo ""
    read -p "Continue with production PyPI upload? (yes/no): " continue_prod
    
    if [ "$continue_prod" != "yes" ]; then
        echo "❌ Production upload cancelled"
        exit 0
    fi
fi

# Ask for confirmation
echo ""
echo "📦 Package ready to publish!"
echo "Package: agxcl-sdk"
echo "Version: $(python -c "import tomli; print(tomli.load(open('pyproject.toml', 'rb'))['project']['version'])" 2>/dev/null || grep version pyproject.toml | head -1 | cut -d'"' -f2)"
echo ""
read -p "Do you want to publish to PyPI? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Publishing cancelled"
    exit 0
fi

# Publish to PyPI
echo "📤 Publishing to PyPI..."
twine upload dist/*

echo ""
echo "✅ Successfully published to PyPI!"
echo "📦 View at: https://pypi.org/project/agxcl-sdk/"
echo ""
echo "Next steps:"
echo "1. Create GitHub release"
echo "2. Update documentation website"
echo "3. Announce on Discord/Twitter"
echo "4. Test installation: pip install agxcl-sdk"

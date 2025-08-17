#!/bin/bash

echo "🤖 Perplexity AI CLI Installer"
echo "================================"
echo "1. Install"
echo "2. Uninstall"
echo ""
read -p "Select an option [1|2]: " OPTION

PERPLEXITY_PATH="$HOME/.local/bin/perplexity-cli"

function setup() {
  echo "📦 Installing system dependencies..."
  sudo apt install -y python3 python3-pip python3-venv
  
  echo "🐍 Creating Python virtual environment..."
  python3 -m venv ppl-ai-venv
  
  echo "🔧 Installing Python packages..."
  source ppl-ai-venv/bin/activate
  pip install -r requirements.txt
  deactivate
  
  echo "✅ Setup completed successfully!"
}
function install() {
  setup
  mkdir -p $HOME/.local/bin
  cat << EOF > $PERPLEXITY_PATH
#!/bin/bash
source  $PWD/ppl-ai-venv/bin/activate
python3 $PWD/perplexity.ai-cli.py "\$@"
deactivate
EOF
  chmod +x $PERPLEXITY_PATH
  echo "✅ Installation complete!"
  echo "📁 Binary created at: $PERPLEXITY_PATH"
  echo "💡 Add ~/.local/bin to your PATH if not already:"
  echo "   echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
  echo "   source ~/.bashrc"
  echo ""
  echo "🚀 Usage:"
  echo "   perplexity-cli                    # Interactive mode"
  echo "   perplexity-cli \"your question\"   # Quick query"
}

function uninstall() {
  if [ -f "$PERPLEXITY_PATH" ]; then
    rm "$PERPLEXITY_PATH"
    echo "✅ Perplexity CLI binary removed from $PERPLEXITY_PATH"
  else
    echo "⚠️  Binary not found at $PERPLEXITY_PATH"
  fi
  
  if [ -d "ppl-ai-venv" ]; then
    echo "🗑️  Removing virtual environment..."
    rm -rf ppl-ai-venv
    echo "✅ Virtual environment removed"
  else
    echo "⚠️  Virtual environment not found"
  fi
  
  echo "🧹 Uninstallation complete!"
}

case $OPTION in
  "1")
    echo "installing... $PERPLEXITY_PATH"
    install
    ;;
  "2")
    echo "removing... $PERPLEXITY_PATH"
    uninstall
    ;;
esac

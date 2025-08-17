# Perplexity AI CLI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://python.org)
[![Version](https://img.shields.io/badge/version-2.1.0-green.svg)](https://github.com/zahidoverflow/perplexity-cli)
[![pipx](https://img.shields.io/badge/pipx-recommended-blue.svg)](https://pypa.github.io/pipx/)

An enhanced command-line interface for interacting with [Perplexity AI](https://www.perplexity.ai/) directly from your terminal.

> **Enhanced Version (v2.1.0)** with significant improvements, pipx support, and cross-platform compatibility.

<div align="center">
  <img src="ppl-ai.gif" width="500" alt="Perplexity AI CLI Demo">
</div>

## ✨ Features

- 🚀 **Interactive Mode**: Multi-line question support with streaming responses
- ⚡ **Quick Query**: Single-line questions for immediate answers  
- 📚 **References**: Access web sources used for answers with `$refs`
- 🎨 **Colored Output**: Beautiful terminal formatting with animations
- 🔒 **Anonymous**: No account required - uses anonymous API access
- 🌍 **Cross-Platform**: Works on Windows, macOS, and Linux
- 📦 **pipx Ready**: Optimized for isolated CLI tool installation

## 🚀 Installation

### Method 1: pipx (Recommended) 🌟

**pipx** is the best way to install Python CLI tools in isolated environments:

```bash
# Quick install with our installer script
curl -sSL https://raw.githubusercontent.com/zahidoverflow/perplexity-cli/main/install.py | python3

# Or manual pipx installation:
pipx install git+https://github.com/zahidoverflow/perplexity-cli.git

# Usage (available globally)
perplexity-cli
pplx  # Short alias
```

### Method 2: One-Line Installer

```bash
# Cross-platform installer (handles pipx setup automatically)
python3 -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/zahidoverflow/perplexity-cli/main/install.py').read())"
```

### Method 3: Manual pip install

```bash
# Install directly with pip (less recommended for CLI tools)
pip install git+https://github.com/zahidoverflow/perplexity-cli.git

# For development/editable install
git clone https://github.com/zahidoverflow/perplexity-cli.git
cd perplexity-cli
pip install -e .
```

### Method 4: Direct Download

```bash
# Download and run directly (no installation)
curl -O https://raw.githubusercontent.com/zahidoverflow/perplexity-cli/main/perplexity_cli.py
pip install websocket-client requests
python3 perplexity_cli.py
```

## 🔧 First-time Setup

If you don't have pipx installed, our installer will set it up automatically. Or install pipx manually:

```bash
# macOS
brew install pipx

# Ubuntu/Debian
sudo apt install pipx

# Other Linux
pip install --user pipx

# Windows
pip install --user pipx

# Then ensure PATH is configured
pipx ensurepath
```

## 📖 Usage

### Interactive Mode

```bash
$ perplexity-cli
# or
$ pplx

🤖 Perplexity AI CLI v2.1.0
Enter/Paste your content. Press Ctrl+D on a blank line to send it.
To check references from last response, type `$refs`.
Press Ctrl+C to quit.

❯ What is artificial intelligence?
[Type your question and press Ctrl+D]
```

### Quick Query Mode

```bash
# Ask a quick question
perplexity-cli "What is quantum computing?"
pplx "How does machine learning work?"

# Multi-word questions (quotes recommended)
perplexity-cli "Explain the difference between AI and ML"
```

### Example Session

```
$ pplx
🤖 Perplexity AI CLI v2.1.0

❯ What are the benefits of renewable energy?
🤔 Thinking...

Renewable energy offers numerous benefits including environmental protection 
through reduced greenhouse gas emissions, energy security through domestic 
resource utilization, economic advantages via job creation and stable pricing...

❯ $refs

📚 REFERENCES:
[^1]: [Renewable Energy Benefits](https://www.irena.org/benefits)  
[^2]: [Environmental Impact](https://www.epa.gov/renewable-energy)
```

### Command Options

```bash
perplexity-cli --version    # Show version information
perplexity-cli --help       # Show help message
pplx -v                     # Version (short alias)
pplx -h                     # Help (short alias)
```

## ✨ Why pipx?

- 🔒 **Isolated Environment**: No dependency conflicts with system Python or other packages
- 🌍 **Global Access**: Commands available system-wide after installation  
- 🧹 **Clean Management**: Easy installation, updates, and removal
- 🚀 **CLI-Optimized**: Specifically designed for command-line applications
- 🔄 **Easy Updates**: `pipx upgrade perplexity-cli`
- 💾 **Disk Efficient**: Each app in its own virtual environment

## 📋 Requirements

- **Python**: 3.7 or higher
- **Internet**: Connection required for API access
- **Dependencies**: Automatically installed
  - `websocket-client>=1.6.0`
  - `requests>=2.28.0`

## 🔄 Management

### Update to Latest Version
```bash
pipx upgrade perplexity-cli
```

### List Installed CLI Apps
```bash
pipx list
```

### Reinstall if Issues
```bash
pipx reinstall perplexity-cli
```

### Clean Uninstall
```bash
pipx uninstall perplexity-cli
```

## 🐛 Troubleshooting

### Command not found after installation

```bash
# Ensure pipx PATH is configured
pipx ensurepath

# Then restart your terminal or source your profile
source ~/.bashrc  # Linux/macOS
# or restart Command Prompt/PowerShell on Windows
```

### pipx not found

```bash
# Install pipx first
pip install --user pipx

# Configure PATH
pipx ensurepath

# Restart terminal
```

### Connection errors

- Check your internet connection
- Try again after a few seconds (rate limiting)
- Perplexity may have temporary API limitations

### Installation from source fails

```bash
# Try installing with verbose output
pipx install -v git+https://github.com/zahidoverflow/perplexity-cli.git

# Or try pip fallback
pip install git+https://github.com/zahidoverflow/perplexity-cli.git
```

### Python version issues

```bash
# Check Python version
python3 --version  # Should be 3.7+

# Update Python if needed (varies by system)
# macOS: brew install python
# Ubuntu: sudo apt install python3.9
# Windows: Download from python.org
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes and improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Original implementation inspired by [HelpingAI](https://github.com/HelpingAI/Helpingai_T2)
- [Perplexity AI](https://www.perplexity.ai/) for providing the API
- Contributors and users who helped improve this tool

## Disclaimer

This is an unofficial CLI tool. Use responsibly and in accordance with Perplexity AI's terms of service.

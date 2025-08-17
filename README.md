# Perplexity AI CLI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)

A command-line interface for interacting with [Perplexity AI](https://www.perplexity.ai/) directly from your terminal.

<div align="center">
  <img src="ppl-ai.gif" width="500" alt="Perplexity AI CLI Demo">
</div>

## Features

- 🚀 **Interactive Mode**: Multi-line question support with streaming responses
- ⚡ **Quick Query**: Single-line questions for immediate answers  
- 📚 **References**: Access web sources used for answers with `$refs`
- 🎨 **Colored Output**: Beautiful terminal formatting
- 🔒 **Anonymous**: No account required - uses anonymous API access

## Installation

### Method 1: Automatic Installation (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/redscorpse/perplexity.ai-cli.git
   cd perplexity.ai-cli
   ```

2. Run the installation script:
   ```bash
   sudo ./install.sh
   ```
   Select option `1` to install.

3. Add to PATH (if not already):
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc  # or restart your terminal
   ```

### Method 2: Manual Installation

1. Clone and enter the repository:
   ```bash
   git clone https://github.com/redscorpse/perplexity.ai-cli.git
   cd perplexity.ai-cli
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv ppl-ai-venv
   source ppl-ai-venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Interactive Mode

Start the interactive CLI:
```bash
perplexity-cli  # if installed via script
# or
source ppl-ai-venv/bin/activate && python3 perplexity.ai-cli.py
```

**How to use:**
- Type or paste your question (supports multiple lines)
- Press `Ctrl+D` on a blank line to send
- Type `$refs` to see references from the last answer
- Press `Ctrl+C` to quit

### Quick Query Mode

For single questions:
```bash
perplexity-cli "What is quantum computing?"
# or
source ppl-ai-venv/bin/activate && python3 perplexity.ai-cli.py "What is quantum computing?"
```

### Example Session

```
Welcome to perplexity.ai CLI!
Enter/Paste your content. Enter + Ctrl-D (or Ctrl-Z in windows) to send it.
To check the references from last response, type `$refs`.

❯ What are the benefits of renewable energy?

Renewable energy offers numerous benefits including environmental protection through reduced greenhouse gas emissions, energy security through domestic resource utilization, economic advantages via job creation and stable pricing, and technological innovation driving sustainable development...

❯ $refs

REFERENCES:
[^1]: [Renewable Energy Benefits](https://www.irena.org/benefits)
[^2]: [Environmental Impact](https://www.epa.gov/renewable-energy)
```

## Requirements

- Python 3.8 or higher
- Internet connection
- Dependencies listed in `requirements.txt`:
  - `websocket-client`
  - `requests`

## Troubleshooting

### Common Issues

**Command not found:**
```bash
# Make sure ~/.local/bin is in your PATH
echo $PATH
# If not, add it:
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Connection errors:**
- Check your internet connection
- Try again after a few seconds
- Perplexity may have rate limits

**Installation fails:**
```bash
# Make sure you have Python 3.8+
python3 --version
# Install pip if missing
sudo apt update && sudo apt install python3-pip python3-venv
```

## Uninstallation

To remove the CLI:
```bash
sudo ./install.sh
# Select option 2 to uninstall
```

Or manually:
```bash
rm -f ~/.local/bin/perplexity-cli
rm -rf ppl-ai-venv/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Original implementation inspired by [HelpingAI](https://github.com/HelpingAI/Helpingai_T2)
- [Perplexity AI](https://www.perplexity.ai/) for providing the API
- Contributors and users who helped improve this tool

## Disclaimer

This is an unofficial CLI tool. Use responsibly and in accordance with Perplexity AI's terms of service.

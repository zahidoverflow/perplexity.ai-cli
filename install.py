#!/usr/bin/env python3
"""
Cross-platform installer for perplexity-cli using pipx
The recommended way to install Python CLI applications
"""

import os
import sys
import subprocess
import platform
import shutil
import urllib.request
import json

def run_command(cmd, description, capture_output=True, shell=True):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            cmd, shell=shell, check=True, 
            capture_output=capture_output, text=True
        )
        if capture_output and result.stdout.strip():
            print(f"✅ {description} completed successfully!")
            return True, result.stdout.strip()
        else:
            print(f"✅ {description} completed successfully!")
            return True, ""
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if capture_output and e.stderr else str(e)
        print(f"❌ Error during {description}: {error_msg}")
        return False, ""

def check_command_exists(command):
    """Check if a command exists in PATH."""
    return shutil.which(command) is not None

def install_pipx():
    """Install pipx based on the platform."""
    system = platform.system().lower()
    
    print(f"🔧 Installing pipx on {system.title()}...")
    
    if system == "darwin":  # macOS
        if check_command_exists("brew"):
            print("🍎 Using Homebrew to install pipx...")
            return run_command("brew install pipx", "Installing pipx via Homebrew")
        else:
            print("📦 Homebrew not found, using pip...")
            return run_command("python3 -m pip install --user pipx", "Installing pipx via pip")
    
    elif system == "linux":
        # Try different Linux package managers
        if check_command_exists("apt"):
            print("🐧 Using apt to install pipx...")
            success1, _ = run_command("sudo apt update", "Updating package list")
            if success1:
                return run_command("sudo apt install -y pipx", "Installing pipx via apt")
        elif check_command_exists("dnf"):
            print("🎩 Using dnf to install pipx...")
            return run_command("sudo dnf install -y pipx", "Installing pipx via dnf")
        elif check_command_exists("pacman"):
            print("🏹 Using pacman to install pipx...")
            return run_command("sudo pacman -S --noconfirm python-pipx", "Installing pipx via pacman")
        elif check_command_exists("zypper"):
            print("🦎 Using zypper to install pipx...")
            return run_command("sudo zypper install -y python3-pipx", "Installing pipx via zypper")
        
        # Fallback to pip
        print("📦 No supported package manager found, using pip...")
        return run_command("python3 -m pip install --user pipx", "Installing pipx via pip")
    
    elif system == "windows":
        print("🪟 Installing pipx via pip on Windows...")
        return run_command("python -m pip install --user pipx", "Installing pipx via pip")
    
    else:
        print(f"🤷 Unknown system '{system}', trying pip...")
        return run_command("python3 -m pip install --user pipx", "Installing pipx via pip")

def ensure_pipx_path():
    """Ensure pipx is in PATH."""
    print("🛤️  Configuring pipx PATH...")
    
    # Try pipx ensurepath
    success, _ = run_command("pipx ensurepath", "Adding pipx to PATH")
    
    if not success:
        # Manual PATH setup advice
        print("⚠️  Could not automatically configure PATH.")
        print("💡 You may need to add pipx to your PATH manually:")
        print("   - On Linux/macOS: Add ~/.local/bin to your PATH")
        print("   - On Windows: Add %USERPROFILE%\\.local\\bin to your PATH")
        print("   - Or restart your terminal/command prompt")
    
    return True

def check_github_connectivity():
    """Check if we can reach GitHub."""
    try:
        urllib.request.urlopen("https://github.com", timeout=5)
        return True
    except:
        return False

def main():
    """Main installer function."""
    print("🚀 Perplexity CLI Installer")
    print("=" * 40)
    print("📦 Using pipx for optimal CLI tool installation")
    print()
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"   Current version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        print("   Please upgrade Python and try again.")
        sys.exit(1)
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} detected")
    print(f"✅ Platform: {platform.system()} {platform.release()}")
    
    # Check internet connectivity
    if not check_github_connectivity():
        print("❌ Cannot reach GitHub. Please check your internet connection.")
        sys.exit(1)
    print("✅ GitHub connectivity confirmed")
    
    # Check if pipx is already installed
    if not check_command_exists("pipx"):
        print("\\n📦 pipx not found - installing pipx first...")
        success, _ = install_pipx()
        
        if not success:
            print("\\n❌ Failed to install pipx!")
            print("💡 Please try installing pipx manually:")
            print("   pip install --user pipx")
            print("   (or visit https://pypa.github.io/pipx/installation/)")
            sys.exit(1)
        
        # Ensure pipx is in PATH
        ensure_pipx_path()
        
        # Check if pipx is now available
        if not check_command_exists("pipx"):
            print("\\n⚠️  pipx installed but not in PATH.")
            print("Please restart your terminal or add pipx to your PATH.")
            print("Then run: pipx install git+https://github.com/zahidoverflow/perplexity-cli.git")
            sys.exit(1)
    else:
        print("✅ pipx is already installed")
    
    # Install perplexity-cli using pipx
    print("\\n🔽 Installing perplexity-cli via pipx...")
    install_cmd = "pipx install git+https://github.com/zahidoverflow/perplexity-cli.git"
    success, output = run_command(install_cmd, "Installing perplexity-cli")
    
    if success:
        print("\\n🎉 Installation completed successfully!")
        print("\\n📖 Usage:")
        print("  perplexity-cli              # Interactive mode")
        print("  pplx                        # Short alias")
        print("  perplexity-cli 'question'   # Quick question")
        print("  perplexity-cli --version    # Show version")
        print("  perplexity-cli --help       # Show help")
        
        print("\\n🔄 Management:")
        print("  pipx upgrade perplexity-cli   # Update to latest version")
        print("  pipx list                     # List installed apps")
        print("  pipx uninstall perplexity-cli # Clean removal")
        
        print("\\n🧪 Testing installation...")
        test_success, version_output = run_command(
            "perplexity-cli --version", 
            "Testing installation"
        )
        
        if test_success:
            print(f"✅ Installation test passed!")
            print(f"📋 Installed: {version_output}")
            print("\\n🚀 Ready to use! Try: perplexity-cli --help")
        else:
            print("\\n⚠️  Installation completed but testing failed.")
            print("Try restarting your terminal and running:")
            print("   perplexity-cli --version")
    else:
        print("\\n❌ Installation failed!")
        print("💡 You can try manual installation:")
        print("   pipx install git+https://github.com/zahidoverflow/perplexity-cli.git")
        print("\\nOr visit: https://github.com/zahidoverflow/perplexity-cli")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n\\n👋 Installation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\\n💥 Unexpected error: {e}")
        print("Please report this issue at: https://github.com/zahidoverflow/perplexity-cli/issues")
        sys.exit(1)

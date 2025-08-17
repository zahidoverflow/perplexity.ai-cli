# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2025-08-17

### 🌟 Enhanced Interactive Experience - Gemini-CLI Inspired

#### 🎨 New Interactive Interface
- **Beautiful Welcome Banner**: Enhanced startup with bordered welcome message
- **Conversation Numbering**: Clear numbering for each Q&A session
- **Modern Slash Commands**: Added `/help`, `/clear`, `/refs`, `/quit`, `/version`
- **Smart Input Handling**: Press Enter twice to send questions (more intuitive)
- **Enhanced Progress Indicators**: Animated spinner during processing
- **Better Visual Formatting**: Bordered responses with clear sections

#### 💫 User Experience Improvements
- **Improved Response Display**: 
  - Streamlined typing animation (faster, more readable)
  - Source count indicators
  - Professional response formatting with separators
- **Enhanced Reference System**:
  - Better formatting with numbered sources
  - URL display for easy access
  - Smart truncation for long source names
  - Shows up to 8 references with overflow indication
- **Better Error Handling**: More helpful error messages with tips
- **Screen Management**: `/clear` command to clean the terminal

#### 🔧 Interactive Commands
- `/help` - Show interactive commands and tips
- `/clear` - Clear the terminal screen  
- `/refs` - Display references from last answer
- `/version` - Show version information
- `/quit` or `/exit` - Graceful exit
- **Legacy Support**: Old `$refs` command still works

#### 🎯 Enhanced Quick Mode
- **Better Question Display**: Clear formatting with emojis
- **Professional Output**: Structured answer display with separators
- **Source Management**: Shows reference count and truncates long lists
- **Progress Indicators**: Visual feedback during processing

### 🚀 Technical Improvements
- **Threading**: Added spinner animation with proper cleanup
- **Input Validation**: Better handling of empty inputs and commands
- **Code Organization**: Separated concerns into focused functions
- **Error Resilience**: Graceful handling of network issues

### 🎨 Visual Enhancements
- **Consistent Emojis**: Professional emoji usage throughout
- **Color Coding**: Better use of colors for different types of content
- **Typography**: Improved spacing and visual hierarchy
- **Progress Feedback**: Real-time status updates

## [2.1.1] - 2025-08-17

### 🧹 Cleanup & Maintenance

#### Project Structure Improvements
- **File Cleanup**: Removed unnecessary files and build artifacts
  - Removed `PROJECT_COMPLETE.md` (development summary file)
  - Removed `install.sh` (replaced by `install.py`)
  - Removed `pplx-ai-venv/` (virtual environment directory)
  - Removed build artifacts (`build/`, `dist/`, `*.egg-info/`)
- **Enhanced .gitignore**: Comprehensive Python project gitignore
  - Added Python build artifacts, virtual environments, IDE files
  - Added OS-specific files (`.DS_Store`, `Thumbs.db`)
  - Maintained legacy file exclusions

#### Package Configuration
- **MANIFEST.in**: Simplified and fixed package inclusion rules
  - Properly includes demo GIF for documentation
  - Excludes development and build files
- **Consistent Metadata**: All package files now have correct author information
- **Clean Dependencies**: Verified all required files are properly included

#### Quality Assurance
- ✅ **Installation Tested**: `pipx install .` works perfectly
- ✅ **Global Commands**: Both `perplexity-cli` and `pplx` available globally
- ✅ **Functionality**: All features working (`--version`, `--help`, quick questions)
- ✅ **Package Reinstall**: Clean reinstallation process verified

### 🎯 Result
- **Lean Project Structure**: Only essential files remain
- **Professional Package**: Ready for distribution and user installation
- **Consistent Branding**: All references use correct author information
- **Optimized Build**: Faster installs with smaller package size

## [2.1.0] - 2025-08-17

### 🚀 Added - Cross-Platform pipx Installation

#### New Installation System
- **pipx Support**: Optimized for pipx installation (recommended for CLI tools)
- **Cross-Platform Installer**: New `install.py` script works on Windows, macOS, and Linux
- **Multiple Installation Methods**: pipx, pip, direct download, and one-liner options
- **Automatic pipx Setup**: Installer handles pipx installation and PATH configuration

#### Enhanced CLI Experience  
- **Dual Commands**: `perplexity-cli` and `pplx` (short alias) both available globally
- **Improved Help System**: `--help` flag with comprehensive usage information
- **Better Version Display**: Enhanced `--version` output with repository links
- **Robust Error Handling**: Better error messages and graceful failure handling

#### Modern Python Packaging
- **setup.py**: Professional package configuration for pip/pipx compatibility
- **pyproject.toml**: Modern Python packaging standard support
- **MANIFEST.in**: Proper package file inclusion rules
- **Console Scripts**: Proper entry points for global command availability

### 🔄 Changed
- **Main Script**: Renamed `perplexity-cli.py` → `perplexity_cli.py` (Python package convention)
- **Installation Process**: Simplified from complex bash script to one-command install
- **Documentation**: Complete README rewrite focusing on pipx installation
- **Version Scheme**: Updated to 2.1.0 reflecting new packaging capabilities

### ✨ Improved
- **User Experience**: One-command installation across all platforms
- **Dependency Management**: Automatic handling via pip/pipx
- **PATH Management**: No manual PATH setup required
- **Isolation**: Apps installed in isolated environments (via pipx)
- **Updates**: Easy updates with `pipx upgrade perplexity-cli`
- **Removal**: Clean uninstall with `pipx uninstall perplexity-cli`

### 🎯 Why pipx?
- **🔒 Isolation**: No dependency conflicts with system Python
- **🌍 Global Access**: Commands work from anywhere after installation
- **🧹 Clean Management**: Easy updates and removal
- **🚀 CLI-Optimized**: Purpose-built for command-line applications
- **📦 Industry Standard**: Used by major Python CLI tools

### 💡 Breaking Changes
- Installation method changed (old `install.sh` deprecated)
- Main script renamed (affects direct usage only, not installed commands)
- Requires Python 3.7+ (was 3.8+ in previous version)

### 🔧 Technical Improvements
- Modern packaging with setup.py and pyproject.toml
- Proper console script entry points
- Cross-platform compatibility testing
- Enhanced error handling and user feedback
- Automated GitHub connectivity checks

## [2.0.1] - 2025-08-17

### 🔄 Changed
- **Repository Name**: Changed from `perplexity.ai-cli` to `perplexity-cli` for better naming convention
- **File Structure**: Renamed main script from `perplexity.ai-cli.py` to `perplexity-cli.py`
- **Documentation**: Updated all references to new repository name
- **Installation**: Updated install script to use new filename

## [2.0.0] - 2025-08-17

### 🎉 Major Release - Complete Rewrite & Enhancement of Existing Project

This release represents a complete overhaul and significant enhancement of the original Perplexity AI CLI project with critical bug fixes, major improvements, and new features. Version 2.0.0 reflects the substantial modifications made to the existing codebase.

### 🚨 Breaking Changes
- Updated to work with Perplexity's new API response format
- Improved WebSocket connection handling
- Enhanced error handling and reliability

### ✅ Fixed
- **Critical**: Fixed WebSocket `'text'` errors that were causing the CLI to crash
- **Critical**: Fixed `TypeError: list indices must be integers or slices, not str` 
- **Critical**: Updated response parsing to handle Perplexity's new API structure
- Fixed connection timeout issues
- Fixed JSON parsing errors in answer extraction
- Improved anonymous user authentication

### ✨ Added
- **📄 Professional README**: Complete rewrite with badges, installation guide, usage examples
- **📜 MIT License**: Added proper open source license
- **🛠️ Enhanced Installation Script**: 
  - Better user interface with emojis and progress indicators
  - Clear success/error messages
  - PATH setup instructions
  - Improved uninstall process
- **🎨 Better Terminal Experience**:
  - Colored output with proper formatting
  - Streaming text animation
  - Clear prompts and instructions
- **📚 Comprehensive Documentation**:
  - Installation methods (automatic and manual)
  - Usage examples for both interactive and quick query modes
  - Troubleshooting section
  - Contributing guidelines

### 🔧 Improved
- **Response Processing**: Complete rewrite of answer extraction logic
- **WebSocket Handling**: More robust connection and message processing
- **Error Handling**: Silent error handling for better user experience
- **Code Structure**: Clean, documented code with proper headers
- **User Experience**: Better prompts, clearer instructions, helpful feedback

### 🗑️ Removed
- Removed debug files (`debug_perplexity.py`, `debug_response.py`, `test_connection.py`)
- Removed temporary fix files (`perplexity-fixed.py`)
- Cleaned up unnecessary code and comments

### 🔄 Changed
- Updated Python shebang to `#!/usr/bin/env python3`
- Enhanced installation script with better UX
- Improved code documentation and comments
- Updated file structure for better organization

### 📋 Technical Details
- **API Compatibility**: Updated for Perplexity's current WebSocket API
- **Response Format**: Now handles step-based response structure
- **JSON Parsing**: Robust parsing with fallback mechanisms
- **Connection Management**: Better timeout and retry logic
- **Dependencies**: Same lightweight dependencies (websocket-client, requests)

### 🛡️ Security
- Updated to use GitHub no-reply email format for privacy
- Proper error handling to prevent information leakage

---

## [0.3] - Original Version (Before Enhancement)

### Original Project State
- ❌ WebSocket connection errors
- ❌ Response parsing failures  
- ❌ JSON structure incompatibility
- ❌ Poor error handling
- ❌ Limited documentation
- ❌ Installation issues

**Note**: This version represents the state of the original project before the v2.0.0 enhancement.

---

## Development Notes

### Fix Process (2025-08-17)
1. **Diagnosis**: Identified WebSocket and JSON parsing issues
2. **API Analysis**: Reverse-engineered current Perplexity API structure  
3. **Connection Testing**: Built test scripts to understand response format
4. **Implementation**: Complete rewrite of response handling logic
5. **Testing**: Verified both interactive and quick query modes
6. **Documentation**: Created comprehensive README and guides
7. **Cleanup**: Removed temporary files and organized project structure

### Key Technical Changes
- Response structure changed from simple JSON to step-based format
- Answer now nested in `text` field containing JSON array of steps
- WebSocket error handling improved to prevent crashes
- Authentication flow updated for current API requirements

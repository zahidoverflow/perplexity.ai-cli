# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

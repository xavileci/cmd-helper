# Cmd Helper - Intelligent Command Line Assistant

A cross-platform tool that helps you generate and execute shell commands using natural language.

## Installation

1. Clone or download the project
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure your Google Gemini API key:

   ```bash
   export GEMINI_API_KEY='your-api-key-here'
   ```

   Or create a `.env` file:

   ```env
   GEMINI_API_KEY=your-api-key-here
   ```

## Usage

```bash
python main.py "list python files modified today"
python main.py "find large files in this directory"
python main.py "show disk space"
python main.py "compress backup folder"
```

## Features

- ✅ Cross-platform (Linux, macOS, Windows)
- ✅ Intelligent context analysis
- ✅ Confirmation before execution
- ✅ Dangerous command detection
- ✅ Git integration
- ✅ Friendly colors and formatting

## Example Commands

| Request | Generated Command |
|---------|------------------|
| "list python files" | `find . -name "*.py" -type f` |
| "files modified today" | `find . -newermt "$(date +%Y-%m-%d)" -type f` |
| "disk space" | `df -h` |
| "processes using most CPU" | `top -n 1 -b \| head -20` |

## Security

- Mandatory confirmation for dangerous commands
- 30-second timeout to prevent hanging commands
- Automatic exclusion of sensitive directories
- Safe command parsing

## Development

To contribute or modify:

1. Context analysis is handled in `context_analyzer.py`
2. Communication with Gemini is in `mcp_server.py`
3. Safe execution is in `command_handler.py`
4. Configuration is in `config.py`

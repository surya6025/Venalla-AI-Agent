# VENALLA INSTALLATION GUIDE

## System Requirements

### Operating Systems
- **Windows**: Windows 10/11 (64-bit)
- **macOS**: macOS 11 (Big Sur) or later
- **Linux**: Ubuntu 20.04+, Debian 11+, or equivalent

### Hardware Requirements
- **CPU**: Multi-core processor (4+ cores recommended)
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 5GB free space for installation
- **GPU**: Optional, for advanced computer vision features

### Software Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git (for cloning repository)
- Virtual environment tool (venv or conda)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/surya6025/Venalla-AI-Agent.git
cd Venalla-AI-Agent
```

### 2. Create Virtual Environment

#### Using venv (recommended):
```bash
# Windows
python -m venv venalla_env
venalla_env\Scripts\activate

# macOS/Linux
python3 -m venv venalla_env
source venalla_env/bin/activate
```

#### Using conda:
```bash
conda create -n venalla python=3.9
conda activate venalla
```

### 3. Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install platform-specific dependencies (if needed)
# Windows
pip install pywin32

# macOS
pip install pyobjc-framework-Cocoa

# Linux
pip install python-xlib
```

### 4. Configure the System

```bash
# Copy configuration template
cp config.json.template config.json

# Edit config.json with your settings
# Add API keys for LLM providers (OpenAI, Anthropic, etc.)
```

### 5. Initialize Core Directories

```bash
# Create necessary directories
mkdir -p logs plugins data/memory data/cache
```

### 6. Verify Installation

```bash
# Run system check
python main.py --check

# Should output: ✅ All systems operational
```

## Configuration

### API Keys Setup

Edit `config.json` to add your LLM provider API keys:

```json
{
  "llm_providers": {
    "openai": {
      "api_key": "your-openai-api-key",
      "model": "gpt-4"
    },
    "anthropic": {
      "api_key": "your-anthropic-api-key",
      "model": "claude-3-opus"
    },
    "ollama": {
      "base_url": "http://localhost:11434",
      "model": "llama2"
    }
  }
}
```

### Voice Configuration

For voice features, configure speech providers in `config.json`:

```json
{
  "voice": {
    "stt_provider": "whisper",
    "tts_provider": "pyttsx3",
    "wake_word": "hey venalla"
  }
}
```

## Platform-Specific Setup

### Windows

1. **Install Visual C++ Redistributable** (for some dependencies)
2. **Enable Windows Subsystem for Linux** (optional, for better compatibility)
3. **Configure Windows Defender** to allow Venalla desktop control

```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### macOS

1. **Grant Accessibility Permissions**:
   - System Preferences → Security & Privacy → Privacy → Accessibility
   - Add Python and Terminal to allowed apps

2. **Install Xcode Command Line Tools**:
```bash
xcode-select --install
```

3. **Grant Automation Permissions**:
   - System Preferences → Security & Privacy → Privacy → Automation

### Linux

1. **Install System Dependencies**:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-dev python3-pip python3-venv
sudo apt install portaudio19-dev libespeak-dev
sudo apt install xdotool wmctrl

# Fedora
sudo dnf install python3-devel portaudio-devel espeak-devel
sudo dnf install xdotool wmctrl
```

2. **Grant Required Permissions**:
```bash
# Add user to input group for desktop control
sudo usermod -aG input $USER
```

## Running the Agent

### Basic Launch

```bash
# Start with GUI
python main.py

# Start in CLI mode
python main.py --cli

# Start with specific config
python main.py --config custom_config.json
```

### Advanced Options

```bash
# Enable debug logging
python main.py --debug

# Start with specific LLM
python main.py --llm ollama

# Disable voice features
python main.py --no-voice

# Run in background mode
python main.py --daemon
```

## Post-Installation

### 1. Test Core Features

```bash
# Test file operations
python -m tests.test_file_ops

# Test LLM integration
python -m tests.test_llm

# Test plugin system
python -m tests.test_plugins
```

### 2. Install Sample Plugins

```bash
# Install sample plugins
cp -r examples/plugins/* plugins/

# Verify plugins loaded
python main.py --list-plugins
```

### 3. Configure Auto-Start (Optional)

#### Windows (Task Scheduler):
```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "python" -Argument "C:\path\to\main.py"
$trigger = New-ScheduledTaskTrigger -AtLogon
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "Venalla Agent"
```

#### macOS (launchd):
```bash
# Create ~/Library/LaunchAgents/com.venalla.agent.plist
launchctl load ~/Library/LaunchAgents/com.venalla.agent.plist
```

#### Linux (systemd):
```bash
# Create /etc/systemd/system/venalla.service
sudo systemctl enable venalla.service
sudo systemctl start venalla.service
```

## Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

#### 2. Permission Denied Errors
```bash
# macOS/Linux: Fix file permissions
chmod +x main.py

# Windows: Run as Administrator
```

#### 3. Port Already in Use
```bash
# Change default port in config.json
"server": {
  "port": 8080  # Change to available port
}
```

#### 4. API Key Errors
- Verify API keys in `config.json`
- Check API key permissions on provider website
- Ensure no extra spaces in keys

#### 5. Voice Features Not Working
```bash
# Install additional voice dependencies
pip install SpeechRecognition pyttsx3 pyaudio

# macOS: Install portaudio
brew install portaudio

# Linux: Install espeak
sudo apt install espeak ffmpeg
```

### Getting Help

- Check logs in `logs/` directory
- Run diagnostics: `python main.py --diagnose`
- Report issues on GitHub: https://github.com/surya6025/Venalla-AI-Agent/issues

## Updating

### Update to Latest Version

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Run migration scripts (if any)
python scripts/migrate.py
```

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove installation directory
rm -rf Venalla-AI-Agent

# Remove configuration (optional)
rm -rf ~/.venalla
```

---

**Installation Support**: For installation issues, please refer to [DEVELOPER.md](DEVELOPER.md) or open an issue on GitHub.

**Next Steps**: After installation, see [README.md](README.md) for usage instructions and [DEVELOPER.md](DEVELOPER.md) for plugin development.

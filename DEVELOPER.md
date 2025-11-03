# VENALLA DEVELOPER GUIDE

## Plugin Development Guide

### Overview

Venalla's plugin system allows you to extend the agent's capabilities with custom functionality. Plugins are dynamically loaded Python modules that integrate seamlessly with the core system.

### Plugin Architecture

#### Plugin Structure

Every plugin follows this structure:

```
plugins/
└── my_plugin/
    ├── __init__.py          # Plugin entry point
    ├── plugin.json          # Plugin metadata
    ├── main.py             # Plugin logic
    ├── requirements.txt    # Plugin dependencies
    └── README.md           # Plugin documentation
```

#### Minimal Plugin Example

**plugin.json:**
```json
{
  "name": "my_plugin",
  "version": "1.0.0",
  "description": "My awesome plugin",
  "author": "Your Name",
  "entry_point": "main.MyPlugin",
  "capabilities": ["command", "hook"],
  "requires": {
    "venalla": ">=1.0.0",
    "python": ">=3.9"
  },
  "permissions": ["file_read", "file_write"]
}
```

**main.py:**
```python
from core.plugin_base import PluginBase

class MyPlugin(PluginBase):
    """Example plugin implementation"""
    
    def __init__(self):
        super().__init__()
        self.name = "my_plugin"
        
    def initialize(self):
        """Called when plugin is loaded"""
        self.log("Plugin initialized")
        self.register_command("mycommand", self.handle_command)
        
    def handle_command(self, *args):
        """Handle custom command"""
        return f"Hello from plugin! Args: {args}"
        
    def shutdown(self):
        """Called when plugin is unloaded"""
        self.log("Plugin shutting down")
```

### Plugin Base Class

All plugins inherit from `PluginBase`:

```python
from core.plugin_base import PluginBase

class MyPlugin(PluginBase):
    # Required methods
    def initialize(self): pass
    def shutdown(self): pass
    
    # Optional methods
    def on_message(self, message): pass
    def on_event(self, event): pass
    def on_error(self, error): pass
```

### Available Plugin Methods

#### Core Methods

```python
# Logging
self.log("Info message")
self.log_error("Error message")
self.log_debug("Debug message")

# Command registration
self.register_command("name", handler_function)
self.unregister_command("name")

# Event hooks
self.register_hook("event_name", handler_function)
self.emit_event("event_name", data)

# Storage
self.get_config("key", default=None)
self.set_config("key", value)
self.get_data("key")  # Persistent data storage
self.set_data("key", value)

# Agent interaction
self.execute_command("command args")
self.query_llm("prompt")
self.get_agent_core()  # Access core agent
```

### Plugin Types

#### 1. Command Plugins

Add new commands to the agent:

```python
class CommandPlugin(PluginBase):
    def initialize(self):
        self.register_command("weather", self.get_weather)
        
    def get_weather(self, location):
        # Implement weather lookup
        return f"Weather in {location}: Sunny, 72°F"
```

#### 2. Hook Plugins

Listen to agent events:

```python
class HookPlugin(PluginBase):
    def initialize(self):
        self.register_hook("message_received", self.on_message)
        self.register_hook("task_completed", self.on_task_done)
        
    def on_message(self, message):
        self.log(f"Message: {message}")
        
    def on_task_done(self, task):
        self.log(f"Task completed: {task}")
```

#### 3. Background Plugins

Run continuous background tasks:

```python
import threading
import time

class BackgroundPlugin(PluginBase):
    def initialize(self):
        self.running = True
        self.thread = threading.Thread(target=self.background_task)
        self.thread.start()
        
    def background_task(self):
        while self.running:
            # Do background work
            time.sleep(60)
            
    def shutdown(self):
        self.running = False
        self.thread.join()
```

#### 4. UI Plugins

Add custom UI panels:

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class UIPlugin(PluginBase):
    def initialize(self):
        self.ui_panel = self.create_ui_panel()
        self.register_ui_component("my_panel", self.ui_panel)
        
    def create_ui_panel(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("My Plugin Panel"))
        widget.setLayout(layout)
        return widget
```

### Plugin Permissions

Declare required permissions in `plugin.json`:

```json
{
  "permissions": [
    "file_read",
    "file_write",
    "network_access",
    "system_commands",
    "llm_access",
    "desktop_control"
  ]
}
```

### Testing Plugins

#### Unit Tests

```python
import unittest
from plugins.my_plugin.main import MyPlugin

class TestMyPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = MyPlugin()
        self.plugin.initialize()
        
    def test_command(self):
        result = self.plugin.handle_command("test")
        self.assertIsNotNone(result)
        
    def tearDown(self):
        self.plugin.shutdown()
```

#### Manual Testing

```bash
# Load plugin in debug mode
python main.py --debug --plugin my_plugin

# Test command
> mycommand arg1 arg2

# Check logs
tail -f logs/plugins/my_plugin.log
```

### Plugin Installation

#### Manual Installation

```bash
# Copy plugin to plugins directory
cp -r my_plugin/ plugins/

# Install plugin dependencies
pip install -r plugins/my_plugin/requirements.txt

# Restart Venalla
python main.py
```

#### Automatic Installation

```bash
# Install from GitHub
python scripts/install_plugin.py https://github.com/user/venalla-plugin

# Install from local path
python scripts/install_plugin.py /path/to/plugin
```

### Plugin Best Practices

#### 1. Error Handling

```python
def handle_command(self, *args):
    try:
        # Command logic
        result = self.process(*args)
        return result
    except Exception as e:
        self.log_error(f"Command failed: {e}")
        return f"Error: {str(e)}"
```

#### 2. Configuration

```python
def initialize(self):
    # Load config with defaults
    self.api_key = self.get_config("api_key", "")
    if not self.api_key:
        self.log_error("API key not configured")
```

#### 3. Resource Cleanup

```python
def shutdown(self):
    # Close connections
    if hasattr(self, 'connection'):
        self.connection.close()
    
    # Cancel timers
    if hasattr(self, 'timer'):
        self.timer.cancel()
    
    self.log("Cleaned up resources")
```

#### 4. Async Operations

```python
import asyncio

class AsyncPlugin(PluginBase):
    async def async_operation(self):
        result = await self.fetch_data()
        return result
        
    def handle_command(self, *args):
        # Run async in thread pool
        return asyncio.run(self.async_operation())
```

## Contributing to Venalla

### Development Setup

```bash
# Clone repository
git clone https://github.com/surya6025/Venalla-AI-Agent.git
cd Venalla-AI-Agent

# Create virtual environment
python -m venv venalla_dev
source venalla_dev/bin/activate  # macOS/Linux
# venalla_dev\Scripts\activate  # Windows

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt
```

### Code Style

We follow PEP 8 with some modifications:

```bash
# Format code
black .

# Check style
flake8 .

# Type checking
mypy core/ plugins/
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_agent_core.py

# Run with coverage
pytest --cov=core --cov-report=html
```

### Commit Guidelines

Follow conventional commits:

```
feat: Add new plugin system feature
fix: Resolve memory leak in agent core
docs: Update developer guide
test: Add tests for LLM manager
refactor: Improve error handling
```

### Pull Request Process

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and commit: `git commit -m 'feat: Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Documentation

All new features require documentation:

```python
def new_feature(param1: str, param2: int) -> bool:
    """
    Brief description of what the feature does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Example:
        >>> new_feature("test", 42)
        True
    """
    pass
```

## API Reference

### Agent Core API

```python
from core.agent_core import AgentCore

agent = AgentCore()

# Process commands
result = agent.process_command("file read test.txt")

# Register command handlers
agent.register_command("mycommand", handler_function)

# Access metrics
metrics = agent.metrics
```

### LLM Manager API

```python
from core.llm_manager import LLMManager

llm = LLMManager()

# Query LLM
response = llm.query("What is AI?")

# Switch models
llm.switch_model("gpt-4")

# Streaming
for chunk in llm.stream_query("Tell me a story"):
    print(chunk, end="")
```

### Plugin Manager API

```python
from core.plugin_manager import PluginManager

pm = PluginManager()

# Load plugin
pm.load_plugin("my_plugin")

# List plugins
plugins = pm.list_plugins()

# Reload plugin
pm.reload_plugin("my_plugin")

# Unload plugin
pm.unload_plugin("my_plugin")
```

## Troubleshooting Development Issues

### Common Issues

#### Plugin Not Loading

```bash
# Check plugin structure
python scripts/validate_plugin.py plugins/my_plugin

# Check logs
tail -f logs/plugin_manager.log
```

#### Import Errors

```bash
# Verify Python path
python -c "import sys; print(sys.path)"

# Reinstall in development mode
pip install -e .
```

#### Test Failures

```bash
# Run with verbose output
pytest -vv

# Run single test with debug
pytest -vv -s tests/test_specific.py::test_function
```

## Resources

- **Documentation**: [docs/](docs/)
- **Examples**: [examples/](examples/)
- **Issue Tracker**: https://github.com/surya6025/Venalla-AI-Agent/issues
- **Discussions**: https://github.com/surya6025/Venalla-AI-Agent/discussions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

**Need Help?** Open an issue or join our community discussions!

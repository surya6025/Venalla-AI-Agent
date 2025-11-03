#!/usr/bin/env python3
"""
VENALLA GOD-LEVEL AI AGENT - MAIN BOOTSTRAP
Omnipotent desktop AI with auto-error rectification
"""

import sys
import os
import traceback
import subprocess
import importlib
import json
from pathlib import Path
from typing import Optional

# =============================================================================
# AUTO-ERROR RECTIFIER FOR BOOTSTRAP
# =============================================================================

class BootstrapErrorRectifier:
    """Automatic error recovery for bootstrap process"""
    
    @staticmethod
    def ensure_dependencies():
        """Auto-install missing dependencies"""
        required_packages = [
            'PyQt6',
            'requests',
            'psutil',
        ]
        
        missing = []
        for package in required_packages:
            try:
                importlib.import_module(package.lower().replace('-', '_'))
            except ImportError:
                missing.append(package)
        
        if missing:
            print(f"⚠️  Missing dependencies: {', '.join(missing)}")
            print("📦 Auto-installing...")
            
            for package in missing:
                try:
                    subprocess.check_call(
                        [sys.executable, '-m', 'pip', 'install', package],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    print(f"✅ Installed {package}")
                except subprocess.CalledProcessError:
                    print(f"❌ Failed to install {package}")
                    return False
        
        return True
    
    @staticmethod
    def ensure_directories():
        """Create required directory structure"""
        directories = [
            'core',
            'plugins',
            'data',
            'logs',
            'temp',
        ]
        
        base_path = Path(__file__).parent
        
        for directory in directories:
            dir_path = base_path / directory
            dir_path.mkdir(exist_ok=True)
        
        print("✅ Directory structure verified")
    
    @staticmethod
    def ensure_config():
        """Create default config if missing"""
        config_path = Path(__file__).parent / 'config.json'
        
        if not config_path.exists():
            default_config = {
                "app_name": "Venalla AI Agent",
                "version": "1.0.0",
                "default_llm": "ollama",
                "ollama_url": "http://localhost:11434",
                "openai_api_key": "",
                "anthropic_api_key": "",
                "max_workers": 10,
                "auto_update": True,
                "voice_enabled": False,
                "theme": "dark"
            }
            
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            print("✅ Created default config.json")

# =============================================================================
# MAIN BOOTSTRAP
# =============================================================================

def main():
    """
    God-Level AI Agent Main Entry Point
    Handles all bootstrap errors automatically
    """
    
    print("="*70)
    print("🚀 VENALLA GOD-LEVEL AI AGENT")
    print("   Omnipotent Desktop AI with Auto-Error Rectification")
    print("="*70)
    print()
    
    try:
        # Step 1: Ensure dependencies
        print("[1/4] Checking dependencies...")
        if not BootstrapErrorRectifier.ensure_dependencies():
            print("❌ Failed to install dependencies")
            print("   Please run: pip install -r requirements.txt")
            return 1
        
        # Step 2: Ensure directory structure
        print("[2/4] Verifying directory structure...")
        BootstrapErrorRectifier.ensure_directories()
        
        # Step 3: Ensure config
        print("[3/4] Checking configuration...")
        BootstrapErrorRectifier.ensure_config()
        
        # Step 4: Launch main window
        print("[4/4] Launching main window...")
        print()
        
        # Import PyQt6 after ensuring it's installed
        from PyQt6.QtWidgets import QApplication
        
        # Import main window
        try:
            from core.main_window import MainWindow
        except ImportError:
            print("❌ Could not import MainWindow")
            print("   Make sure main_window.py exists in the core directory")
            return 1
        
        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("Venalla AI Agent")
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        print("✅ Venalla AI Agent launched successfully!")
        print("   Window should now be visible")
        print()
        
        # Run event loop
        return app.exec()
    
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        return 0
    
    except Exception as e:
        print("\n❌ CRITICAL ERROR")
        print(f"   {type(e).__name__}: {str(e)}")
        print("\nFull traceback:")
        print(traceback.format_exc())
        print("\n" + "="*70)
        print("ERROR RECOVERY SUGGESTIONS:")
        print("="*70)
        
        error_type = type(e).__name__
        
        if 'ModuleNotFoundError' in error_type or 'ImportError' in error_type:
            print("• Missing Python package detected")
            print("  Solution: pip install -r requirements.txt")
        
        elif 'FileNotFoundError' in error_type:
            print("• Missing file detected")
            print("  Solution: Ensure all core files are present")
        
        elif 'PermissionError' in error_type:
            print("• Permission denied")
            print("  Solution: Run with appropriate permissions")
        
        elif 'QT' in str(e) or 'Qt' in str(e):
            print("• PyQt6 issue detected")
            print("  Solution: pip install --upgrade PyQt6")
        
        else:
            print("• Unknown error")
            print("  Please check the traceback above")
        
        print("\nIf the problem persists, check:")
        print("• Python version (3.8+ required)")
        print("• All files are in correct locations")
        print("• config.json is valid JSON")
        print("="*70)
        
        return 1

if __name__ == '__main__':
    sys.exit(main())

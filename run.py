#!/usr/bin/env python3
"""
Simple run script for deployment compatibility
"""
import subprocess
import sys

if __name__ == "__main__":
    # Run the main application
    subprocess.run([sys.executable, "main.py"])
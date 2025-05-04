#!/usr/bin/env bash

# Install Python deps
pip install -r requirements.txt

# Install Playwright Chromium
playwright install chromium

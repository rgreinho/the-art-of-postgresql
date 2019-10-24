#!/bin/bash
set -euo pipefail

# Install brew if needed.
brew --version || /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# Update brew.
brew update

# Install brew formulas.
brew install \
  pgloader

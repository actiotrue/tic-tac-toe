#!/bin/bash
set -e

uv run python -m pytest "${1:-.}" -vx
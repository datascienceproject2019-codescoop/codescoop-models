#!/usr/bin/env bash

VENV_PYTHON_PATH="./notebook-venv/bin/python"

case "$1" in
  venv)
    echo "source ./notebook-venv/bin/activate"
    ;;
  venv:create)
    virtualenv notebook-venv
    ;;
  pip:install)
    pip install -r requirements.txt
    ;;
  pip:save)
    pip freeze > requirements.txt
    ;;
  notebook)
    $VENV_PYTHON_PATH -m jupyter notebook
    ;;
  *)
    echo $"Command '$1' not found, usage: $0 [service:action]"
    exit 1
esac

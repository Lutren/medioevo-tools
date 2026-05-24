@echo off
setlocal
set "APP_DIR=%~dp0"
set "PYTHONPATH=%APP_DIR%;%PYTHONPATH%"
set "WABI_WORKBENCH_CLOUD_FIRST=1"
set "WABI_ALLOW_CLOUD_PROVIDERS=1"
set "WABI_BUILD_ASSIST_CLOUD=1"
set "WABI_LLM_PROVIDER_CLOUD_DEFAULT=1"
set "WABI_PROVIDER=nvidia"
python -m wabi_sabi.cli.main hablar --cloud %*

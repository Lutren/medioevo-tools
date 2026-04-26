import requests
import json
import sys
from claudio.core.model_router import Router

API_URL = 'http://localhost:8888'

def list_modelos(arg=None):
    if arg == 'auto':
        # call router dry-run for default session
        r = requests.post(API_URL + '/v1/router/route', json={'task_type': 'codigo', 'prompt_tokens': 10, 'dry_run': True})
        print('Resolved cascade:', r.json())
        return
    if arg == 'local':
        r = Router().route('codigo', 10, force_local_only=True)
        print('Local-only models:', r)
        return
    # default listing
    print('Available models: qwen3-coder:480b-cloud, qwen3:8b (local), qwen2.5-coder:7b (local)')

if __name__ == '__main__':
    list_modelos(sys.argv[1] if len(sys.argv) > 1 else None
)
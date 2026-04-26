import os
from claudio.core.model_router import Router, MODELS
backup = MODELS['local'].copy()
MODELS['local'].pop('qwen3:8b', None)
r = Router().route('razonamiento', 10)
print('route_result', r)
logp = r'C:\\Users\\L-Tyr\\claudio\\logs\\router_decisions.jsonl'
if os.path.exists(logp):
    with open(logp,'r',encoding='utf-8') as f:
        lines = f.readlines()[-10:]
        for l in lines:
            print('LOG_LINE', l.strip())
else:
    print('LOG_MISSING')
MODELS['local'] = backup

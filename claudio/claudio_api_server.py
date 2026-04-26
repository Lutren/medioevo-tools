from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
from claudio.core.model_router import Router

router = Router()

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/v1/router/status':
            # Return basic status
            resp = {'active_models': list(router.cloud_order), 'note': 'local-only models configured in code'}
            self._set_headers()
            self.wfile.write(json.dumps(resp).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error':'not found'}).encode('utf-8'))

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == '/v1/router/route':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                task_type = data.get('task_type')
                prompt_tokens = int(data.get('prompt_tokens', 0))
                dry = data.get('dry_run', True)
                force_local = data.get('force_local_only', False)
                res = router.route(task_type, prompt_tokens, dry_run=dry, force_local_only=force_local)
                self._set_headers()
                self.wfile.write(json.dumps(res).encode('utf-8'))
            except Exception as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error':'not found'}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Handler, port=8888):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting claudio API server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

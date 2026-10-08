import json
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
from .planner import plan
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  if self.path!='/':self.send_error(404);return
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(Path(__file__).with_name('index.html').read_bytes())
 def do_POST(self):
  status=200
  try:
   if self.path!='/plan':raise ValueError()
   if self.headers.get('Origin') not in (None,'http://127.0.0.1:8002'):status=403;raise ValueError()
   size=int(self.headers.get('Content-Length','0'))
   if not 0<size<=4096:raise ValueError()
   result=plan(json.loads(self.rfile.read(size)))
  except (ValueError,TypeError):
   status=status if status==403 else 400;result={'error':'Entrada inválida. Revise os campos.'}
  self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.end_headers();self.wfile.write(json.dumps(result,ensure_ascii=False).encode())
if __name__=='__main__':
 print('Synthetic leisure demo: http://127.0.0.1:8002');HTTPServer(('127.0.0.1',8002),Handler).serve_forever()

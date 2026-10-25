import sqlite3, uuid, datetime
DEFAULT_PORT=8765
COURSES=[{'id':'robot','title':'로봇 좌표계 입문','tag':'robot','lessons':[{'title':'관절과 좌표','text':'관절 좌표는 각 관절의 회전량을 나타내고, 작업 좌표는 도구 끝단의 위치와 방향을 나타냅니다.'},{'title':'가상 실습 준비','text':'가상 환경에서 이동 범위와 충돌 여부를 확인한 뒤 실제 장비 절차를 따릅니다.'}],'question':'도구 끝단의 위치를 표현하는 좌표는?','options':['작업 좌표','파일 경로'],'answer':0}, {'id':'xr','title':'XR 학습 기록 입문','tag':'xr','lessons':[{'title':'xAPI와 LRS','text':'xAPI는 학습 경험 기록을 위한 표준이고 LRS는 그 기록을 저장하는 시스템입니다.'},{'title':'수료 기준','text':'차시 학습과 퀴즈 평가를 구분해 기록하면 학습 진도와 성취를 따로 분석할 수 있습니다.'}],'question':'xAPI 기록을 저장하는 시스템은?','options':['GPU','LRS'],'answer':1}]

def db():
 c=sqlite3.connect(ROOT/'learning.sqlite3');c.execute('CREATE TABLE IF NOT EXISTS progress(course TEXT,lesson INTEGER,PRIMARY KEY(course,lesson))');c.execute('CREATE TABLE IF NOT EXISTS events(id TEXT PRIMARY KEY,statement TEXT)');c.execute('CREATE TABLE IF NOT EXISTS scores(course TEXT PRIMARY KEY,passed INTEGER)');return c

def get(path):
 with db() as c:
  if path=='/api/courses':
   return {'courses':[{k:v for k,v in x.items() if k!='answer'} for x in COURSES],'progress':c.execute('SELECT course,lesson FROM progress').fetchall(),'scores':c.execute('SELECT course,passed FROM scores').fetchall()}
  if path=='/api/events':return [json.loads(x[0]) for x in c.execute('SELECT statement FROM events')]
 raise ValueError('not found')

def post(path,data):
 course=next((x for x in COURSES if x['id']==data.get('course')),None)
 if course is None:raise ValueError('unknown course')
 with db() as c:
  if path=='/api/complete':
   lesson=data.get('lesson')
   if type(lesson)!=int or not 0<=lesson<len(course['lessons']):raise ValueError('invalid lesson')
   c.execute('INSERT OR IGNORE INTO progress VALUES(?,?)',(course['id'],lesson));verb='completed';obj=course['id']+'/lesson/'+str(lesson);result={'completion':True}
  elif path=='/api/quiz':
   choice=data.get('choice')
   if type(choice)!=int or not 0<=choice<len(course['options']):raise ValueError('invalid choice')
   passed=choice==course['answer'];c.execute('INSERT OR REPLACE INTO scores VALUES(?,?)',(course['id'],int(passed)));verb='passed' if passed else 'failed';obj=course['id']+'/quiz';result={'success':passed,'score':{'scaled':float(passed)}}
  else:raise ValueError('unknown endpoint')
  event={'id':str(uuid.uuid4()),'actor':{'objectType':'Agent','account':{'homePage':'https://example.org/metasongi-learning','name':'local-learner'}},'verb':{'id':'http://adlnet.gov/expapi/verbs/'+verb,'display':{'en-US':verb}},'object':{'id':'https://example.org/metasongi-learning/'+obj},'result':result,'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()}
  c.execute('INSERT INTO events VALUES(?,?)',(event['id'],json.dumps(event)));return {'result':result,'statement':event}
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json, os
ROOT=Path(__file__).resolve().parent
class Handler(BaseHTTPRequestHandler):
 def reply(self,data,status=200):
  raw=json.dumps(data,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
 def do_GET(self):
  if self.path=='/':
   raw=(ROOT/'index.html').read_bytes();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
  else:
   try:self.reply(get(self.path))
   except ValueError as e:self.reply({'error':str(e)},404)
 def do_POST(self):
  if self.headers.get('Origin') not in (None,'http://localhost:'+str(self.server.server_port),'http://127.0.0.1:'+str(self.server.server_port)):
   return self.reply({'error':'origin rejected'},403)
  try:
   size=int(self.headers.get('Content-Length','0'))
   if not 0<size<=1000000:raise ValueError('invalid request size')
   data=json.loads(self.rfile.read(size));self.reply(post(self.path,data))
  except (ValueError,KeyError,TypeError) as e:self.reply({'error':str(e)},400)
  except Exception as e:
   print(type(e).__name__,str(e));self.reply({'error':'request failed; see server log'},500)
if __name__=='__main__':
 port=int(os.environ.get('PORT',DEFAULT_PORT));print(f'Open http://localhost:{port}');ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()

import cgi, cgitb, os, sys, urllib
from StringIO import StringIO
class Ob():
	class Buffer:
		def __init__(self,v = ''):
			self.v = v
		def __str__(self):
			return self.v
		def str(self):
			return self.v
		def __call__(self,v):
			self.v += v
	def __init__(self):
		self.stack = [self.Buffer()]
		self.cur = 0
		self.index = 0
		super
	def __call__(self,out,new=None):
		if new:
			self.cur += 1
			self.stack.append(self.Buffer())
		self.stack[self.cur](out)
	def flush(self,till=None):
		sys.stdout.write(self.take(till))
	def take(self,till=None):
		if till == None: #flush current
			v = self.stack[self.cur].str()
			if self.cur == 0:
				self.stack = [self.Buffer()]
			else:
				del self[self.cur]
				self.cur -= 1
			return v
		elif till == 0: #flush all
			v = ''.join(self)
			self.stack = [self.Buffer()]
			self.cur = 0
			return v
	def __len__(self):
		return len(self.stack)
	def __getitem__(self,key):
		return self.stack[key].str()
	def __setitem__(self,key,value):
		self.stack[key] = value
	def __delitem__(self,key):
		del self.stack[key]
	def __iter__(self):
		self.index = len(self)
		return self
	def next(self):
		if self.index == 0:
			raise StopIteration
		self.index -= 1
		return self[self.index]

class DefaultDict(dict):
	def __init__(self,default='',**items):
		self.default = default
		dict.__init__(self, **items)
	def __getitem__(self,key):
		if key in self:
			return self.get(key)
		else:
			import copy
			return self.setdefault(key, copy.deepcopy(self.default))
	def __copy__(self):
		return DefaultDict(self.default, **self)
class Http:
	def __init__(self,buffer):
		
		global headers, form, environ
		self.headers = headers = {'Status':'200 OK','Content-Type':'text/html'}
		
		self.headersSent = 0
		self.environ = (dict(os.environ.items()))
		import cgi, cgitb
		input = sys.stdin.read(40000)
		self.form = DefaultDict()
		if input:
			self.form.update(self.urlDecode(input))
		if self.environ['QUERY_STRING']:
			self.form.update(self.urlDecode(self.environ['QUERY_STRING']))
		
		cgitb.enable()
		
		self.buffer = buffer
	def urlDecode(self,query):
		d = DefaultDict()
		parts = query.split('&')
		for part in parts:
			if part.find('=') != -1:
				k,v = map(urllib.unquote_plus, part.split('='))
				d[k] = v
		return d
	def sendHeaders(self):
		sys.stdout.write('Status: %s\r\n' % self.headers['Status'])
		del self.headers['Status']
		for k,v in self.headers.items():
			sys.stdout.write('%s: %s\r\n' % (k,v))
		sys.stdout.write('\r\n')	
	def purge(self):
		if self.headersSent == False:
			self.sendHeaders()
		self.buffer.flush(0)


"""
	For use in templating, instantiate (done in run.cgi) using tpl = webServe.Template(ob), where ob = buffer object.
	Add variables to template scopt by tpl.context['variableName'] = variable
"""

class Template:
	def __init__(self,buffer):
		#from mako.template import Template
		from mako import template
		self.mako = template.Template
		from mako import exceptions
		self.exceptions = exceptions
		self.context = {'css':[],'js':[]}
		self.buffer = buffer
	def __getitem__(self,key):
		return self.context[key].str()
	def __setitem__(self,key,value):
		self.context[key] = value
	def __delitem__(self,key):
		del self.context[key]
	def get(self,file):
		try:
			return self.mako(filename='tmpl/'+file+'.mako').render(**self.context)
		except:
			return self.exceptions.html_error_template().render()
		pass
	def gets(self,files):
		for file in files:
			self.context['content'] = self.get(file)
		return self.context['content']
	def out(self,file):
		self.buffer(self.get(file))
	def outs(self,files):
		self.buffer(self.gets(files))
	def setContext(context):
		self.context.update(context)
	def quotes(self,items):
		for k,v in items.items():
			items[k] = cgi.escape(v)
		return items

"""
	instantiate like "log = webServe.Logger()", and then use like "log(variable)"
"""
class Logger:
	def __init__(self):
		pass
	
	def __call__(self,item):
		import datetime
		if not os.path.isfile('log'):
			fh = open('log','w')
		elif os.path.getsize('log') > 50000:
			fh = open('log','w')
		else:
			fh = open('log','a')
		log = "\n\n--------------\nLog "+str(datetime.date.today())+"\n"+str(item)
		fh.write(log)
		fh.close()

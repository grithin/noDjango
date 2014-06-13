#!/usr/bin/python
#sqlalchemy, mako, formencode, toscawidgets or formbuilder, nose (testing?)
import os, sys, pgdb, re, webServe
db = pgdb.connect('localhost:capob:capob:lD57)[ZPry{;G7V+8h(tfx,QBzBC->cuUF*En+-j').cursor()
log = webServe.Logger()
ob = webServe.Ob()
Http = webServe.Http(ob)
tpl = webServe.Template(ob)
tpl['form'] = tpl.quotes(Http.form)
#for k,v in Http.environ.items():
#	print k+' : '+v
sitePaths = [
	['^/$','main'],
	['^/work/?(.*)','work'],
	['^/root/?(.*)','root'],
	['^/springRts(.*)','springRts'],
	['^/resume.*','resume'],
	['^/(contact).*','contact'],
	['^/(request).*','contact']
]
for v in sitePaths:
	match = re.search(v[0],Http.environ['REQUEST_URI'])
	if match:
		exec 'import ctrl.'+v[1]
		break

Http.purge()

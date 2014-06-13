from __main__ import *
import time, base64


"""
Time tuple (returned by localtime)
0	4-digit year	2008
1	Month	1 to 12
2	Day	1 to 31
3	Hour	0 to 23
4	Minute	0 to 59
5	Second	0 to 61 (60 or 61 are leap-seconds)

"""
timeTuple = time.localtime(time.time())
todaysCode = base64.b64encode(str(timeTuple[0])+str(timeTuple[1])+str(timeTuple[2]))
if Http.form:
	if Http.form.has_key('captcha') and Http.form['captcha'] == str(todaysCode):
		log('Contact: '+Http.form['contact']+' '+Http.environ['REMOTE_ADDR']+', '+Http.environ['HTTP_USER_AGENT']+"\nSubject: "+Http.form['subject']+"\nBody:\n"+Http.form['body'])
		tpl['sent'] = 1
	else:
		tpl['failedCaptcha'] = 1

tpl.context['todaysCode'] = todaysCode
tpl.outs(['contact','gen'])


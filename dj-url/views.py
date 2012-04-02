import django
from django import http
from django import shortcuts
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from google.appengine.api import users
from google.appengine.ext import db
import random

class ShortUrl(db.Model):
    ourl = db.StringProperty()
    code=db.StringProperty()
    surl=db.StringProperty()


def main(request):
    return shortcuts.render_to_response('index.html')


def handle_error(request,template, msg, params=None):

    if params is None:
        params={}
    params['error']=msg
    return shortcuts.render_to_response(template, params)

def posted(request):
    try:
	s=1
	z=0
	count=[]
	ourl = request.POST['url']
	code=request.POST['slug']
        char_array = "abcdefgijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_"
        notes= db.GqlQuery("SELECT * FROM ShortUrl WHERE  ourl= :1",ourl)
     	count=notes.fetch(1)
	oslug=db.GqlQuery("SELECT * FROM ShortUrl WHERE  code= :1",code)
     	cnt=oslug.fetch(1)
	z=len(count)
	y=len(cnt)
	if z > 0:
	    surl=count[0].surl
 	if code:
	    if y >0:
	        raise SlugException("""
                The customized url you specified (%s) <b>has already been taken</b>.
                Try using a different url or leave it blank for a default.
                """ % code)
	    elif y==0:
	        #surl="http://0.0.0.0:8080/"+code
		surl="http://dj-url.appspot.com/"+code
		data=ShortUrl()
		data.ourl=ourl
		data.code=code
		data.surl=surl
		data.put()

        elif z==0:
	    while s>0:
	        word = "".join(random.choice(char_array) for i in range(4))
                x = db.GqlQuery("SELECT * FROM ShortUrl WHERE code=:1",word)
                count = x.fetch(1)
                s = len(count)   		
	    surl="http://dj-url.appspot.com/"+word
	    #surl="http://0.0.0.0:8080/"+word
	    data=ShortUrl()
	    data.ourl=ourl
	    data.code=word
	    data.surl=surl
	    data.put()
	params={}
	params['ref']=ourl
	params['ShortUrl']=ourl
	params['short_url']= surl.replace("www.", "")
	return shortcuts.render_to_response("index.html", params)

    except SlugException, slug_error:
        return handle_error(request,"index.html",str(slug_error),{})
    except Exception, ex:
        msg = """The URL you submitted (%s) does not appear to be a valid one !
         <br/>%s.
         """ % (request.POST['url'], str(ex))
        return handle_error(request,"index.html",msg,{})


class SlugException(Exception):
    def __init__(self, value = ''):
        self.value = value
    def __str__(self):
        return self.value


def forwardurl(request,path):
    try:
	code = request.path[1:]
        x = ShortUrl.all()
        x = db.GqlQuery("SELECT * FROM ShortUrl WHERE code= :1",path)
        count = x.fetch(1)
	y=len(count)
        if y==1:
            ourl = count[0].ourl
	    return http.HttpResponseRedirect(ourl)
	else:
	    raise SlugException("""
                The code you specified (%s) does not exists in the database !
                """ % code)
    except SlugException, slug_error:
        return handle_error(request,"index.html",str(slug_error),{})




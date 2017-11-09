# -*- coding:UTF-8 -*-

from django.shortcuts import render,redirect
import os,hashlib
from django.http import HttpResponseRedirect,HttpResponse
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
import jwt, requests
from django.urls.base import reverse



CLIENT_ID = '488760976240-k45t4bkdcjq63lvo7q6pc1orcsesfu7r.apps.googleusercontent.com'
CLIENT_SECRET = 'daht4NSsVXG6QP0q_plZ0-L0'
state = hashlib.sha256(os.urandom(1024)).hexdigest()
# 위조방지토큰 만듬
APPLICATION_NAME = 'apiProject'
GOOGLE_AUTH_ENDPOINT = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_ENDPOINT = 'https://accounts.google.com/o/oauth2/token'

def home(request):
    return render(request,'rogin/home.html')

def login(request):
    if request.session.get('id'):
        return render(request,'rogin/home.html')

    request.session['state'] = state
    params = {
        'client_id':CLIENT_ID,
        'state':state,
        'scope':'openid email',
        'response_type':'code',
        'redirect_uri':'http://localhost:8000/oauth/callback',
    }
    return HttpResponseRedirect("%s?%s" % (GOOGLE_AUTH_ENDPOINT, urlencode(params)))


    # render_template = 뿌려줄 템플릿을 설정하고 변수로 보냄

def callback(request):
    if request.GET.get('state') != request.session.get('state'):
        return HttpResponse('Invalid state parameter', status=401)
    # 처음에 만든 state와 이후에 서버에서 받은 state(위조방지 토큰)를 비교함

    code = request.GET.get('code')
    data = {
        'code':code,
        'client_id':CLIENT_ID,
        'client_secret':CLIENT_SECRET,
        'redirect_uri':'http://localhost:8000/oauth/callback',
        'grant_type' : 'authorization_code'
    }

    resp = requests.post(GOOGLE_TOKEN_ENDPOINT,data=data)
    tokens = resp.json()

    id_token = jwt.decode(tokens['id_token'], verify=False)
    # post방식으로 보냄

    request.session['id'] = id_token.get('email')
    #세션 생성


    #return render(request,"rogin/login.html",{'parms':parms})
    # access_token과 code 교환과정
    return render(request,'rogin/login.html',{'id_token':id_token})

def logout(request):
    del request.session['id']
    return HttpResponseRedirect(reverse('oauth:home'))

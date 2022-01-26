from django.contrib.auth import login
from django.db.models.fields.json import JSONField
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

import hashlib
import hmac
import base64

import time
import random
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
import requests

import os
import sys
import urllib.request
from urllib import request,parse
from requests.models import encode_multipart_formdata

from selenium import webdriver
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup as bs

import json
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import numpy as np

import threading

from .models import Livekw, Mainkw, Rawkw, Newskw, KeywordHistory1, ExpandKeyword, NewsTagsCollector

import traceback

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.sessions.models import Session

import csv

import random

from pytz import timezone

from django.utils import timezone

today=timezone.now().strftime('%Y-%m-%d')

# Create your views here.

class Signature:
    @staticmethod
    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)

        hash.hexdigest()
        return base64.b64encode(hash.digest())

def index(request):
    now_time=timezone.now()
    context={
        'now_time':now_time
    }
    return render(request, 'main.html', context)
    
@csrf_exempt
def search(request):
    if request.method=="POST":    
        start = time.time()    
        keyword=json.loads(request.body).get('textVal') # javascript fetch() 데이터 받아옴
        print("keyword : |",keyword,"|")
        # Mainkw DB에 새로운 키워드를 찾은 경우 
        print("=== Keyword is new one. ===")
        print("level 1 : START") # Debugging Lv 1
        if len(keyword)>1:
            # 키워드 조회 시작함
            try:
                keyword_search_lists = naverAdsAPI(keyword) # 네이버검색광고 API 검색량 조회 
                print("level 2 : 검색량 조회 시작") # Debugging Lv 2

                # PC검색량 데이터
                monthlyPcQcCnt=replaceSearchData(keyword_search_lists[0].get('monthlyPcQcCnt'))

                # MOBILE 검색량 데이터
                monthlyMobileQcCnt=replaceSearchData(keyword_search_lists[0].get('monthlyMobileQcCnt'))
                searchAmount=monthlyPcQcCnt+monthlyMobileQcCnt
            except:
                print(traceback.format_exc())

            
            # 키워드 검색 트렌드 조회
            try: 
                try:
                    period, trend = getDataLabMomentum(keyword, '')
                    period_mobile, trend_mobile = getDataLabMomentum(keyword,'mo')
                    trend = [round(e * (searchAmount/trend[-1])) for e in trend]
                    trend_mobile = [round(e * ((monthlyMobileQcCnt)/trend_mobile[-1])) for e in trend_mobile]
                except:
                    print(traceback.format_exc())
                try:
                    period_year, trend_year = getDataLabMomentumMonth(keyword)
                    period_year = [e[:-3] for e in period_year]
                    trend_year = [round(e * (searchAmount/trend_year[-1]),0) for e in trend_year]
                except:
                    print(traceback.format_exc())
            # 검색 트렌드 API 콜 다쓰면 random()함수 이용 / 임의의 데이터 채움
            except:
                try:
                    trend=[e*random.randrange(1,100) for e in [1]*31]
                    trend_mobile=[e*random.randrange(1,100) for e in [1]*31]
                    period=[(datetime.today()-relativedelta(days=e)).strftime('%Y-%m-%d') for e in range(31,-1,-1)]  
                    trend=[round(e * (searchAmount/trend[-1])) for e in trend]
                    trend_mobile=[round(e * ((monthlyMobileQcCnt)/trend_mobile[-1])) for e in trend_mobile]
                except:
                    print(traceback.format_exc())
                try:
                    trend_year=[e*random.randrange(1,100) for e in [1]*12]
                    period_year=[(datetime.today()-relativedelta(months=e)).strftime('%Y-%m') for e in range(12,-1,-1)]  
                    trend_year=[round(e * (searchAmount/trend_year[-1]),0) for e in trend_year]
                except:
                    print(traceback.format_exc())

            # 블로그 발행량 데이터 조회 / list 형식으로 받아옴
            # 네이버 search API 먼저 사용 후 콜 다되면 BeautifulSoup 사용
            try:
                print("Naver API is used")
                blog_total_count=naverSearchAPI_blog(keyword) # 블로그 발행량
                knin_total_count=naverSearchAPI_kin(keyword) # 지식인 발행량
                
            except:                  
                print("BeautifulSoup is used")
                blog_total_count=getPubTotalCounter(keyword) # 블로그 발행량
                knin_total_count=getPubTotalCounter_kin(keyword) # 지식인 발행량
            print("level 3.1 : 발행량 조회 완료") # Debugging Lv 3.1


            # 키워드 등급 매기기
            # 발행량이 0인 경우 divizion by zero Error 발생
            try:
                keywordRating=ratingKeyword(searchAmount, blog_total_count)
            except:
                print(traceback.format_exc())

            print("level 4 : 키워드 등급 책정 완료") # Debugging Lv 4
                    
            # Database 적재작업
            #   - 사람들이 검색한 키워드는 먼저 "rawkw DB"에 적재된다.
            #   - 이 후 추가적인 프로그램을 돌려서 블로그 발행량 + 키워드 품질 지수를 추가해서 "mainkw DB"에 적재한다.
            
                # 새로운 키워드 발견 / 데이터베이스 생성
            if monthlyPcQcCnt+monthlyMobileQcCnt>100 and monthlyPcQcCnt>30 and monthlyMobileQcCnt>30:
                try:
                    Mainkw.objects.create(
                        keyword=keyword,                                    
                        searchPC=monthlyPcQcCnt,                            
                        searchMOBILE=monthlyMobileQcCnt,                            
                        kwQuality=keywordRating,                
                        created_on=today,               
                        pubAmountTotalBlog=blog_total_count,                
                        pubAmountTotalKin=knin_total_count,                         
                        )
                    print("level 5 -- New keyword || Created") # Debugging Lv 5
                except:
                    # 키워드가 이미 존재한다면 DB UPDATE 진행
                    Mainkw.objects.filter(keyword=keyword).update(
                            searchPC=monthlyPcQcCnt,
                            searchMOBILE=monthlyMobileQcCnt,                       
                            pubAmountTotalBlog=blog_total_count,
                            pubAmountTotalKin=knin_total_count,
                            kwQuality=keywordRating,
                            )
                    print("level 5 -- keyword Exists || Updated")         
            else:
                print("level 5 -- 검색량이 너무 작습니다")

            # 검색 히스토리 DB 등록
            try:
                KeywordHistory1.objects.create(user_id=request.COOKIES.get('csrftoken'), keyword=keyword, searchPC=monthlyPcQcCnt, searchMOBILE=monthlyMobileQcCnt, pubAmountTotalBlog=blog_total_count, kwQuality=keywordRating)
                
            except:
                print(traceback.format_exc())

            # 연관검색어 rawkw에 DB CREATE 작업 진행
            # 연관검색어로 반환받은 리스트 중 검색량에 "< 10"이 들어간 경우
            # 전체 리스트를 for loop으로 돌려서 제거하는 방법밖에 없다.
            # 검색어로 지정된 키워드는 제외함.
            keyword_search_lists_filtered = []
            for keyword_list in keyword_search_lists[1:]:
                keyword_search_lists_filtered_dict = {}
                monthlyPcQcCnt_rel=replaceSearchData(keyword_list.get('monthlyPcQcCnt'))
                monthlyMobileQcCnt_rel=replaceSearchData(keyword_list.get('monthlyMobileQcCnt'))
                
                try:
                    if monthlyPcQcCnt_rel+monthlyMobileQcCnt_rel>1000 and monthlyPcQcCnt_rel>=100 and monthlyMobileQcCnt_rel>=100:
                        Rawkw.objects.create(keyword = keyword_list.get('relKeyword'), searchPC=monthlyPcQcCnt_rel, searchMOBILE=monthlyMobileQcCnt_rel, created_on=today)
                except:
                    # print(traceback.format_exc())
                    pass

                keyword_search_lists_filtered_dict = {
                    'relKeyword':keyword_list.get('relKeyword'),
                    'monthlyPcQcCnt':monthlyPcQcCnt_rel,
                    'monthlyMobileQcCnt':monthlyMobileQcCnt_rel
                    }
                keyword_search_lists_filtered.append(keyword_search_lists_filtered_dict)

            # dict 형태로 반환되는 결과에서 정렬할 기준이 "< 0 str"과 int가 혼합되서 반환됨 => 정렬불가//
            keyword_search_lists_filtered=sorted(keyword_search_lists_filtered, key=lambda x:x.get('monthlyMobileQcCnt'), reverse=True)    
            print("level 6 : rawkw DB LIST is CREATED") # Debugging Lv 6

            if Mainkw.objects.filter(keyword=keyword).exists():
                # 검색량 / 발행량 그래프          
                try:
                    kwdataFromDB = Mainkw.objects.filter(keyword=keyword).values()
                    context = {
                        'monthlyPcQcCnt':kwdataFromDB[0].get('searchPC'),
                        'monthlyMobileQcCnt':kwdataFromDB[0].get('searchMOBILE'),
                        'mothlyTotal' : (kwdataFromDB[0].get('searchPC') + kwdataFromDB[0].get('searchMOBILE')),
                        'relKeyword':kwdataFromDB[0].get('keyword'),
                        'blog_total_count':kwdataFromDB[0].get('pubAmountTotalBlog'),
                        'knin_total_count':kwdataFromDB[0].get('pubAmountTotalKin'),
                        'keywordRating':kwdataFromDB[0].get('kwQuality'),
                        'keyword_search_lists':keyword_search_lists_filtered[:100],
                        'period':period,
                        'trend':trend,
                        'period_year':period_year,
                        'trend_year':trend_year,
                        'trend_mobile':trend_mobile,
                    }
                except Exception as e:
                    print(traceback.format_exc())
                    context = {
                        'monthlyPcQcCnt':0,
                        'monthlyMobileQcCnt':0,
                        'mothlyTotal':0,
                        'relKeyword':keyword,
                        'blog_total_count':0,
                        'knin_total_count':0,
                        'keywordRating':'Error',
                        'keyword_search_lists':[],
                        'period':period,
                        'trend':trend,
                        'period_year':period_year,
                        'trend_year':trend_year,
                        'trend_mobile':trend_mobile,
                    }
                    return JsonResponse(context, safe=False)   
            else:
                context = {
                'monthlyPcQcCnt':monthlyPcQcCnt,
                'monthlyMobileQcCnt':monthlyMobileQcCnt,
                'mothlyTotal':monthlyPcQcCnt+monthlyMobileQcCnt,
                'relKeyword':keyword,
                'blog_total_count':blog_total_count,
                'knin_total_count':knin_total_count,
                'keywordRating':keywordRating,
                'keyword_search_lists':keyword_search_lists_filtered[:100],
                'period':period,
                'trend':trend,
                'period_year':period_year,
                'trend_year':trend_year,
                'trend_mobile':trend_mobile,
            }
            print("level 7 : FINISH") # Debugging Lv 6
            end = time.time()
            time_elapsed=timedelta(seconds=end-start)
            print(time_elapsed)
            return JsonResponse(context, safe=False)
        else:
            context = {
                'monthlyPcQcCnt':0,
                'monthlyMobileQcCnt':0,
                'mothlyTotal':0,
                'relKeyword':keyword,
                'blog_total_count':0,
                'knin_total_count':0,
                'keywordRating':'검색어 없음',
                'keyword_search_lists':[],
                'period':[],
                'trend':[],
                'period_year':[],
                'trend_year':[],
                'trend_mobile':[],
            }
            return JsonResponse(context, safe=False) 

def replaceSearchData(data):
    """
        # 기능 : 검색량 '< 10' 제거
    """
    try:
        resultData = int(data.replace('< ','')) # PC / MOBILE 검색량 조회
    except:
        resultData = data
    return resultData

def ratingKeyword(searchAmount, blog_total_count):
    """
        # 기능 : 키워드 품질 평가
    """
    try:
        # Condition1 : 발행량 1,000건 이하
        if blog_total_count < 1000:
            # Condition2 : 검색량 10,000건 이상
            if searchAmount > 10000:
                keywordRating='A+'
            elif searchAmount > 5000:
                keywordRating='A'
            elif searchAmount > 1000:
                keywordRating='A-'
            else:
                keywordRating='F'
        # Condition1 : 발행량 10,000건 이하
        elif blog_total_count < 10000:
            # Condition2 : 검색량 10,000건 이상
            if searchAmount > 10000:
                keywordRating='B+'
            elif searchAmount > 5000:
                keywordRating='B'
            elif searchAmount > 1000:
                keywordRating='B-'
            else:
                keywordRating='F'
        # Condition1 : 발행량 1,000,000건 이하
        elif blog_total_count < 1000000:
            # Condition2 : 검색량 10,000건 이상
            if searchAmount > 10000:
                keywordRating='C+'
            elif searchAmount > 5000:
                keywordRating='C'
            elif searchAmount > 1000:
                keywordRating='C-'
            else:
                keywordRating='F'
        # D => 발행량 10,000,000건 이하
        elif blog_total_count < 10000000:
            # Condition2 : 검색량 10,000건 이상
            if searchAmount > 10000:
                keywordRating='D+'
            elif searchAmount > 5000:
                keywordRating='D'
            elif searchAmount > 1000:
                keywordRating='D-'
            else:
                keywordRating='F'
        else:
            keywordRating='F'
    except:
        print(traceback.format_exc())
    return keywordRating
       
def getDataLabMomentum(keyword,device):
    """
        # 이름 : Naver SearchTrend API 사용
        # 구분 : PC / MOBILE
        # 기능 : 전체 검색량 추이 검색
    """
    client_id = "y118x7mal4_oDlBRqK4r"
    client_secret = "U934zQQSpn"

    now=datetime.now()
    # keyword=input('검색어를 입력하세요 : ')

    period_list=[]
    trend_list=[]
    
    monthAgo=(now-relativedelta(months=1)).strftime('%Y-%m-%d')
    url = "https://openapi.naver.com/v1/datalab/search"
    startDate=today
    endDate=monthAgo
    # timeUnit='date/week/month'
    groupName=keyword
    keywords=keyword
    # device='pc/mo'
    # ages='- 1: 0∼12세/- 2: 13∼18세/- 3: 19∼24세/- 4: 25∼29세/- 5: 30∼34세/- 6: 35∼39세/- 7: 40∼44세/- 8: 45∼49세/- 9: 50∼54세/- 10: 55∼59세/- 11: 60세 이상'
    # gender='m/f'

    body = f"{{\"startDate\":\"{monthAgo}\",\"endDate\":\"{today}\",\"timeUnit\":\"date\",\"keywordGroups\":[{{\"groupName\":\"test\",\"keywords\":[\"{keyword}\"]}}],\"device\":\"{device}\",\"ages\":[],\"gender\":\"\"}}"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    request.add_header("Content-Type","application/json")
    response = urllib.request.urlopen(request, data=body.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        data=response_body.decode('utf-8')
        results=json.loads(data)
        results_list=results['results'][0]['data']
        for data in results_list:
            period_list.append(data['period'])
            trend_list.append(data['ratio'])
        return period_list, trend_list
    else:
        print("Error Code:" + rescode)

def getDataLabMomentumMonth(keyword):
    """
    # 이름 : Naver SearchTrend API 사용
    # 기능 : 월 검색량 추이 검색
    """
    client_id = "y118x7mal4_oDlBRqK4r"
    client_secret = "U934zQQSpn"

    period_list=[]
    trend_list=[]

    now=datetime.now()
    yearAgo=(now-relativedelta(years=1)).strftime('%Y-%m-%d')
    # keyword=input('검색어를 입력하세요 : ')
    
    
    url = "https://openapi.naver.com/v1/datalab/search"
    timeUnit='month'
    device='pc'
    ages=''
    gender=''

    body = f"{{\"startDate\":\"{yearAgo}\",\"endDate\":\"{today}\",\"timeUnit\":\"{timeUnit}\",\"keywordGroups\":[{{\"groupName\":\"test\",\"keywords\":[\"{keyword}\"]}}],\"device\":\"\",\"ages\":[],\"gender\":\"\"}}"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    request.add_header("Content-Type","application/json")
    response = urllib.request.urlopen(request, data=body.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        data=response_body.decode('utf-8')
        results=json.loads(data)
        results_list=results['results'][0]['data']
        
        for data in results_list:
            period_list.append(data['period'])
            trend_list.append(data['ratio'])
        return period_list, trend_list

    else:
        print("Error Code:" + rescode)

def getPubTotalCounter(kw):
    """
        # 기능 : BeautifulSoup를 이용한 블로그 발행량 조회
    """
    try:
        keyword=parse.quote(kw)
        html=requests.get(f'https://m.blog.naver.com/SectionPostSearch.naver?orderType=sim&searchValue={keyword}')
        soup=bs(html.text, 'html.parser')
        totalValue=soup.find(class_='number__M9oWH').get_text()
        try:
            totalValue=int(totalValue.replace(',','').replace('건','').strip())
        except:
            print(traceback.format_exc())
            totalValue=10

        return totalValue
        
    except:
        print(traceback.format_exc())
        totalValue=10
        return totalValue

def getPubTotalCounter_kin(kw):
    """
        # 기능 : BeautifulSoup를 이용한 지식iN 발행량 검색
    """
    try:
        keyword=parse.quote(kw)
        html=requests.get(f'https://kin.naver.com/search/list.naver?query={keyword}')
        soup=bs(html.text, 'html.parser')
        totalValue=soup.find(class_='number').get_text().replace('(1-10/','').replace(')','').replace(',','')
        try:
            totalValue=int(totalValue.replace('(1-10/','').replace(')','').replace(',',''))
        except:
            print(traceback.format_exc())
            totalValue=10
        return totalValue
    except:
        print(traceback.format_exc())
        totalValue=10
        return totalValue

def naverAdsAPI(keyword):
    """
        # 목적 : 네이버광고 API fetch 함수
        # 출력 : 키워드 검색량 + 연관검색어
    """
    lists = []

    def get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID):
        timestamp = str(round(time.time() * 1000))
        signature = Signature.generate(timestamp, method, uri, SECRET_KEY)
        return {'Content-Type': 'application/json; charset=UTF-8', 
                'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 
                'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}

    search_keyword = keyword
    BASE_URL = 'https://api.naver.com'
    API_KEY = '0100000000ce9bdb5901ac1f0e07c30198bebd57e41924b79249169f83eabcfbc94622d23f'
    SECRET_KEY = 'AQAAAADOm9tZAawfDgfDAZi+vVfkPhxLJkypdy++j0sM6s4xLg=='
    CUSTOMER_ID = '1844975'

    uri = '/keywordstool'
    method = 'GET'
    r = requests.get(BASE_URL + uri+'?hintKeywords={}&showDetail=1'.format(search_keyword.replace(' ','').strip()),
                    headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    lists = r.json().get('keywordList')
    return lists

def naverSearchAPI_blog(keyword):
    """
        # 목적 : Naver 검색 API
        # 출력 : 블로그 발행량
    """
    response_body_dict = {}

    client_id = "y118x7mal4_oDlBRqK4r"
    client_secret = "U934zQQSpn"
    query = urllib.parse.quote(keyword)
    display = 1
    start = 1
    url = f"https://openapi.naver.com/v1/search/blog.json?query={query}&display={display}"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read().decode('utf-8')
        response_body_dict = eval(response_body)            
        return int(response_body_dict.get('total'))
    else:
        print("Error Code:" + rescode)
        
def naverSearchAPI_kin(keyword):
    """
        # 목적 : Naver 검색 API
        # 출력 : 지식iN 발행량
    """
    response_body_dict = {}

    client_id = "y118x7mal4_oDlBRqK4r"
    client_secret = "U934zQQSpn"
    query = urllib.parse.quote(keyword)
    display = 1
    start = 1
    url = f"https://openapi.naver.com/v1/search/kin.json?query={query}&display={display}"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read().decode('utf-8')
        response_body_dict = eval(response_body)            
        return int(response_body_dict.get('total'))
    else:
        print("Error Code:" + rescode)

def naverSearchAPI_cafe(keyword):
    """
        # 목적 : Naver 검색 API
        # 출력 : 블로그 발행량
    """
    response_body_dict = {}

    client_id = "y118x7mal4_oDlBRqK4r"
    client_secret = "U934zQQSpn"
    query = urllib.parse.quote(keyword)
    display = 1
    start = 1
    url = f"https://openapi.naver.com/v1/search/blog.json?query={query}&display={display}"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read().decode('utf-8')
        response_body_dict = eval(response_body)            
        return response_body_dict.get('total')
    else:
        print("Error Code:" + rescode)

def live_keyword(request):
    """
        # 목적 : 실시간 검색어 화면 Rendering
    """
    # live_keywords = Livekw.objects.values()
    today=timezone.now()
    live_keywords = Livekw.objects.filter(created_on=today).order_by('-amount')
    context = {
        'live_keywords':live_keywords,
        'today':today,
    }
    return render(request, 'live-keywords.html', context)

@login_required(login_url='authentication:user_login')
def recommend_keywords(request):
    """
        # 목적 : 추천 키워드 화면 Rendering
        # 출력 : Mainkw DB에서 키워드 N개 출력
    """

    recomm_lists = Mainkw.objects.filter(pubAmountTotalBlog__lte=100000, searchMOBILE__gte=10000).order_by('?')[:7]
    
    context = {
        'recomm_lists':recomm_lists,
        }

    
    return render(request, 'recommend_keywords.html', context)

@login_required(login_url='authentication:user_login')
@staff_member_required
def recommend_admin(request):
    """
    # 기능 : 등급별 키워드 조회
    """
    if request.method=="GET":
        return render(request, 'recommend_admin.html')
    if request.method=="POST":
        keyword_input=request.POST['recomm_input']
        keyword_rating=request.POST.get('recomm_rating')
        print(keyword_input)
        print(keyword_rating)
        recomm_lists = Mainkw.objects.filter(keyword__icontains=keyword_input, kwQuality__icontains=keyword_rating).order_by('kwQuality')
        
        context = {
            'recomm_lists':recomm_lists,
            'recomm_lists_count':str(len(recomm_lists))+ "건 조회되었습니다",
            }

        return render(request, 'recommend_admin.html' , context)

@csrf_exempt
def ranking_news(request):
    """
    # 목적 : 추천 뉴스 화면 Rendering
    """
    # today=timezone.now().strftime('%Y-%m-%d')
    if request.method=="GET":
        news_tags=NewsTagsCollector.objects.filter(created_on=today).order_by('-tags_count').values()
        news_keywords = Newskw.objects.filter(created_on=today).order_by('?').values()
        context = {
            'news_keywords':news_keywords,
            'news_tags':news_tags[:20],
            'today':today,
        }
        return render(request, 'ranking_news.html', context)
    if request.method=="POST":
        tags_selected=request.POST['tags_contents']
        news_keywords = Newskw.objects.filter(title__contains=tags_selected, created_on=today).order_by('?').values()
        context = {
            'news_keywords':news_keywords,
            'tags_selected':str(tags_selected)+" 관련뉴스",
            'tags_selected_count':str(len(news_keywords))+" 건 조회됨",
            'tagsTosearchBtn':str(tags_selected)+' 키워드 조회',
            'tags_url':tags_selected,
            'today':today,
        }
        return render(request, 'ranking_news.html',context)

@csrf_exempt
def search_l(request):
    """
    # 목적 : 메인화면에서 검색결과 화면 Rendering
    # 기능 : 
        1. search_l.html화면 1차 rendering
        2. keyword로 views.search로 fetch
        3. fetch_response 데이터로 2차 rendering
    """
    if request.method=="GET":
        keyword=request.GET["search_keyword"]
        if len(keyword)==0 or keyword==' ' or keyword=='  ' or keyword=='   ':
            keyword=''
        context={
            'keyword':keyword,
            'keyword_length':len(keyword),
        }
        return render(request, 'search_l.html', context)
    if request.method=="POST":  
        keyword=request.POST['search_keyword']  
        if len(keyword)==0 or keyword==' ' or keyword=='  ' or keyword=='   ':
            keyword=''
        context={
            'keyword':keyword,
            'keyword_length':len(keyword),
        }
        return render(request, 'search_l.html', context)

@csrf_exempt
def search_l2(request, kw):
    """
    # 목적 : 실시간검색어 + 연관키워드 검색 화면에서 검색결과 화면 Rendering
    # 기능 : 
        1. search_l2.html화면 1차 rendering
        2. keyword로 views.search로 fetch
        3. fetch_response 데이터로 2차 rendering
    """
    if request.method=="GET":
        return render(request, 'search_l.html', {'keyword':kw})
    if request.method=="POST":   
        return render(request, 'search_l.html', {'keyword':kw})

def introductionPage(request):
    """
    # 기능 : 모키 소개글 Rendering
    """
    return render(request, 'introduction.html')

@staff_member_required
def expandKeyword(request):
    """
    # 목적 : 키워드 확장 Rendering
    """
    if request.method=="GET":
        return render(request, 'expandKeyword.html')
    if request.method=="POST":
        return render(request, 'expandKeyword.html')

def expandKeyword_js(request):
    """
    # 목적 : 키워드 확장 로직
    # 출력 : JsonResponse / Javascript(expandKeyword.js)
    """
    if request.method=="POST":
        try:
            start = time.time()  
            result_list=[]
            
            keyword=json.loads(request.body).get('keyword')
            print(keyword, 'JavaScript fetched !')


            if ExpandKeyword.objects.filter(main_keyword=keyword).exists():
                for data in ExpandKeyword.objects.filter(main_keyword=keyword).order_by('kwQuality'):
                    result_dict={
                        'keyword':data.keyword,
                        'monthlyPcQcCnt':data.searchPC,
                        'monthlyMobileQcCnt':data.searchMOBILE,
                        'pubAmount':data.pubAmountTotal,
                        'keywordRating':data.kwQuality,
                    }
                    result_list.append(result_dict)
                return JsonResponse(result_list, safe=False)



            keyword_list=expandKeywordScraper(keyword)
            print("=== Scraper Complete! ===")
            end1 = time.time()
            time_elapsed1=timedelta(seconds=end1-start)
            print(time_elapsed1)

            

            # else:
            analyize_start=time.time()
            for data in keyword_list[:100]:
                result_dict={}
                searchAmountList=naverAdsAPI(data)
                monthlyPcQcCnt=replaceSearchData(searchAmountList[0].get('monthlyPcQcCnt'))
                monthlyMobileQcCnt=replaceSearchData(searchAmountList[0].get('monthlyMobileQcCnt'))
                pubAmount=getPubTotalCounter(data)
                keywordRating=ratingKeyword(monthlyPcQcCnt+monthlyMobileQcCnt, pubAmount)
                result_dict={
                    'keyword':data,
                    'monthlyPcQcCnt':monthlyPcQcCnt,
                    'monthlyMobileQcCnt':monthlyMobileQcCnt,
                    'pubAmount':pubAmount,
                    'keywordRating':keywordRating,
                }
                try:
                    if 'A' in keywordRating:
                        Mainkw.objects.create(
                            keyword=data,                                    
                            searchPC=monthlyPcQcCnt,                            
                            searchMOBILE=monthlyMobileQcCnt,                            
                            kwQuality=keywordRating,                
                            created_on=today,               
                            pubAmountTotalBlog=pubAmount,                
                            )
                except:
                    pass
                try:
                    ExpandKeyword.objects.create(main_keyword=keyword, keyword=data, searchPC=monthlyPcQcCnt, searchMOBILE=monthlyMobileQcCnt, pubAmountTotal=pubAmount, kwQuality=keywordRating)
                except:
                    pass
                result_list.append(result_dict)
            result_list_filtered=sorted(result_list, key=lambda x:x.get('keywordRating'))        
            analyize_end=timedelta(seconds=time.time()-analyize_start)
            end = time.time()
            time_elapsed=timedelta(seconds=end-start)
            print("======= RESULT ======= ")
            print(" 키워드 : ", keyword)
            print(" URL 수집시간 : ", time_elapsed1)
            print(" 키워드 분석시간 : ", analyize_end)
            print(" 총 소요시간 : ", time_elapsed)
            print("====================== ")

            return JsonResponse(result_list_filtered, safe=False)
        except:
            print(traceback.format_exc())
            return JsonResponse('Failed', safe=False)

def expandKeywordScraper(keyword):
    """
    # 목적 : 블로그 URL 수집 & 태그 수집
    # 참고 : BeautifulSoup 사용
    # 설명 : m.blog.naver.com 에서 상위 20개 블로그 긁어옴
    """
    
    keyword=urllib.parse.quote(keyword)
    tags=[]
    urls=[]

    url=f'https://m.blog.naver.com/SectionPostSearch.naver?orderType=sim&searchValue={keyword}'
    html=requests.get(url)
    soup=bs(html.text, 'html.parser')
    urls=soup.findAll(class_='postlist__LXY3R')
    for url in urls:
        try:
            html=requests.get(url.a.attrs['href'])
            soup=bs(html.text, 'html.parser')
            # title=soup.find(class_='se-module se-module-text se-title-text').get_text()
            tags+=soup.find(class_='post_tag').findAll(class_='ell')
            
        except:
            pass
    tags=[e.get_text().replace('#','') for e in tags]

    return list(dict.fromkeys(tags))
    """
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=options) # 크롬 웹 드라이버
    except:
        pass

    블로그 섹션 첫 페이지 수집 
    try:
        url=f'https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=ALL&orderBy=sim&keyword={keyword}'
        driver.get(url)
        sel = Selector(text = driver.page_source)

        # 블로그 링크수집하기
        urls+=sel.xpath('//*[@class="desc"]/a[1]/@href').extract()

        # 블로그 섹션 연관검색어 가져오기
        tags+=sel.xpath('//*[@class="list"]/a/text()').extract()
    except:
        print(traceback.format_exc())

    작업시간 너무 오래걸림 / 1페이지만 수집함(RAM 1GB 서버 환경에서 어쩔 수 없다)
    결국 selenium 포기함



    # 블로그 글 별로 태그 수집로직
    for url in urls:
        time.sleep(0.5)
        try: 
            driver.get(url)
            driver.switch_to.frame('mainFrame')
            sel=Selector(text=driver.page_source)
            temp=sel.xpath('//*[@class="wrap_tag"]//a//span/text()').extract()
            temp=[e.replace('#','') for e in temp]
            tags+=temp
        except:
            print(traceback.format_exc())
    driver.quit()
    return list(set(tags))
    """

@csrf_exempt
@staff_member_required
def blogAnaylize(request):
    """
    # 기능 : 블로그 분석 page rendering
    """
    if request.method=="GET":
        return render(request, 'blogAnalyze.html')
    if request.method=="POST":
        return render(request, 'blogAnalyze.html')

def blogAnaylize_js(request):
    """
    # 기능 : 블로그 분석 javascript fetch function
    # 참고 : BeautifulSoup 사용
    # 설명 : m.blog.naver.com 에서 상위 20개 블로그 긁어옴
    """
    if request.method=="POST":
        start=time.time()
        result_list=[]

        print("postAnalize Javascript fetched !")
        keyword=json.loads(request.body).get('keyword')
        kw=parse.quote(keyword)
        url=f'https://m.blog.naver.com/SectionPostSearch.naver?orderType=sim&searchValue={kw}'
        html=requests.get(url)
        soup=bs(html.text, 'html.parser')
        urls=soup.findAll(class_='postlist__LXY3R')
        end1=time.time()
        elapsed1=timedelta(seconds=end1-start)
        print("=== URL 수집 소요시간 : ", elapsed1, " ===")
        for url in urls:
            try:
                # Text Length
                text_str=[]
                html=requests.get(url.a.attrs['href'])
                soup=bs(html.text, 'html.parser')
                text_str+=soup.findAll(class_='se-text-paragraph')
                text_str=[e.find('span').get_text().replace('\u200b','').replace('\n\n\n\n','') for e in text_str]
                text_str=list(dict.fromkeys(text_str))
                text_str=' '.join(text_str)
                # Keyword 반복
                str_count=text_str.count(keyword)+text_str.count(keyword.replace(' ',''))
                # Image Counting
                img_count=soup.findAll(class_='se-module se-module-image')
                # Vedio Counting
                vedio_count=soup.findAll(class_='se-component se-video se-l-default')

                result_dict={
                        'textLen':len(text_str), 
                        'imageCount':len(img_count),
                        'vedioCount':len(vedio_count),
                        'keywordCount':str_count,
                    }
                result_list.append(result_dict)
            except:
                print(traceback.format_exc())
                pass
        end2=time.time()
        elapsed2=timedelta(seconds=end2-start)
        print("=== 블로그 분석 완료 : ", elapsed2, " ===")
        return JsonResponse(result_list, safe=False)
        """
        # try:
        #     print("postAnalize Javascript fetched !")
        #     keyword=json.loads(request.body).get('keyword')
        #     options = webdriver.ChromeOptions()
        #     options.add_argument('headless')
        #     options.add_argument('window-size=1920x1080')
        #     options.add_argument("disable-gpu")
        #     driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=options) # 크롬 웹 드라이버
        # except:
        #     pass
        
        # kw_quote=parse.quote(keyword)
        # result_list=[]
        # urls=[]

        # # 블로그 섹션 첫 페이지 수집
        # try:
        #     url=f'https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=ALL&orderBy=sim&keyword={kw_quote}'
        #     driver.get(url)
        #     sel = Selector(text = driver.page_source)

        #     # 블로그 링크수집하기
        #     urls+=sel.xpath('//*[@class="desc"]/a[1]/@href').extract()
            
        # except:
        #     print(traceback.format_exc())  

        # # 블로그 글 분석 로직(글갯수, 이미지/동영상 갯수, 키워드 반복 횟수)
        # for url in urls:
        #     time.sleep(1)
        #     try: 
        #         result_dict={}
        #         driver.get(url)
        #         driver.switch_to.frame('mainFrame')
        #         sel=Selector(text=driver.page_source)
                
        #         # text
        #         text = sel.xpath('//*[@class="se-main-container"]//text()').extract()
        #         text=list(dict.fromkeys(text))
        #         text_str=' '.join(text)

        #         # image
        #         image=sel.xpath('//*[contains(@class,"se-module se-module-image")]').extract()

        #         # vedio
        #         vedio=sel.xpath('//*[contains(@class, "se-component se-video se-l-default")]').extract()

        #         # 키워드 반복
        #         str_count=text_str.count(keyword)+text_str.count(keyword.replace(' ',''))
        #         print('keyword : ', keyword, keyword.replace(' ',''))
        #         print('keyword 반복 : ', text_str.count(keyword), text_str.count(keyword.replace(' ','')))
        #         # print("================================================")
        #         # print("1. text 갯수 : ",len(text_str))
        #         # print("2. image 갯수 : ", len(image))
        #         # print("3. vedio 갯수 : ", len(vedio))
        #         # print('4. 키워드 반복횟수 : ',str_count)
        #         # print("================================================")
        #         result_dict={
        #                 'textLen':len(text_str), 
        #                 'imageCount':len(image),
        #                 'vedioCount':len(vedio),
        #                 'keywordCount':str_count,
        #             }
        #         result_list.append(result_dict)
                
        #     except:
        #         print(traceback.format_exc())
        #         return JsonResponse(list('failed'), safe=False)
        # driver.quit()
        """

def keywordHistory(request):
    """
    # 목적 : 검색기록 page rendering
    """
    if request.method=="GET":
        keywordhistory=KeywordHistory1.objects.filter(user_id=request.COOKIES.get('csrftoken')).order_by('-id')
        
        context={
            'data':keywordhistory
        }
        return render(request, 'keyword_history.html', context)
    if request.method=="POST":
        keywordhistory=KeywordHistory1.objects.filter(user_id=request.COOKIES.get('csrftoken'))
        return JsonResponse(str(len(keywordhistory)), safe=False)

def delete_history(request):
    """
    # 기능 : 검색기록 삭제버튼
    """
    if request.method=="POST":
        token_value=request.COOKIES.get('csrftoken')
        KeywordHistory1.objects.filter(user_id=token_value).delete()
        return redirect('keywordHistory')

@csrf_exempt
def toKeywordHistory(request):
    """
    # 목적 : 검색기록 저장
    """
    if request.method=="POST":
        data=json.loads(request.body)
        keyword=data.get('keyword')
        monthlyPcQcCnt=data.get('searchPC')
        monthlyMobileQcCnt=data.get('searchMOBILE')
        blog_total_count=data.get('pubAmountTotal')
        keywordRating=data.get('kwRating')
        try:
            KeywordHistory1.objects.create(user_id=request.COOKIES.get('csrftoken'), keyword=keyword, searchPC=monthlyPcQcCnt, searchMOBILE=monthlyMobileQcCnt, pubAmountTotal=blog_total_count, kwQuality=keywordRating)
            return JsonResponse(str(keyword)+' to history success',safe=False)
        except:
            print(traceback.format_exc())
            return JsonResponse('failed',safe=False)

def history_export_csv(request):
    """
    # 목적 : 검색기록 csv 파일 다운로드
    """
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = f'attachment; filename=Mokey_History_{today}.csv'
    writer=csv.writer(response)
    writer.writerow(['#','키워드','PC 검색량','Mobile 검색량', '전체 발행량', '키워드 등급'])
    datas=KeywordHistory1.objects.filter(user_id=request.COOKIES.get('csrftoken'))

    for i in range(len(datas)):
        writer.writerow([i+1, datas[i].keyword, datas[i].searchPC, datas[i].searchMOBILE, datas[i].pubAmountTotal, datas[i].kwQuality])
    return response

def expand_export_csv(request, keyword):
    """
    # 목적 : 키워드 확장 csv 파일 다운로드
    """
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = f'attachment; filename=Mokey_{str(keyword)}.csv'
    writer=csv.writer(response)
    writer.writerow(['#','키워드','PC 검색량','Mobile 검색량', '전체 발행량', '키워드 등급'])
    datas=ExpandKeyword.objects.filter(main_keyword=keyword).order_by('kwQuality')

    for i in range(len(datas)):
        writer.writerow([i+1, datas[i].keyword, datas[i].searchPC, datas[i].searchMOBILE, datas[i].pubAmountTotal, datas[i].kwQuality])
    return response




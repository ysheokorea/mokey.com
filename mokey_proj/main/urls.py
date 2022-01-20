from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('search-l2/search', views.search, name='search2'),

    path('live-keyword', views.live_keyword, name='live_keyword'),
    path('recomm-keyword', views.recommend_keywords, name='recommend_keywords'), 
    path('recomm-admin', views.recommend_admin, name='recommend_admin'),

    path('ranking-news', views.ranking_news, name="ranking_news"),

    path('search-l', views.search_l, name="search_l"),
    path('search-l2/<str:kw>', views.search_l2, name="search_l2"),
    
    path('intro', views.introductionPage, name='introductionPage'),
    
    path('expand-keyword', csrf_exempt(views.expandKeyword), name='expandKeyword'),
    path('expandKeyword_js', csrf_exempt(views.expandKeyword_js), name='expandKeyword_js'),

    path('blogAnaylize', csrf_exempt(views.blogAnaylize), name='blogAnaylize'),
    path('blogAnaylize_js', csrf_exempt(views.blogAnaylize_js), name='blogAnaylize_js'),

    path('history', views.keywordHistory, name='keywordHistory'),
    path('del-history', views.delete_history, name='delete_history'),


    path('toKeywordHistory', views.toKeywordHistory, name='toKeywordHistory'),

    path('history-export-csv', views.history_export_csv, name='history_export_csv'),
    path('expand-export-csv/<str:keyword>', views.expand_export_csv, name='expand_export_csv'),
]


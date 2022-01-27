from django.urls import reverse
from django.contrib.sitemaps import Sitemap 

class StaticViewSitemap(Sitemap): 
    priority = 0.5 
    changefreq = 'weekly' 
    
    def items(self): 
        return [
            'index',
            'live_keyword',
            'ranking_news',
            'introductionPage',
        ] 
        
    def location(self, item): 
        return reverse(item)

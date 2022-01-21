from django.db import models

# Create your models here.
class Livekw(models.Model):
    ranking = models.IntegerField(null=True, blank=True)
    keyword = models.CharField(max_length = 200)
    amount = models.CharField(max_length = 100)
    keywordNewsTitle=models.CharField(null=True, blank=True, max_length=1000)
    keywordNewsLink=models.CharField(null=True, blank=True, max_length=1000)
    livekwImage = models.ImageField(null=True, blank=True, default='live_keywords.png')
    created_on = models.DateField(auto_now_add=True)


    def __str__(self):
        return str(self.keyword)

    class Meta:
        db_table = 'livekw'
        constraints=[
            models.UniqueConstraint(fields=['ranking','keyword','amount'], name='unique livekw')
        ]

class Mainkw(models.Model):
    keyword = models.CharField(max_length = 200, primary_key=True)
    searchPC = models.IntegerField()
    searchMOBILE = models.IntegerField()
    pubAmountMonth = models.IntegerField(null=True, blank=True)
    pubAmountTotalBlog = models.IntegerField(null=True, blank=True)
    pubAmountTotalKin=models.IntegerField(null=True, blank=True)
    pubAmountTotalCafe = models.IntegerField(null=True, blank=True)
    kwQuality=models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)   
    category=models.CharField(max_length=100, null=True)   

    def __str__(self):
        return str(self.keyword)

    class Meta:
        db_table = 'mainkw'
        constraints=[
            models.UniqueConstraint(fields=['keyword'], name='unique mainkw')
        ]

class Rawkw(models.Model):
    keyword = models.CharField(max_length=100, primary_key=True)
    searchPC = models.IntegerField()
    searchMOBILE = models.IntegerField()
    created_on = models.DateField(auto_now_add=True)       

    def __str__(self):
        return str(self.keyword)

    class Meta:
        db_table = 'rawkw'
        constraints=[
            models.UniqueConstraint(fields=['keyword'], name='unique rawkw')
        ]

class Newskw(models.Model):
    title = models.CharField(max_length = 300)
    link = models.CharField(max_length = 300)
    newskwImage = models.ImageField(null=True, blank=True, default='output.png')
    created_on = models.DateField(auto_now_add=True)    

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'newskw'
        constraints=[
            models.UniqueConstraint(fields=['title','link'], name='unique newskw')
        ]

class KeywordHistory1(models.Model):
    user_id=models.CharField(max_length=1000, null=True, blank=True)
    keyword=models.CharField(max_length=1000)
    searchPC=models.IntegerField()
    searchMOBILE=models.IntegerField()
    pubAmountTotalBlog = models.IntegerField(null=True, blank=True)
    kwQuality=models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table='keyword_history'
        constraints=[
            models.UniqueConstraint(fields=['user_id', 'keyword'], name='unique keyword_history')
        ]

class ExpandKeyword(models.Model):
    main_keyword=models.CharField(max_length=1000, null=True, blank=True)
    keyword=models.CharField(max_length=1000, null=True, blank=True)
    searchPC=models.IntegerField(null=True, blank=True)
    searchMOBILE=models.IntegerField(null=True, blank=True)
    pubAmountTotal = models.IntegerField(null=True, blank=True)
    kwQuality=models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return str(self.keyword)

    class Meta:
        db_table='expand_keyword'
        constraints=[
            models.UniqueConstraint(fields=['main_keyword', 'keyword'], name='unique expand_keyword')
        ]



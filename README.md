# Mokey Project

# 1. 프로젝트 개요
 - 블로그 발행건수 대비 검색량을 보여준다.
 - 블로그를 발행하는 생산자들에게 황금 키워드를 제공한다.
 - 사람들이 검색하면 DB는 점점 많이 쌓이고, 황금키워드를 채굴할 확률이 높아진다.
 - 황금키워드를 개당 100원에 판다.
 - 10만명에게 100원씩 받고 황금키워드를 팔면 10,000,000원 수익이다.

# 홍보계획
 - 블로그 키워드 중복건수 / 이미지 갯수 / 동영상 갯수 / 태그를 분석해서, 상위 랭크의 블로그 글을 분석해준다.
 - 블로그 글들을 분석자료를 사람들한테 무료로 뿌리면서, 광고를 게재해서 뿌린다.
 - 블로그 생산자들의 피드백을 들으면서 점점 더 빌드업한다.

# 수익화
- 사람들이 많이 사용하면 할수록 DB가 많이 쌓인다.
- 키워드를 판다. 다른 사이트에서 팔아도 되고, 회원 가입해서 정액제로 팔아도 된다.
- 분석자료를 계속해서 생산해서 분석자료를 판다.
- 웹사이트 자체 광고도 집행한다. 일방문자 1000명이 넘어가면 광고수익으로도 월 100만원은 번다.

# 빌드업 계획
 1) search 결과물 더 붙이기
  - 기간별 그래프
  - 섹션 구성 디스플레이
  - 연관검색어 디스플레이
  - 회원가입 기능
  - 키워드 등급 부여
  - 양 옆에 광고 붙이기(먼저 쿠팡 광고로 시작)

# 백업 
  - data/Dajango_project/14_1_mokey_backup(GIT) : 백업
  - /home/ys/project/Django/14_mokey_deploy(GIT) : 작업

# 프로젝트 진행 과정
 2021.12.22
  - 데이터베이스 작업 진행 
  - 검색화면에서 키워드 검색 후 메인 키워드는 "mainkw"로, 연관검색어는 "rawkw"로 분류
  - 'rawkw"에서 블로그 총발행량 크롤링 후 "mainkw"로 전송
  - 추가 작업 필요사항
    : 총발행량 까지 가져와야 됨
    : 키워드 카테고리 분류 데이터베이스 항목 추가
    : 검색 중 화면(프로세스 원) 표시
    : 키워드 검색량 10미만은 데이터베이스 작업 제외
    : AWS 배포(Chrome Driver / wordcloud image 관리)
    : 추천키워드 1분에 3번만 제공(Session programming)

 2022.01.15
  - 소스코드 정리 및 배포
  - 블로그 분석기능 추가(/ 검색도중 HTML 비활성화)
  - 키워드 확장기능 추가(블로그 섹션 5페이지까지 스크래핑 및 태그 분석 / 검색도중 HTML 비활성화)
  - 네이버 로그인 기능 제외
  - 배포 후 예정 작업{
    @ 데이터랩 API 제휴 신청(일 1000call 제한 풀기)
    @ JWT 발급 및 사용자 정보 확인 / 웹페이지 기능 제한
    @ 한줄뉴스 SVG 태그 도입
    @ 키워드 공유하기 버튼(카카오 및 네이버)
    @ 로그인 기능 확장(개인정보 처리 약관 + 네이버,구글,카카오 로그인 API 붙이기)
  }
  - 광고 패널 포지셔닝
  - 목표 : 일 방문 1000명 / 페이지뷰 : 5000 view
    
2022.01.16
  - AWS 배포 진행 중 uWSGI + Nginx 설정 에러발생
  - Youtube 보고 진행 중

2022.01.17
   - AWS 배포 진행중
   - Nginx, uWSGI, unix socket, Django

2022.01.18
   - AWS 배포 완료
   - 가비아 도메인 등록완료 [https://www.mokey.net]

2022.01.19
   - AWS 배포 완료
   - COUPANG Partners 배너 배치 완료
   - uWSGI connection timeout Error PATCH 완료
   - Google Analytics + Google Search Console + Naver Search Advisor 등록완료
  
2022.01.20
   - [Closed]Naver API Client Key / Application 정리(mokey.net)
   - [Closed]Naver API 앱 검수 요청
   - [Closed]키워드 추천 관리자 모드 화면 추가
   - [Closed] search-l2/history javascript fetch 안되는 문제


2022.01.21
   - [Closed]블로그 확장기능 BeautifulSoup 적용
   - [Closed]회원가입 E-mail 인증기능 / 메일 전송
   - [Closed]인기뉴스 랭킹 charField->integerField 변경
   - [Closed]블로그 확장 Table 규격 맞추기
   - [Closed]블로그 확장 키워드 검색 최대 100개 증가
   - [Open]회원가입 E-mail Template 작성
   - [Open]구글 서치콘솔 하부 URL 색인 등록
   - [Open]CRONTAB DB 삭제 로직 구현   

2022.01.22
   - [Closed] 파이썬 datetime timezone 변경
   - [Closed] 블로그 확장 #Tag Log 기능 추가
   - [Closed] 블로그 확장 광고 클릭 가능기능 추가
   - [Closed] Livekw Database => amount Field Alter(Char->Integer)
   - [Closed] Livekw Dtaabase => UniqueConstraint(['ranking', 'keyword', 'amount']->['keyword'])

2022.01.23
   - [Closed] ranking-news 필터 태그 추가

2022.01.25
   - [Closed] AWS server SWAP Memory 추가

2022.01.27
   - [Open] Google Adsense 신청
   - [Closed] 사이트등록{daum, naver, Google Sitemap.xml, Bing GSC 연동, ZUM 등록}
   - [Closed] sitemap.xml 추가
   - [Closed] robots.txt 추가


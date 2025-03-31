import feedparser

# 키워드를 받아서, RSS 피드에서 해당 키워드가 포함된 제목들만 리턴하는 함수
def fetch_headlines_with_keyword(rss_url, keyword, max_entries=50):
    feed = feedparser.parse(rss_url)
    headlines = []

    # 키워드가 포함된 뉴스 제목만 필터링
    for entry in feed.entries[:max_entries]:
        if keyword.lower() in entry.title.lower():  # 대소문자 구분 없이 비교
            headlines.append({'title': entry.title, 'link': entry.link})

    return headlines


# 여러 페이지의 RSS를 처리하는 함수 (RSS 페이지들을 리스트로 리턴)
def fetch_multiple_pages_with_keyword(rss_urls, keyword, max_entries=50):
    all_headlines = []

    for rss_url in rss_urls:
        page_headlines = fetch_headlines_with_keyword(rss_url, keyword, max_entries)
        all_headlines.append(page_headlines)  # 각 페이지의 헤드라인을 리스트로 저장

    return all_headlines

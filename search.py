import requests
from bs4 import BeautifulSoup

#네이버 금융에서 전체 종목을 가져오기
def get_stock_list():
    url = 'https://finance.naver.com/sise/sise_market_sum.naver?sosok=0'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    stock_table = soup.select('table.type_2 tr')
    
    #종목명과 종목코드 저장
    stock_dict = {}
    
    for row in stock_table:
        cols = row.find_all('td')
        if len(cols) > 1:
            name_tag = cols[1].select_one('a')
            code_tag = cols[1].select_one('a[href]')
            if name_tag and code_tag:
                stock_name = name_tag.text.strip()
                stock_code = code_tag['href'].split('=')[-1]
                stock_dict[stock_name] = stock_code
    
    return stock_dict

#실시간 주가 출력
def get_stock_price(stock_code):
    url = f'https://finance.naver.com/item/main.nhn?code={stock_code}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    price = soup.select_one('.no_today .blind') #종목의 가격 담고있음
    
    if price:
        return price.text
    else:
        return "주가 정보를 찾을 수 없습니다."

def print_st(stock_name):
    stock_dict = get_stock_list() #전체 종목 가져와서  get_stock_list에 저장
        
    #stock_dict에 stock_name 포함 종목 찾아서 matching_stock에 저장
    matching_stocks = {name: stock_dict[name] for name in stock_dict.keys() if stock_name.upper() in name.upper()}
    result = []
    if matching_stocks:
        print("검색 결과:")
        for name, stock_code in matching_stocks.items():
            price = get_stock_price(stock_code)
            print(f"{name} (종목 코드: {stock_code})의 현재 주가: {price}")
            result.append({'itmsNm': name, 'code':stock_code, 'clpr': price})
    else:
        print("해당 종목을 찾을 수 없습니다.")

    return result

def get_exact_stock(stock_name):
    stock_dict = get_stock_list()
    for name in stock_dict.keys():
        if stock_name == name:
            return {'itmsNm': name, 'code': stock_dict[name], 'clpr': int(get_stock_price(stock_dict[name]).replace(',', ''))}
    return None

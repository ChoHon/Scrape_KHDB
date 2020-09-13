import requests
import lxml.html
import csv

def main():
    # last_page = 10 * 100
    khdb_01 = []
    for page in range(1, 1005):
        root_url = 'http://db.history.go.kr/search/searchResultList.do?sort=&dir=&limit=1000&page=' + str(page) + '&pre_page=0&setId=-1&totalCount=0&kristalProtocol=&itemId=jw&synonym=off&chinessChar=on&searchTermImages=1900+~+2000%26nbsp%3B&brokerPagingInfo=&searchKeywordType=periods&searchKeywordMethod=EQ&searchKeyword=1900+~+2000&searchKeywordConjunction=AND'
        resp, root = get_webpage(root_url)
        print("Scraping page(" + str(page) + "/1004)")
        khdb_01 = khdb_01 + scrape_detail(resp)        

    with open('khdb_01_last.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, ['번호', '조사시기', '이름', '소속', '관직', '관등', '공훈', '참고사항'])
        writer.writeheader()
        writer.writerows(khdb_01)

def get_webpage(url):
    response = requests.get(url)
    
    root = lxml.html.fromstring(response.content)
    root.make_links_absolute(response.url)

    return response, root    

def scrape_detail(response):
    root = lxml.html.fromstring(response.content)
    key = root.cssselect('.tbl_bbs_list span')
    value = root.cssselect('.tbl_bbs_list td')
    khdb_01 = []

    for i in range(len(value)//8):
        d = {}
        for j in range(8):
            d[key[j].text_content()] = value[(8*i)+j].text_content()
        khdb_01.append(d)

    return khdb_01

if __name__ == '__main__':
    main()

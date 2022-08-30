from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

url = "https://store.playstation.com/ko-kr/product/JP9200-PPSA02411_00-D2WQDLXBDL000001"
# url = "https://store.playstation.com/ko-kr/concept/10001114"
hanok_url = "https://booking.ddnayo.com/booking-calendar-status?accommodationId=14675&groupId="

res = requests.get(url)
# res.raise_for_status()

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "close"
}
bsObj = BeautifulSoup(session.get(url, headers=headers).content, "html.parser")
# finalPrice = bsObj.find("span", {"class", "psw-t-title-m"})
hanok_data = bsObj.find_all("span", {"class", "jss150"})
# finalPrice = bsObj.find("span", attrs={"data-qa", "mfeCtaMain#offer0#finalPrice"})
# print([item['data-qa'] for item in bsObj.find_all('span', attrs={'data-qa' : True})])

# print(finalPrice.get_text().strip())
print([item['title'] for item in bsObj.find_all("span", {"class", "jss150"})
])
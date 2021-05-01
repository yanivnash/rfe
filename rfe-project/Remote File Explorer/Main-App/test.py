# from urllib.request import Request, urlopen
# from lxml import etree
#
# # xpathselector = '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img'
# xpathselector = '/html/body/div[1]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div/div/div/img'
# url = "https://www.google.com/search?q=NSIS+logo&tbm=isch&ved=2ahUKEwiA5anSpqbwAhWP0oUKHQqZAMcQ2-cCegQIABAA&oq=NSIS+logo&gs_lcp=CgNpbWcQA1AAWABgvLb8B2gAcAB4AIABAIgBAJIBAJgBAKoBC2d3cy13aXotaW1n&sclient=img&ei=pySMYMD1FI-llwSKsoK4DA&bih=937&biw=1920"
# url2 = "https://www.bing.com/images/search?view=detailV2&ccid=0E49kBjb&id=F8239064CF66C2884F8E1B407AD23E0F39CC3D12&thid=OIP.0E49kBjb2n3_qaTpN1VyFgHaHa&mediaurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fRd04e3d9018dbda7dffa9a4e937557216%3frik%3dEj3MOQ8%252b0npAGw%26riu%3dhttp%253a%252f%252fpngimg.com%252fuploads%252fchrome_logo%252fchrome_logo_PNG30.png%26ehk%3dVB2ZdIalM%252fwXSNE%252fB4Mf4Bk5f1UYhuvtUqKr%252fnJSsOk%253d%26risl%3d%26pid%3dImgRaw&exph=1024&expw=1024&q=google+chrome+logo&simid=608054020717695371&ck=91DE2FD485B85A8E456AA56FB0A55A6D&selectedIndex=0&FORM=IRPRST&ajaxhist=0"
#
# # # req = Request('http://www.cmegroup.com/trading/products/#sortField=oi&sortAsc=false&venues=3&page=1&cleared=1&group=1', headers={'User-Agent': 'Mozilla/5.0'})
# # req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
# # webpage = urlopen(url).read()
# # print(webpage)
#
# response = urlopen(url2)
# htmlparser = etree.HTMLParser()
# tree = etree.parse(response, htmlparser)
# tree.xpath(xpathselector)
# print(response)
# tree.find(xpathselector)
# print(tree.getroot())
#
#
# import lxml.html
# import requests
#
# url = "http://www.example.com/servlet/av/ResultTemplate=AVResult.html"
# response = requests.get(url, stream=True)
# response.raw.decode_content = True
# tree = lxml.html.parse(response.raw)
#
#
# from lxml.cssselect import CSSSelector
#
# td_empformbody = CSSSelector('td.empformbody')
# # for elem in td_empformbody(tree):
# #     # Do something with these table cells.
# #
# # for cell in soup.select('table#foobar td.empformbody'):
# #     # Do something with these table cells.
#
# print(td_empformbody)


from bs4 import BeautifulSoup
from lxml import etree
import requests


# URL = "https://en.wikipedia.org/wiki/Nike,_Inc."
icon_name = 'PowerPoint'
URL = f"https://www.google.com/search?q={icon_name}+logo&newwindow=1&hl=en&sxsrf=ALeKk03_3mH_awXS2UWry7EgXMwViGLtEQ:1619816415283&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjR2aKw7qbwAhVIXRoKHVAkAMwQ_AUoAXoECAEQAw&biw=1920&bih=937"
# URL = "https://www.google.com/search?q=NSIS+logo&newwindow=1&hl=en&sxsrf=ALeKk03_3mH_awXS2UWry7EgXMwViGLtEQ:1619816415283&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjR2aKw7qbwAhVIXRoKHVAkAMwQ_AUoAXoECAEQAw&biw=1920&bih=937#imgrc=KVE25-b5Us6qgM"

# DEL
HEADERS = ({'User-Agent':
			'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
			(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
			'Accept-Language': 'en-US, en;q=0.5'})
# DEL

webpage = requests.get(URL, headers=HEADERS)
# print(webpage.content)
soup = BeautifulSoup(webpage.content, "html.parser")
# print(soup)
dom = etree.HTML(str(soup))
# print(dom.xpath('//*[@id="firstHeading"]')[0].text)
# print(dom.xpath('//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img'))#[0].text)

new_url = str(soup)
new2_url = new_url[new_url.find('src="h') + 5:]
pic_url = new2_url[:new2_url.find('"')]
print(pic_url)

# download

response = requests.get(pic_url)

with open(f'downloaded_icons/.lnk.{icon_name}.png', 'wb') as file:
	file.write(response.content)
# print(soup.prettify())

from urllib import request
from bs4 import BeautifulSoup
import re

url = 'https://item.szlcsc.com/8796.html'
try:
    response = request.urlopen(url, timeout=5)
except BaseException as e:
    print(e)
    os._exit()

html = response.read().decode('utf-8')

#with open('save.html','w',encoding="utf-8") as f:
#    f.write(html)

def find_price_group(html):
    soup = BeautifulSoup(html, features="lxml")
    return soup.find_all('tr',class_="sample-list-tr")


def find_numbers(tag):
    number_tag = tag.find('td',align="right")
    if number_tag is None:
        return 'None'
    else:
        # print("stripped_strings type is ",type(number_tag.stripped_strings))
        # print(number_tag.stripped_strings)
        # print(number_tag)
        num = re.search(r'([1-9]{1}\d*?)\+', next(number_tag.stripped_strings), re.S).group(1)
        return num

def find_price(tag):
    price_tag = tag.find('p',class_="goldenrod")
    if price_tag == None:
        return 'None'
    else:
        price = [price for price in price_tag.stripped_strings]
        return re.search(r'￥([1-9]{1}[\d\.]*)', price[0], re.S).group(1)
        # return re.search(r'￥([1-9]{1}[\d\.]*)', next(price_tag.stripped_strings), re.S).group(1)


price_group = find_price_group(html)
print('-----------------------------------------------------')
print('%s %s %s' % ('序号'.ljust(8), '数量'.ljust(8), '单价'.ljust(8)))
for i,tag in enumerate(price_group, 1):
    # print(tag)
    numbers = find_numbers(tag)
    prices = find_price(tag)
    print('-----------------------------------------------------')
    print("%s %s %s" % (str(i).ljust(10), str(numbers).ljust(10), str(prices).ljust(10)))



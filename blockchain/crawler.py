from lxml import etree
import requests
import random
from blockchain.headers import headers


def getTxList(chain, address):
    if chain == "polygon":
        getPolygonTx(address)


def getPolygonTx(address):
    randH = random.randint(0, len(headers) - 1)
    uri = 'https://mumbai.polygonscan.com/address/' + address
    print(uri)
    try:
        res = requests.get(uri, headers=headers[randH],
                           timeout=5).content.decode()
        # 利用etree.HTML, 将字符串解析为HTML文档
        html = etree.HTML(res)
        tbody = html.xpath("/html/body/div[1]/main/div[4]/div[2]/div[2]/div/div[1]/div[2]/table/tbody")
        tbody = tbody[0]
        for i in range(len(tbody)):
            Method = tbody[i].xpath('./td[3]/span/text()')[0]
            Age = tbody[i].xpath('./td[6]/span/text()')[0]
            From = tbody[i].xpath('./td[7]/span/text()')[0]
            To = tbody[i].xpath('./td[9]/span/text()')
            Value = tbody[i].xpath('./td[10]/text()')[0]
            TxnFee = tbody[i].xpath('./td[11]/span/text()')[1]
            print(i, Method, Age, From, To, Value, TxnFee)

    except Exception as e:
        print(e)

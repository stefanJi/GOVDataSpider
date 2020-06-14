# coding=utf-8
# 来源: http://data.stats.gov.cn/tablequery.htm?code=AA130Q
import json

from pyecharts.charts import Bar
from requests import Session, Request

URL = 'http://data.stats.gov.cn/tablequery.htm'


def make_query(data):
    """
    构造 query
    :param data: 格式 202004
    :return: query map
    """
    wds = json.dumps([
        {"wdcode": "sj", "valuecode": data}
    ])
    return {
        "m": "QueryData",
        "code": "AA130Q",
        "wds": wds
    }


DATE = (
    '201901',
    '201902',
    '201903',
    '201904',
    '201905',
    '201906',
    '201907',
    '201908',
    '201909',
    '201910',
    '201911',
    '201912',
    '202001',
    '202002',
    '202003',
    '202004',
    '202005',
    '202006',
    '202007',
    '202008',
    '202009',
    '202010'
)

s = Session()


def refresh_cookie():
    pre = s.prepare_request(Request("GET", 'http://data.stats.gov.cn/', headers={
        "Referer": "http://data.stats.gov.cn/tablequery.htm?code=AA130Q",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "X-Requested-Wit": "XMLHttpRequest",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "host": "data.stats.gov.cn"
    }))
    s.send(pre)


def query(date):
    def do(url):
        query_map = make_query(date)
        pre = s.prepare_request(Request("GET", url, params=query_map, headers={
            "Referer": "http://data.stats.gov.cn/tablequery.htm?code=AA130Q",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "X-Requested-Wit": "XMLHttpRequest",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "host": "data.stats.gov.cn"
        }))
        return s.send(pre)

    r = do(URL)
    if r.status_code / 100 == 3:
        print("redirect")
        r = do(r.headers['location'])

    if r.status_code / 100 != 2:
        print("request failed!({}) {}".format(r.status_code, r.text))
        return []

    result = []
    try:
        json_data = r.json()
        data = json_data['exceltable']
        for i in range(5, len(data) - 1, 4):
            name = data[i]['data']
            total = format_number(data[i + 1]['data'])
            new = format_number(data[i + 2]['data'])
            old = format_number(data[i + 3]['data'])
            result.append({'name': name, 'total': total, 'new': new, 'old': old})
    except Exception as e:
        print("code: {} text: {}".format(r.status_code, r.text))
        print(e)
    return result


def format_number(data):
    if data == '' or data == ' ':
        return 0.0
    else:
        return float(data)


def main():
    refresh_cookie()
    provices = {}
    for date in DATE:
        result = query(date)
        for item in result:
            name = item['name']
            provices.setdefault(name, [])
            provices[name].append(item['total'])
    if len(provices.keys()) == 0:
        return

    bar = Bar()
    bar.add_xaxis(DATE)

    for p in provices.keys():
        bar.add_yaxis(p, provices[p])

    bar.render('housing_sales_area.html')


if __name__ == '__main__':
    main()

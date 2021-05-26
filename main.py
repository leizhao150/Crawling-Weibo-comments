import time
import requests
from bs4 import BeautifulSoup
import json

# 请求头配置
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'SINAGLOBAL=4315370677412.562.1620629918393; UOR=,,www.baidu.com; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5F5HXv1mlHhSDKhBMGPzhh5JpX5KMhUgL.FoqEeoB7Sh2RShq2dJLoIEMLxKBLBonLB.2LxKqLBKzLBKqLxKqL1h.LBKMLxKML1-BL1h5feo5t; ALF=1653566914; SSOLoginState=1622030914; SCF=AvxcUtqnxb1uZHvqa2fzrckJ92Gpd8yN5DNCsnA6dljuo5tEeDRHj16qIe9yN_Bri7FDa1aHNAMNeJYjgvX9Dt8.; SUB=_2A25NqkoTDeRhGeBM6VYR9C_EzzqIHXVu3jzbrDV8PUNbmtB-LWbTkW9NRRfG4oRyetRbq2v9-WgpuXZiiyRzDElM; wvr=6; _s_tentry=weibo.com; Apache=7542731870195.625.1622030924421; ULV=1622030924435:6:6:1:7542731870195.625.1622030924421:1621304749446; webim_unReadCount=%7B%22time%22%3A1622030956976%2C%22dm_pub_total%22%3A3%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A43%2C%22msgbox%22%3A0%7D; WBStorage=202105262009|undefined',
    'Host': 's.weibo.com',
    'Referer': 'https://s.weibo.com/weibo?q=%E8%B6%85%E7%BA%A7%E7%BA%A2%E6%9C%88%E4%BA%AE&Refer=SWeibo_box',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
}

# 获取页面内容
def get_texts(pages):
    texts = []
    for i in range(1, pages+1):
        url = 'https://s.weibo.com/weibo?q=%23%E5%A7%9A%E7%AD%96%23&Refer=SWeibo_box&page={0}'.format(i)
        ses = requests.Session()
        response = ses.get(url=url, headers=headers)
        if response.status_code == 200:
            texts.append(response.text)
        print("第%s页采集完成!"%(i))
        # 休眠2秒
        time.sleep(2)
    return texts

# 解析页面
def parse_page(text):
    infos = []
    soup = BeautifulSoup(text)
    for div in soup.find_all('div', attrs={"class": "card-wrap", 'action-type': "feed_list_item"}):
        p_tag = div.find('p', attrs={'class':"txt", 'node-type': "feed_list_content_full"})
        if p_tag == None:
            p_tag = div.find('p', attrs={'class': "txt", 'node-type': "feed_list_content"})
        if p_tag == None: continue
        nick_name = ''
        if p_tag.has_attr(key='nick-name'): nick_name = p_tag.attrs['nick-name']
        txt = p_tag.text.strip()
        favorite = div.find_next('a', attrs={'action-type':"feed_list_favorite"}).text.replace("收藏", "").strip()
        forward = div.find_next('a', attrs={'action-type': "feed_list_forward"}).text.replace("转发", "").strip()
        comment = div.find_next('a', attrs={'action-type': "feed_list_comment"}).text.replace("评论", "").strip()
        like = div.find_next('a', attrs={'action-type': "feed_list_like"}).text.strip()
        infos.append({
            "nick_name": nick_name,
            "txt": txt,
            "favorite": favorite,
            "forward": forward,
            "comment": comment,
            "like": like
        })
    return infos


if __name__ == '__main__':
    pages = 10
    texts = get_texts(pages)
    contents = []
    for text in texts:
        content = parse_page(text)
        contents.extend(content)
    # 保存数据到文件中
    with open('./txt.json', 'a', encoding='utf-8') as fp:
        for txt in contents:
            print(txt)
            txt = json.dumps(txt)
            print('=' * 100)
            fp.write(txt + "\n")

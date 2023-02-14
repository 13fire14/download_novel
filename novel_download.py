import streamlit as st
import requests
from lxml import etree
import time
import re
from tqdm import tqdm
import os
import pinyin as py
st.title('小说免费下载平台')
st.subheader("长篇小说需要一定的下载时间，请耐心等候")
name_chinese=st.text_input('请输入小说名称')
# name_chinese='天龙八部'
name=py.get(name_chinese,format='strip')
#获取拼音
novel_url=f'https://www.51shucheng.net/{name}'
#伪装自己是浏览器
headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'}
resp=requests.get(novel_url,headers=headers)
resp.encoding='utf_8'
try:
    url_all=re.findall('<li>.*<a href="(.*)" title=.*</a>',resp.text)
    url=url_all[0]
    st.subheader("当前书城中存在此小说，正在下载")
    for i in tqdm(range(len(url_all))):
        #伪装自己
        headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'}
        #发出请求访问
        resp=requests.get(url,headers=headers)
        #保证不乱码
        resp.encoding='utf_8'
        #打印网页源代码
        e=etree.HTML(resp.text)
        title=e.xpath('/html/body/div[1]/div[4]/h1/text()')[0]
        info='\n'.join(e.xpath('/html/body/div[1]/div[4]/div[3]/p/text()'))
        
        #获取下一章网址
        url=e.xpath('/html/body/div[1]/div[6]/div[1]/a/@href')[0]
        st.write(f'{i}/{len(url_all)}:{title}')
        time.sleep(0.2)
        # print(info)
        with open(f'.\{name_chinese}.txt','a',encoding='utf-8') as f:
            f.write(title+'\n\n'+info+'\n\n')
    file=os.getcwd()
    finally_file=os.path.join(file, f'{name_chinese}.txt')
    st.write(f"小说已经下载完成，存放在{finally_file}")
except:
    st.write(f"当前书城并没有收录该小说,网址为{novel_url},可查看")

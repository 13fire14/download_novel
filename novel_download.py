# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:19:06 2023

@author: bianca
"""

#%%app代码存放处
# -*- coding: utf-8 -*-

#%% 爬取小说平台
#导入库
import streamlit as st
import requests
from lxml import etree#解析网站
import time
import re
from tqdm import tqdm
import os           #获取服务器的小说
import pinyin as py#中文改为拼音
import pandas as pd

st.set_page_config(page_title='小说免费下载平台')
st.title('小说免费下载平台')
# st.subheader("长篇小说需要一定的下载时间，请耐心等候")
#%%获取登陆时间
import datetime
 
SHA_TZ = datetime.timezone(
    datetime.timedelta(hours=8),
    name='Asia/Shanghai',
)
 
# 协调世界时
utc_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
beijing_now = utc_now.astimezone(SHA_TZ)
time_login=beijing_now.strftime('%Y-%m-%d %H:%M:%S')
st.write(f'当前登陆时间为：{time_login}')
#%%数据上传
def data_load(user_data):
    for i in range(len(user_data)):
        if i ==len(user_data)-1:
            with open('./user_data.txt','a',encoding='utf-8')as f:
                f.write(user_data[i])
                f.write('\n')
        else:
            with open('./user_data.txt','a',encoding='utf-8')as f:
                f.write(user_data[i])
                f.write(',')
#%%先将储存库中所有小说清空
novel_list1=os.listdir()
file1=os.getcwd()
novel_chandle=[]
for i in novel_list1:
    if 'requirements'or'user_data' not in i:
        if '.txt' in i:
            novel_chandle.append(i)
            # os.remove(os.path.join(file1, i))
st.sidebar.dataframe(novel_chandle)
#%%编写爬取的函数
def novel_paqu(name):
    #计算总的时间
    time_now_all=time.time()
    novel_url=f'https://www.51shucheng.net/{name}'
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'}
    resp=requests.get(novel_url,headers=headers)
    resp.encoding='utf_8'
    
    try:
        e=etree.HTML(resp.text)
    #获取小说所属类别
        novel_class=e.xpath('/html/body/div[1]/div[3]/div[1]/div[1]/a[2]/@title')[0]
        url_all=re.findall('<li>.*<a href="(.*)" title=.*</a>',resp.text)
        url=url_all[0]
        st.subheader("当前书城中存在此小说，正在下载")
        for i in tqdm(range(len(url_all))):
            #计算每章需要时间
            time_now=time.time()
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
            time.sleep(0.2)
            # print(info)
            with open(f'.\{name_chinese}.txt','a',encoding='utf-8') as f:
                f.write(title+'\n\n'+info+'\n\n')
            time_waste=round(time.time()-time_now,0)
            st.sidebar.write(f'{i+1}/{len(url_all)}:{title},耗时{time_waste}秒')
        file=os.getcwd()
        finally_file=os.path.join(file, f'{name_chinese}.txt')
        #st.write(f"小说已经下载完成，存放在{finally_file}")
        novel=open(f'.\{name_chinese}.txt','r',encoding='utf-8')
        st.download_button('保存到本地',novel,file_name=f'{name_chinese}.txt')
        download=1
        time_all_waste=round(time.time()-time_now_all,0)
    except:
        download=2
        st.write(f"当前书城并没有收录该小说,网址为{novel_url},可查看")
        st.write(download)
        time_all_waste=0
        novel_class=''
    return download,time_all_waste,novel_class
#%%重新下载
def novel_paqu_again(name):
    time_now_all=time.time()
    novel_url=f'https://www.51shucheng.net/{name}'
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'}
    resp=requests.get(novel_url,headers=headers)
    resp.encoding='utf_8'
    e=etree.HTML(resp.text)
#获取小说所属类别
    novel_class=e.xpath('/html/body/div[1]/div[3]/div[1]/div[1]/a[2]/@title')[0]
#获取小说第一章节网址
    url_all=re.findall('<li>.*<a href="(.*)" title=.*</a>',resp.text)
    url=url_all[0]
    for i in tqdm(range(len(url_all))):
        #计算每章需要时间
        time_now=time.time()
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
        time.sleep(0.2)
        # print(info)
        with open(f'.\{name_chinese}-1.txt','a',encoding='utf-8') as f:
            f.write(title+'\n\n'+info+'\n\n')
        time_waste=round(time.time()-time_now,0)
        st.sidebar.write(f'{i+1}/{len(url_all)}:{title},耗时{time_waste}秒')
    file=os.getcwd()
    finally_file=os.path.join(file, f'{name_chinese}-1.txt')
    #st.write(f"小说已经下载完成，存放在{finally_file}")
    novel=open(f'.\{name_chinese}-1.txt','r',encoding='utf-8')
    time_all_waste=round(time.time()-time_now_all,0)
    st.download_button('保存到本地',novel,file_name=f'{name_chinese}.txt')
    return download,time_all_waste,novel_class
#%%页面设置
name_chinese=st.text_input('请输入小说名称')
# name_chinese='天龙八部'
download=1
time_all_waste=0
novel_class=''
if name_chinese=='':
    st.write('积累的年代，就安然等待吧。不要焦虑，不要迷茫。时人不识凌云木，直待凌云始道高')
else:
    if name_chinese=='曾文正':
        #数据查看
        data=pd.read_table('./user_data.txt',header=None,sep=',')
        st.write(data)
    else:
        name=py.get(name_chinese,format='strip')
        #已经获取到小说名字————先判断是否已经有了，有了的话可直接提供下载到本地，也可选择继续下载，建议继续下载
        novel_list=os.listdir()
        if f'.\{name_chinese}.txt' in novel_list:
            # print('yes')
            download=1
            st.write('当前平台已收录此小说，是否选择直接下载(如果是正在更新的小说，建议重新下载)')
            col1,col2=st.columns(2)
            with col1:
                if st.button('直接下载'):
                    novel=open(f'.\{name_chinese}.txt','r',encoding='utf-8')
                    file=os.getcwd()
                    finally_file=os.path.join(file, f'{name_chinese}.txt')
                    st.write(f"小说已经下载完成，存放在{finally_file}")
                    st.download_button('保存到本地',novel,file_name=f'{name_chinese}.txt')
                    time_all_waste=0
                    novel_url=f'https://www.51shucheng.net/{name}'
                    headers={
                        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'}
                    resp=requests.get(novel_url,headers=headers)
                    resp.encoding='utf_8'
                    e=etree.HTML(resp.text)
                #获取小说所属类别
                    novel_class=e.xpath('/html/body/div[1]/div[3]/div[1]/div[1]/a[2]/@title')[0]
                    user_data=[f'{pd.to_datetime(time_login)}',f'{name_chinese}',f'{time_all_waste}',f'{download}',f'{novel_class}']
                    data_load(user_data)
            with col2:
                if st.button('重新下载'):
                    with open(f'.\{name_chinese}-1.txt','w',encoding='utf-8') as f:
                        f.close()
                    download,time_all_waste,novel_class=novel_paqu_again(name)
                    user_data=[f'{pd.to_datetime(time_login)}',f'{name_chinese}',f'{time_all_waste}',f'{download}',f'{novel_class}']
                    data_load(user_data)
        else:
            download,time_all_waste,novel_class=novel_paqu(name)
            user_data=[f'{pd.to_datetime(time_login)}',f'{name_chinese}',f'{time_all_waste}',f'{download}',f'{novel_class}']
            data_load(user_data)
    
        
        

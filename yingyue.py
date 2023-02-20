# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 21:08:06 2023

@author: bianca
"""

#%%爬取映月读书网
import requests
import re
import pinyin
from lxml import etree
import random
import datetime
import time as t
import streamlit as st
import os
import pandas as pd
#%%
st.set_page_config(page_title='明月傍窗好读书')
#%%展示数据
def show_data():
    data=pd.read_table('./用户数据.txt',header=None,sep=',')
    st.table(data)
#%%展示已下载的小说
def show_book(book_list):
    book_list1=[]
    for i in book_list:
        if '用户数据'  not in i:
            if 'requirements' not in i:
                book_list1.append(i)
    st.sidebar.table(book_list1)
#%%一键清除所有小说（慎用）
def delete_novel(file,book_list):
    for i in book_list:
        if '用户数据'  not in i:
            if 'requirements' not in i:
                txt=os.path.join(file,f'{i}')
                os.remove(txt)
#%%一键清除用户数据（慎用）
def delete_data(file,book_list):
    for i in book_list:
        if '用户数据' in i:
            txt=os.path.join(file,f'{i}')
            os.remove(txt)
#%%加载数据
def user_data_load(column):
    for c in range(len(column)):
        if c!=len(column)-1:
            with open('./用户数据.txt','a',encoding='utf-8') as U:
                U.write(column[c])
                U.write(',')
        else:
            with open('./用户数据.txt','a',encoding='utf-8') as U:
                U.write(column[c])
                U.write('\n')
#%%获取作者姓名
def get_author(url,header):
    resp=requests.get(url,headers=header)
    resp.encoding='utf_8'
    #获取作者
    author=re.findall('<p>作者：(.*)</p>',resp.text)[0]
    return author,resp
#%%获取章节数
def get_all_page(url,user_agent):
    header={'user-agent':random.choice(user_agent)}
    resp=requests.get(url,headers=header)
    resp.encoding='utf_8'
    try:
        
        #获取总页数
        page_all=re.findall('<a href=".*?" >下页</a><span>共 (.*?) 页</span>', resp.text)[0]
        #获取跳转到最后一页的链接
        page_str=re.findall('<a href="(.*?)" >下页</a>', resp.text)[0]
        page_list=list(page_str)
        page_list[-2]=page_all
        page_url=''.join(page_list)
        resp=requests.get(page_url,headers=header)
        resp.encoding='utf_8'
        #获取最后一章
        num=re.findall('<a href=".*?title="第(.*?)章',resp.text)[-1]
    except:
        num=len(re.findall('<li><a href="(.*?)" title=.*?</a></li>', resp.text,re.S))-3
    return num
#%%编制第一次爬取的函数
def get_book_first(name_chinese,url,header,user_agent):
    try:
        #%%获取第一章
        author,resp=get_author(url, header)
        #获取总章节数
        num=get_all_page(url,user_agent)
        #获取第一章网址
        url=re.findall('<li><a href="(.*?)" title=.*?</a></li>', resp.text,re.S)[3]
        
        #%% #获取最后一章的提示（用不到了）
        # url_finally='https://www.yydushu.com/longzu/25849.html'
        # resp=requests.get(url_finally,headers=header)
        # resp.encoding='utf_8'
        # e=etree.HTML(resp.text)
        # url=e.xpath('/html/body/div[1]/article/nav[2]/ul/li[2]/a/@href')[0]
        
        #%%点击第一章
        i=1#章节累计
        time_star=t.time()
        while True:
            header={'user-agent':random.choice(user_agent)}
            resp=requests.get(url, headers=header)
            resp.encoding='utf-8'
            e=etree.HTML(resp.text)
            info='\n'.join(e.xpath('/html/body/div[1]/article/div[3]/p/text()'))
            title=e.xpath('/html/body/div[1]/article/header/h1/text()')[0]
            st.sidebar.write(f'{i}/{num} {title}----下载完成')
            with open(f'./{name_chinese}.txt','a',encoding='utf-8') as f:
                f.write(title+'\n\n'+info+'\n\n')
            url=e.xpath('/html/body/div[1]/article/nav[2]/ul/li[2]/a/@href')[0] 
            if url=="javascript:alert('这是最后一章！')":
                break
            i+=1#章节累计
        st.write(f'{i}章都已经下载完成')
        time_need=round(t.time()-time_star,2)
        result='成功'
        book=open(f'./{name_chinese}.txt','r',encoding='utf-8')
        st.download_button('已下载完成，可点击直接保存哦',book,f'{name_chinese}.txt')
        
        
    except:
        st.subheader('没有收录该书')
        author='none'
        i='none'
        time_need='none'
        result='失败'
    return result,author,i,time_need
#%%第二次爬取
def get_book_again(name_chinese,url,header,user_agent):
    author,resp=get_author(url, header)
    #获取总章节数
    num=get_all_page(url,user_agent)
    #获取第一章网址
    url=re.findall('<li><a href="(.*?)" title=.*?</a></li>', resp.text,re.S)[3]
    
    #%%点击第一章
    i=1#章节累计
    time_star=t.time()
    while True:
        header={'user-agent':random.choice(user_agent)}
        resp=requests.get(url, headers=header)
        resp.encoding='utf-8'
        e=etree.HTML(resp.text)
        info='\n'.join(e.xpath('/html/body/div[1]/article/div[3]/p/text()'))
        title=e.xpath('/html/body/div[1]/article/header/h1/text()')[0]
        st.sidebar.write(f'{i}/{num} {title}----下载完成')
        with open(f'./{name_chinese}-副本.txt','a',encoding='utf-8') as f:
            f.write(title+'\n\n'+info+'\n\n')
        url=e.xpath('/html/body/div[1]/article/nav[2]/ul/li[2]/a/@href')[0] 
        if url=="javascript:alert('这是最后一章！')":
            break
        i+=1#章节累计
    st.write(f'{i}章都已经下载完成')
    time_need=round(t.time()-time_star,2)
    result='成功'
    book=open(f'./{name_chinese}-副本.txt','r',encoding='utf-8')
    st.download_button('点击保存',book,f'{name_chinese}.txt')
    return result,author,i,time_need

#%%标题

st.title('欢迎来到免费小说下载平台')
st.subheader('网站收录书籍有限，如若搜索不到，请见谅')
#%%检索内存是否有该小说
file=os.getcwd()
file_local=os.listdir(file)
book_list=[]
for b in file_local:
    if '.txt' in b:
        book_list.append(b)

#%%获取小说名字和网址
# name_chinese='天龙八部'
name_chinese=st.text_input('请输入您要下载的小说：')
st.markdown('''
            温馨提示：如果书名中存在多音字情况，容易搜索不到，可输入拼音
            如水浒传，龙王传说，可输入水浒zhuan，龙王chuan说
            ''')
name_pinyin=pinyin.get(name_chinese,format='strip')
expander=st.expander(f'书名拼音为{name_pinyin}')
expander.write('请检查拼音是否有误,,如果没错请点击搜索，如果出错请按照上示提示修改书名')
#%%增加小说对应列表
name_list={'zhetian':'cd-zhetian','damingfenghua':'daminghuangfei','shenmu':'cd-shenmu','douluodalu2':'douluodalu2jueshitangmen',
           'douluodalu3':'wanglongchuanshuo','shibingtuji':'shibing'}
try:
    name=name_list[f'{name_pinyin}']
except:
    name=name_pinyin
#形成网址
url=f'https://www.yydushu.com/{name}'
#%%获取时间（仅用做记录登陆时间）
SHA_TZ = datetime.timezone(datetime.timedelta(hours=8),name='Asia/Shanghai')
utc_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)#协调世界时
beijing_now = utc_now.astimezone(SHA_TZ)
time_login=beijing_now.strftime('%Y-%m-%d %H:%M:%S')
#%%虚拟浏览器
user_agent=['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41',
'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36',
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
]

header={'user-agent':random.choice(user_agent)}


#判断小说是否在里面
if f'{name_chinese}.txt' in book_list:
    col1,col2=st.columns(2)
    with col1:
        if st.button('天降大礼，享受零秒下载'):
            book=open(f'./{name_chinese}.txt','r',encoding='utf-8')
            st.download_button('点击保存',book,f'{name_chinese}.txt')
            result='成功'
            author,resp=get_author(url, header)
            i='none'
            time_need='none'
            class_download='仓库里直接获取'
            data=[f'{time_login}',f'{name_chinese}',f'{author}',f'{result}',f'{i}',f'{time_need}',f'{class_download}']
            user_data_load(data)
    with col2:
        if st.button('尚在更新的小说建议重新下载'):
            with open(f'./{name_chinese}-副本.txt','w',encoding='utf_8') as f:
                f.close()
            result,author,i,time_need=get_book_again(name_chinese,url,header,user_agent)
            class_download='重新下载'
            data=[f'{time_login}',f'{name_chinese}',f'{author}',f'{result}',f'{i}',f'{time_need}',f'{class_download}']
            user_data_load(data)
else:
    if st.button('搜索'):
        result,author,i,time_need=get_book_first(name_chinese,url,header,user_agent)
        class_download='首次搜索'
        data=[f'{time_login}',f'{name_chinese}',f'{author}',f'{result}',f'{i}',f'{time_need}',f'{class_download}']
        user_data_load(data)
        
# #%%获取数据
#     data=[f'{time_login}',f'{name_chinese}',f'{author}',f'{result}',f'{i}',f'{time_need}']
#     user_data_load(data)
#%%第一次
column=['搜索时间','书名','作者','下载结果','共多少章节','耗费时长','下载情况']
def tool_box():
    choose=st.sidebar.selectbox('功能选择', ['点击查看','用户数据','已下载的小说','一键插入标题行','一键清除用户数据（慎用）','一键清除小说（慎用）','清除具体的小说'])
    if choose=='用户数据':
        show_data()
    elif choose=='一键清除用户数据（慎用）':
        delete_data(file,book_list)
    elif choose=='一键插入标题行'  :
        user_data_load(column)
    elif choose=='已下载的小说':
        show_book(book_list)
    elif choose=='一键清除小说（慎用）':
        delete_novel(file, book_list)
    elif choose=='清除具体的小说':
        
        book1=[i for i in book_list if 'requirements' not in i]
        book1.insert(0,'无')
        book2=st.sidebar.selectbox('选择要删除的小说',book1)
        txt=os.path.join(file,book2)
        os.remove(txt)
    
    
code='zwz'
code1=st.sidebar.text_input('输入密码，解锁功能')
if code1 !=code: 
    st.sidebar.warning('管理者专属')
    st.stop()
st.success(
    tool_box()
    )    




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
import getpass


st.set_page_config(page_title='小说免费下载平台')
st.title('小说免费下载平台')
str1 = getpass.getuser()
st.write(str1)
# st.subheader("长篇小说需要一定的下载时间，请耐心等候")
#%%先将储存库中所有小说清空
novel_list1=os.listdir()
file1=os.getcwd()
novel_chandle=[]
for i in novel_list1:
    if 'requirements' not in i:
        if '.txt' in i:
            novel_chandle.append(i)
            #一键清除所有小说内存
            #os.remove(os.path.join(file1, i))
st.sidebar.subheader('当前书城已下载小说目录')
st.sidebar.dataframe(novel_chandle)
#%%编写爬取的函数
def novel_paqu(name):
    novel_url=f'https://www.51shucheng.net/{name}'
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
            st.sidebar.write(f'{i}/{len(url_all)}:{title}')
            time.sleep(0.2)
            # print(info)
            with open(f'.\{name_chinese}.txt','a',encoding='utf-8') as f:
                f.write(title+'\n\n'+info+'\n\n')
        file=os.getcwd()
        finally_file=os.path.join(file, f'{name_chinese}.txt')
        st.write(f"小说已经下载完成")
        novel=open(f'.\{name_chinese}.txt','r',encoding='utf-8')
        st.download_button('保存到本地',novel,file_name=f'{name_chinese}.txt')
    except:
        st.write(f"当前书城并没有收录该小说,网址为{novel_url},可查看")
#%%重新下载
def novel_paqu_again(name):
    novel_url=f'https://www.51shucheng.net/{name}'
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'}
    resp=requests.get(novel_url,headers=headers)
    resp.encoding='utf_8'
    url_all=re.findall('<li>.*<a href="(.*)" title=.*</a>',resp.text)
    url=url_all[0]
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
        st.sidebar.write(f'{i}/{len(url_all)}:{title}')
        time.sleep(0.2)
        # print(info)
        with open(f'.\{name_chinese}-1.txt','a',encoding='utf-8') as f:
            f.write(title+'\n\n'+info+'\n\n')
    file=os.getcwd()
    finally_file=os.path.join(file, f'{name_chinese}-1.txt')
    st.write(f"小说已经下载完成")
    novel=open(f'.\{name_chinese}-1.txt','r',encoding='utf-8')
    st.download_button('保存到本地',novel,file_name=f'{name_chinese}.txt')

#%%页面设置
name_chinese=st.text_input('请输入小说名称')
# name_chinese='天龙八部'
if name_chinese=='':
    st.write('积累的年代，就安然等待吧。不要焦虑，不要迷茫。时人不识凌云木，直待凌云始道高')
else:
    name=py.get(name_chinese,format='strip')
    #已经获取到小说名字————先判断是否已经有了，有了的话可直接提供下载到本地，也可选择继续下载，建议继续下载
    novel_list=os.listdir()
    if f'.\{name_chinese}.txt' in novel_list:
        #st.write('yes')
        st.write('当前平台已收录此小说，是否选择直接下载(如果是正在更新的小说，建议重新下载)')
        col1,col2=st.columns(2)
        with col1:
            if st.button('直接下载'):
                novel=open(f'.\{name_chinese}.txt','r',encoding='utf-8')
                file=os.getcwd()
                finally_file=os.path.join(file, f'{name_chinese}.txt')
                st.write(f"小说已经下载完成，存放在{finally_file}")
                st.download_button('保存到本地',novel,file_name=f'{name_chinese}.txt')
        with col2:
            if st.button('重新下载'):
                with open(f'.\{name_chinese}-1.txt','w',encoding='utf-8') as f:
                    f.close()
                novel_paqu_again(name)
    else:
        #st.write('no')
        novel_paqu(name)

# -*- coding: UTF-8 -*- 

#哔哩哔哩收藏夹

import requests
import json
import os
import time
import re
import sys
import io
import urllib.request
import threading
import random

from local_dict import localJsonType
from local_dict import saveJson




# #下载路径
DOWNLOAD_PATH = '#########'
# #要下载的收藏夹id
FAV_LIST = '#########'
# #下载线程数
THREAD_MAX = 10






# #更改输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
# #当前日期
date = time.strftime('%y-%m-%d',time.localtime(time.time()))
# #B站视频域名
BILIBILI_URL = 'https://www.bilibili.com/video/'


#创建路径
def mkdir(PATH):
	folder = os.path.exists(PATH)
	if not folder:					#判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(PATH)			#makedirs 创建文件时如果路径不存在会创建这个路径
		
def loadFavorite(path, favlist):
    ##预读取收藏夹信息
    #收藏夹api
    url = 'https://api.bilibili.com/medialist/gateway/base/spaceDetail?media_id=' + favlist + '&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&jsonp=jsonp'
    #get请求
    html = requests.get(url)
    #解析json
    res = {}
    res = json.loads(html.text)
    #总内容
    media_count = res['data']['info']['media_count']
    if (media_count==0):
        print('收藏夹里面没有视频哦，请检查收藏夹id')
        exit()
    #收藏夹主人昵称
    owner = res['data']['info']['upper']['name']
    #收藏夹名
    favname = res['data']['info']['title']

    path = path + '\\' + owner + '\\' + favname
    mkdir(path)
    
    print('下载:  ' + owner + ' 的收藏夹 \'' + favname + '\'')
    print('路径:  ' + path)
    print('正在获取收藏夹媒体信息...')
    sys.stdout.flush()
    ##分页分批次读收藏夹内容
    npage=2
    while len(res['data']['medias'])<media_count:
        #收藏夹api
        url = 'https://api.bilibili.com/medialist/gateway/base/spaceDetail?media_id=' + favlist + '&pn='+ str(npage) +'&ps=20&keyword=&order=mtime&type=0&tid=0&jsonp=jsonp'
        #get请求
        html = requests.get(url)
        #解析json
        res['data']['medias'] += json.loads(html.text)['data']['medias']
        #下一页
        npage += 1
        
    #保存原始json
    with open(path + '\\Raw.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(res, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':')))
        
    return res


def loadLocalInfo(path, res):
    #收藏夹主人昵称
    owner = res['data']['info']['upper']['name']
    #收藏夹名
    favname = res['data']['info']['title']
    PATH = path + '\\' + owner + '\\' + favname
    ##读取本地已下载记录
    localJson = {}
    localJsonPath = PATH + '\\local' + '.json'
    try:#尝试打开读取本地记录
        with open(localJsonPath, 'r', encoding='utf-8') as f:
            #读取本地记录
            try:
                localJson = json.loads(f.read(-1))
                status = localJson['status']
            except:
                print('本地记录文件损坏，请检查下载记录')
                exit()
        
    except:#否则新建本地记录
        localJson = localJsonType().localNew
        status = localJson['status']

    ##上次退出异常
    if (status=='bad'):
        print('上次下载异常退出，请检查下载文件和下载记录')
        exit()

    ##对比-更新本地记录
    localJson['info']['cover'] = res['data']['info']['cover']
    localJson['info']['intro'] = res['data']['info']['intro']
    localJson['info']['title'] = res['data']['info']['title']

    # localJson['status'] = 'bad'
    localJson['media_count'] = res['data']['info']['media_count']

    with open(localJsonPath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(localJson, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':')))
    
    return localJson


def showList(path, res, show):
    #收藏夹主人昵称
    owner = res['data']['info']['upper']['name']
    #收藏夹名
    favname = res['data']['info']['title']
    PATH = path + '\\' + owner + '\\' + favname
    
    flog = open(PATH + '\\' + favname + ' ' + date + '.log', 'w', encoding='utf-8')#  下载 21-09-05.log
    
    if (show == 1):
        print('\n****收藏夹信息****\n\n')
        sys.stdout.flush()
    
    video_urls = []
    #轮询raw.json提取视频信息
    for media in iter(res['data']['medias']):
        #大信息
        title = media['title']#标题/文件名
        slink = media['short_link']#哔哩哔哩视频短链
        page  = media['page']#分p数
        
        #给每个视频建立文件夹
        titlePath = PATH + '\\' + re.sub(r'[\\/:*?"<>|]+', "_", title)#文件名非法检测
        mkdir(titlePath)
        
        ## 下载
        #封面下载
        coverUrl = media['cover']
        urllib.request.urlretrieve(coverUrl, titlePath + '/' + 'cover.jpg')
        
        ## 输出视频标题
        #记录分p视频
        if (page!=1):
            flog.writelines(title + ' ' + str(page) + 'p\n')
            for i in range(page-1):
                flog.writelines('    ├--- ' + str(i+1) + ' ' + media['pages'][i]['title'] + '\n')
            flog.writelines('    └--- ' + str(i+2) + ' ' + media['pages'][i+1]['title'] + '\n')
        else:
            flog.writelines(title + '\n')
        flog.writelines('\n')
        
        #输出分p视频
        if (show == 1):
            if (page!=1):
                print(title + ' ' + str(page) + 'p')
                for i in range(page-1):
                    print('    ├--- ',str(i+1),media['pages'][i]['title'])
                print('    └--- ',str(i+2),media['pages'][i+1]['title'])
            else:
                print(title)
            print(' ')
        
        ##提取you-get下载信息
        if (page != 1):
            for i in range(page):
                    downloadName = re.sub(r'[\\/:*?"<>|]+', "_", media['pages'][i]['title'])#文件名非法检测
                    video_urls.append({
                        'url' : BILIBILI_URL + media['bv_id'] + '?p=' + str(i+1),
                        'name' : downloadName,
                        'path' : titlePath,
                        'size' : media['pages'][i]['dimension']
                    })
        else:
            downloadName = re.sub(r'[\\/:*?"<>|]+', "_", media['pages'][0]['title'])#文件名非法检测
            video_urls.append({
                'url' : BILIBILI_URL + media['bv_id'],
                'name' : downloadName,
                'path' : titlePath,
                'size' : media['pages'][0]['dimension']
            })
        
    flog.close()
    sys.stdout.flush()
    return video_urls
    
    
def get_max_resolution(res):
    if (res >= 1080):
        return ' '
    elif (res >= 720):
        return '720 '
    elif (res >= 480):
        return '480 '
    elif (res >= 360):
        return '360 '
        
##多线程参考:
##https://www.cnblogs.com/hanmk/p/12990017.html

def main(url, video_name, save_path, size):
    resolution = min(int(size['height']), int(size['width']))
    resolute = get_max_resolution(resolution)
        
    """
    主函数：实现下载图片功能
    :param url: 图片url
    :param image_name: 图片名称
    :return:
    """
    with pool_sema:
        print('正在下载: {}'.format(video_name))
        sys.stdout.flush()
        #完整文件路径(包含文件名及后缀)
        file_path = save_path + '\\' + video_name + '.flv'
        you_get_vedio = 'you-get --format=flv' + resolute + '-o "' + save_path + '" -O "' + video_name + '" ' + url  
        if not os.path.exists(file_path):  # 判断是否存在文件，不存在则爬取
            try:
                # print('\t' + you_get_vedio)
                os.system(you_get_vedio)
                #time.sleep(random.randint(4,9))
                # print('\t下载成功：{}'.format(video_name))
            except:
                print(video_name, " 下载失败")
            
        else:
            print(video_name, '已存在')
        sys.stdout.flush()
class MyThread(threading.Thread):
    """继承Thread类重写run方法创建新进程"""
    def __init__(self, func, args):
        """

        :param func: run方法中要调用的函数名
        :param args: func函数所需的参数
        """
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        self.func(self.args[0], self.args[1], self.args[2], self.args[3])
        # 调用func函数
        # 因为这里的func函数其实是上述的main()函数，它需要3个参数；args传入的是个参数元组，拆解开来传入
        
if __name__ == '__main__':
        
    remote_list = {}
    remote_list = loadFavorite(DOWNLOAD_PATH, FAV_LIST)
    
    local_list = {}
    local_list = loadLocalInfo(DOWNLOAD_PATH, remote_list)
    
    down_list = []
    down_list = showList(DOWNLOAD_PATH, remote_list, 0)
    
    pool_sema = threading.BoundedSemaphore(THREAD_MAX) # 或使用Semaphore方法
    
    print('正在下载收藏夹\'{}\'\n\n'.format(remote_list['data']['info']['title']))
    sys.stdout.flush()
    
    thread_list = []
    for t in down_list:
        m = MyThread(main, (t["url"], t["name"], t["path"], t["size"]))  # 调用MyThread类，得到一个实例
        thread_list.append(m)

    for m in thread_list:
        m.start()  # 调用start()方法，开始执行

    for m in thread_list:
        m.join()  # 子线程调用join()方法，使主线程等待子线程运行完毕之后才退出
    
    ######下载之前判定文件是否存在::根据文件名（若up主改分p标题，也会重新下载：增量下载）
    ######多线程（线程数可选）下载
    ######annie 作者：思思陆思思 https://www.bilibili.com/read/cv5720475/ 出处：bilibili
    ######you-get反反爬
    ######you-get 多文件/多p下载，分p命名
    ######断点续传
    
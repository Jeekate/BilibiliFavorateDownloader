# -*- coding: UTF-8 -*- 
 
class localJsonType(object):
    localNew = {"info":{"cover":"","intro":"","title":""},"medias":[],"local":0,"total":0,"media_count":0,"status":"new"}

    
class saveJson(object):
    def save(local, src):
        mediaType = {"bv_id":"","bvid":"","cover":"","duration":0,"intro":"","page":0,"pages":[],"pubtime":0,"short_link":"","title":""}
        for item in iter(mediaType):
        
            if (item == 'pages'):
                for i in range(src['page']):#分p视频 第(i+1)个视频
                    pageType = {"dimension":{},"duration":0,"page":0,"title":""}
                    for pageItem in iter(pageType):
                        pageType[pageItem] = src['pages'][i][pageItem]
                    
                    mediaType['pages'].append(pageType)
            else:
                mediaType[item] = src[item]
        local.append(mediaType)
    
#data{}
{
    "info":
    {
        "cover":"收藏夹封面.jpg",
        "intro":"收藏夹简介",
        "title":"收藏夹标题"
    },
    "medias":[],
    "local":0,
    "total":0,
    "media_count":0,
    "status":"new"
}
#medias[]
{
    "bv_id":"视频bv号",
    "bvid":"视频bv号",
    "cover":"视频封面.jpg",
    "duration":0,
    "intro":"视频简介",
    
    "page":0,
    "pages":[],
    
    "pubtime":0,

    "short_link":"https://b0.tv/BV0Kh0W0Yp",
    "title":"视频标题"
}
#pages[]
{
    "dimension":{"height":0,"rotate":0,"width":0},
    "duration":0,
    "page":0,
    "title":"分p标题"
}
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    cityName = scrapy.Field()               # 城市名
    distinctName = scrapy.Field()           # 区名
    areaName = scrapy.Field()               # 二级区域名
    categoryLevelA = scrapy.Field()         # 一级分类
    categoryLevelB = scrapy.Field()         # 二级分类
    restaurantName = scrapy.Field()         # 店名
    restaurantStar = scrapy.Field()         # 店家总体评分
    scoreOfTaste = scrapy.Field()           # 店家口味评分
    scoreOfEnvironment = scrapy.Field()     # 店家环境评分
    scoreOfService = scrapy.Field()         # 店家服务评分
    averageCost = scrapy.Field()            # 平均消费
    restaurantAddress = scrapy.Field()      # 店址
    restaurantTel = scrapy.Field()          # 电话
    # recipeLiked = scrapy.Field()          #推荐菜(这个没有爬到)
    commentCount = scrapy.Field()           # 评论数
    commentSum = scrapy.Field()             # 评论总结

    rankTotal_5_Count = scrapy.Field()      # 总评给5星的人数
    rankTotal_4_Count = scrapy.Field()
    rankTotal_3_Count = scrapy.Field()
    rankTotal_2_Count = scrapy.Field()
    rankTotal_1_Count = scrapy.Field()

    customerName = scrapy.Field()           # 顾客用户名
    customerLevel = scrapy.Field()          # 顾客星级  0-199  200-399  400-999 1000-1999 2000-4999 5000-
    customerVIP = scrapy.Field()            # 顾客是否是VIP   http://www.dianping.com/vdper/index
    commRankTotal = scrapy.Field()          # 总体星级评价
    commRankTaste = scrapy.Field()          # 口味星级评价
    commRankEnvironment = scrapy.Field()    # 环境星级评价
    commRankService = scrapy.Field()        # 服务星级评价
    commCostPer = scrapy.Field()            # 用户填的人均消费
    commentContent = scrapy.Field()         # 评论内容
    commentLiked = scrapy.Field()           # 评论被赞数
    commentDate = scrapy.Field()            # 评论日期

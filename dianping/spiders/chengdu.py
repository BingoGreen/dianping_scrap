# -*- coding: utf-8 -*-
import scrapy
from dianping.items import DianpingItem
from scrapy.http import Request
import re
from bs4 import BeautifulSoup
from lxml import etree


class Shenzhen(scrapy.Spider):
    name = 'chengdu'
    #allowed_domains = ['dianping.com']
    #start_urls = ['http://www.dianping.com/shenzhen/food']

    def start_requests(self):
        cookies = {'_hc.v':'8654cd8b-0489-5fa2-f99f-44188026fdac.1499862484',
            'dper':'b4445f2b0b95a6af2d8be13348186e2fcd96ecbbf6bea2c4febd34e5eea8a0e0',
            'ua':'15813742616',
            '__utma':'1.1767765916.1499862484.1500695080.1500699351.4',
            '__utmc':'1',
            '__utmz':'1.1499862484.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
            'll':'7fd06e815b796be3df069dec7836c3df',
            '_lxsdk_cuid':'15d69b0020bc8-0724c4d1ee9696-8383667-1aeaa0-15d69b0020cc8',
            '_lxsdk':'15d69b0020bc8-0724c4d1ee9696-8383667-1aeaa0-15d69b0020cc8',
            'PHOENIX_ID':'0a010725-15d6977971e-55ce959',
            '__mta':'217823785.1500716732776.1500717103138.1500720988445.6',
            's_ViewType':'10',
            '_lxsdk_s':'15d6a371f2c-4d3-7f4-3ff%7C%7C5',
            'JSESSIONID':'2B99F3BA03316D61330AFD385DA2E49',
            'aburl':'1',
            'cy':'1',
            'cye':'shanghai'
        }

        yield Request('http://www.dianping.com/chengdu/food', meta={'cityName': 'Chengdu'}, cookies=cookies,
                      callback=self.parse)


    def parse(self, response):
        #box用来截取二级区域那一块网页源代码
        box = re.findall(r'<div class="fpp_business">.*?</a></li> </ul> </dd> </dl> </div> </div>', response.body.decode('utf-8'))
        box = box[0]
        soup = BeautifulSoup(box, 'lxml')
        soup = soup.prettify()
        soup = etree.HTML(soup)
        distincts = soup.xpath('//dl')
        cityName = response.meta['cityName']
        for distinct in distincts:
            #区名
            distinctName = distinct.xpath('dt/a/text()')[0].strip()
            areas = distinct.xpath('dd/ul/li')
            for area in areas:
                #areaName = distinct.xpath('a/text()').extract()[0]
                #获取二级区域的链接
                areaURL = area.xpath('a/@href')[0]  # 不是完整地址
                #进入二级区域页面，获取每家店的链接
                yield Request('http://www.dianping.com'+areaURL, meta = {'distinctName':distinctName,'cityName':cityName}, callback = self.parse_area)

    def parse_area(self, response):
        distinctName = response.meta['distinctName']
        cityName = response.meta['cityName']
        restaurants = response.xpath('//*[@id = "shop-all-list"]/ul/li')
        #print('\n\n\n\n\n\n', response.headers, response.url)
        for restaurant in restaurants:
            restaurantURL = restaurant.xpath('div[@class = "txt"]/div[1]/a/@href').extract()[0]  #不是完整地址
            print('http://www.dianping.com' + restaurantURL)
            #进入店家地址，开始抓数据
            yield Request('http://www.dianping.com'+restaurantURL, meta = {'distinctName':distinctName, 'cityName': cityName}, callback = self.parse_restaurant)
        #获取下一页的链接
        try:
            nextlink = response.xpath('//div[@class = "page"]/a[last()]/@href').extract()[0] #不是完整地址
            yield Request('http://www.dianping.com'+nextlink, meta = {'distinctName': distinctName, 'cityName': cityName}, callback = self.parse_area)
            #print('\n\n\n\n\nabc')
        except:
            pass

    def parse_restaurant(self, response):
        distinctName = response.meta['distinctName']
        cityName = response.meta['cityName']
        '''breadcrumb = response.xpath('//*[@id = "body"]//div[@class = "breadcrumb"]/a/text()').extract()
        areaName = breadcrumb[1].strip()
        categoryLevelA = breadcrumb[2].strip()
        try:
            categoryLevelB = breadcrumb[3].strip()
        except:
            categoryLevelB = categoryLevelA'''
        restaurantName = response.xpath('//h1[@class = "shop-name"]/text()').extract()[0].strip()
        restaurantStar = response.xpath('//div[@class = "brief-info"]/span[1]/@class').extract()[0]
        restaurantStar = int(re.match(r'.*?(\d+)',restaurantStar).group(1))
        if restaurantStar == 50:
            restaurantStar = 10
        elif restaurantStar == 45:
            restaurantStar = 9
        elif restaurantStar == 40:
            restaurantStar = 8
        elif restaurantStar == 35:
            restaurantStar = 7
        elif restaurantStar == 30:
            restaurantStar = 6
        elif restaurantStar == 25:
            restaurantStar = 5
        elif restaurantStar == 20:
            restaurantStar = 4
        elif restaurantStar == 15:
            restaurantStar = 3
        elif restaurantStar == 10:
            restaurantStar = 2
        elif restaurantStar == 5:
            restaurantStar = 1
        else:
            restaurantStar = 0

        score = response.xpath('//div[@class = "brief-info"]/span[@id = "comment_score"]/span/text()').extract()
        try:
            scoreOfTaste = float(score[0][3:])
            scoreOfEnvironment = float(score[1][3:])
            scoreOfService = float(score[2][3:])
        except:
            scoreOfTaste = ''
            scoreOfEnvironment = ''
            scoreOfService = ''
        try:
            averageCost = re.match(r'.*?(\d+)', response.xpath('//div[@class = "brief-info"]/span[@id = "avgPriceTitle"]/text()').extract()[0]).group(1)
            averageCost = int(averageCost)
        except:
            averageCost = ''
        restaurantAddress = response.xpath('//div[@class = "expand-info address"]/span[2]/text()').extract()[0].strip()
        restaurantTel = response.xpath('//p[@class = "expand-info tel"]/span[2]/text()').extract()
        try:
            restaurantTel = restaurantTel[0]
        except:
            restaurantTel = '无联系方式'
        try:
            commentCount = re.match(r'(\d+)',response.xpath('//div[@class = "brief-info"]/span[@id = "reviewCount"]/text()').extract()[0]).group(1)
            commentCount = int(commentCount)
        except:
            commentCount = ''
        commentSum = response.xpath('//*[@id = "summaryfilter-wrapper"]//div[@class = "content"]/span//text()').extract()
        if not len(commentSum) == 0:
           commentSum = ','.join(commentSum)
        else:
           commentSum = '无评论总结'

        #commentURL = response.xpath('//*[@id = "morelink-wrapper"]/p/a/@href').extract()[0]
        commentURL = response.url + '/review_more'
        #print('http://www.dianping.com' + commentURL)
        yield Request(commentURL, meta = {
            'distinctName': distinctName,
            'cityName' : cityName,
            #'areaName': areaName,
            #'categoryLevelA': categoryLevelA,
            #'categoryLevelB': categoryLevelB,
            'restaurantName': restaurantName,
            'restaurantStar': restaurantStar,
            'scoreOfTaste': scoreOfTaste,
            'scoreOfEnvironment': scoreOfEnvironment,
            'scoreOfService': scoreOfService,
            'averageCost': averageCost,
            'restaurantAddress': restaurantAddress,
            'restaurantTel': restaurantTel,
            'commentCount': commentCount,
            'commentSum': commentSum},
                      callback = self.parse_comment)

    def parse_comment(self, response):
        item = DianpingItem()
        categoryLevelA_range = ['面包甜点', '自助餐', '咖啡厅', '西餐', '台湾菜', '贵州菜', '江西菜', '东南亚菜', '其他', '俄罗斯菜', '新疆菜', '粤菜', '素菜', '日本料理', '日本菜', '云贵菜', '小吃快餐', '家常菜', '私房菜', '串串香', '本帮江浙菜', '江浙菜', '苏州江浙', '烧烤', '烤鱼', '鲁菜', '客家菜', '南京/江浙菜', '蟹宴', '茶馆', '创意菜', '面馆', '酒吧', '北京菜', '快餐简餐', '小吃', '海鲜', '火锅', '湘菜', '川菜', '兔头/兔丁', '西北菜', '粥粉面', '云南菜', '粤菜/潮州菜', '东北菜', '农家菜', '小龙虾', '大闸蟹', '粉面馆', '湖北菜', '杭帮/江浙菜', '茶餐厅', '徽菜', '闽菜', '韩国料理']
        customers = response.xpath('//div[@class = "comment-list"]/ul/li')
        crumb = response.xpath('//div[@class = "crumb"]//li')
        if len(crumb) == 7:
            areaName = crumb[2].xpath('strong//span/text()').extract()[0]
            categoryLevelA = crumb[3].xpath('strong//span/text()').extract()[0]
            categoryLevelB = crumb[4].xpath('strong//span/text()').extract()[0]
        elif len(crumb) == 6:
            categoryLevelA = crumb[-3].xpath('strong//span/text()').extract()[0]
            if categoryLevelA in categoryLevelA_range:
                categoryLevelA = categoryLevelA
                categoryLevelB = categoryLevelA
                areaName = crumb[-4].xpath('strong//span/text()').extract()[0]
            else:
                categoryLevelB = categoryLevelA
                categoryLevelA = crumb[-4].xpath('strong//span/text()').extract()[0]
                areaName = crumb[-5].xpath('strong//span/text()').extract()[0]
        else:
            areaName = crumb[1].xpath('strong//span/text()').extract()[0]
            categoryLevelA = crumb[-3].xpath('strong//span/text()').extract()[0]
            categoryLevelB = categoryLevelA
        if len(customers) == 0:
            item['distinctName'] = response.meta['distinctName']
            item['cityName'] = response.meta['cityName']
            item['areaName'] = areaName
            item['categoryLevelA'] = categoryLevelA
            item['categoryLevelB'] = categoryLevelB
            item['restaurantName'] = response.meta['restaurantName']
            item['restaurantStar'] = response.meta['restaurantStar']
            item['scoreOfTaste'] = response.meta['scoreOfTaste']
            item['scoreOfEnvironment'] = response.meta['scoreOfEnvironment']
            item['scoreOfService'] = response.meta['scoreOfService']
            item['averageCost'] = response.meta['averageCost']
            item['restaurantAddress'] = response.meta['restaurantAddress']
            item['restaurantTel'] = response.meta['restaurantTel']
            item['commentCount'] = response.meta['commentCount']
            item['commentSum'] = response.meta['commentSum']
            item['rankTotal_5_Count'] = ''
            item['rankTotal_4_Count'] = ''
            item['rankTotal_3_Count'] = ''
            item['rankTotal_2_Count'] = ''
            item['rankTotal_1_Count'] = ''
            item['customerName'] = ''
            item['customerLevel'] = ''
            item['customerVIP'] = ''
            item['commRankTotal'] = ''
            item['commRankTaste'] = ''
            item['commRankEnvironment'] = ''
            item['commRankService'] = ''
            item['commCostPer'] = ''
            item['commentContent'] = ''
            item['commentDate'] = ''
            item['commentLiked'] = ''
            yield item
        else:
            rankTotal_5_Count = response.xpath('//div[@class = "comment-star"]/dl/dd[2]//text()').extract()[1]
            rankTotal_5_Count = int(rankTotal_5_Count.replace('(','').replace(')',''))
            rankTotal_4_Count = response.xpath('//div[@class = "comment-star"]/dl/dd[3]//text()').extract()[1]
            rankTotal_4_Count = int(rankTotal_4_Count.replace('(','').replace(')',''))
            rankTotal_3_Count = response.xpath('//div[@class = "comment-star"]/dl/dd[4]//text()').extract()[1]
            rankTotal_3_Count = int(rankTotal_3_Count.replace('(','').replace(')',''))
            rankTotal_2_Count = response.xpath('//div[@class = "comment-star"]/dl/dd[5]//text()').extract()[1]
            rankTotal_2_Count = int(rankTotal_2_Count.replace('(','').replace(')',''))
            rankTotal_1_Count = response.xpath('//div[@class = "comment-star"]/dl/dd[6]//text()').extract()[1]
            rankTotal_1_Count = int(rankTotal_1_Count.replace('(','').replace(')',''))
            for customer in customers:
                distinctName = response.meta['distinctName']
                cityName = response.meta['cityName']
                areaName = areaName
                categoryLevelA = categoryLevelA
                categoryLevelB = categoryLevelB
                restaurantName = response.meta['restaurantName']
                restaurantStar = response.meta['restaurantStar']
                scoreOfTaste = response.meta['scoreOfTaste']
                scoreOfEnvironment = response.meta['scoreOfEnvironment']
                scoreOfService = response.meta['scoreOfService']
                averageCost = response.meta['averageCost']
                restaurantAddress = response.meta['restaurantAddress']
                restaurantTel = response.meta['restaurantTel']
                commentCount = response.meta['commentCount']
                commentSum = response.meta['commentSum']

                customerName = customer.xpath('div[1]//p[@class = "name"]/a/text()').extract()[0]
                customerLevel = customer.xpath('div[1]//p[@class = "contribution"]/span/@title').extract()[0]
                if customerLevel == '':
                    customerLevel = 1
                elif '200' in customerLevel:
                    customerLevel = 2
                elif '400' in customerLevel:
                    customerLevel = 3
                elif '1000' in customerLevel:
                    customerLevel = 4
                elif '2000' in customerLevel:
                    customerLevel = 5
                elif '5000' in customerLevel:
                    customerLevel = 6
                else:
                    customerLevel = ''
                customerVIP = customer.xpath('div[1]//i[@class = "icon-vip"]').extract()
                if len(customerVIP) != 0:
                    customerVIP = 1
                else:
                    customerVIP =0
                try:
                    commRankTotal = customer.xpath('div[2]//div[@class = "user-info"]/span[1]/@class').extract()[0]
                    commRankTotal = int(commRankTotal[-2])
                except:
                    commRankTotal = ''
                rankList = customer.xpath('div[2]//div[@class = "comment-rst"]/span/text()').extract()
                try:
                    commRankTaste = int(rankList[0][-1])
                    commRankEnvironment = int(rankList[1][-1])
                    commRankService = int(rankList[2][-1])
                except:
                    commRankTaste = ''
                    commRankEnvironment = ''
                    commRankService = ''
                try:
                    commCostPer = customer.xpath('div[2]//div[@class = "user-info"]/span[2]/text()').extract()[0]
                    commCostPer = int(re.match(r'.*?(\d+)', commCostPer).group(1))
                except:
                    commCostPer = ''
                commentContent = ('\n'.join(customer.xpath('div[2]//div[@class = "J_brief-cont"]//text()').extract())).strip()
                commentDate = customer.xpath('div[2]//div[@class = "misc-info"]/span[@class = "time"]/text()').extract()[0]
                commentLiked = customer.xpath('div[2]//span[@class = "col-right"]/span[1]/a/span/text()').extract()
                try:
                    commentLiked = commentLiked[1].replace('(','').replace(')','')
                    commentLiked = int(commentLiked)
                except:
                    commentLiked = ''
                item['cityName'] = cityName
                item['distinctName'] = distinctName
                item['areaName'] = areaName
                item['categoryLevelA'] = categoryLevelA
                item['categoryLevelB'] = categoryLevelB
                item['restaurantName'] = restaurantName
                item['restaurantStar'] = restaurantStar
                item['scoreOfTaste'] = scoreOfTaste
                item['scoreOfEnvironment'] = scoreOfEnvironment
                item['scoreOfService'] = scoreOfService
                item['averageCost'] = averageCost
                item['restaurantAddress'] = restaurantAddress
                item['restaurantTel'] = restaurantTel
                item['commentCount'] = commentCount
                item['commentSum'] = commentSum
                item['rankTotal_5_Count'] = rankTotal_5_Count
                item['rankTotal_4_Count'] = rankTotal_4_Count
                item['rankTotal_3_Count'] = rankTotal_3_Count
                item['rankTotal_2_Count'] = rankTotal_2_Count
                item['rankTotal_1_Count'] = rankTotal_1_Count
                item['customerName'] = customerName
                item['customerLevel'] = customerLevel
                item['customerVIP'] = customerVIP
                item['commRankTotal'] = commRankTotal
                item['commRankTaste'] = commRankTaste
                item['commRankEnvironment'] = commRankEnvironment
                item['commRankService'] = commRankService
                item['commCostPer'] = commCostPer
                item['commentContent'] = commentContent
                item['commentDate'] = commentDate
                item['commentLiked']= commentLiked
                yield item
            try:
                origin_url = re.match(r'(http:.*?more)', response.url).group(1)        #后面重新调用此函数，response.url会改变，需要re去掉？参数，变回最初的url
                nextlink = origin_url + response.xpath('//div[@class = "Pages"]/a[last()]/@href').extract()[0]
                yield Request(nextlink, meta = {
                'distinctName': distinctName,
                'cityName': cityName,
                #'areaName': areaName,
                #'categoryLevelA': categoryLevelA,
                #'categoryLevelB': categoryLevelB,
                'restaurantName': restaurantName,
                'restaurantStar': restaurantStar,
                'scoreOfTaste': scoreOfTaste,
                'scoreOfEnvironment': scoreOfEnvironment,
                'scoreOfService': scoreOfService,
                'averageCost': averageCost,
                'restaurantAddress': restaurantAddress,
                'restaurantTel': restaurantTel,
                'commentCount': commentCount,
                'commentSum': commentSum},
                              callback = self.parse_comment)
            except:
                pass








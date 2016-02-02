# python-for-data-analysis
practice


#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-01-17 17:17:37
# Project: Qianchengwuyou
import re
import urlparse
import HTMLParser
import json
import time
import random

import pymongo
from pyspider.libs.base_handler import *


client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['51job']
collections = db['resume']


class Handler(BaseHandler):
    host = 'http://ehire.51job.com/'
    headers = {
        "Host": "ehire.51job.com",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
    }
    html_parser = HTMLParser.HTMLParser()
    
    crawl_config = {
        'itag': 'v20',
        'last_modifed': False,
    }

    def _set_cookies(self, cookies):
        self._cookies = cookies

    def get_cookies(self):
        return self._cookies
    
    def on_start(self):
        self.crawl('http://ehire.51job.com/MainLogin.aspx',
                       headers={"Host": "ehirelogin.51job.com",
                           "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0",
                           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                           "Accept-Language": "en-US,en;q=0.5",
                           "Accept-Encoding": "gzip, deflate",
                           "Referer": "http://ehire.51job.com/MainLogin.aspx",
                           "Connection": "keep-alive",
                           },
                        method='GET',
                        callback=self.init)
    
    def init(self, response):
        self.crawl('https://ehirelogin.51job.com/Member/UserLogin.aspx', 
           headers={
               "Host": "ehirelogin.51job.com",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Referer": "http://ehire.51job.com/MainLogin.aspx",
                "Connection": "keep-alive"
           },
           cookies=response.cookies,
           fetch_type='js',
           data={
               'userName': 'zkkj294', 'password': 'qwe12312',
              'ctmName': '%E6%89%BE%E5%BA%93%E7%A7%91%E6%8A%80',
              'checkCode': "", 'oldAccessKey': "f9a81e560db34a7",
              'langtype': "Lang=&Flag=1", 'isRememberMe':"true",
              'sc': "fe8a33fffe305b1d", 'returl':"",
              'ec':"867aaac1f3fc4d00a9f2d37867638ca4"
           },
           callback=self.search_resume,
        )
    
    def search_resume(self, response):
        headers = self.headers.copy()
        headers.update({
            "Referer": "http://ehire.51job.com/MainLogin.aspx",
        })
        data = {
                "AREA$Value":"",
                "DpSearchList":"",
                "JOBSTATUS":"99",
                "KEYWORD":"ios",
                "LASTMODIFYSEL":"5",
                "MainMenuNew1$CurMenuID":"MainMenuNew1_imgResume|sub4",
                "SEX":"99",
                "TopDegreeFrom":"",
                "TopDegreeTo":"",
                "WORKFUN1$Text":u"最多只允许选择3个项目",
                "WORKFUN1$Value":u"$高级软件工程师|0106$软件工程师|0107$软件UI设计师/工程师|0144$",
                "WORKINDUSTRY1$Text":u"最多只允许选择3个项目",
                "WORKINDUSTRY1$Value":"",
                "WorkYearFrom":"0",
                "WorkYearTo":"99",
                "__EVENTARGUMENT":"",
                "__EVENTTARGET":"",
                "__LASTFOCUS":"",
                "ddlEndDate":"7",
                "ddlSendCycle":"1",
                "ddlSendNum":"10",
                "hidChkedExpectJobArea":"",
                "hidChkedKeyWordType":"2",
                "hidChkedRelFunType":"",
                "hidIsFirstLoadJobDiv":"1",
                "hidNeedRecommendFunType":"",
                "hidPostBackFunType":"",
                "hidSearchID":"2,3,6,23,8,1,4,5,25,2,3,6,23,2,3,6,23,2,3,6,23",
                "hidSearchNameID":"",
                "hidTable":"",
"hidValue":"KEYWORDTYPE#2*LASTMODIFYSEL#5*JOBSTATUS#99*WORKYEAR#0|99*SEX#99*AREA#*TOPDEGREE#|*WORKINDUSTRY1#*WORKFUN1#$高级软件工程师|0106$软件工程师|0107$软件UI设计师/工程师|0144$*KEYWORD#ios",
"hidWhere":"00#2#0#0|99|20150716|20160116|99|99|99|99|99|000000|000000|99|99|99|0000|99|99|99|00|010601070144|99|99|99|0000|99|99|00|99|99|99|99|99|99|99|99|99|000000|0|0|0000#%BeginPage%#%EndPage%#ios",
                "txtJobName":"",
                "txtSearchName":"",
                "txtSendEmail":"",
                "txtUserID":u"--多个ID号用空格隔开--",
        }
        view_state = re.search('id="__VIEWSTATE"\s*value="(.*?)"', response.text, re.MULTILINE).group(1)
        data['__VIEWSTATE'] = view_state

        self.crawl('http://ehire.51job.com/Candidate/SearchResume.aspx',
            method='POST',
            headers=headers,
            data=data,
            fetch_type='js',
            js_script="""
               function() {
                   window.scrollTo(0,document.body.scrollHeight);
               }
            """,
            cookies=response.cookies,
            callback=self.resume_first_page,
            save={'cookies': response.cookies},
        )
        # return {
        #     "url": response.url,
        #     "title": response.doc('title').text(),
        # }

    def resume_first_page(self, response):
        cookies = response.save['cookies']
        content = response.text
        headers = self.headers.copy()
        headers.update({
            'Referer': 'http://ehire.51job.com/Candidate/SearchResume.aspx'
        })
        data = {
            "cbxColumns$0": "AGE",
            "cbxColumns$1": "WORKYEAR",
            "cbxColumns$14": "LASTUPDATE",
            "cbxColumns$2": "SEX",
            "cbxColumns$4": "AREA",
            "cbxColumns$8": "TOPMAJOR",
            "cbxColumns$9": "TOPDEGREE",
            "ctrlSerach$AREA$Text": u"选择/修改",
            "ctrlSerach$JOBSTATUS": "99",
            "ctrlSerach$KEYWORD": "ios",
            "ctrlSerach$KEYWORDTYPE": "2",
            "ctrlSerach$LASTMODIFYSEL": "5",
            "ctrlSerach$SEX": "99",
            "ctrlSerach$WORKFUN1$Text": u"高级软件工程师,软件工程师,软件UI设计师/工程师",
            "ctrlSerach$WORKFUN1$Value": u"$高级软件工程师|0106$软件工程师|0107$软件UI设计师/工程师|0144$",
            "ctrlSerach$WORKINDUSTRY1$Text": u"选择/修改",
            "ctrlSerach$WorkYearFrom": "0",
            "ctrlSerach$WorkYearTo": "99",
            "ctrlSerach$hidChkedExpectJobArea": "0",
            "ctrlSerach$hidSearchID": "23,25,5,8,3,6,4,1,2",
            "ctrlSerach$txtUserID": u"-多个简历ID用空格隔开-",
            "hidDisplayType": "0",
            "hidValue": u"KEYWORDTYPE#2*LASTMODIFYSEL#5*JOBSTATUS#99*WORKYEAR#0|99*SEX#99*TOPDEGREE#|*WORKFUN1#$高级软件工程师|0106$软件工程师|0107$软件UI设计师/工程师|0144$*KEYWORD#ios",
            "hidWhere": u"00#2#0#0|99|20150731|20160131|99|99|99|99|99|000000|000000|99|99|99|0000|99|99|99|00|010601070144|99|99|99|0000|99|99|00|99|99|99|99|99|99|99|99|99|000000|0|0|0000|99#%BeginPage%#%EndPage%#ios",
            "hidYellowTip": "0",
            "pagerBottom$nextButton": u"下一页",
            "pagerBottom$txtGO": 0,
        }
        resume_url_list = re.findall('<a href="(/Candidate/ResumeView\.aspx.*?)"', content, re.MULTILINE)
        resume_url_list = [self.html_parser.unescape(urlparse.urljoin(self.host, relative_url)) for relative_url in resume_url_list]
        print 'first page resume number is %s' % len(resume_url_list)
        resume_url_list = re.findall('<a href="(/Candidate/ResumeView\.aspx.*?)"', content, re.MULTILINE)
        resume_url_list = [self.html_parser.unescape(urlparse.urljoin(self.host, relative_url)) for relative_url in resume_url_list]
        # for resume_url in resume_url_list:
        #     self.crawl(
        #         resume_url,
        #         cookies=cookies,
        #         headers={
        #             "Host": "ehire.51job.com",
        #             "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0",
        #             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #             "Accept-Language": "en-US,en;q=0.5",
        #             "Accept-Encoding": "gzip, deflate",
        #             "Referer": "http://ehire.51job.com/Candidate/SearchResume.aspx",
        #             "Connection": "keep-alive",
        #             "Cache-Control": "max-age=0",
        #         },
        #         method='GET',
        #         callback=self.parse_resume,
        #         exetime=time.time() + random.randint(1, 20),
        #     )
        # disable = re.search(r'class="ctrlPaginationBt3" disabled="disabled"', response.text, re.MULTILINE)
        pagerBottom_txtGO = int(data.get('pagerBottom$txtGO', 0))
        # if pagerBottom_txtGO < 300:  # has next page
        view_state = re.search('id="__VIEWSTATE"\s*value="(.*?)"', response.text, re.MULTILINE)
        hidCheckKey = re.search('id="hidCheckKey"\s*value="(.*?)"', response.text, re.MULTILINE)
        hidCheckUserIds = re.search('id="hidCheckUserIds"\s*value="(.*?)"', response.text, re.MULTILINE)
        data['__VIEWSTATE'] = view_state and view_state.group(1)
        data['hidCheckKey'] = hidCheckKey and hidCheckKey.group(1)
        data['hidCheckUserIds'] = hidCheckUserIds and hidCheckUserIds.group(1)
        pagerBottom_txtGO += 1
        data['pagerBottom$txtGO'] = pagerBottom_txtGO
        data['pagerBottom$nextButton'] = u'下一页'
        self.crawl(
            'http://ehire.51job.com/Candidate/SearchResume.aspx',
            method='POST',
            data=data,
            fetch_type='js',
            js_script="""
               function() {
                   window.scrollTo(0,document.body.scrollHeight);
               }
            """,
            cookies=cookies,
            headers=headers,
            callback=self.resume_detail,
            save={'cookies': cookies, 'data': data},
            exetime=time.time() + 7
        )
        return {
            "url": response.url,
            "title": response.doc('title').text(),
            "page": pagerBottom_txtGO,
            "next_page": pagerBottom_txtGO + 1,
        }


    def resume_detail(self, response):
        cookies = response.save['cookies']
        content = response.text
        headers = self.headers.copy()
        headers.update({
            'Referer': 'http://ehire.51job.com/Candidate/SearchResume.aspx'
        })
        resume_url_list = re.findall('<a href="(/Candidate/ResumeView\.aspx.*?)"', content, re.MULTILINE)
        resume_url_list = [self.html_parser.unescape(urlparse.urljoin(self.host, relative_url)) for relative_url in resume_url_list]
        for resume_url in resume_url_list:
            self.crawl(
                resume_url,
                cookies=cookies,
                headers={
                    "Host": "ehire.51job.com",
                    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate",
                    "Referer": "http://ehire.51job.com/Candidate/SearchResume.aspx",
                    "Connection": "keep-alive",
                    "Cache-Control": "max-age=0",
                },
                method='GET',
                callback=self.parse_resume,
                exetime=time.time() + random.randint(1, 20),
            )
        # disable = re.search(r'class="ctrlPaginationBt3" disabled="disabled"', response.text, re.MULTILINE)
        data = response.save['data'].copy()
        pagerBottom_txtGO = int(data.get('pagerBottom$txtGO', 0))
        # if pagerBottom_txtGO < 300:  # has next page
        view_state = re.search('id="__VIEWSTATE"\s*value="(.*?)"', response.text, re.MULTILINE)
        hidCheckKey = re.search('id="hidCheckKey"\s*value="(.*?)"', response.text, re.MULTILINE)
        hidCheckUserIds = re.search('id="hidCheckUserIds"\s*value="(.*?)"', response.text, re.MULTILINE)
        data['__VIEWSTATE'] = view_state and view_state.group(1)
        data['hidCheckKey'] = hidCheckKey and hidCheckKey.group(1)
        data['hidCheckUserIds'] = hidCheckUserIds and hidCheckUserIds.group(1)
        pagerBottom_txtGO += 1
        print 'page %s , resume number is %s' % (pagerBottom_txtGO, len(resume_url_list))
        data['pagerBottom$txtGO'] = pagerBottom_txtGO
        data['pagerBottom$nextButton'] = u'下一页'
        self.crawl(
            'http://ehire.51job.com/Candidate/SearchResume.aspx',
            method='POST',
            data=data,
            fetch_type='js',
            js_script="""
               function() {
                   window.scrollTo(0,document.body.scrollHeight);
               }
            """,
            cookies=cookies,
            headers=headers,
            callback=self.resume_detail,
            save={'cookies': cookies, 'data': data},
            exetime=time.time() + 17,
        )
        return {
            "url": response.url,
            "title": response.doc('title').text(),
            "page": pagerBottom_txtGO,
        }

    @config(priority=2)
    def parse_resume(self, response):
        content = response.text

        data = {}
        id = re.findall(r'<b>\s*ID:(\d*)</b>', content, re.MULTILINE)
        id = id and id[0]
        if id and not collections.find_one({'_id': id}):
            data['_id'] = id
            job = 'ios'
            data['job'] = job
            experiences = re.findall(r'<td.*?><span class="blue"><b>([\s\S]*?)\|', content, re.MULTILINE)
            print 'experiences is %s' % experiences
            data['experiences'] = (experiences or None) and re.sub(r'\s', '', experiences[0])
            city = re.findall(u'目标地点：\s*<span.*?>([\s\S]*?)</span>', content, re.MULTILINE)
            print 'city is %s' % city
            data['city'] = (city or None) and re.sub(r'\s', '', city[0])
            expected_salary = re.findall(u'期望薪资：\s*<span.*?>([\s\S]*?)</span>', content, re.MULTILINE)
            print 'expected_salary is %s' % expected_salary
            data['expected_salary'] = (expected_salary or None) and re.sub(r'\s', '', expected_salary[0])
            current_salary = re.findall(u'目前薪资：</td><td.*?>([\S\s]*?)</td>', content, re.MULTILINE)
            print 'current_salary is %s' % current_salary
            current_salary = (current_salary or None) and current_salary[0]
            if current_salary:
                data['current_salary'] = re.sub(r'\s', '', current_salary)
            expected_industry = re.findall(u'希望行业：\s*<span.*?>([\s\S]*?)</span>', content, re.MULTILINE)
            data['expected_industry'] = (expected_industry or None) and re.sub(r'\s', '', expected_industry[0])
            expected_position = re.findall(u'目标职能：\s*<span.*?>([\s\S]*?)</span>', content, re.MULTILINE)
            data['expected_position'] = (expected_position or None) and re.sub(r'\s', '', expected_position[0])
            print json.dumps(data, indent=4)
            collections.save(data)
            data['url'] = response.url
            data['title'] = response.doc('title').text()
            return data

    
    def print_page(self, response):
        print "**************************************************"
        return {'url': response.url,
                'content': response.text}

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/2 14:29
# @Author  : HT
# @Site    : 
# @File    : main.py
# @Software: PyCharm Community Edition
# @Describe: Desc
# @Issues  : Issues

from BaseModule import HTTPRequest
from BaseModule.WebDriverManager import WebDriverManager
import time, re
import json
from BaseModule import DateProcessing

from lxml import  etree
from BaseModule import MySqlOperationer

DOUMI_URL = "https://vip.doumi.com/login"


def _getPostId(html_source):
    htmlEmt = etree.HTML(html_source)
    results = htmlEmt.xpath('//div[@class="bList-item-opBtn"]')
    # print(result)
    post_ids = list()
    for result in results:
        result_source = etree.tostring(result).decode('utf-8')
        # print(result_source)
        result = re.findall(r'post_id=(.*?)&', result_source)
        if len(result) > 0:
            post_ids.append(result[0])
    return post_ids
# def _longinGetHeaderAndToken():

def _getInfosPostID(zhiwei_name, post_id, header, token):
    url = 'https://vip.doumi.com/employer/manage/ajaxscreen'

    types_map = {
        '0' : '待处理',
        '12': '通过初筛',
        '3': '待面试',
        '5': '已录用',
    }
    for type_num, typename in types_map.items():
        total_pages = 1
        current_page = 0
        print('正在请求数据 type:%s'%(typename))
        allsqls = list()
        while current_page < total_pages:
            parms = {'_token': token,
                     'page': str(current_page),
                     'post_id': post_id,
                     'age_end': '',
                     'age_start': '',
                     'exprid': '',
                     'gender': '',
                     'healthcard': '',
                     'height_end': '',
                     'height_start': '',
                     'seachstr': '',
                     'sortid': '',
                     'status': str(type_num),
                     'weight_end': '',
                     'weight_start': '',
                     'work_addr': '',
                     'workdate': ''
                     }
            current_page += 1
            response = HTTPRequest.post(url, parms, header)
            json_str = response.content.decode('utf-8')
            print(json_str);
            json_obj = json.loads(json_str)
            total_pages = int(json_obj['total'])

            json_datas = json_obj['data']
            for result in json_datas:
                # print(result)
                #user_mobile是空的话就另外数据进行插入
                _id = result.get("id", 0)
                user_id = result.get("user_id", 0)
                biz_uid = result.get("biz_uid", 0)
                user_name = result.get("user_name", "0")
                user_mobile = result.get("user_mobile", "0")
                post_id = result.get("post_id", 0)
                city_id = result.get("city_id", 0)
                addr_id = result.get("addr_id", 0)
                listing_status = result.get("listing_status", 0)
                work_time = result.get("work_time", "0")
                create_at = result.get("create_at", 0)
                modify_at = result.get("modify_at", 0)
                member_status = result.get("member_status", 0)
                remark = result.get("remark", "0")
                entry_date = result.get("entry_date                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      ", 0)
                listing_text = result.get("listing_text", "0")
                status_text = result.get("status_text", "0")
                mobile_attribution = result.get("mobile_attribution", "0")
                create_at_text = result.get("create_at_text", "0")
                job_type_exprience = result.get("job_type_exprience", "0")
                job_type_exprience = str(job_type_exprience)
                job_type_exprience = job_type_exprience.replace("'","")
                job_times = result.get("job_times", 0)
                age = result.get("age", 0)
                if type(age) != int:
                    if len(age) == 0:
                        age = 0
                gender = result.get("gender", 0)
                height = result.get("height", 0)
                weight = result.get("weight", 0)
                birth_date = result.get("birth_date", 0)
                name = result.get("name", "0")
                real_name = result.get("real_name", "0")
                is_read_phone = result.get("is_read_phone", 0)
                fanggezi_num = result.get("fanggezi_num", 0)
                is_health_cert = result.get("is_health_cert", 0)
                superform = result.get("superform", "0")
                notice_apply_hour = result.get("notice_apply_hour", 0)
                listing_remark_status = result.get("listing_remark_status", "0")
                listing_remark_text = result.get("listing_remark_text", "0")
                experience_text = result.get("experience_text", "0")
                prefer_district = result.get("prefer_district", "0")
                prefer_street = result.get("prefer_street", "0")

                if user_mobile == "0" or len(user_mobile) ==0:
                    print('没有电话')
                    phone = _getPhone(_id, post_id, token, header)
                    user_mobile = phone
                # print(result)
                insert_sql = """
                INSERT INTO fengmingdw.dbo.doumi_data
        ( add_date ,
          id ,
          user_id ,
          biz_uid ,
          user_name ,
          user_mobile ,
          post_id ,
          city_id ,
          addr_id ,
          listing_status ,
          work_time ,
          create_at ,
          modify_at ,
          member_status ,
          remark ,
          entry_date ,
          listing_text ,
          status_text ,
          mobile_attribution ,
          create_at_text ,
          job_type_exprience ,
          job_times ,
          age ,
          gender ,
          height ,
          weight ,
          birth_date ,
          name ,
          real_name ,
          is_read_phone ,
          fanggezi_num ,
          is_health_cert ,
          superform ,
          notice_apply_hour ,
          listing_remark_status ,
          listing_remark_text ,
          experience_text ,
          prefer_district ,
          prefer_street,
          zhiwei_name,
          zhiwei_id
          
        )
VALUES  ( '{}' , -- add_date - date
          {} , -- id - int
          {} , -- user_id - int
          {} , -- biz_uid - int
          N'{}' , -- user_name - nvarchar(100)
          N'{}' , -- user_mobile - nvarchar(100)
          {} , -- post_id - int
          {} , -- city_id - int
          {} , -- addr_id - int
          {} , -- listing_status - int
          N'{}' , -- work_time - nvarchar(100)
          {} , -- create_at - int
          {} , -- modify_at - int
          {} , -- member_status - int
          N'{}' , -- remark - nvarchar(100)
          {} , -- entry_date - int
          N'{}' , -- listing_text - nvarchar(100)
          N'{}' , -- status_text - nvarchar(100)
          N'{}' , -- mobile_attribution - nvarchar(100)
          N'{}' , -- create_at_text - nvarchar(100)
          N'{}' , -- job_type_exprience - nvarchar(100)
          {} , -- job_times - int
          {} , -- age - int
          {} , -- gender - int
          {} , -- height - int
          {} , -- weight - int
          {} , -- birth_date - int
          N'{}' , -- name - nvarchar(100)
          N'{}' , -- real_name - nvarchar(100)
          {} , -- is_read_phone - int
          {} , -- fanggezi_num - int
          {} , -- is_health_cert - int
          N'{}' , -- superform - nvarchar(100)
          {}, -- notice_apply_hour - int
          N'{}' , -- listing_remark_status - nvarchar(100)
          N'{}' , -- listing_remark_text - nvarchar(100)
          N'{}' , -- experience_text - nvarchar(100)
          N'{}' , -- prefer_district - nvarchar(100)
          N'{}'  ,-- prefer_street - nvarchar(100)
          N'{}' , -- prefer_district - nvarchar(100)
          N'{}'  -- prefer_street - nvarchar(100)
        )""".format(DateProcessing.get_datestr(-1)[:10], _id, user_id, biz_uid, user_name, user_mobile,
                post_id, city_id, addr_id, listing_status, work_time, create_at, modify_at, member_status,
                     remark, entry_date, listing_text, status_text, mobile_attribution, create_at_text, job_type_exprience,
                     job_times, age, gender, height, weight, birth_date, name, real_name, is_read_phone, fanggezi_num, is_health_cert, superform,
              notice_apply_hour, listing_remark_status, listing_remark_text, experience_text, prefer_district, prefer_street ,zhiwei_name, post_id)
                print(insert_sql)
                allsqls.append(insert_sql)

                if len(allsqls) > 50:
                    print('正在插入数据库')
                    MySqlOperationer.my_mssql.execNonQuerys(allsqls)
                    allsqls.clear()
                print('sql len: %d' %len(allsqls))
        if len(allsqls) > 0:
            MySqlOperationer.my_mssql.execNonQuerys(allsqls)
            allsqls.clear()



def _getPhone(aid, pid, token, header):
    # 后台网站
    # https://vip.doumi.com/login

    url = 'https://vip.doumi.com/employer/manage/readphone'
    parm = {'aid': aid,
            '_token': token,
            'pid': pid}
    response = HTTPRequest.post(url, data=parm, headers=header)
    response_str = response.content.decode('utf-8')
    json_obj = json.loads(response_str)
    data = json_obj.get('data')
    if data :
        phone = data.get(str(aid))
        return phone


if __name__ == '__main__':
    # d = WebDriverManager()
    # driver = d.getFreeDriver()
    # driver.get(DOUMI_URL)
    #
    # driver.find_element_by_id('phone_id').send_keys('18126821788')
    # driver.find_element_by_id('password_id').send_keys('qwe123456')
    # driver.find_element_by_id('jz_submit_login').click()
    #
    # source = driver.page_source
    # result = re.findall(r"_token:'(.*)'}", source)
    # if len(result) < 0:
    #     print('获取token失败')
    #     quit(0)
    # token = result[0]
    # print('token : ', token)
    # cookies_list = driver.get_cookies()
    # cookie_str = str()
    # for cookie_dict in cookies_list:
    #     cookie_str+= "%s=%s; "%(cookie_dict['name'], cookie_dict['value'])
    #
    # cookie_str = cookie_str[:-2]
    # print('cookie_Str :', cookie_str)


    # cookie_str = 'PHPSESSID=7auna3s9qj36rgoujtgp4n2dl3; dmb_uuid=0c0f75fc-e2fa-11e8-8d51-1418774d6214; bdid=0; b_web_citydomain=bj; dmb_loginfrom=vip; doumi_melon=eyJpdiI6IkZrTVpsanJyR0hRUGkwUjR5N3BuM3c9PSIsInZhbHVlIjoibmFcL3hGaHFCSnBxdENFdWRSMjMyU1NkNko0M3ZqWURsbXgxZ2pKZ0VjdllodWc2Mk15aGxzRWNHYSthcTkxR1wvVEZMVmtLMG5VZ2FlRmFRd3JMRmNudz09IiwibWFjIjoiM2UxZWYxZjc2NWMzNzE0MjZiNzlkNDRjMmE4YTA1ZTM2OGU1NTA2MGUxMjQwMTJiZjJiMWQ2YTA2Mjg0ODdlMiJ9; dmb_from=direct_visits'
    # token = 'uQ53R6yrZPcXrGvFEjVULLHm95idaqzCZnzn2FUx'
    infos = [
        #帐户：18126821788
        #密码：qwe123456
        # ("PHPSESSID=rrpor4sa94kkc0i61lv2ahcuo5; dmb_uuid=8eef4b26-ec66-11e8-b080-1418774d0625; b_web_citydomain=bj; dmb_loginfrom=vip; dmb_from=direct_visits; bdid=0; doumi_melon=eyJpdiI6IkE1YWlQalRvVmR0UzQwbGNXQnBYR2c9PSIsInZhbHVlIjoieTI5K0ZPdmRPQlwvZlY0RGY0Q3dzeHhQbzlwaitQdmdId2dvZUxLd3RSbEZNaHhKc3B5a0FxMXBEVW1JTElRYWk0cGxsWnpaNkZsRVRxOHl0Uzkxb25nPT0iLCJtYWMiOiI4ZWE2MWE3YjE1ZjMwY2I0MjhiYjgzOTQzZDU3ZjZiZmJjY2JhZGMyNjY2YWE1ZjMzMjNlZWNlMGYxOTJiNWRiIn0%3D; ganji_jz_wc_jzuid=eyJpdiI6IlNQRWRFTlwvY3dEMVdJTFdLV2k5VEdnPT0iLCJ2YWx1ZSI6Im80Qm9XaFFBNFpwdHViajlCY0JSM2c9PSIsIm1hYyI6IjE1MzJiMjIwY2U2NGI3ODVhNzYyNGIxODI5NjQzMDBlOTdlOWU1YWQ3YTg5NjM4N2JmMjQ2NGYwMDhkYzhhMmQifQ%3D%3D; ganji_jz_login_source=eyJpdiI6ImZDWDdxQzNiUlFLK3pmN3FaSGtoUHc9PSIsInZhbHVlIjoiVVFoRVdUMk1mZUlDRGl1SHV6bHo1eXlDVlVaYVQycGNzeE1ySVhLaTB6YUJ1Zk1qTDJqMFRxNCs2UGFFSmVhQ2ozR09ITW4zVmJ5MjFQYU1lbHBmdzlqYjhRVzNMUmlTeWVyVmxubnlXUVI0dmUzRGE4bFZRd0E5SHcwbWhQaWZMTnZUWEF5SmdZcDVCb3Z4eWVLcnhnPT0iLCJtYWMiOiJmMjkwN2U5MDJlMDc2YTM2Y2YxZTZmMmY3YWFjYzlmY2Y4NmQzOTA5OTA3MDY2ODcxZjVhZjQ0MmM1MWJhNzNmIn0%3D; dmb_userid=41457062; cid=1736466; is_first=1; is_active=1; related_bd_id=4668; GUID_FRIST_GUIDE_KEY=GUID11_20_41457062",
        #       'hCPGuaXm8r3poSynD10Civ2Hp78G1e2atvzspvVe',
        #       [
        #          ('5455414', '详情页职位_电商集团优惠券项目招黄金会员，仅限宝妈'),
        #        ('5455838', '列表页职位_电商集团新项目招黄金会员代理，仅限宝妈'),
        #        ('5455404', '列表页职位_优惠券项目招黄金会员，限22岁以上大学生')
        #  ]),

            #13120307778
            #CIJI123456
             # ('PHPSESSID=b1ope2atp6gbku0hg9nqosmiu3; dmb_uuid=e0d85572-0b0b-11e9-a0f8-1418774d0625; ganji_uuid=7009084666826649261815; sid=35170942197; ganji_jz_wc_jzuid=eyJpdiI6IldZenQ2aVJxRzZTRm1uWXFvNGhLNFE9PSIsInZhbHVlIjoieHh2Z2NOTUxMeWVxV1h6S1I4dURnZz09IiwibWFjIjoiYzBjZjA5MTA4MGQ0YzljNGVlZWEwYTZjMmQwMjA0MTZlNTJmMjMwNTU5YjMyZmJlYjQzOWZiZDVhMTQ0ZWU2NSJ9; ganji_jz_login_source=eyJpdiI6Ik5DUGtDZ3g4bFllQThwbGxEMGVTQkE9PSIsInZhbHVlIjoiazJuWWRXMTVWSEJVUjJXS0FFV052VHN1M0thSFl2WkwyS0lIWHVkVnZXWGV6NzJRaDBiYXpnRThxRjVDZGtsbjc1bUlTaUNTckFlQUwzeXJjb24zQW5JU3MranhjQ0krYit0WGdhTXpuXC9TRmo2T3RMQm9jK0ZMazdJeE1qeHNWMWl6TUoyYk1ZMVhGRVk0dlY1Q29Fdz09IiwibWFjIjoiYmE2ZjQyNDFmMGIyZGRlMGUxMWNhZGUwMGExZjY0ZDI1ZTc0NjhhYTNmYjI0MTcwYjBjOTczMzU2MTUzMzY1OSJ9; dmb_loginfrom=vip; cid=1804189; is_first=1; is_active=1; related_bd_id=4668; GUID_FRIST_GUIDE_KEY=GUID12_29_42798216; dmb_userid=42798216; b_web_citydomain=bj; dmb_from=direct_visits; bdid=0; doumi_melon=eyJpdiI6ImpEMjdhOHBEWWRyaHJxNlBtV2xNVkE9PSIsInZhbHVlIjoiMExZc2lIcVpzYUxXTWxWZmlBMFV4VURvMHkwNnlHK2xweHBOQzBCQ29QTHFPdVQzRVwvUjJualhUeE5PVlcyRGZPbWo4YTBFTUtET0MrRW9OSEZJQVdnPT0iLCJtYWMiOiI1NzY0Yjg1N2RhYjM3ZWRlOTAyNThlMzMwODg3NDEwZmE2MWZmMmUwN2Q5Yjk5OTI2ZGY1MGFlZjFlMThhODBkIn0%3D; ca_source=-; ca_name=-; ca_kw=-; ca_id=-; ca_s=self; ca_n=-; ca_i=-; ca_from=-; Hm_lvt_7c0a2fe029631e2d7436151fab071753=1546048002; Hm_lpvt_7c0a2fe029631e2d7436151fab071753=1546048002',
             #  'AxAcmrzjTXa3m3iQp00pbzuFQuiLamA7WsT2pESI',
             #  [('5728966', '列表页职位_优惠券电商新项目招黄金会员代理，仅限宝妈'),
             #   ('5680655', '列表页职位_电商集团新项目招黄金会员代理，仅限宝妈'),
             #   ('5679633', '列表页职位_社交电商新项目招会员，限22岁以上大学生'),
             #   ('5679678', '详情页职位_社交电商新项目招黄金会员代理，仅限宝妈'),
             #   ('5691553', '搜索页职位_在家可做社交电商项目招会员代理，仅限宝妈'),
             #   ('5691535', '搜索页职位_在家可做社交电商项目招会员代理，仅限宝妈'),
             #   ('5691519', '搜索页职位_电商集团新项目招黄金会员代理，仅限宝妈'),
             #   ('5758337', '运营位职位_社交电商新项目招黄金会员代理，仅限宝妈')]),
            #
            # #15989220016
            # #CIJI123456
            #  ('PHPSESSID=cdh2s958f5a1maasn75rn37412; dmb_uuid=126f447e-0b0c-11e9-98e2-1418774d6214; ganji_uuid=7009084666826649261815; sid=35248574092; ganji_jz_wc_jzuid=eyJpdiI6Im5QRlFnZlJ5d3dkVHNMN2d5b2VtRmc9PSIsInZhbHVlIjoiSHBcL1FydnY1eG14VGNxb1RiVmEzUkE9PSIsIm1hYyI6ImY0N2QwNjViNWE4YzEyZjEzNTljODgwM2VkYWYwZjAwNDlmOTE5MGQwMmNkMDUwOWQ5YmY1MWIxZjRjMzlmZGUifQ%3D%3D; ganji_jz_login_source=eyJpdiI6IjRVMFFkYU5nc2p6cXRaRElOMUhlUmc9PSIsInZhbHVlIjoickN1blRkWWtVNlwvUFdzNWxac2F6S2pxTDdIeWp6WGE3WExhcXdpaURlZGdcL1hqSW9mRjFvZHE1K3RxS21IMkFFaWQyMlY2OHN4dEpjaTF6XC94K0FlNlNxWDY2Rk5Ka1BlZVRwUVVjRjY3WHY3dWlsQmd6VXRNQ1NVeTJwKzBsV3JubVRmOVFFc3lIVkI4U0FZYkNySXdnPT0iLCJtYWMiOiJhYTMxZjRhMjkzYTFhODA2ZjFmMTZiYzAwMGMwYzZlZGI5MjZkMjZmZWEwNTdlM2MwNWQ2ZTJhNmFhN2I4MGNjIn0%3D; dmb_loginfrom=vip; cid=1804289; is_first=1; is_active=1; related_bd_id=4668; GUID_FRIST_GUIDE_KEY=GUID12_29_42802710; dmb_userid=42802710; b_web_citydomain=bj; dmb_from=direct_visits; bdid=0; doumi_melon=eyJpdiI6IlpHK2xQMkRqWXNuS1JxWXpuKzU1eUE9PSIsInZhbHVlIjoiSkxNMEhIS1QzNlR4RXhkKzBncEQ5Q1wvTlwvVzE5em1nTHJZeWhVSGZQY2VnSjdSRkU2TUZXZ1NJN0lcL09KaXdCT3VJOENGejI2cm1rKzhcL3V5UHNtTGlnPT0iLCJtYWMiOiI3ZTA4ZmZiYjU0YTM5MzUzOGEwNjE4ODU4NTAyYWFiMmY4ODc5OTA2N2YwZTAwYjMzNTc5YTcwYmE4ZDIxZTMwIn0%3D; Hm_lvt_7c0a2fe029631e2d7436151fab071753=1546048048; Hm_lpvt_7c0a2fe029631e2d7436151fab071753=1546048061; ca_source=-; ca_name=-; ca_kw=-; ca_id=-; ca_s=self; ca_n=-; ca_i=-; ca_from=-',
            #   'JhqklI4syduur7eWG1RGfZKaxPdiP52hNcWDS3Fo',
            #   [('5679717', '列表页职位_社交电商新项目招黄金会员代理，仅限宝妈'),
            #    ('5679713', '列表页职位_社交电商招会员代理，限22岁以上大学生'),
            #    ('5679722', '详情页职位_社交电商新项目招黄金会员代理，仅限宝妈'),
            #    ('5758455', '搜索页职位_在家可做社交电商项目招会员代理，仅限宝妈'),
            #    ('5758439', '搜索页职位_在家可做社交电商项目招会员代理，仅限宝妈'),
            #    ('5758357', '搜索页职位_在家可做社交电商项目招会员代理，仅限宝妈'),
            #    ('5758468', '运营位职位_社交电商新项目招黄金会员代理，仅限宝妈')]),

            #18022358780
            #CIJI123456
             # ('PHPSESSID=26q50r579v5dd8s7quec4g0fo0; dmb_uuid=2ca13244-0b0c-11e9-a586-1418774d0625; ganji_uuid=7009084666826649261815; sid=35292268895; ganji_jz_wc_jzuid=eyJpdiI6IllHR1ZhdVlnKzFXOTVFNWZUbElubUE9PSIsInZhbHVlIjoiZUw4R3dyUlFEVk1sV0Rtc3RNVzJBZz09IiwibWFjIjoiZTk5OGM0NjNhYTkyZjZkNDM1ZGJiYzFjNDYyZmM3NTUzOTliYzAzM2YwY2I0MGMzMzY3YTBhZDZmY2NhNmQxMyJ9; ganji_jz_login_source=eyJpdiI6IjRjdVQraDk0OXZiaFF6SnN5WDBcL2JnPT0iLCJ2YWx1ZSI6ImVcL1JJbHdOcGhPb0tMK3ZqZVBWd3UxdzI4RWJ6Z0hLTjRaakFFS3g1TjM3K1l5T2kyTUh5eElJR3IrWXVoaTVHXC8yK1wvRXdZUlh6M2dDY3lvb0ZTRmZObG5zNU1sRlwvczBhajRObUp5WTdxMzhqR2tiZjcwT25rVjN5R21vaFJUZnc2RjZjU0t1XC9NZDVHMWs0cTl0a1d3PT0iLCJtYWMiOiIxOGNkZDQ0NzAyYjM1M2MyODE2MTk1ZWI3NTMzN2M5NDIxZDBiN2E1NzNlNDUyMzViYzE1ZTZmODliODcxMDZjIn0%3D; dmb_loginfrom=vip; cid=1804291; is_first=1; is_active=1; related_bd_id=4668; GUID_FRIST_GUIDE_KEY=GUID12_29_42802800; dmb_userid=42802800; b_web_citydomain=bj; dmb_from=direct_visits; bdid=0; doumi_melon=eyJpdiI6IjVBelwvNkI3WjYyd3hEUHlcL2htSk0rQT09IiwidmFsdWUiOiI2aDg1cWxaMU92TDJhTkFkWlM4ZUV3QVwvTjc5dUJwWDc5ZkU1Rm1Yc3Byc3kydm9oczJwU0NmZnlwektuK0RhRmlCakU4enNwVElyT2Zyd1dJR1h0cXc9PSIsIm1hYyI6IjE2NmQ0MDg0MDgyOTliOTI0ZTAzYTY5NmRiMWI4ODFiOTdiN2MxZjVlNmY0OWUwODQyMzIxZmM3ZDkyZjM0MGEifQ%3D%3D; Hm_lvt_7c0a2fe029631e2d7436151fab071753=1546048091; Hm_lpvt_7c0a2fe029631e2d7436151fab071753=1546048104; ca_source=-; ca_name=-; ca_kw=-; ca_id=-; ca_s=self; ca_n=-; ca_i=-; ca_from=-',
             #  'iAUfiZRPng9g3WDgtA3ojqyC6oqnEB2KM82FxmOT',
             #  [('5679731', '列表页职位_社交电商新项目招黄金会员代理，仅限宝妈'),
             #   ('5679727', '列表页职位_社交电商项目招会员，限22岁以上大学生'),
             #   ('5679734', '详情页职位_社交电商新项目招黄金会员代理，仅限宝妈'),
             #   ('5758606', '搜索页职位_在家可做社交电商项目招会员代理，仅限宝妈'),
             #   ('5758603', '搜索页职位_在家可做社交电商项目招会员代理，仅限宝妈'),
             #   ('5758594', '搜索页职位_在家可做社交电商项目招会员代理，仅限宝妈'),
             #   ('5758618', '运营位职位_社交电商新项目招黄金会员代理，仅限宝妈')]),

            #15112111531
            # CIJI123456
            #  ('PHPSESSID=2ddds5r5nv10tv1gt6sjvg0s75; dmb_uuid=4d185b92-0b0c-11e9-8ece-1418774d6214; ganji_uuid=7009084666826649261815; sid=35347064861; ganji_jz_wc_jzuid=eyJpdiI6InkwQkxxcVpEb3JvM3F1ekdsZXNhRnc9PSIsInZhbHVlIjoiU0I1S1p0cENvdEZxYndkZ1wvcWQ3Y2c9PSIsIm1hYyI6ImViYjJjZGYwMjFlY2IwOGQxMzdiNTkzNGIzNzNmMTU0ODFkOThlMjUyZjE1ZWU0YmI3NjYzMDQ3NWNmYzQzNjQifQ%3D%3D; ganji_jz_login_source=eyJpdiI6InBaRmdRajRKbGxnOEdacUhzeFh4Tnc9PSIsInZhbHVlIjoidUZQRE5rRXVtN0ZSWTZNQlhzR0htR29IMHJIdGJXd2xsclRUUDRiaXBvVXZ4d0lkNmp4Mjc5MngrZjdkblJIMEd2QW12aUZxcWtNNGJVdDEzaTdPUXU1d1d0Nm1vSUc0TDVhK3k4WTZKczFBY0paeTRFRkZcL0llaUhYd0FzeEVWU3lXUUoxeWJ2MDM0cmhZUG92YUhRUT09IiwibWFjIjoiYzAwNDE3YzA0ZWFhMzI5YTdiMWMyZmU1MmIyYTA0Mzg4MGI0Y2Q2NDAwYzFkMmZlOTUzYTNhMDI0ODAyYWVlNiJ9; dmb_loginfrom=vip; cid=1804314; is_first=1; is_active=1; related_bd_id=4668; GUID_FRIST_GUIDE_KEY=GUID12_29_42804634; dmb_userid=42804634; b_web_citydomain=bj; dmb_from=direct_visits; bdid=0; doumi_melon=eyJpdiI6IlNkXC9xdlhDeWFtd1JrSXpDRjdhMXV3PT0iLCJ2YWx1ZSI6IjFXSFQ3bFJmYUp6Wkk3N2JmaWdiaFphQW5TaytIRjVNVm9CYlhoVG04a01aRG01ZEZrSFpFeXNhYkJJTDRZTTVZdXduYlwvbnFUSkhSbWk2dmloenRaQT09IiwibWFjIjoiZjc2MTc1MDNmMzIwMWNiZDhlZWFkZDYyZDk0M2UyOWY4NmQyZDMwNTNlZDU3OWIyZWE3NGViZmEzMDk1YmE2YSJ9; Hm_lvt_7c0a2fe029631e2d7436151fab071753=1546048146; Hm_lpvt_7c0a2fe029631e2d7436151fab071753=1546048160; ca_source=-; ca_name=-; ca_kw=-; ca_id=-; ca_s=self; ca_n=-; ca_i=-; ca_from=-',
            #   'iReuDt9sk6jl7PqFm7jB30PAdxV5FbeDxoHxaQOY',
            #   [('5679741', '列表页职位_社交电商新项目招黄金会员代理，仅限宝妈'),
            #    ('5679738', '列表页职位_社交电商项目招会员，限22岁以上大学生'),
            #    ('5679744', '详情页职位_社交电商新项目招黄金会员，仅限宝妈'),
            #    ('5758584', '搜索页职位_在家可做社交电商项目招会员代理，仅限宝妈'),
            #    ('5758576', '搜索页职位_在家可做社交电商项目招会员代理，仅限宝妈'),
            #    ('5758570', '搜索页职位_在家可做社交电商项目招会员代理，仅限宝妈'),
            #    ('5758589', '运营位职位_社交电商新项目招黄金会员代理，仅限宝妈')])]

            #17701997194
            #ciji654321
            ('PHPSESSID=tutcj594g4mroe5icd657v0jf7; dmb_uuid=db6595e6-30c7-11e9-a586-1418774d0625; ganji_uuid=2282455201787465107323; sid=36844322456; ganji_jz_wc_jzuid=eyJpdiI6IkxEcnhHWFBxS1k5aVluR1BzS1lJaGc9PSIsInZhbHVlIjoiUkQxSnBTRlZXTnhldFhQdURQcGlaQT09IiwibWFjIjoiMTBhZTEzYTc3MDhhYjUzNmU3MTdmOTI2Y2FlOWUzNGI4MjE2NTk0NGIwYzgyM2QzOGU1ODJlMjAzYTcxZjM5OSJ9; ganji_jz_login_source=eyJpdiI6IjZaXC9EQnBVVWU3Z3NkS05yK2JHMndnPT0iLCJ2YWx1ZSI6Ijlza3o1TDFWK3ZldkhzaGhoUDFObjZIMXMxRllvclc4MnZRQ3FydkVUOE9oXC9POUdhMjR6UXh2KzlLVzJqZU1IcXJQQzNEcHNGK3ZzaXZEbVV2MVI3RDNYcTRvY3lyRUo2RU1rbnNJKzd2VnVib290TG9Cc205RG04RjRwdlBGTUMyQUhxSXpldzc2YWJRYVdVV095a2c9PSIsIm1hYyI6ImY2ZTBhNWE4YTdiMzU2YmVhNWZhMWViZjU2MmU4NzJiMmE5NzNhYWYzZTFmMDQ1NDM5YTViOWJlNjY1YjIyYWUifQ%3D%3D; dmb_loginfrom=vip; cid=1804189; is_first=1; is_active=1; related_bd_id=4668; GUID_FRIST_GUIDE_KEY=GUID2_15_42798216; ca_source=-; ca_name=-; ca_kw=-; ca_id=-; ca_s=self; ca_n=-; ca_i=-; ca_from=-; ganji_jz_b_web_citydomain=eyJpdiI6ImRyekRXK0F2dzlRdGhiQnR0ZnhtekE9PSIsInZhbHVlIjoiQlVLOWNhb2FMTzBqaEtWbE8rS0JaZz09IiwibWFjIjoiYWFlNmU1YmRmYWE5YjUzMzc3Y2QyNTdkNDAwOGE3MzExZWZkNTVlNWJkOWRmZjliOTc3YWI2MWJhMDRlMDFkNiJ9; dmb_userid=42798216; b_web_citydomain=bj; dmb_from=direct_visits; bdid=0; doumi_melon=eyJpdiI6InN3TzBjWnRFZitJeVdOb2dpaU9xUlE9PSIsInZhbHVlIjoiOGRtbktyUCswTUp2TCtlcStXbkswY0NmNFdRQTFFOHFTdTY1SjZQa0JaMmlDbUhBcGNQKzk0VnZWTmpIUnlkb2FtZ3UwYTlcL3JKdHBcLzl0cEhRTWhXZz09IiwibWFjIjoiYjU2NmNmYTRhNDY2YWJmMzFjNDI2YWI3ZDRjZjNiNWNlYmRmN2MxODgyNjI0NjZjZTY5NTNkZjU1NmMyYmRjMSJ9; Hm_lvt_7c0a2fe029631e2d7436151fab071753=1550197352; Hm_lpvt_7c0a2fe029631e2d7436151fab071753=1550210995; ca_source=-; ca_name=-; ca_kw=-; ca_id=-; ca_s=self; ca_n=-; ca_i=-; ca_from=-',
             'XupzRl2FXF6w17h1RNZQ6Qr8tMvCaalCd94QikiL',
            [('5728966', '列表页职位_京东优惠券推广在家兼职招募，全职妈妈'),
            ('5679633', '列表页职位_京东淘宝拼多多招募优惠券推广在家兼职，仅限宝妈'),
            ('5679678', '详情页职位_天猫拼多多优惠券推广在家兼职招募，仅限宝妈'),
            ('5848251', '搜索页职位_淘宝拼多多优惠券代理，在家可做 分享赚钱，仅限宝妈'),
            ('5848242', '搜索页职位_京东淘宝优惠券代理，在家可做 分享赚钱，仅限宝妈'),
            ('5848224', '搜索页职位_淘宝天猫优惠券代理，在家可做 分享赚钱，仅限宝妈'),
            ('5758337', '运营位职位_社交电商新项目招黄金会员代理，仅限宝妈')]),

            #17727671743
            #ciji654321
            ('PHPSESSID=1iki4fla2g7r1lqgp6kenlrpf0; dmb_uuid=0e116b20-30e9-11e9-9fab-1418774d6214; ganji_uuid=2282455201787465107323; sid=51100797536; ganji_jz_wc_jzuid=eyJpdiI6IkNxS0pYSENLc3dScVJDVmVmUmp5WVE9PSIsInZhbHVlIjoiNTJOeWQ4Mnhjb2pUV0l6YUxRQVJvdz09IiwibWFjIjoiNDEwOTBlMjlhNjJjOTg5MDBkMGU1NDA3YzZjZDdlOGFiYjFlZWI2MTc1MzQ5N2NjNWEwMjQxM2RmZTIxNWNkNiJ9; ganji_jz_login_source=eyJpdiI6ImJDQ254d0Via0hsVWN5MFBoalFJREE9PSIsInZhbHVlIjoiK2RPXC9cLzRiTXVSTGpiY2xcL0pUNGtnNCt4Mm14UkhxazlaQmFDbVlHRG90OTN4R3FZTWJUeWl1RXBaUzM5Vm1lU0pXNTBwUTE1Uk9LRzBmSmZJSHV0RmhSVis5NlhBK0c5eTBsTVRMZ1BROUFKVDY5Mk40YXBKTjEwQmVmdmNVaklIdzNKYUE1UDh3ZWxqU2UwQ0RBeTVRPT0iLCJtYWMiOiJjMTAyNzk1YTAwODEwOGEyODQwYjFiNGZhMGZhZTI4ODQwNzdjOGNhMjFjYjZjODAzN2U1YzdmZWZhYjBhNjc2In0%3D; dmb_loginfrom=vip; cid=1804289; is_first=1; is_active=1; related_bd_id=4668; GUID_FRIST_GUIDE_KEY=GUID2_15_42802710; ca_source=-; ca_name=-; ca_kw=-; ca_id=-; ca_s=self; ca_n=-; ca_i=-; ca_from=-; ca_source=-; ca_name=-; ca_kw=-; ca_id=-; ca_s=self; ca_n=-; ca_i=-; ca_from=-; ganji_jz_b_web_citydomain=eyJpdiI6Im5MdHM5Z2xMWVhjMmV4QjBhVjRKcEE9PSIsInZhbHVlIjoiY094VlF4V3B1YldFVll1YzBWZGdCUT09IiwibWFjIjoiNTNmZjU5YjZlYmZiZTlkMTIxMjJmMGZkYjlkNmI5ZTQ3Mzc2YmUyMzAzMjJmNGMxMjU5YTZiYmFiODM3MThhMSJ9; dmb_userid=42802710; b_web_citydomain=bj; dmb_from=direct_visits; bdid=0; doumi_melon=eyJpdiI6IjA4QndGUHU2ZEc0V0xqRmZGRDUrd3c9PSIsInZhbHVlIjoiM1RMNlJreXdjRnJkS1NXWllJRDU0U2dtTmhXWVV1ZkxlazdXNDNyTWlvN1ppVTFodnl6OVYwUHNWVDIxZnhmVzV6Um5iWnZVVzk5Uk1tSVRnM3pPdEE9PSIsIm1hYyI6IjUwNjNjNmRlMDVmNzdiYTJhNDE3Y2U3ZDQ2ZDMxZDE1NmUwYjFmMWMzY2U1NzdjOWU3NjQyNDI1NGZmY2IyYjkifQ%3D%3D; Hm_lvt_7c0a2fe029631e2d7436151fab071753=1550211098; Hm_lpvt_7c0a2fe029631e2d7436151fab071753=1550211137',
            'mqVGYFj3V4yg3uYs2yXkCtbBilFgpvvxii4mZ1UF',
            [('5679717', '列表页职位_天猫优惠券推广在家兼职招募，仅限宝妈'),
            ('5679713', '列表页职位_拼多多招募优惠券推广在家兼职，仅限宝妈'),
            ('5679722', '详情页职位_淘宝京东优惠券推广在家兼职招募，仅限宝妈'),
            ('5848197', '搜索页职位_淘宝拼多多优惠券代理，在家可做 分享赚钱，仅限宝妈'),
            ('5848182', '搜索页职位_京东淘宝优惠券代理，在家可做 分享赚钱，仅限宝妈'),
            ('5848171', '搜索页职位_淘宝天猫优惠券代理，在家可做 分享赚钱，仅限宝妈'),
            ('5758468', '运营位职位_社交电商新项目招黄金会员代理，仅限宝妈，仅限宝妈')]),

            #17702059744
            #ciji654321
            ('PHPSESSID=6bfm2iaoijplcsbuec2ngklaf7; dmb_uuid=3c373340-30e9-11e9-80dd-1418774d6214; ganji_uuid=2282455201787465107323; sid=51177829733; ganji_jz_wc_jzuid=eyJpdiI6ImlIUjJscVJcL1FndUMxYXhuQ25odG13PT0iLCJ2YWx1ZSI6Ik1xZk5TYnFncWJPamJITUdnUlV1ZHc9PSIsIm1hYyI6ImMyZTBhMmVmNzE3OWU2MTg0ZDYxNWNhZGEzNTk1ZGU5MDg2YTdjZmVkMWEyZDI0YzdlOTA0NTQ5ODdhOTg3MDcifQ%3D%3D; ganji_jz_login_source=eyJpdiI6InpqMFBVQXhGWXdHaGFuVDFaU2hpaEE9PSIsInZhbHVlIjoiNnpSYjdnMVBlclRKUEdZbWJRd0FESlo1bjZFcGlGUk1udXU0bnU1cG80ZlJHTHQ3MDBSTjZNK1p1b1R5eXRubjdubm9VMWZOcnJCWDBhbnU0ZTY5UFlONlZITWFmYjJYRmNWeU9oMU9ONGlVcjlrUmZpcGk0bkRzZW9UZmp2Ylg4dFB4UnN3TExEZGZyYmx0UVJZb3FnPT0iLCJtYWMiOiI4ZDliNGExN2U5YTUyMjI3OWUxZTZlZjNiNGMyNmQyMjZmYTY4MDE4MjBiYTE0Yzk1NmE2MGYzNTk3YzI5MDhmIn0%3D; dmb_loginfrom=vip; cid=1804291; is_first=1; is_active=1; related_bd_id=4668; GUID_FRIST_GUIDE_KEY=GUID2_15_42802800; ca_source=-; ca_name=-; ca_kw=-; ca_id=-; ca_s=self; ca_n=-; ca_i=-; ca_from=-; ganji_jz_b_web_citydomain=eyJpdiI6IlJUY003YVhzN29SbjhBSm1RSHdJZ3c9PSIsInZhbHVlIjoiejd5SGhyOHlrQ1hVRWJoQmNEU2o3UT09IiwibWFjIjoiYWZhNGY5ZDgyNjUyNTJiOGRkZjFmOGQyN2UzN2MyMThmODU2ZWQ4OTg0MWJhOGI5NGU2NDk5OTFiNDU3MDMzZCJ9; dmb_userid=42802800; b_web_citydomain=bj; dmb_from=direct_visits; bdid=0; doumi_melon=eyJpdiI6IkxESWhFMlpJMUNSOTRlZmVxcjRFK0E9PSIsInZhbHVlIjoiRFdleitHV1lNRnJZYlpKYWNcL2k4ZW9MZHBlM3YrYXBQVjA1dTBQd0lWY0JNN2xFZ2FBSGdJVFB5XC8yQkpuS0dsTDdDMlJiZEE2a3MwWGVzOGg3SkkwZz09IiwibWFjIjoiMzZjNTM2MzE2MGNmZWY3YzJmNzcxYWUyODI2NWVjNDU1ZGUwYjc5ZDkxMmJjZWI4ODFhNDk1ZjhhNDYyOTM4ZiJ9; Hm_lvt_7c0a2fe029631e2d7436151fab071753=1550211178; Hm_lpvt_7c0a2fe029631e2d7436151fab071753=1550211206',
            'KlogTUIxIamY3YtYxg3553H4VhbMYxC26bjpLOUw',
            [('5679731', '列表页职位_拼多多京东招募优惠券推广在家兼职，仅限宝妈'),
            ('5679727', '列表页职位_淘宝拼多多优惠券推广在家兼职招募，仅限宝妈'),
            ('5679734', '详情页职位_拼多多京东优惠券推广在家兼职招募，仅限宝妈'),
            ('5818101', '搜索页职位_淘宝天猫优惠券代理，在家可做 分享赚钱，仅限宝妈'),
            ('5818068', '搜索页职位_京东淘宝优惠券代理，在家可做 分享赚钱，仅限宝妈'),
            ('5818020', '搜索页职位_淘宝拼多多优惠券代理，在家可做 分享赚钱，仅限宝妈'),
            ('5758618', '社交电商新项目招黄金会员代理，仅限宝妈')]),

            #17702061754
            #ciji654321
            ('PHPSESSID=oje3l3vmpbhla4r15t263vagd1; ganji_jz_b_web_citydomain=eyJpdiI6IjNWaEpvZGRqVjB0OEpyQ2dheWdZWFE9PSIsInZhbHVlIjoiM0JsNW9lOWRhXC9jUW1vYms5UDRiU1E9PSIsIm1hYyI6ImU1MmU3ZGY5YTM5Mzg3MmVjZGVjMzEwZGFlZDc3OWQ2OTFlODI0ZmY5OTI4Y2MzOTg0ZDg3ZmU3ZTIzMDFkZTMifQ%3D%3D; dmb_uuid=608f8a30-30e9-11e9-98e2-1418774d6214; ganji_uuid=2282455201787465107323; sid=51237536281; ganji_jz_wc_jzuid=eyJpdiI6IlVcL01ldURpOGd1VTRBOVUyUStzSG53PT0iLCJ2YWx1ZSI6IkkyXC9qbDdnalU0S0R2ZmU4Yklack9BPT0iLCJtYWMiOiIyODNiZTMzNjg0YTkzNzJmOTIwMzg5OGQ1ZGM1NzdlNTlhOTdiYjdjNjY5NTUzZjE5ZjI2NzE0NmVjNDY5MmE5In0%3D; ganji_jz_login_source=eyJpdiI6ImlYbksxQjIxK3Vsbmd3ank1TWRpMHc9PSIsInZhbHVlIjoiMWdUXC9EUTlZcWJ0R1hYUms2YXpGbzc2b0phenVVbGxmdGIzdTZrNGttczFYeHVHa1dHWUd4eU53NDZkbTFwZ0RRbVdERHI4VWtyQUxsdldWWm9Hdk5IYXRscGRXd2kyTXBqS2drcWxmZUYrOGFEdktDMXlTSFhQbGFlQUMweUJ1cG85Y0Vsc1wvcHRwZVhvMGpNYXlRWnc9PSIsIm1hYyI6IjJhY2E4N2VlZWQ2MGEzMjBkZmUyNmU5YjgzNDg5NzY2MTZjNTZhZjEzNDNmYjk2OTY0ZjMyODRiYmFhZDJiYTUifQ%3D%3D; dmb_loginfrom=vip; cid=1804314; is_first=1; is_active=1; related_bd_id=4668; GUID_FRIST_GUIDE_KEY=GUID2_15_42804634; dmb_userid=42804634; b_web_citydomain=bj; dmb_from=direct_visits; bdid=0; doumi_melon=eyJpdiI6IktDQ0F4dmVnV0FYMERFUE91REp6M3c9PSIsInZhbHVlIjoieldkY3V3NVwvdHJyN2JQWFlscXdBTDJCSHB2b1p5TjZTTjdnTjdCd2NxMGQreWw5QVI5OWRmS1hyRHZGQklLRXRUQmFmckphaGt6RExMb3pIWlwvV3pZQT09IiwibWFjIjoiODI0YTA2ZDA0YWMxOWYwMjExYzE1M2FlMzBhYjNmOGUwMTY2NDM2ZGZiZmU0ZWJiMDI0ZTYzOGU1NWEwNjVlZSJ9; Hm_lvt_7c0a2fe029631e2d7436151fab071753=1550211237; Hm_lpvt_7c0a2fe029631e2d7436151fab071753=1550211258; ca_source=-; ca_name=-; ca_kw=-; ca_id=-; ca_s=self; ca_n=-; ca_i=-; ca_from=-',
             'Lm7t6p40h6htCm2fmemQqfZUemhUiqXWTTW8CXGe',
            [('5679741', '列表页职位_京东拼多多淘宝优惠券推广在家兼职招募，仅限宝妈'),
            ('5679738', '列表页职位_京东淘宝优惠券推广在家兼职招募，仅限宝妈'),
            ('5679744', '详情页职位_京东天猫优惠券推广在家兼职招募，仅限22岁以上在校大学生'),
            ('5848401', '搜索页职位_淘宝拼多多优惠券代理，在家可做 分享赚钱，仅限宝妈'),
            ('5848360', '搜索页职位_京东淘宝优惠券代理，在家可做 分享赚钱，仅限宝妈'),
            ('5848331', '搜索页职位_淘宝天猫优惠券代理，在家可做 分享赚钱，仅限宝妈'),
            ('5758589', '运营位职位_社交电商新项目招黄金会员代理，仅限宝妈')])]

    # header = HTTPRequest.getHeader(cookie_str, token)
    # #招聘中 URl
    # ingUrl = 'https://vip.doumi.com/pointgold/index?postStatus=ing'
    # payload = {'postStatus':'ing'}
    # result = HTTPRequest.get(ingUrl, payload, headers=header)
    # # print(result.content)
    # # post_ids = _getPostId(result.content)
    #
    # post_ids = [('5455414', '详情页职位_电商集团优惠券项目招黄金会员，仅限宝妈'),
    #             ('5455838', '列表页职位_电商集团新项目招黄金会员代理，仅限宝妈'),
    #             ('5455404', '列表页职位_优惠券项目招黄金会员，限22岁以上大学生')]
    # for post_id in post_ids:
    #     _getInfosPostID(post_id[1], post_id[0], header, token)


    for info in infos:
        cookie_str = info[0]
        token = info[1]

        header = HTTPRequest.getHeader(cookie_str, token)
        # 招聘中 URl
        ingUrl = 'https://vip.doumi.com/pointgold/index?postStatus=ing'
        payload = {'postStatus': 'ing'}
        result = HTTPRequest.get(ingUrl, payload, headers=header)
        print(len(result.content))
        # post_ids = _getPostId(result.content)

        # print(len(info))
        post_ids = info[2]
        for post_id in post_ids:
            _getInfosPostID(post_id[1], post_id[0], header, token)




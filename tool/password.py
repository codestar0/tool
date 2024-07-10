#!/usr/bin/env python
# coding:utf-8
import os
import time
import json
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from commons import Logger
from pypinyin import lazy_pinyin

'''
    社工密码生成器
    1.收集相关信息
    2.汉字转拼音
    3.不同的信息抽取方式
    4.关键信息组合
'''

# 初始化线程锁
g_mutex = threading.Lock()
# ⽇志⽂件⽬录为当前⽬录所在⽂件下的log⽬录
log_dir = os.path.dirname(os.path.abspath(__file__)) + '/log/'
# 目录不存在则创建
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
# 日志格式
cur_time = time.strftime('%Y-%m-%d-%H', time.localtime(time.time())).replace(
    ':', '').replace(' ', '_')
LogFile = log_dir + cur_time + '.log'
logging = Logger(LogFile, level='debug').logger


class Person(object):
    person = None
    # 定义一些分隔符、常用密码
    Delimiters = ["", "-", ".", "|", "_", "+", "#", "@"]
    Prefix = ["", ]
    Suffix = ["", "123", "@", "abc", ".", "123.", "!!!", ]

    def __init__(self):
        try:
            conf = json.load(open("passwd.json", encoding="utf-8"))
            self.person ={
                'name': conf['name'],
                'phone': conf['phone'],
                'card': conf['card'],
                'birthday': conf['birthday'],
                'hometown': conf['hometown'],
                'place': conf['place'],
                'qq': conf['qq'],
                'company': conf['company'],
                'school': conf['school'],
                'account': conf['account'],
                'password': conf['password']
            }
        except Exception as e:
            logging.error('Manager __init__ error: {}'.format(e))

    # def out(self):
    #     result = []
    #     for i in self.person['birthday']:
    #         print(i)

    # 获取拼⾳
    def get_pinyin(self, word):
        pinyin = ""
        for i in lazy_pinyin(word):
            pinyin = pinyin + ''.join(i)
        return pinyin

    # 获取缩写
    def get_abbreviation(self, word):
        result = ""
        for i in word:
            result += self.get_pinyin(i)[0]
        return result

    # 获取全拼
    def get_full_pinyin(self, word):
        return self.get_pinyin(word)

    # ⾸字⺟⼤写
    def get_title(self, word):
        return word.title()

    def get_name_component(self):
        result = []
        # 获取姓名全拼
        result.append(self.get_pinyin(self.person['name']))
        # 获取 姓 全拼
        result.append(self.get_pinyin(self.person['name'][0]))
        # 获取 名 全拼
        result.append(self.get_pinyin(self.person['name'][1:]))
        # 获取⾸字⺟⼤写姓名全拼
        result.append(self.get_title(self.get_pinyin(self.person['name'])))
        # 获取⾸字⺟⼤写 姓 全拼
        result.append(self.get_title(self.get_pinyin(self.person['name'][0])))
        # 获取⾸字⺟⼤写 名 全拼
        result.append(self.get_title(self.get_pinyin(self.person['name'][1:])))
        # 获取缩写姓名拼⾳(只有⾸字⺟)
        result.append(self.get_abbreviation(self.person['name']))
        # 获取缩写 姓 拼⾳
        result.append(self.get_abbreviation(self.person['name'][0]))
        # 获取缩写 名 拼⾳
        result.append(self.get_abbreviation(self.person['name'][1:]))
        # print(result)
        return result

    def get_phone_component(self):
        result = []
        for phone in self.person['phone']:
            # 获取⼿机号
            result.append(phone)
            # 获取⼿机号后四位
            result.append(phone[-4:])
        return result

    def get_card_component(self):
        result = []
        # 获取银⾏卡号
        result.append(self.person['card'])
        # 获取银⾏卡号后六位
        result.append(self.person['card'][-6:])
        # 获取银⾏卡号前六位
        result.append(self.person['card'][0:6])
        return result

    def get_birthday_component(self):
        result = []
        year = self.person['birthday'][0]
        month = self.person['birthday'][1]
        day = self.person['birthday'][2]
        # 获取年/⽉/⽇的各种组合
        result.append(year)
        result.append(year[2:])
        result.append(month + day)
        result.append(year + month + day)
        return result

    def get_hometown_component(self):
        result = []
        # 获取地址全拼
        result.append(self.get_pinyin(self.person['hometown'][0]))
        result.append(self.get_pinyin(self.person['hometown'][1]))
        result.append(self.get_pinyin(self.person['hometown'][2]))
        # 获取⾸字⺟⼤写的地址全拼
        result.append(self.get_title(self.get_pinyin(self.person['hometown'][0])))
        result.append(self.get_title(self.get_pinyin(self.person['hometown'][1])))
        result.append(self.get_title(self.get_pinyin(self.person['hometown'][2])))
        # 获取缩写的地址拼⾳
        result.append(self.get_abbreviation(self.person['hometown'][0]))
        result.append(self.get_abbreviation(self.person['hometown'][1]))
        result.append(self.get_abbreviation(self.person['hometown'][2]))
        return result

    def get_place_component(self):
        result = []
        for place in self.person['place']:
            result.append(self.get_pinyin(place[0]))
            result.append(self.get_pinyin(place[1]))
            result.append(self.get_pinyin(place[2]))
            result.append(self.get_title(self.get_pinyin(place[0])))
            result.append(self.get_title(self.get_pinyin(place[1])))
            result.append(self.get_title(self.get_pinyin(place[2])))
            result.append(self.get_abbreviation(place[0]))
            result.append(self.get_abbreviation(place[1]))
            result.append(self.get_abbreviation(place[2]))
        return result

    def get_qq_component(self):
        result = []
        for qq in self.person['qq']:
            result.append(qq)
        return result

    # 获取公司信息
    def get_company_component(self):
        result = []
        for company in self.person['company']:
            for name in company:
                result.append(self.get_pinyin(name))
                result.append(self.get_title(self.get_pinyin(name)))
                result.append(self.get_abbreviation(name))
        return result

    # 获取学校信息
    def get_school_component(self):
        result = []
        for school in self.person['school']:
            for name in school:
                result.append(self.get_pinyin(name))
                result.append(self.get_title(self.get_pinyin(name)))
                result.append(self.get_abbreviation(name))
        return result

    # 获取账号信息
    def get_account_component(self):
        result = []
        for account in self.person['account']:
            result.append(self.get_pinyin(account))
            result.append(self.get_title(self.get_pinyin(account)))
            result.append(self.get_abbreviation(account))
        return result

    # 通过不同⽅式获取各组件信息
    def get_all_component(self):
        result = []
        result.append(self.get_name_component())
        result.append(self.get_phone_component())
        result.append(self.get_card_component())
        result.append(self.get_birthday_component())
        result.append(self.get_hometown_component())
        result.append(self.get_place_component())
        result.append(self.get_qq_component())
        result.append(self.get_company_component())
        result.append(self.get_school_component())
        result.append(self.get_account_component())
        return result

    def write_password(self, password, filename):
        try:
            # 加锁
            g_mutex.acquire()
            # passwd = set()
            # passwd.update(password)
            with open(filename, "a+", encoding='utf-8') as f:
                for passwd in password:
                    f.write("%s\n" % passwd)
        except Exception as e:
            logging.error('Write flie error: {}'.format(e))
        finally:
            # 释放锁
            g_mutex.release()

    # 密码组合到set()
    def combined_character(self, compents, Delimiter, prefix, suffix):
        passwd = set()
        pass_one = self.combined_character_one(compents, Delimiter, prefix, suffix)
        passwd.update(pass_one)
        pass_two = self.combined_character_tow(compents, Delimiter, prefix, suffix)
        passwd.update(pass_two)
        # print(passwd)
        return passwd

    # 生成单组件密码
    def combined_character_one(self, compents, Delimiter, prefix, suffix):
        passwd = set()
        for compent in compents:
            for i in compent:
                if Delimiter == "":
                    password1 = prefix + i + Delimiter + suffix
                    # self.write_password(password, filename)
                    passwd.add(password1)
                    continue
                password2 = prefix + i + Delimiter + suffix
                passwd.add(password2)
                # self.write_password(password, filename)
                password3 = prefix + Delimiter + i + suffix
                passwd.add(password3)
                # self.write_password(password, filename)
        return passwd
        # print("++++++++++",passwd)

    # 生成双组件密码
    def combined_character_tow(self, compents, Delimiter, prefix, suffix):
        passwd = set()
        for compent_a in compents:
            for compent_b in compents:
                for i in compent_a:
                    for j in compent_b:
                        password = prefix + i + Delimiter + j + suffix
                        passwd.add(password)
                        # self.write_password(password, filename)
        return passwd


    def gen_pass(self):
        try:
            passwd = set()
            compents = self.get_all_component()  # 获取成分信息
            # 单组件密码
            for Delimiter in self.Delimiters:
                for prefix in self.Prefix:
                    for suffix in self.Suffix:
                        passwd_one = self.combined_character(compents, Delimiter, prefix, suffix)
                        passwd.update(passwd_one)
            # 两组件密码
            for Delimiter in self.Delimiters:
                for prefix in self.Prefix:
                    for suffix in self.Suffix:
                        passwd_two = self.combined_character(compents, Delimiter, prefix, suffix)
                        passwd.update(passwd_two)
            return passwd
        except Exception as e:
            logging.error('Generate password error: {}'.format(e))

class Worker(object):

    def __init__(self, filename=None):
        if filename is not None:
            self.filename = filename
        else:
            self.filename = 'password.list'
        self.pool1 = ThreadPoolExecutor(max_workers=16)  # 生成线程池
        self.pool2 = ThreadPoolExecutor(max_workers=16)

    def start(self):
        try:
            thread_list1 = []
            thread_list2 = []
            g = Person()
            # 开启第一个线程池生成密码
            future1 = self.pool1.submit(g.gen_pass)
            thread_list1.append(future1)
            wait(thread_list1)  # 等待线程结束
            result = future1.result()

            # 开启第二个线程池写入密码
            future2 = self.pool2.submit(g.write_password, result, self.filename)
            thread_list2.append(future2)
            wait(thread_list2)

        except Exception as e:
            logging.error('Start error: {}'.format(e))


def main():
    p = Worker()
    p.start()


if __name__ == "__main__":
    start_time = time.time()
    # gen_pass()
    main()
    end_time = time.time()
    print("[*] 扫描结束，共计扫描时间: %.2f s" % (end_time - start_time))






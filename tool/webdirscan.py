import os
import time
import threading
import requests
import json
from concurrent.futures import wait, ThreadPoolExecutor
from requests.packages import urllib3
from commons import Logger


# 关闭请求https的告警
urllib3.disable_warnings()
# 初始化线程锁
g_mutex = threading.Lock()
# ⽇志⽂件⽬录为当前⽬录下的log⽬录
log_dir = os.path.dirname(os.getcwd()) + '/log/'
# 目录不存在则创建
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
# 日志格式
cur_time = time.strftime('%Y-%m-%d-%H', time.localtime(time.time())).replace(
    ':', '').replace(' ', '_')
LogFile = log_dir + cur_time + '.log'
logging = Logger(LogFile, level='debug').logger


class Worker(object):
    site = None
    cfg = None

    def __init__(self, site, cfg, pool, outfile=None):
        self.site = site
        self.cfg = cfg
        self.pool = pool
        self.outfile = outfile



    def start(self):
        try:
            scan_list = []
            for web_dir in self.cfg['dics']:
                # 每次扫描一个域名，遍历web目录
                t = Scanner(self.site, web_dir, self.outfile)
                # 启动线程池
                future = self.pool.submit(t.run)
                # 追加线程
                scan_list.append(future)
            wait(scan_list)
        except Exception as e:
            logging.error('Start error: {}'.format(e))


class Scanner(object):
    site = None
    cfg = None
    request_method = None
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0)'
                      ' Gecko/20100101 Firefox/127.0'
    }

    # 初始化
    def __init__(self, site, cfg, outfile=None):
        try:
            self.site = site
            self.cfg = cfg
            if outfile is not None:
                self.outfile = outfile
            else:
                self.outfile = "urls_out.txt"

            # 去掉域名最后的'/'
            if self.site.endswith('/'):
                self.site = self.site[:-1]
            # 加上https://
            if '://' not in self.site:
                self.site = 'http://' + self.site
        except Exception as e:
            logging.error('Scanner init error: {}'.format(e))

    def run(self):
        self.scan_one(self.site, self.cfg)

    # 扫描单个
    def scan_one(self, site, dic):
        # 路径前缀加'/'
        if not dic.startswith('/'):
            dic = '/' + dic
        url = site + dic
        try:

            # allow_redirects=False不允许重定向，防⽌重定向误识别为存在的⻚⾯
            res = requests.get(url, verify=False, allow_redirects=False, headers=self.headers, timeout=8)
            if res.status_code == requests.codes.ok:
                print('\033[93m[+]\033[96m{}\033[0m {}'.format(res.status_code, url))
                self.write_flie(self.outfile, url)
            else:
                print('\033[95m[-]\033[31m{}\033[0m {}'.format(res.status_code, url))
        except Exception as e:
            # 遇到最大连接数跳过
            if 'Max retries exceeded with url' in str(e):
                pass
            else:
                logging.error('Scanner run error: {}, url: {}'.format(e, url))

    # 写文件
    def write_flie(self, file, msg):
        try:
            # 加锁
            g_mutex.acquire()
            with open("../{}".format(file), 'a+') as f:
                f.write('{}\r\n'.format(msg))
        except Exception as e:
            logging.error('Write flie error: {}'.format(e))
        finally:
            # 释放锁
            g_mutex.release()


class Manager(object):
    cfg = None

    def __init__(self, outfile=None):
        self.outfile = outfile
        try:
            conf = json.load(open('../tool_data/config.json'))  # 读取配置文件
            self.cfg = {
                'website': self.read_website(conf['website']),
                'dics': self.read_web_path(conf['dic_folder']),
                'threads_num': conf['threads_num']
            }
            self.pool = ThreadPoolExecutor(max_workers=self.cfg['threads_num'])  # 生成线程池
        except Exception as e:
            logging.error('Manager __init__ error: {}'.format(e))

    # 启动扫描
    def start(self):
        try:
            for site in self.cfg['website']:
                w = Worker(site, self.cfg, self.pool, self.outfile)
                w.start()
        except Exception as e:
            logging.error('Manager start error: {}'.format(e))

    # 读取web域名
    def read_website(self, webcfg):
        try:
            websites = []
            with open(webcfg, 'r') as webs:
                for web in webs.readlines():
                    websites.append(web.strip())
            return websites
        except Exception as e:
            logging.error('Read website failed: {}'.format(e))

    # 读取web路径
    def read_web_path(self, diccfg):
        try:
            dics = []
            diclist = os.listdir(diccfg)  # 先获取要读的目录
            diclist.sort()
            for filename in diclist:
                filename = diccfg + '/' + filename  # 组合目录+文件名，循环要读取的具体文件
                with open(filename, 'r') as dic:
                    for line in dic.readlines():
                        dics.append(line.strip())
            return dics
        except Exception as e:
            logging.error('Read web path failed: {}, dicname: {}'.format(e, filename))


def main():
    w = Manager()
    w.start()


if __name__ == '__main__':
    main()
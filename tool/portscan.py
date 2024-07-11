import nmap
from concurrent.futures import ThreadPoolExecutor, wait
import time

pr_blue = '\033[94m'
pr_red = '\033[31m'
pr_yellow = '\033[93m'
pr_green = '\033[96m'


class portScan(object):

    def __init__(self, target_ip, start_port, end_port):
        self.ip = target_ip
        self.start_port = start_port
        self.end_port = end_port

    def portscan(self, host, port):
        '''
        使用namp做指纹识别
        :param host: 目的ip
        :param port: 端口
        :return:
        '''
        try:
            nmScan = nmap.PortScanner()
            nmScan.scan(host, str(port))
            state = nmScan[host]["tcp"][int(port)]["state"]  # 端口状态
            protocol = nmScan[host]["tcp"][int(port)]["name"]  # 协议
            product = nmScan[host]["tcp"][int(port)]["product"]  # 系统
            version = nmScan[host]["tcp"][int(port)]["version"]  # 版本
            extrainfo = nmScan[host]["tcp"][int(port)]["extrainfo"]
            # print(nmScan[host]["tcp"][int(port)])
            result = "{}[*] {}{} tcp/{} {}[{}]\n{}{} {}".format(
                pr_red, pr_blue, host, port, pr_green, state, pr_yellow, product, version)
            if extrainfo:
                result += "os: {}".format(extrainfo)
            print(result)
        except nmap.PortScannerError as e:
            print("{}Scan error: {}".format(pr_red, str(e)))
        except Exception as e:
            print("{}Unexpected error: {}".format(pr_red, str(e)))

    def start(self):
        '''
        启动多线程扫描端口
        :return:
        '''
        # tgtPorts = str(self.start_port).split(",")
        # print(tgtPort0s)
        pool = ThreadPoolExecutor(max_workers=20)
        tgtPorts = []
        for port in range(self.start_port, self.end_port + 1):
            tgtPorts.append(str(port))
        if (self.ip == None) | (tgtPorts[0] == None):
            print("请按照规则输入IP和端口")
            exit(0)

        # Scan the hosts with the ports etc
        future = [pool.submit(self.portscan, self.ip, tgtPort) for tgtPort in tgtPorts]
        wait(future)



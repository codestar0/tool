import optparse
import argparse
import os
import nmap
from lxml import etree
from netaddr import IPNetwork
from commons import YamlConf


def c_Scan(hosts, ports):
    '''
    -sS:隐藏扫描
    -n:不用域名解析
    --min-hostgroup: 调整并行扫描组的大小
    -sV:版本探测
    :return:
    '''
    try:
        print(hosts, ports)
        c_scan = nmap.PortScanner()
        c_scan.scan(hosts=hosts, ports=ports,
                    arguments='-sV --open --min-hostgroup 2 --min-parallelism 500 --host-timeout 60 -T4')
        for host in c_scan.all_hosts():
            print(host)
            for proto in c_scan[host].all_protocols():
                print('----------')
                print('Protocol : %s' % proto)
                lport = c_scan[host][proto].keys()
                print(c_scan[host][proto])
                for port in sorted(lport):
                    if len(c_scan[host][proto][port]['name']) > 0:
                            print('port : {}\tstate : {}\tService : {}'
                                  .format(port, c_scan[host][proto][port]['state'],
                                          c_scan[host][proto][port]['name']))
                    else:
                        print('port : {}\tstate : {}\t'
                              .format(port, c_scan[host][proto][port]['state']))
    except nmap.PortScannerError as e:
        print("Scan error: " + str(e))
    except Exception as e:
        print("Unexpected error: " + str(e))


def subnetScan(host, hostOnly=False, configFile=None):
    '''
    C段扫描
    :param host:
    :param hostOnly:
    :param configFile:
    :return:
    '''
    confFile = configFile if configFile else os.path.join('./tool_data', 'port_mapping.yaml')

    portsConf = YamlConf(confFile)  # 加载配置文件
    httpPorts = [str(k) for k in portsConf if portsConf[k]['protocol'] == "http"]  # 提取http协议的端口
    httpPorts = ",".join(httpPorts)
    # 判断是否进行C段扫描
    if not hostOnly:
        # print(host + '/24')
        c_Scan(host + '/24', httpPorts)
    else:
        # print(host)
        c_Scan(host, httpPorts)

if __name__ == '__main__':
    subnetScan('192.168.133.132', hostOnly=True)





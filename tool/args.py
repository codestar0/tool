import argparse

from nmapscan import subnetScan
from password import Worker
from webdirscan import Manager
from sqlburp import SqlBurp
from portscan import portScan

# C段扫描
def donmapscan(args):

    subnetScan(args.host, args.hostonly)

# 社工密码生成
def dopasswdgen(args):

    passwd = Worker(args.output)
    passwd.start()

# web目录扫描
def dowebdirscan(args):
    webscan = Manager(args.output)
    webscan.start()

# mysql用户名密码爆破
def dosqlburp(args):

    sqlburp = SqlBurp(args.host, args.port)
    sqlburp.start_sql_brup()

# 端口扫描
def doportscan(args):

    portscan = portScan(args.host, args.startPort, args.endPort)
    portscan.start()



def main():
    parser = argparse.ArgumentParser(description="渗透测试辅助工具")
    subparser = parser.add_subparsers(title="子命令", description="使用子命令,使用 'args.py 子命令 -h' 获得子命令帮助")

    # C段扫描
    subnet = subparser.add_parser("subnet", help="C段扫描工具")
    subnet.add_argument("host", help=u"指定扫描目的IP")
    subnet.add_argument("--hostonly", action="store_true", help=u"仅扫描目的Host,不进行C段扫描")
    # subnet.add_argument("-o", "--output", help=u"指定输出文件")
    subnet.set_defaults(func=donmapscan)

    # 社工密码生成
    passwdgen = subparser.add_parser("passwdgen", help="社会工程学密码字典生成,指定信息在passwd.json")
    passwdgen.add_argument("-o", "--output", help="指定输出文件")
    passwdgen.set_defaults(func=dopasswdgen)

    # Web目录扫描
    webscan = subparser.add_parser("webscan", help="web目录扫描,web域名配置文件websites.txt")
    webscan.add_argument("-o", "--output", help="指定输出文件")
    webscan.set_defaults(func=dowebdirscan)

    # 数据库用户名密码baopo
    sqlburp = subparser.add_parser("sqlburp", help="mysql数据库用户名密码爆破,导入mysql_user.txt、mysql_pass.txt数据")
    sqlburp.add_argument("host", help="数据库IP地址,like:127.0.0.1")
    sqlburp.add_argument("port", type=int, help="数据库端口,like:3306")
    sqlburp.set_defaults(func=dosqlburp)

    portscan = subparser.add_parser("portscan", help="端口扫描工具，请配置目的IP和端口范围")
    portscan.add_argument("host", help="目的IP,like:127.0.0.1")
    portscan.add_argument("startPort", type=int, help="起始端口,like:3306")
    portscan.add_argument("endPort", type=int, help="结束端口,like:3336")
    portscan.set_defaults(func=doportscan)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()

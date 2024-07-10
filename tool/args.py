import argparse

from nmapscan import nmapScan, subnetScan
from password import Worker
from webdirscan import Manager


def donmapscan(args):

    subnetScan(args.host, args.hostonly)

def dopasswdgen(args):

    passwd = Worker(args.output)
    passwd.start()

def dowebdirscan(args):
    webscan = Manager(args.output)
    webscan.start()


def main():
    parser = argparse.ArgumentParser(description="渗透测试辅助工具")
    subparser = parser.add_subparsers(title="子命令", description="使用子命令，使用 'args.py 子命令 -h' 获得子命令帮助")

    # C段扫描
    subnet = subparser.add_parser("subnet", help="C段扫描工具")
    subnet.add_argument("host", help=u"指定扫描目的Host")
    subnet.add_argument("--hostonly", action="store_true", help=u"仅扫描目的Host，不进行C段扫描")
    # subnet.add_argument("-o", "--output", help=u"指定输出文件")
    subnet.set_defaults(func=donmapscan)

    # 社工密码生成
    passwdgen = subparser.add_parser("passwdgen", help="社会工程学密码字典生成，指定信息在passwd.json")
    passwdgen.add_argument("-o", "--output", help="指定输出文件")
    passwdgen.set_defaults(func=dopasswdgen)

    # Web目录扫描
    webscan = subparser.add_parser("webscan", help="web目录扫描,web域名配置文件websites.txt")
    webscan.add_argument("-o", "--output", help="指定输出文件")
    webscan.set_defaults(func=dowebdirscan)


    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()

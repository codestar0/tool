import argparse

from nmapscan import nmapScan, subnetScan
from password import Worker


def donmapscan(args):

    subnetScan(args.host, args.hostonly)

def dopasswdgen(args):

    passwd = Worker(args.output)
    passwd.start()


def main():
    parser = argparse.ArgumentParser(description="渗透测试辅助工具")
    subparser = parser.add_subparsers(title="子命令", description="使用子命令，使用 'args.py 子命令 -h' 获得子命令帮助")

    subnet = subparser.add_parser("subnet", help="C段扫描工具")
    subnet.add_argument("host", help=u"指定扫描目的Host")
    subnet.add_argument("--hostonly", action="store_true", help=u"仅扫描目的Host，不进行C段扫描")
    # subnet.add_argument("-o", "--output", help=u"指定输出文件")
    subnet.set_defaults(func=donmapscan)

    passwdgen = subparser.add_parser("password", help="社会工程学密码字典生成，指定信息在passwd.json")
    passwdgen.add_argument("-o", "--output", help="指定输出文件")
    passwdgen.set_defaults(func=dopasswdgen)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()

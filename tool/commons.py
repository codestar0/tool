import sys
import types
import yaml


from colorama import Fore, Style


class PenError(Exception):
    def __init__(self, errorMsg):
        self.errorMsg = errorMsg

    def __str__(self):
        #return self.errorMsg.encode(sys.stdout.encoding)
        return self.errorMsg


class YamlConf(object):
    '''
    Yaml配置文件加载器
    '''
    def __new__(cls, path):
        try:
            _file = open(path, "r", encoding="utf-8")
            result = yaml.safe_load(_file)
        except IOError:
            raise PenError("Loading yaml file '{0}' failed, read file failed".format(path))
        except yaml.YAMLError as error:
            raise PenError("Loading yaml file '{0}' failed, yaml error, reason: '{1}'".format(path,str(error)))
        except Exception as error:
            raise PenError("Loading yaml file '{0}' failed, reason: {1}".format(path,str(error)))

        return result


class Output(object):
    '''
    终端输出功能
        该类用于输出信息到控制台和文件
    '''

    _WIDTH = 80
    _CHAR = "-"

    def __init__(self, title=None, tofile=None):
        '''
        @params:
            title: 输出的标题
            tofile: 输出文件
        '''
        self._title = title
        self._fileName = tofile
        self._file = self._openFile(tofile)

    def _openFile(self, filename):
        if filename:
            try:
                _file = open(filename, "w")
            except IOError:
                _file = None
                raise PenError("open output file '{0}' failed".format(filename))
        else:
            _file = None

        return _file

    def openFile(self, filename):
        self._fileName = filename
        self._file = self._openFile(filename)

    def init(self, title=None, tofile=None):
        if title: self._title = title
        if tofile:
            self._fileName = tofile
            self._file = self._openFile(tofile)

        self.raw(self._banner())
        self.yellow(u"[{0}]".format(self._title))
        self.raw(self._CHAR * self._WIDTH)

    # @classmethod
    # def safeEncode(cls, msg, method=None):
    #     '''
    #     安全编码
    #         如果msg中有不能编码的字节，自动处理为16进制
    #     '''
    #     if isinstance(msg, str):
    #         return msg
    #     elif isinstance(msg, unicode):
    #         method = method.lower() if method else sys.stdin.encoding
    #         try:
    #             return msg.encode(method)
    #         except UnicodeError:
    #             resultList = []
    #             for word in msg:
    #                 try:
    #                     encodedWord = word.encode(method)
    #                 except UnicodeError:
    #                     encodedWord = "\\x" + repr(word)[4:6] + "\\x" + repr(word)[6:8]
    #
    #                 resultList.append(encodedWord)
    #
    #             return "".join(resultList)
    #     else:
    #         try:
    #             msg = unicode(msg)
    #         except UnicodeDecodeError:
    #             msg = str(msg)
    #         return cls.safeEncode(msg, method)

    @classmethod
    def R(cls, msg):
        '''
        字符串着色为红色
        '''
        return Fore.RED + msg + Style.RESET_ALL

    @classmethod
    def Y(cls, msg):
        '''
        字符串着色为橙色
        '''
        return Fore.YELLOW + msg + Style.RESET_ALL

    @classmethod
    def B(cls, msg):
        '''
        字符串着色为蓝色
        '''
        return Fore.BLUE + msg + Style.RESET_ALL

    @classmethod
    def G(cls, msg):
        '''
        字符串着色为绿色
        '''
        return Fore.GREEN + msg + Style.RESET_ALL

    @classmethod
    def raw(cls, msg):
        '''
        无颜色输出
        '''
        print
        cls.safeEncode(msg)

    @classmethod
    def red(cls, msg):
        '''
        打印红色信息
        '''
        cls.raw(cls.R(msg))

    @classmethod
    def yellow(cls, msg):
        '''
        打印橙色信息
        '''
        cls.raw(cls.Y(msg))

    @classmethod
    def blue(cls, msg):
        '''
        打印蓝色信息
        '''
        cls.raw(cls.B(msg))

    @classmethod
    def green(cls, msg):
        '''
        打印绿色信息
        '''
        cls.raw(cls.G(msg))

    @classmethod
    def info(cls, msg):
        cls.raw(msg)

    @classmethod
    def error(cls, msg):
        cls.red(msg)

    @classmethod
    def warnning(cls, msg):
        cls.yellow(msg)

    def write(self, data):
        '''
        写入数据到文件
        '''
        if self._file:
            try:
                self._file.write(data)
                return True
            except IOError:
                raise PenError("write output file '{0}' failed".format(self._fileName))
        else:
            return False

    def writeLine(self, line, parser=None):
        '''
        写入一行数据到文件
        @params:
            line: 待写入的数据
            parser: 处理待写入数据的回调函数
        '''
        if self._file:
            if parser and isinstance(parser, types.FunctionType):
                line = parser(line)
            try:
                self._file.write(line + "\n")
                return True
            except IOError:
                raise PenError("write output file '{0}' failed".format(self._fileName))
        else:
            return False

    def _banner(self):
        '''
        生成banner信息
        '''
        fmt = "|{0:^" + "{0}".format(self._WIDTH + 7) + "}|"

        banner = "+" + self._CHAR * (self._WIDTH - 2) + "+\n"
        banner = banner + fmt.format(self.Y("PentestDB.") + " Tools and Resources for Web Penetration Test.") + "\n"
        banner = banner + fmt.format(self.G("https://github.com/alpha1e0/pentestdb")) + "\n"
        banner = banner + "+" + self._CHAR * (self._WIDTH - 2) + "+\n"

        return banner

    def close(self):
        self.raw(self._CHAR * self._WIDTH)
        if self._file:
            self._file.close()

    def __enter__(self):
        self.init()
        return self

    def __exit__(self, *args):
        self.close()


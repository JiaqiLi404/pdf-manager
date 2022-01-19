import base64
import tkinter as tk
import requests
from tkinter import *
from PIL import Image, ImageTk
import os
import File_Controller as fc
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from tkinter import scrolledtext

'''
class ListboxWithPreview():
    def __init__(self, root, x, y):
        self.__chose = None
        self.__li = []
        self.__eachheight = 35
        self.__boxnum = 0
        self.__x = x
        self.__y = y
        width = 250
        height = 850

        def onclick(event):
            print(event)

        # 创建容器
        self.__canvas = Canvas(root, width=width, height=height, scrollregion=(0, 0, width * 2, 1000), bg='white')

        self.__canvas.place(x=x, y=y, anchor=NW)  # 放置canvas的位置
        self.__frame = Frame(self.__canvas, bg='white', width=width * 4, height=2000)  # 把frame放在canvas里
        self.__frame.place(x=0, y=0)  # frame的长宽，和canvas差不多的
        self.__frame.bind('<Button-1>', onclick)
        vbar = Scrollbar(self.__canvas, orient=VERTICAL)  # 竖直滚动条
        vbar.place(x=width - 15, width=17, height=height)
        vbar.configure(command=self.__canvas.yview)
        hbar = Scrollbar(self.__canvas, orient=HORIZONTAL)  # 水平滚动条
        hbar.place(x=0, y=height - 15, width=width, height=17)
        hbar.configure(command=self.__canvas.xview)
        self.__canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)  # 设置
        self.__canvas.create_window((27, 10),
                                    window=self.__frame)  # create_window

    def addlist(self, txt):
        label = tk.Label(self.__frame, text=txt, font=("宋体", 18), bg='white')
        self.__li.append(label)
        self.__boxnum = self.__boxnum + 1
        label.place(x=494, y=1100, anchor=NW)
        if self.__boxnum == 1:
            self.__chose = self.__li[0]
            self.__li[0].config(bg='grey')
'''

curfile = 0
curpage = 0
tok = None


class WR_Page():
    def __init__(self):
        global wr_page, tok

        def on_closing():
            sys.exit(0)

        wr_page = Toplevel()
        wr_page.title('PDF Manager v1.0               Designed by LJQ')
        wr_page.geometry('1920x1020+0+0')
        wr_page["background"] = 'white'
        wr_page.resizable(0, 0)  # 防止用户调整尺寸
        wr_page.protocol("WM_DELETE_WINDOW", on_closing)
        self.ui()
        tok = self.gettoken()

    def mainloop(self):
        wr_page.mainloop()

    def show(self):
        wr_page.update()
        wr_page.deiconify()

    def hide(self):
        wr_page.withdraw()

    def gettoken(self):
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&' \
               'client_id=7CWcCF98Fw24no52jLYYi92b&client_secret=zWBwxSbskSqMqzV4L6V0gOZZvyMRHEpK'
        response = requests.get(host)
        # if response:
        # print(response.json())
        return response.json()["access_token"]

    def ocr(self, path):
        bai_du_ocr_max = 4096
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
        # 二进制方式打开图片文件
        f = open(path, 'rb')
        img = base64.b64encode(f.read())
        params = {"image": img, "paragraph": 'true'}
        access_token = tok
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        # if response:
        # print(response.json())
        return response.json()

    def ui(self):
        global file_dir, pages_inf, libox1, libox2, label_img, text
        pages_inf = []
        file_dir = os.listdir(fc.getcurrpath() + '/temp')
        # print(file_dir)

        yscroll1 = Scrollbar(wr_page, orient=VERTICAL)
        yscroll1.place(x=390, y=75, height=890)
        xscroll1 = Scrollbar(wr_page, orient=HORIZONTAL)
        xscroll1.place(x=25, y=970, width=383)
        yscroll2 = Scrollbar(wr_page, orient=VERTICAL)
        yscroll2.place(x=505, y=75, height=890)

        file_list = StringVar()
        libox1 = Listbox(wr_page, width=30, height=37, listvariable=file_list, yscrollcommand=yscroll1.set,
                         xscrollcommand=xscroll1.set, font=('宋体', 17), selectmode=tk.SINGLE)
        file_list.set(tuple(file_dir))

        pagelist = StringVar()
        libox2 = Listbox(wr_page, width=5, height=37, listvariable=pagelist, yscrollcommand=yscroll2.set,
                         font=('宋体', 17))

        yscroll1["command"] = libox1.yview
        xscroll1["command"] = libox1.xview
        yscroll2["command"] = libox2.yview

        for i in file_dir:
            pages_inf.append(fc.getmaxpage(i))
        pages = []
        for j in range(pages_inf[0]):
            pages.append(str(j + 1))
        pagelist.set(tuple(pages))

        def choosefile(event):
            global curfile, curpage
            libox2.itemconfig(curpage, bg='white')
            libox1.itemconfig(curfile, bg='white')
            curfile = libox1.curselection()[0]
            libox1.itemconfig(curfile, bg='grey')
            pages = []
            for j in range(pages_inf[curfile]):
                pages.append(str(j + 1))
            pagelist.set(tuple(pages))

            libox2.itemconfig(0, bg='grey')
            curpage = 0
            flashimg()

        def choosepage(event):
            global curpage
            libox2.itemconfig(curpage, bg='white')
            curpage = libox2.curselection()[0]
            libox2.itemconfig(curpage, bg='grey')
            flashimg()

        libox1.select_set(0)
        libox1.itemconfig(0, bg='grey')
        libox2.select_set(0)
        libox2.itemconfig(0, bg='grey')
        libox1.bind('<Double-Button-1>', choosefile)
        libox2.bind('<Double-Button-1>', choosepage)
        libox1.place(x=25, y=75)
        libox2.place(x=440, y=75)
        path = os.getcwd() + '\\temp\\' + file_dir[curfile] + '\\' + str(curpage) + '.png'
        # path=fc.getcurrpath()+'/temp/'+file_dir[curfile]+'/'+str(curpage)+'.png'
        img_open = Image.open(path)
        img_open = img_open.resize((670, 910))
        self.img_png = ImageTk.PhotoImage(image=img_open)
        label_img = tk.Label(wr_page, image=self.img_png)
        label_img.place(x=550, y=75)

        def flashimg():
            global img_png
            path = os.getcwd() + '\\temp\\' + file_dir[curfile] + '\\' + str(curpage) + '.png'
            # path=fc.getcurrpath()+'/temp/'+file_dir[curfile]+'/'+str(curpage)+'.png'
            img_open = Image.open(path)
            img_open = img_open.resize((670, 910))
            self.img_png = ImageTk.PhotoImage(image=img_open)
            label_img.config(image=self.img_png)
            wr_page.update()

        text = scrolledtext.ScrolledText(wr_page, width=60, height=42, font=("宋体", 14))
        text.place(x=1260, y=187)

        def pagetotext():
            path = os.getcwd() + '\\temp\\' + file_dir[curfile] + '\\' + str(curpage) + '.png'
            result = self.ocr(path)
            words = result["words_result"]
            t = ''
            para_inf = []
            for p in result['paragraphs_result']:
                para_inf.append(int(p['words_result_idx'][-1]))
            num = 0
            for w in words:
                # print(w,w['words'],t)
                t = t + w['words']
                if para_inf.count(num) > 0:
                    t = t + '\n' + '  '
                num = num + 1
            # print(t)
            text.delete(0.0, END)
            text.insert(INSERT, t)
            wr_page.update()
            print("文字识别成功")

        def filetotext():
            pass

        def filetoword():
            pass

        def alltoword():
            pass

        def goback():
            pass

        tk.Label(wr_page, text="选择文件：", bg='white', font=('黑体', 15)).place(x=25, y=40, anchor=NW)
        tk.Label(wr_page, text="页码：", bg='white', font=('黑体', 15)).place(x=440, y=40, anchor=NW)
        tk.Label(wr_page, text="预览：", bg='white', font=('黑体', 15)).place(x=550, y=40, anchor=NW)
        tk.Label(wr_page, text="结果展示：", bg='white', font=('黑体', 15)).place(x=1260, y=157, anchor=NW)

        tk.Button(wr_page, text='将该页转为文字', bg='white', font=('黑体', 13), width=20, height=2, command=pagetotext) \
            .place(x=1260, y=25, anchor=NW)
        tk.Button(wr_page, text='将该文件转为文字', bg='white', font=('黑体', 13), width=20, height=2, command=filetotext) \
            .place(x=1520, y=25, anchor=NW)
        tk.Button(wr_page, text='将该文件转为word', bg='white', font=('黑体', 13), width=20, height=2, command=filetoword) \
            .place(x=1260, y=95, anchor=NW)
        tk.Button(wr_page, text='将所有文件转为word', bg='white', font=('黑体', 13), width=20, height=2, command=alltoword) \
            .place(x=1520, y=95, anchor=NW)
        tk.Button(wr_page, text='返回', bg='white', font=('黑体', 13), width=10, height=2, command=goback) \
            .place(x=1777, y=60, anchor=NW)


def start():
    wrpage = WR_Page()
    wrpage.mainloop()

# start()

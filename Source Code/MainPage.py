import tkinter as tk
from tkinter import *
from tkinter import filedialog
from TkinterDnD2 import *
import os
import File_Controller as fc
from tkinter.messagebox import *
import Words_Recongnize as wr
import WaterMark_Remover as wm_r


# pyinstaller -F MainPage.py --add-data D:\PycharmProjects\pdf_manager\venv\tcl\tkdnd2.8;tkdnd
class MainPage:

    def __init__(self):
        global main_page, filelist
        filelist = []
        main_page = TkinterDnD.Tk()
        main_page.title('PDF Manager v1.0               Designed by LJQ')
        main_page.geometry('1600x900+150+50')
        main_page["background"] = 'white'
        main_page.resizable(0, 0)  # 防止用户调整尺寸
        self.ui()

    def destorywin(self):
        global w
        w.destory()

    def show(self):
        main_page.mainloop()

    def hide(self):
        main_page.withdraw()

    def ui(self):
        # 文件导入功能
        def open_file():
            files = filedialog.askopenfiles(title=u'批量导入PDF文件', filetypes=[("PDF", ".pdf")])
            temp = []
            for f in files:
                temp.append(f.name)
            add = fc.getallpdf(temp)
            if not add:
                return
            for f in add:
                if filelist.count(f) == 0:
                    filelist.append(f)
                    libox1.insert('end', os.path.abspath(f))

        def open_dir():
            files = filedialog.askdirectory()
            add = fc.getallpdf([files])
            if not add:
                return
            for f in add:
                if filelist.count(f) == 0:
                    filelist.append(f)
                    libox1.insert('end', os.path.abspath(f))

        tk.Button(main_page, text='导入PDF文件\r\n(支持拖拽)', bg='white', font=('黑体', 30), width=20, height=9
                  , command=open_file).place(x=500, y=200, anchor=NW)
        tk.Button(main_page, text='导入文件夹\r\n(支持拖拽)', bg='white', font=('黑体', 30), width=20, height=9
                  , command=open_dir).place(x=1000, y=200, anchor=NW)

        # 页面跳转功能
        def jumptoWM(event):
            if len(filelist) > 0:
                mainPage.hide()
                fc.cvt2img(filelist, 2.8)
                wm_r.start()
            else:
                showinfo("提示", "请先导入以'.pdf'结尾的PDF文件哦")

        def jumptoWR(event):
            if len(filelist) > 0:
                mainPage.hide()
                fc.cvt2img(filelist, 1.5)
                # time.sleep(2)
                wr.start()
            else:
                showinfo("提示", "请先导入以'.pdf'结尾的PDF文件哦")

        def jumptoNM(event):
            print(event)

        def jumptoCP(event):
            print(event)

        depart = 252
        start = 500
        b3 = tk.Button(main_page, text='水印去除', bg='white', font=('黑体', 17), width=12, height=2)
        b3.bind('<Button-1>', jumptoWM)
        b3.place(x=start, y=730, anchor=NW)
        b4 = tk.Button(main_page, text='文字识别', bg='white', font=('黑体', 17), width=12, height=2)
        b4.bind('<Button-1>', jumptoWR)
        b4.place(x=start + depart, y=730, anchor=NW)
        b5 = tk.Button(main_page, text='文件名管理', bg='white', font=('黑体', 17), width=12, height=2)
        b5.bind('<Button-1>', jumptoNM)
        b5.place(x=start + 2 * depart, y=730, anchor=NW)
        b6 = tk.Button(main_page, text='PDF压缩', bg='white', font=('黑体', 17), width=12, height=2)
        b6.bind('<Button-1>', jumptoCP)
        b6.place(x=start + 3 * depart, y=730, anchor=NW)

        # 拖拽功能
        libox1 = tk.Listbox(main_page, width=45, height=33, font=('黑体', 10))
        libox1.place(x=85, y=200, anchor=NW)

        def drop(event):
            if event.data:
                # print(event.data)
                files = []
                temp = event.data.split('/')

                str = temp[0]
                # print(temp)
                for t in temp[1:]:

                    if t.endswith(':'):
                        str = str + '/' + t[0:-3]
                        str = str.rstrip()
                        str = str.strip('{}')
                        files.append(str)
                        str = t[-2:]
                    else:
                        str = str + '/' + t
                str = str.strip('{}')
                files.append(str)
                # print(files)
                add = fc.getallpdf(files)
                if not add:
                    return event.action
                for f in add:
                    if filelist.count(f) == 0:
                        filelist.append(f)
                        libox1.insert('end', os.path.abspath(f))
            return event.action

        main_page.drop_target_register(DND_FILES)
        main_page.dnd_bind('<<Drop>>', drop)

        # 列表功能
        def list_rem():
            temp = libox1.curselection()
            if temp == (): return
            temp = temp[0]
            filelist.pop(temp)
            libox1.delete(temp)
            # print(filelist)

        def list_reimp():
            libox1.delete(0, END)
            filelist.clear()

        tk.Button(main_page, text='移除选中', bg='white', font=('黑体', 12), width=8, height=2, command=list_rem) \
            .place(x=85, y=680, anchor=NW)
        tk.Button(main_page, text='重新导入', bg='white', font=('黑体', 12), width=8, height=2, command=list_reimp) \
            .place(x=330, y=680, anchor=NW)

    def rebuildtemp(self):
        fc.rebuildtemp()


mainPage = MainPage()
mainPage.rebuildtemp()
mainPage.show()

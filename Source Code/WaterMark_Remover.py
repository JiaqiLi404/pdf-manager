import _thread
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import PyPDF2
import File_Controller as fc
from cv2 import *
import cv2.cv2 as cv2
import shutil
import time
import Image_Controller as ic
import gc

curfile = 0
curpage = 1


class WMR_Page():
    def __init__(self):
        global wmr_page, s1, e1, s2, e2, s3, e3, alpha, belta
        s1 = s2 = s3 = e1 = e2 = e3 = -1
        alpha = 1.04
        belta = -8

        def on_closing():
            sys.exit(0)

        wmr_page = Toplevel()
        wmr_page.title('PDF Manager v1.0               Designed by LJQ')
        wmr_page.geometry('1920x1020+0+0')
        wmr_page["background"] = 'white'
        wmr_page.resizable(0, 0)  # 防止用户调整尺寸
        wmr_page.protocol("WM_DELETE_WINDOW", on_closing)
        self.ui()

    def mainloop(self):
        wmr_page.mainloop()

    def show(self):
        print('显示窗体')
        wmr_page.update()
        wmr_page.deiconify()

    def hide(self):
        print('隐藏窗体')
        wmr_page.withdraw()

    def dooperation(self):
        global opcommand
        '''
            operations.append(['矩框置白:', '对文件', curfile + 1, '第', curpage, '页生效']) 6
            operations.append(['RGB滤波:', '对文件', curfile + 1, '第', curpage, '页生效'])
            operations.append(['HSV滤波:', '对文件', curfile+ 1, '第', curpage , '页生效'])            
                operations.append(['矩框置白:', '对文件', curfile + 1, '生效']) 4
                operations.append(['RGB滤波:', '对文件', curfile + 1, '生效'])
                operations.append(['HSV滤波:', '对文件', curfile + 1, '生效'])
                    operations.append(['矩框置白:', '对所有文件生效']) 2
                    operations.append(['RGB滤波:', '对所有文件生效'])
                    operations.append(['HSV滤波:', '对所有文件生效'])
        operations.append(['  (', x1, y1, ')到(', x2, y2, ')'])
        operations.append(['  ', s1, s2, s3, '到', e1, e2, e3])
        operations.append(['  ', s1, s2, s3, '到', e1, e2, e3])
        '''
        for op in operations:
            if op[0] == '矩框置白:':
                if len(op) == 6:
                    opcommand = [0, op[2] - 1, op[4]]
                elif len(op) == 4:
                    opcommand = [0, op[2] - 1]
                else:
                    opcommand = [0]
                continue
            elif op[0] == 'RGB滤波:':
                if len(op) == 6:
                    opcommand = [1, op[2] - 1, op[4]]
                elif len(op) == 4:
                    opcommand = [1, op[2] - 1]
                else:
                    opcommand = [1]
                continue
            elif op[0] == 'HSV滤波:':
                if len(op) == 6:
                    opcommand = [2, op[2] - 1, op[4]]
                elif len(op) == 4:
                    opcommand = [2, op[2] - 1]
                else:
                    opcommand = [2]
                continue

            if opcommand[0] == 0:
                if len(opcommand) == 1 or (len(opcommand) == 2 and opcommand[1] == curfile) or \
                        (len(opcommand) == 3 and opcommand[1] == curfile and opcommand[2] == curpage):
                    self.cvimgaft = ic.setwhite(self.cvimgaft, op[1], op[2], op[4], op[5])
            elif opcommand[0] == 1:
                if len(opcommand) == 1 or (len(opcommand) == 2 and opcommand[1] == curfile) or \
                        (len(opcommand) == 3 and opcommand[1] == curfile and opcommand[2] == curpage):
                    self.cvimgaft = ic.rgbfilter(self.cvimgaft, op[1], op[5], op[2], op[6], op[3], op[7])
            elif opcommand[0] == 2:
                if len(opcommand) == 1 or (len(opcommand) == 2 and opcommand[1] == curfile) or \
                        (len(opcommand) == 3 and opcommand[1] == curfile and opcommand[2] == curpage):
                    self.cvafthsv = cv2.cvtColor(self.cvimgaft, cv2.COLOR_BGR2HSV)
                    self.cvafthsv = ic.hsvfilter(self.cvafthsv, op[1], op[5], op[2], op[6], op[3], op[7])
                    self.cvimgaft = cv2.cvtColor(self.cvafthsv, cv2.COLOR_HSV2BGR)

    def ui(self):
        global file_dir, pages_inf, pages, libox1, libox2, libox3, operations
        operations = []
        pages_inf = []
        file_dir = os.listdir(fc.getcurrpath() + '/temp')

        yscroll1 = Scrollbar(wmr_page, orient=VERTICAL)
        yscroll1.place(x=315, y=75, height=905)
        xscroll1 = Scrollbar(wmr_page, orient=HORIZONTAL)
        xscroll1.place(x=25, y=980, width=307)
        yscroll2 = Scrollbar(wmr_page, orient=VERTICAL)
        yscroll2.place(x=393, y=75, height=905)

        file_list = StringVar()
        libox1 = Listbox(wmr_page, width=32, height=50, listvariable=file_list, yscrollcommand=yscroll1.set,
                         xscrollcommand=xscroll1.set, font=('宋体', 13), selectmode=tk.SINGLE)
        file_list.set(tuple(file_dir))
        pagelist = StringVar()
        libox2 = Listbox(wmr_page, width=4, height=50, listvariable=pagelist, yscrollcommand=yscroll2.set,
                         font=('宋体', 13))
        operationlist = StringVar()
        libox3 = Listbox(wmr_page, width=37, height=34, listvariable=operationlist, font=('宋体', 12))

        yscroll1["command"] = libox1.yview
        xscroll1["command"] = libox1.xview
        yscroll2["command"] = libox2.yview

        for i in file_dir:
            pages_inf.append(fc.getmaxpage(i))
        pages = []
        for j in range(0, pages_inf[0] + 1):
            pages.append(str(j + 1))
        pagelist.set(tuple(pages))

        # 三个列表
        def choosefile(event):
            global curfile, curpage, pages
            if curpage != 0:
                libox2.itemconfig(pages.index(str(curpage)), bg='white')
            libox1.itemconfig(curfile, bg='white')
            curfile = libox1.curselection()[0]
            libox1.itemconfig(curfile, bg='grey')
            pages = fc.getpagelist(file_dir[curfile])
            pagelist.set(tuple(pages))
            libox2.itemconfig(0, bg='grey')
            curpage = int(pages[0])
            flashimg()

        def choosepage(event):
            global curpage, pages
            if curpage != 0:
                libox2.itemconfig(pages.index(str(curpage)), bg='white')
            curpage = int(libox2.get(libox2.curselection()[0]))
            # print(curpage)
            # print(pages.index(str(curpage + 1)))
            libox2.itemconfig(pages.index(str(curpage)), bg='grey')
            flashimg()

        def deleteop(event):
            if operations[libox3.curselection()[0]][0] == '\000\000' or \
                    operations[libox3.curselection()[0]][0] == '\000\000(':
                operations.pop(libox3.curselection()[0] - 1)
                operations.pop(libox3.curselection()[0] - 1)
            else:
                operations.pop(libox3.curselection()[0])
                operations.pop(libox3.curselection()[0])
            operationlist.set(operations)
            flashimg()

        libox1.select_set(0)
        libox1.itemconfig(0, bg='grey')
        libox2.select_set(0)
        libox2.itemconfig(0, bg='grey')
        libox1.bind('<Double-Button-1>', choosefile)
        libox2.bind('<Double-Button-1>', choosepage)
        libox3.bind('<Double-Button-1>', deleteop)
        libox1.place(x=25, y=75)
        libox2.place(x=355, y=75)
        libox3.place(x=1583, y=398)

        # 两个缩略图
        def flashimg():
            # path=fc.getcurrpath()+'/temp/'+file_dir[curfile]+'/'+str(curpage)+'.png'
            path = os.getcwd() + '\\temp\\' + file_dir[curfile] + '\\' + str(curpage - 1) + '.png'
            shutil.copyfile(path, pathcv + '\\' + str(curpage - 1) + '.png')
            self.cvimgbef = cv2.imread(pathcv + '\\' + str(curpage - 1) + '.png')
            cvimgbefprev = cv2.resize(self.cvimgbef, (550, 850))
            cv2image = cv2.cvtColor(cvimgbefprev, cv2.COLOR_BGR2RGB)  # 转换颜色从BGR到RGBA
            current_image = Image.fromarray(cv2image)  # 将图像转换成Image对象
            self.img_bef = ImageTk.PhotoImage(image=current_image)
            label_img1.config(image=self.img_bef)
            self.cvbefhsv = cv2.cvtColor(self.cvimgbef, cv2.COLOR_BGR2HSV)

            self.cvimgaft = self.cvimgbef.copy()
            self.dooperation()
            cvimgaftprev = cv2.resize(self.cvimgaft, (550, 850))
            cv2image = cv2.cvtColor(cvimgaftprev, cv2.COLOR_BGR2RGB)  # 转换颜色从BGR到RGBA
            current_image = Image.fromarray(cv2image)  # 将图像转换成Image对象
            self.img_aft = ImageTk.PhotoImage(image=current_image)
            label_img2.config(image=self.img_aft)
            self.cvafthsv = cv2.cvtColor(self.cvimgaft, cv2.COLOR_BGR2HSV)
            wmr_page.update()

        pathcv = fc.gettemppath()
        label_img1 = tk.Label(wmr_page)
        label_img1.place(x=435, y=125)
        label_img2 = tk.Label(wmr_page)
        label_img2.place(x=1000, y=125)
        flashimg()

        def showbefimg(event):
            cv2.destroyAllWindows()
            img = cv2.resize(self.cvimgbef, (710, 1000))
            cv2.imshow("HD Image", img)
            # plt.imshow(imgcv)
            # plt.xticks([]), plt.yticks([])  # 隐藏x、y轴
            # plt.show()

        def showaftimg(event):
            cv2.destroyAllWindows()
            img = cv2.resize(self.cvimgaft, (710, 1000))
            cv2.imshow("HD Image", img)

        label_img1.bind('<Double-Button-1>', showbefimg)
        label_img2.bind('<Double-Button-1>', showaftimg)

        # 各种标题
        tk.Label(wmr_page, text="选择文件：", bg='white', font=('黑体', 15)).place(x=25, y=40, anchor=NW)
        tk.Label(wmr_page, text="页码：", bg='white', font=('黑体', 15)).place(x=355, y=40, anchor=NW)
        tk.Label(wmr_page, text="原图", bg='white', font=('黑体', 15)).place(x=685, y=90, anchor=NW)
        tk.Label(wmr_page, text="预览", bg='white', font=('黑体', 15)).place(x=1250, y=90, anchor=NW)
        tk.Label(wmr_page, text="双击删除操作：", bg='white', font=('黑体', 12)).place(x=1580, y=368, anchor=NW)

        # 各个功能的按钮
        def showinf(arg):
            global infwin, tv1, tv2, tv3, exitflag
            infwin = Toplevel()
            infwin.title('Image Info')
            infwin.geometry('250x100+0+0')
            infwin["background"] = 'white'
            infwin.resizable(0, 0)  # 防止用户调整尺寸
            tv1 = tk.StringVar()
            tv2 = tk.StringVar()
            tv3 = tk.StringVar()
            l1 = tk.Label(infwin, textvariable=tv1, bg='white', font=('黑体', 10))
            l2 = tk.Label(infwin, textvariable=tv2, bg='white', font=('黑体', 10))
            l3 = tk.Label(infwin, textvariable=tv3, bg='white', font=('黑体', 10))
            l1.place(x=10, y=10, anchor=NW)
            l2.place(x=10, y=30, anchor=NW)
            l3.place(x=10, y=50, anchor=NW)
            if arg == 'RGB Filter' or arg == 'HSV Filter' or arg == 'configwin':
                def newupdateinf(x, y):
                    global tv1, tv2, tv3, infwin
                    txt1 = 'x:' + str(x) + '  y:' + str(y)
                    txt2 = 'r:' + str(img[y, x, 2]) + ' g:' + str(img[y, x, 1]) + ' b:' + str(img[y, x, 0])
                    img2=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
                    txt3 = 'h:' + str(img2[y, x, 0]) + ' s:' + str(img2[y, x, 1]) + ' v:' + str(img2[y, x, 2])
                    tv1.set(txt1)
                    tv2.set(txt2)
                    tv3.set(txt3)
                    infwin.update()

                def newshowinfcv2method(event, x, y, flags, arg):
                    global h
                    if event == cv2.EVENT_MOUSEMOVE:
                        newupdateinf(x, h * dx + y)
                    elif event == cv2.EVENT_MOUSEWHEEL:
                        if (flags < 0 and h == 100) or (flags > 0 and h == 0):
                            return
                        if flags < 0 and h >= 98:
                            h = 100
                        elif flags > 0 and h <= 2:
                            h = 0
                        elif flags < 0:
                            h = h + 3
                        else:
                            h = h - 3
                        cv2.setTrackbarPos('Pos', arg, h)
                        cv2.imshow(arg, img[h * dx:winheight + h * dx, :, :])

                def updateprev(arg):
                    global last, img
                    if arg == 'RGB Filter' or arg == 'HSV Filter':
                        if last != [s1, e1, s2, e2, s3, e3]:
                            if arg == 'RGB Filter':
                                img = self.cvimgaft.copy()
                                img = ic.rgbfilter(img, s1, e1, s2, e2, s3, e3)
                            else:
                                img = self.cvafthsv.copy()
                                img = ic.hsvfilter(img, s1, e1, s2, e2, s3, e3)
                                img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)

                            def nothing(x):
                                global h
                                h = x
                                cv2.imshow(arg, img[x * dx:winheight + x * dx, :, :])

                            cv2.namedWindow(arg)
                            cv2.createTrackbar('Pos', arg, 0, 100, nothing)
                            cv2.imshow(arg, img[h * dx:winheight + h * dx, :, :])
                            cv2.setTrackbarPos('Pos', arg, h)
                            cv2.moveWindow(arg, 350, 0)
                            cv2.setMouseCallback(arg, newshowinfcv2method, arg)
                            last = [s1, e1, s2, e2, s3, e3]
                    elif arg == 'configwin':
                        if last != [alpha, belta]:
                            img = self.cvimgaft.copy()
                            img = ic.sharpenimg(img, alpha, belta)

                            def nothing(x):
                                global h
                                h = x
                                cv2.imshow(arg, img[x * dx:winheight + x * dx, :, :])

                            cv2.namedWindow(arg)
                            cv2.createTrackbar('Pos', arg, 0, 100, nothing)
                            cv2.imshow(arg, img[h * dx:winheight + h * dx, :, :])
                            cv2.setTrackbarPos('Pos', arg, h)
                            cv2.moveWindow(arg, 350, 0)
                            cv2.setMouseCallback(arg, newshowinfcv2method, arg)
                            last = [alpha, belta]

            def des():
                print('线程启动')
                global last
                last = []
                while 1:
                    time.sleep(0.2)
                    if cv2.getWindowProperty(arg, cv2.WND_PROP_AUTOSIZE) == -1:
                        infwin.destroy()
                        if arg == 'RGB Filter' or arg == 'HSV Filter':
                            preconsole.destroy()
                        if arg!='configwin':
                            self.show()
                        print('线程退出')
                        break
                    if arg == 'RGB Filter' or arg == 'HSV Filter' or arg == 'configwin':
                        updateprev(arg)
                    else:
                        time.sleep(0.3)

            _thread.start_new_thread(des, ())

        def delete_page():
            global curpage, libox2, pages
            libox2.itemconfig(pages.index(str(curpage)), bg='white')
            fc.deletepage(file_dir[curfile], curpage - 1)
            pages.remove(str(curpage))
            pages_inf[curfile] = pages_inf[curfile] - 1
            curpage = 0
            pagelist.set(tuple(pages))
            wmr_page.update()

        def showaskwin(arg):
            askwin = Toplevel()
            askwin.title(arg + ' Asker')
            askwin.geometry('400x280+800+300')
            askwin["background"] = 'white'
            askwin.resizable(0, 0)  # 防止用户调整尺寸
            # askwin.attributes("-toolwindow", 1)
            askwin.wm_attributes("-topmost", 1)

            def opapppa1():
                askwin.destroy()
                if arg == 'delete_rectangle':
                    operations.append(['矩框置白:', '对文件', curfile + 1, '第', curpage, '页生效'])
                elif arg == 'RGB Filter':
                    operations.append(['RGB滤波:', '对文件', curfile + 1, '第', curpage, '页生效'])
                elif arg == 'HSV Filter':
                    operations.append(['HSV滤波:', '对文件', curfile + 1, '第', curpage, '页生效'])
                opapppa()

            def opapppa2():
                askwin.destroy()
                if arg == 'delete_rectangle':
                    operations.append(['矩框置白:', '对文件', curfile + 1, '生效'])
                elif arg == 'RGB Filter':
                    operations.append(['RGB滤波:', '对文件', curfile + 1, '生效'])
                elif arg == 'HSV Filter':
                    operations.append(['HSV滤波:', '对文件', curfile + 1, '生效'])
                opapppa()

            def opapppa3():
                askwin.destroy()
                if arg == 'delete_rectangle':
                    operations.append(['矩框置白:', '对所有文件生效'])
                elif arg == 'RGB Filter':
                    operations.append(['RGB滤波:', '对所有文件生效'])
                elif arg == 'HSV Filter':
                    operations.append(['HSV滤波:', '对所有文件生效'])
                opapppa()

            def opapppa():
                if arg == 'delete_rectangle':
                    operations.append(['\000\000(', x1, y1, ')到(', x2, y2, ')'])
                elif arg == 'RGB Filter':
                    operations.append(['\000\000', s1, s2, s3, '到', e1, e2, e3])
                elif arg == 'HSV Filter':
                    operations.append(['\000\000', s1, s2, s3, '到', e1, e2, e3])
                operationlist.set(operations)
                flashimg()

            tk.Button(askwin, text='对本文该页生效', bg='white', font=('黑体', 12), width=18, height=2,
                      command=opapppa1).place(x=120, y=40, anchor=NW)
            tk.Button(askwin, text='对该文件生效', bg='white', font=('黑体', 12), width=18, height=2,
                      command=opapppa2).place(x=120, y=110, anchor=NW)
            tk.Button(askwin, text='对全部文件生效', bg='white', font=('黑体', 12), width=18, height=2,
                      command=opapppa3).place(x=120, y=180, anchor=NW)
            askwin.mainloop()

        def updateinf(x, y):
            global tv1, tv2, tv3, infwin
            txt1 = 'x:' + str(x) + '  y:' + str(y)
            txt2 = 'r:' + str(self.cvimgaft[y, x, 2]) + ' g:' + str(self.cvimgaft[y, x, 1]) + ' b:' + str(
                self.cvimgaft[y, x, 0])
            txt3 = 'h:' + str(self.cvafthsv[y, x, 0]) + ' s:' + str(self.cvafthsv[y, x, 1]) + ' v:' + str(
                self.cvafthsv[y, x, 2])
            tv1.set(txt1)
            tv2.set(txt2)
            tv3.set(txt3)
            infwin.update()

        def showinfcv2method(event, x, y, flags, arg):
            global h
            if event == cv2.EVENT_MOUSEMOVE:
                updateinf(x, h * dx + y)
            elif event == cv2.EVENT_MOUSEWHEEL:
                if (flags < 0 and h == 100) or (flags > 0 and h == 0):
                    return
                if flags < 0 and h >= 98:
                    h = 100
                elif flags > 0 and h <= 2:
                    h = 0
                elif flags < 0:
                    h = h + 3
                else:
                    h = h - 3
                cv2.setTrackbarPos('Pos', arg, h)
                cv2.imshow(arg, self.cvimgaft[h * dx:winheight + h * dx, :, :])

        def chooserectangle(event, x, y, flags, param):
            global x1, y1, x2, y2, flag, h
            if event == cv2.EVENT_LBUTTONDOWN:
                if flag == False:
                    flag = True
                    x1 = x
                    y1 = h * dx + y
                else:
                    x2 = x
                    y2 = h * dx + y
                    cv2.destroyWindow('delete_rectangle')
                    showaskwin('delete_rectangle')

            elif event == cv2.EVENT_MOUSEMOVE:
                if flag == True:
                    img = self.cvimgaft.copy()
                    cv2.rectangle(img, (x1, y1), (x, h * dx + y), (0, 255, 0), 1)
                    cv2.imshow('delete_rectangle', img[h * dx:winheight + h * dx, :, :])
                updateinf(x, h * dx + y)
            elif event == cv2.EVENT_RBUTTONUP:
                flag = False
                cv2.imshow('delete_rectangle', self.cvimgaft[h * dx:winheight + h * dx, :, :])
            elif event == cv2.EVENT_MOUSEWHEEL:
                if (flags < 0 and h == 100) or (flags > 0 and h == 0):
                    return
                if flags < 0 and h >= 98:
                    h = 100
                elif flags > 0 and h <= 2:
                    h = 0
                elif flags < 0:
                    h = h + 3
                else:
                    h = h - 3
                cv2.setTrackbarPos('Pos', 'delete_rectangle', h)
                img = self.cvimgaft.copy()
                if flag == True:
                    cv2.rectangle(img, (x1, y1), (x, (h - 12) * dx + y), (0, 255, 0), 1)
                cv2.imshow('delete_rectangle', img[h * dx:winheight + h * dx, :, :])

        def delete_rectangle():
            self.hide()
            showpreviewwin('delete_rectangle')

        def showconsolewin(arg):
            # r-h,g-s,b-v
            global preconsole, s1, s2, s3, e1, e2, e3
            result = []
            preconsole = Toplevel()
            preconsole.title(arg + ' Console')
            preconsole.geometry('300x650+0+300')
            preconsole["background"] = 'white'
            preconsole.resizable(0, 0)  # 防止用户调整尺寸

            if arg == 'RGB Filter':
                t1 = '当起始值与结束值均为-1时代表该颜色不参与过滤'
                t2 = '红色的范围:'
                t3 = '绿色的范围:'
                t4 = '蓝色的范围:'
            elif arg == 'HSV Filter':
                t1 = '当起始值与结束值均为-1时代表该参数不参与过滤'
                t2 = '色调的范围:'
                t3 = '饱和度范围:'
                t4 = '明度的范围:'

            def completeb():
                cv2.destroyWindow(arg)
                showaskwin(arg)

            tk.Button(preconsole, text='完成', command=completeb, bg='white', font=('黑体', 13), width=12, height=2) \
                .place(x=90, y=570)
            tk.Label(preconsole, text=t1, bg='white', font=('宋体', 10)).place(x=0, y=0)
            tk.Label(preconsole, text=t2, bg='white', font=('宋体', 12)).place(x=25, y=25)
            tk.Label(preconsole, text=t3, bg='white', font=('宋体', 12)).place(x=25, y=200)
            tk.Label(preconsole, text=t4, bg='white', font=('宋体', 12)).place(x=25, y=375)
            s1 = s2 = s3 = e1 = e2 = e3 = -1
            tks1 = tk.StringVar()
            tks2 = tk.StringVar()
            tks3 = tk.StringVar()
            tke1 = tk.StringVar()
            tke2 = tk.StringVar()
            tke3 = tk.StringVar()

            def eset(arg=None):
                global s1, s2, s3, e1, e2, e3
                if arg is not None and (arg.get() == '' or arg.get() == ' ' or arg.get == '-'):
                    return

                def returnnum(str):
                    if str == '' or str == ' ':
                        return -1
                    return int(str)

                if arg is None or arg is tks1:
                    s1 = returnnum(tks1.get())
                    scale1.set(s1)
                if arg is None or arg is tke1:
                    e1 = returnnum(tke1.get())
                    scale2.set(e1)
                if arg is None or arg is tks2:
                    s2 = returnnum(tks2.get())
                    scale3.set(s2)
                if arg is None or arg is tke2:
                    e2 = returnnum(tke2.get())
                    scale4.set(e2)
                if arg is None or arg is tks3:
                    s3 = returnnum(tks3.get())
                    scale5.set(s3)
                if arg is None or arg is tke3:
                    e3 = returnnum(tke3.get())
                    scale6.set(e3)

                preconsole.update()

            entry = tk.Entry(preconsole, textvariable=tks1, bg='white', font=('宋体', 12), width=5)
            entry.place(x=25, y=70)
            entry = tk.Entry(preconsole, textvariable=tke1, bg='white', font=('宋体', 12), width=5)
            entry.place(x=25, y=115)
            entry = tk.Entry(preconsole, textvariable=tks2, bg='white', font=('宋体', 12), width=5)
            entry.place(x=25, y=245)
            entry = tk.Entry(preconsole, textvariable=tke2, bg='white', font=('宋体', 12), width=5)
            entry.place(x=25, y=290)
            entry = tk.Entry(preconsole, textvariable=tks3, bg='white', font=('宋体', 12), width=5)
            entry.place(x=25, y=420)
            entry = tk.Entry(preconsole, textvariable=tke3, bg='white', font=('宋体', 12), width=5)
            entry.place(x=25, y=465)

            def sset(event=None):
                global s1, s2, s3, e1, e2, e3
                s1 = scale1.get()
                e1 = scale2.get()
                s2 = scale3.get()
                e2 = scale4.get()
                s3 = scale5.get()
                e3 = scale6.get()
                tks1.set(str(s1))
                tks2.set(str(s2))
                tks3.set(str(s3))
                tke1.set(str(e1))
                tke2.set(str(e2))
                tke3.set(str(e3))
                preconsole.update()

            if arg == 'RGB Filter':
                scale1 = tk.Scale(preconsole, from_=-1, to=255, orient=tk.HORIZONTAL, length=190, showvalue=0,
                                  command=sset)
                scale2 = tk.Scale(preconsole, from_=-1, to=255, orient=tk.HORIZONTAL, length=190, showvalue=0,
                                  command=sset)
            elif arg == 'HSV Filter':
                scale1 = tk.Scale(preconsole, from_=-1, to=180, orient=tk.HORIZONTAL, length=190, showvalue=0,
                                  command=sset)
                scale2 = tk.Scale(preconsole, from_=-1, to=180, orient=tk.HORIZONTAL, length=190, showvalue=0,
                                  command=sset)
            scale1.place(x=85, y=70)
            scale2.place(x=85, y=115)
            scale3 = tk.Scale(preconsole, from_=-1, to=255, orient=tk.HORIZONTAL, length=190, showvalue=0, command=sset)
            scale3.place(x=85, y=245)
            scale4 = tk.Scale(preconsole, from_=-1, to=255, orient=tk.HORIZONTAL, length=190, showvalue=0, command=sset)
            scale4.place(x=85, y=290)
            scale5 = tk.Scale(preconsole, from_=-1, to=255, orient=tk.HORIZONTAL, length=190, showvalue=0, command=sset)
            scale5.place(x=85, y=420)
            scale6 = tk.Scale(preconsole, from_=-1, to=255, orient=tk.HORIZONTAL, length=190, showvalue=0, command=sset)
            scale6.place(x=85, y=465)
            if arg == 'RGB Filter':
                scale1.set(255)
                scale2.set(255)
                scale3.set(255)
                scale4.set(255)
                scale5.set(255)
                scale6.set(255)
            if arg == 'HSV Filter':
                scale1.set(-1)
                scale2.set(-1)
                scale3.set(-1)
                scale4.set(-1)
                scale5.set(255)
                scale6.set(255)
            sset()
            tks1.trace("w", lambda name, index, mode, tks1=tks1: eset(tks1))
            tke1.trace("w", lambda name, index, mode, tke1=tke1: eset(tke1))
            tks2.trace("w", lambda name, index, mode, tks2=tks2: eset(tks2))
            tke2.trace("w", lambda name, index, mode, tke2=tke2: eset(tke2))
            tks3.trace("w", lambda name, index, mode, tks3=tks3: eset(tks3))
            tke3.trace("w", lambda name, index, mode, tke3=tke3: eset(tke3))

        def showpreviewwin(arg):
            global flag, dx, h, winheight
            winheight = 950
            # _thread.start_new_thread(showinf,())
            h = 0
            dx = int((self.cvimgaft.shape[0] - winheight) / 100) + 1

            def nothing(x):
                global h
                h = x
                cv2.imshow(arg, self.cvimgaft[x * dx:winheight + x * dx, :, :])

            cv2.namedWindow(arg)
            cv2.createTrackbar('Pos', arg, 0, 100, nothing)
            cv2.imshow(arg, self.cvimgaft[0:winheight, :, :])
            cv2.moveWindow(arg, 350, 0)

            if arg == 'delete_rectangle':
                flag = False
                cv2.setMouseCallback(arg, chooserectangle)
            elif arg == 'RGB Filter' or arg == 'HSV Filter':
                showconsolewin(arg)
                cv2.setMouseCallback(arg, showinfcv2method, arg)

            showinf(arg)

        def rgb_threshold():
            self.hide()
            showpreviewwin('RGB Filter')

        def hsv_threshold():
            self.hide()
            showpreviewwin('HSV Filter')

        def flashselfimg():
            path = os.getcwd() + '\\temp\\' + file_dir[curfile] + '\\' + str(curpage - 1) + '.png'
            shutil.copyfile(path, pathcv + '\\' + str(curpage - 1) + '.png')
            self.cvimgbef = cv2.imread(pathcv + '\\' + str(curpage - 1) + '.png')
            self.cvbefhsv = cv2.cvtColor(self.cvimgbef, cv2.COLOR_BGR2HSV)
            self.cvimgaft = self.cvimgbef.copy()
            self.dooperation()
            self.cvafthsv = cv2.cvtColor(self.cvimgaft, cv2.COLOR_BGR2HSV)

        def showconfigwin():
            global alpha, belta, iscol
            iscol = True

            def setalpha(event):
                global alpha
                alpha = scale1.get()

            def setbelta(event):
                global belta
                belta = scale2.get()

            def setbw():
                global iscol
                iscol = False
                configwin.destroy()
                cv2.destroyAllWindows()
                pic2pdfmain()

            def setcol():
                global iscol
                iscol = True
                configwin.destroy()
                cv2.destroyAllWindows()
                pic2pdfmain()

            configwin = Toplevel()
            showpreviewwin('configwin')
            configwin.title('Configuration Window')
            configwin.geometry('570x380+650+250')
            configwin["background"] = 'white'
            configwin.resizable(0, 0)  # 防止用户调整尺寸
            configwin.wm_attributes("-topmost", 1)
            tk.Label(configwin, text='请尽量向右调节对比度滑块后适度调节亮度滑块，使你看到的字体最清晰', width=65, bg='white',
                     font=('宋体', 12)).place(x=15, y=15, anchor=NW)
            tk.Label(configwin, text='对比度:', bg='white', font=('黑体', 10)).place(x=10, y=75, anchor=NW)
            tk.Label(configwin, text='亮度:', bg='white', font=('黑体', 10)).place(x=20, y=160, anchor=NW)
            scale1 = tk.Scale(configwin, from_=0.5, to=1.5, orient=tk.HORIZONTAL, bg='white', length=480, showvalue=1,
                              tickinterval=3,
                              resolution=0.02, command=setalpha)
            scale1.place(x=70, y=55)
            scale1.set(alpha)
            scale2 = tk.Scale(configwin, from_=-80, to=80, orient=tk.HORIZONTAL, bg='white', length=480, showvalue=1,
                              resolution=2,
                              command=setbelta)
            scale2.place(x=70, y=140)
            scale2.set(belta)
            tk.Button(configwin, text='输出黑白PDF(文件小，速度快)', bg='white', font=('黑体', 13), width=45, height=2,
                      command=setbw).place(x=80, y=220, anchor=NW)
            tk.Button(configwin, text='输出彩色PDF(文件大，速度慢)', bg='white', font=('黑体', 13), width=45, height=2,
                      command=setcol).place(x=80, y=300, anchor=NW)
            configwin.mainloop()

        def showsuccwin():
            path = fc.getcurrpath() + '/output/'

            def opendir():
                start_directory = r'' + path
                os.startfile(start_directory)
                succwin.destroy()

            succwin = Toplevel()
            succwin.title('Operation Succeed!')
            succwin.geometry('350x200+800+300')
            succwin["background"] = 'white'
            succwin.resizable(0, 0)  # 防止用户调整尺寸
            succwin.wm_attributes("-topmost", 1)
            tk.Button(succwin, text='打开输出目录', bg='white', font=('黑体', 13), width=16, height=2, command=opendir) \
                .place(x=100, y=120, anchor=NW)
            tk.Label(succwin, text='PDF文件生成成功,输出目录为\r\n' + fc.getcurrpath() + '\r\n' + '/output/', width=39, bg='white',
                     font=('宋体', 11)).place(x=20, y=20, anchor=NW)

        def complete():
            showconfigwin()

        def pic2pdfmain():
            global curpage, curfile, aftname
            aftname = '.png'
            cf = curfile
            cp = curpage
            print('\r\n\r\n\r\n开始pdf去水印')
            sumpage = 0
            for f in file_dir:
                sumpage = sumpage + fc.getmaxpage(f) + 1
            curfile = 0
            proc = 0
            stri = '正在进行PDF去水印……'
            fc.showwaitwin(stri, proc,3)
            self.hide()
            dx = 50 / sumpage
            for file in file_dir:
                print('正在处理', file)
                pages = 0
                flag = 1
                # doc = fitz.open()
                fc.cleantemp()
                pic_list = []
                if fc.getmaxpage(file) == -1:
                    continue
                for pagefile in range(0, fc.getmaxpage(file) + 1):
                    path = os.getcwd() + '\\temp\\' + file + '\\' + str(pagefile) + '.png'
                    if not os.path.exists(path):
                        proc = proc + dx + dx
                        fc.updateproc(stri, proc, 3)
                        continue
                    pages = pages + 1
                    shutil.copyfile(path, pathcv + '\\' + str(pagefile) + '.png')
                    curpage = pagefile + 1
                    flashselfimg()
                    os.remove(pathcv + '\\' + str(pagefile) + '.png')
                    if not iscol:
                        self.cvimgaft = cv2.cvtColor(self.cvimgaft, cv2.COLOR_BGR2GRAY)
                    self.cvimgaft = ic.sharpenimg(self.cvimgaft, alpha, belta)
                    # cv2.imwrite(pathcv + '\\' + str(pagefile) + '.jpg', self.cvimgaft, [cv2.IMWRITE_JPEG_QUALITY, 80])
                    cv2.imwrite(pathcv + '\\' + str(pagefile) + '.png', self.cvimgaft, [cv2.IMWRITE_PNG_COMPRESSION, 0])
                    proc = proc + dx
                    fc.updateproc(stri, proc, 3)
                    pic_list.append(str(pagefile) + aftname)
                    if pages == 55:
                        pic2pdftemp(file, pic_list, flag)
                        fc.cleantemp()
                        pic_list = []
                        gc.collect()
                        flag = flag + 1
                        pages = 0
                    proc = proc + dx
                    fc.updateproc(stri, proc, 3)
                pic2pdf(file, pic_list, flag)
                curfile = curfile + 1
            fc.destorywin()
            showsuccwin()
            self.show()
            curfile = cf
            curpage = cp
            print('pdf去水印操作完成')

        def pic2pdftemp(file, pic_list, flag):
            print('正在生成', file, flag)
            im_list = []
            if pic_list != []:
                path = pathcv + '\\' + pic_list[0]
                im1 = Image.open(path)
                pic_list.pop(0)
                for i in pic_list:
                    img = Image.open(pathcv + '\\' + i)
                    im_list.append(img)
                im1.save(fc.getcurrpath() + '/output/' + file + str(flag) + '.pdf', "PDF", resolution=180.0,
                         save_all=True,
                         append_images=im_list)
                del im1
                im_list = []
                gc.collect()

        def pic2pdf(file, pic_list, flag):
            print('正在生成', file, flag)
            im_list = []
            if pic_list != []:
                path = pathcv + '\\' + pic_list[0]
                im1 = Image.open(path)
                pic_list.pop(0)
                for i in pic_list:
                    img = Image.open(pathcv + '\\' + i)
                    im_list.append(img)
                im1.save(fc.getcurrpath() + '/output/' + file + '.pdf', "PDF", resolution=180.0, save_all=True,
                         append_images=im_list)
                del im1
                im_list = []
                gc.collect()
            if flag > 1:
                print('正在合成', file)
                if pic_list != []:
                    if os.path.exists(fc.getcurrpath() + '/output/' + file + str(flag) + '.pdf'):
                        os.remove(fc.getcurrpath() + '/output/' + file + str(flag) + '.pdf')
                    os.rename(fc.getcurrpath() + '/output/' + file + '.pdf',
                              fc.getcurrpath() + '/output/' + file + str(flag) + '.pdf')
                    flag=flag+1

                for f in range(1, flag):
                    im_list.append(fc.getcurrpath() + '/output/' + file + str(f) + '.pdf')

                # merge the file.
                opened_file = [open(file_name, 'rb') for file_name in im_list]
                pdfFM = PyPDF2.PdfFileMerger()
                for f in opened_file:
                    pdfFM.append(f)
                # output the file.
                with open(fc.getcurrpath() + '/output/' + file + '.pdf', 'wb') as write_out_file:
                    pdfFM.write(write_out_file)
                # close all the input files.
                for f in opened_file:
                    f.close()
                for f in im_list:
                    os.remove(f)

        def noise_threshold():
            pass

        def rotation_correction():
            pass

        def back():
            pass

        dep = 62
        st = 50
        tk.Button(wmr_page, text='删除该页', bg='white', font=('黑体', 13), width=12, height=2,
                  command=delete_page).place(x=1600, y=st, anchor=NW)
        tk.Button(wmr_page, text='矩框置白', bg='white', font=('黑体', 13), width=12, height=2,
                  command=delete_rectangle).place(x=1755, y=st, anchor=NW)
        tk.Button(wmr_page, text='RGB滤波', bg='white', font=('黑体', 13), width=12, height=2,
                  command=rgb_threshold).place(x=1600, y=st + dep, anchor=NW)
        tk.Button(wmr_page, text='HSV滤波', bg='white', font=('黑体', 13), width=12, height=2,
                  command=hsv_threshold).place(x=1755, y=st + dep, anchor=NW)
        tk.Button(wmr_page, text='底噪矫正', bg='white', font=('黑体', 13), width=12, height=2,
                  command=noise_threshold).place(x=1600, y=st + 2 * dep, anchor=NW)
        tk.Button(wmr_page, text='旋转矫正', bg='white', font=('黑体', 13), width=12, height=2,
                  command=rotation_correction).place(x=1755, y=st + 2 * dep, anchor=NW)
        tk.Button(wmr_page, text='完成', bg='white', font=('黑体', 13), width=12, height=2,
                  command=complete).place(x=1600, y=st + 3.5 * dep, anchor=NW)
        tk.Button(wmr_page, text='返回', bg='white', font=('黑体', 13), width=12, height=2,
                  command=back).place(x=1755, y=st + 3.5 * dep, anchor=NW)


def start():
    wmrpage = WMR_Page()
    wmrpage.mainloop()


if __name__ == '__main__':
    start()

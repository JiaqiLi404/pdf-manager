import os
import shutil
import tkinter as tk
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor
import psutil
import fitz
from tkinter import *


def getallpdf(files):
    temp = []
    filelist = []
    if not files:
        return temp
    for f in files:
        if not os.path.exists(f):
            continue
        if os.path.isdir(f):
            temp = getallfiles(f)
        else:
            temp.append(f)
    for t in temp:
        # print(t)
        if (t.endswith('.pdf') or t.endswith('.PDF')) and filelist.count(t) == 0:
            t = t.replace('\\', '/')
            filelist.append(t)
    return filelist


def getallfiles(dir):
    list = []
    files = os.listdir(dir)
    for f in files:
        f = dir + '/' + f
        if os.path.isfile(f):
            list.append(f)
        else:
            list.extend(getallfiles(f))
    # print(list)
    return list


def getcurrpath():
    path = os.getcwd()
    path = path.replace('\\', '/')
    return path


def rebuildtemp():
    print('正在重建缓存目录')
    path = getcurrpath()
    if os.path.exists(path + '/temp'):
        shutil.rmtree(path + '/temp')
    os.mkdir(path + '/temp')
    if not os.path.exists(path + '/output'):
        os.mkdir(path + '/output')
    if os.path.exists(os.getcwd()[:os.getcwd().index(':') + 2] + 'temp'):
        shutil.rmtree(os.getcwd()[:os.getcwd().index(':') + 2] + 'temp')
    os.mkdir(gettemppath())
    print('缓存目录建立成功')


def gettemppath():
    return os.getcwd()[:os.getcwd().index(':') + 2] + 'temp'


def cleantemp():
    print('正在清理缓存')
    path = gettemppath()
    files = os.listdir(path)
    for f in files:
        os.remove(path + '\\' + f)


def getfilename(file):
    return file[file.rindex('/'):file.rindex('.')].rstrip()


def getpagelist(file):
    pages = []
    # print(os.listdir(getcurrpath()+'/temp/'+file))
    files = os.listdir(getcurrpath() + '/temp/' + file)
    if files == []:
        return -1
    for p in files:
        # print(p[:p.rindex('.')])
        pages.append(int(p[:p.rindex('.')]) + 1)
    pages.sort()
    for i in range(0, len(pages)):
        pages[i] = str(pages[i])
    # print(pages)
    return pages


def deletepage(file, page):
    os.remove(getcurrpath() + '/temp/' + file + '/' + str(page) + '.png')


def pdf_to_img(file, dp, eachproc):
    global proc
    pdfile = fitz.open(file)
    eachproc2 = eachproc / pdfile.pageCount
    imgpath = getcurrpath() + '/temp' + getfilename(file)
    i = 1
    while os.path.exists(imgpath):
        imgpath = imgpath + '(' + str(i) + ')'
        i = i + 1
    os.mkdir(imgpath)
    for idx in range(pdfile.pageCount):
        # print('正在处理: ', file, ' 第', idx, '页')
        # print("path:", imgpath)
        page = pdfile[idx]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = dp  # (2-->1584x1224)
        zoom_y = dp
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        pix.writePNG(imgpath + '/' + str(idx) + '.png')  # 将图片写入指定的文件夹内
        # print("处理完成")
        proc = proc + eachproc2
        updateproc('正在将PDF文件转换为图片……', proc, 2)


def cvt2img(files, dp):
    global w, proc
    w = tk.Tk()
    w.withdraw()
    tasks = []
    cpunum = mp.cpu_count() - 1
    memnum = int(psutil.virtual_memory().free / 1000000000) * 4
    if memnum < cpunum:
        cpunum = memnum
    # print(memnum)
    eachproc = 100 / len(files)
    # print('eachproc:',eachproc)
    proc = 0
    # _thread.start_new_thread(createwaitwin, ('正在将PDF文件转换为图片……', proc,))
    showwaitwin('正在将PDF文件转换为图片……', proc,2)
    print('\r\n\r\n开始将PDF文件转换为图片')
    for f in files:
        print("正在转换", f)
        pdf_to_img(f, dp, eachproc)
    print("PDF文件转换图片操作完成")
    destorywin()


'''
    with ThreadPoolExecutor(max_workers=cpunum) as executor:
        for f in files:
            # print('正在处理: ', f)
            result = executor.submit(pdf_to_img, f)
            tasks.append(result)
    while True:
        t = len(tasks)
        exit_flag = True
        for task in tasks:
            if not task.done():
                exit_flag = False
                t = t - 1
        if exit_flag:
            win.destroy()
            break
        else:
            print(t)
            updateproc('正在将PDF文件转换为图片……', t * eachproc)
'''


def showwaitwin(stri, proc,it):
    global win, tex, w
    win = Toplevel()
    win.title('正在操作中')
    win.geometry('480x140+750+400')
    win["background"] = 'white'
    win.resizable(0, 0)
    tex = tk.StringVar()
    w = tk.Label(win, bg='white', textvariable=tex, font=('宋体', 13))
    stri = stri + format(proc, '.' + str(it) + 'f') + '%'
    w.place(x=100, y=50, anchor=NW)
    tex.set(stri)
    win.update()


def updateproc(stri, proc, it):
    global tex
    stri = stri + format(proc, '.' + str(it) + 'f') + '%'
    tex.set(stri)
    win.update()


def destorywin():
    win.destroy()


def getmaxpage(filename):
    path = getcurrpath() + '/temp/' + filename
    files = os.listdir(path)
    if files == []:
        return -1
    max = 0
    for i in files:
        num = int(i[: i.rindex('.')])
        if num > max:
            max = num
    return max


def getminpage(filename):
    path = getcurrpath() + '/temp/' + filename
    files = os.listdir(path)
    if files == []:
        return -1
    min = getmaxpage(filename)
    for i in files:
        num = int(i[: i.rindex('.')])
        if num < min:
            min = num
    return min


def exitgram():
    w.destroy()

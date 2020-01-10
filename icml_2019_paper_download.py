#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   icml_2019.py
@Time    :   2020/01/09 17:56:48
@Author  :   Zhi-Hao Tan 
@Version :   1.0
@Contact :   tanzh.lamda@gmail.com
@License :   (C)Copyright 2020-2021, LAMDA Group, Nanjing University
@Desc    :   None
'''

# here put the import lib
import urllib
import re
import os
import nips_download


def getKernelUrl(html):
    reg = r'<p_class="title">[A-Za-z_\-\$:]*?[Kk]ernel[A-Za-z_\-\$:]*?</p>.*?\.pdf"'
    # 这个re式可以说是最全的了
    url_re = re.compile(reg)
    url_kernel_lst = url_re.findall(html)
    url_kernel_lst = list(set(url_kernel_lst))
    return url_kernel_lst


def getPdfUrlAndName(url_lst):
    # 由于icml的url不是paper的title，所以还需要单独提取一下pdfname和url
    name_lst = []
    url_kernel_lst = []
    for raw_str in url_lst:
        reg_name = r'[A-Za-z_\-\$:]*?[Kk]ernel[A-Za-z_\-\$:]*?(?=<)'
        url_re_name = re.compile(reg_name)
        name_lst.append(url_re_name.search(raw_str)[0].replace(':', '') + '.pdf')
        # 很多文章title中有冒号要去掉，不然无法保存
        reg_url = r'http://[^:]*?\.pdf'
        url_pdf = re.compile(reg_url)
        url_kernel_lst.append(url_pdf.search(raw_str)[0])
    return [name_lst, url_kernel_lst]


def getICMLFile(url, file_name):
    try:
        u = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        print(url, "url file not found")
        return

    block_sz = 8192
    with open(file_name, 'wb') as f:
        while True:
            buffer = u.read(block_sz)
            if buffer:
                f.write(buffer)
            else:
                break

    print("Successful to download " + file_name, flush = True) # 强制刷新流，及时打印结果


if __name__ == "__main__":
    raw_url = "http://proceedings.mlr.press/v97/"

    html = nips_download.getHtml(raw_url) # 可以直接调用nips_download中的函数
    # nips_download.writeHtml('icml_2019.html', html)
    # html = nips_download.readHtml('icml_2019.html')
    html = html.replace('\n', '')
    html = html.replace('\r', '')
    html = html.replace('\t', '')
    html = html.replace(' ', '_')

    # nips_download.writeHtml('icml_2019_1.html', html)

    # html = nips_download.readHtml('icml_2019_1.html')

    url_kernel_lst = getKernelUrl(html)
    # print(len(url_kernel_lst))

    for url in url_kernel_lst[:]:
        print(url)

    [name_lst, url_kernel_lst] = getPdfUrlAndName(url_kernel_lst)
    # print(len(url_kernel_lst))

    # for url in url_kernel_lst[:]:
    #   print(url)
    # print(len(name_lst))
    for name in name_lst:
        print(name)

    if not os.path.exists('pdf_download'):
        # 文件夹不存在时，再进行创建
        os.mkdir('pdf_download')
    os.chdir(os.path.join(os.getcwd(), 'pdf_download'))

    for i in range(len(url_kernel_lst)):
        getICMLFile(url_kernel_lst[i], name_lst[i])

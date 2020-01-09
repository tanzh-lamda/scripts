#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   nips_download.py
@Time    :   2020/01/08 16:49:00
@Author  :   Zhi-Hao Tan 
@Version :   1.0
@Contact :   tanzh.lamda@gmail.com
@License :   (C)Copyright 2020-2021, LAMDA Group, Nanjing University
'''

import urllib.request  
import re  
import os


def getHtml(url):
            page = urllib.request.urlopen(url)
    html = page.read().decode()      page.close()      return html


def getKernelUrl(html):
        reg = r'/\d.*?-kernels?.*?(?=")'
                        url_re = re.compile(reg)
    url_kernel_lst = url_re.findall(html)
    url_kernel_lst = list(set(url_kernel_lst))

        for i in range(len(url_kernel_lst)):
        url_kernel_lst[i] = 'https://papers.nips.cc/paper' + url_kernel_lst[i] + '.pdf'
    return url_kernel_lst


def writeHtml(filename, html):
        with open(filename, 'w', encoding='utf-8') as writer:
                writer.write(html)


def getFile(url):
    file_name=url.split('/')[-1]

    try:
        u=urllib.request.urlopen(url)
    except urllib.error.HTTPError:
                print(url, "url file not found")
        return

    block_sz=8192
    with open(file_name,'wb') as f:
        while True:
            buffer= u.read(block_sz)
            if buffer:
                f.write(buffer)
            else:
                break

    print("Successful to download " + file_name)


def readHtml(filename):
        with open(filename, 'r', encoding='utf-8') as reader:
        html = reader.read()
    return html


def writeListToTxt(filename, list_):
        with open(filename, 'w', encoding='utf-8') as writer:
        for line in list_:
            writer.write(line + '\n')


if __name__ == "__main__":
    raw_url = "https://papers.nips.cc/book/advances-in-neural-information-processing-systems-32-2019"
    html = getHtml(raw_url)
    
    writeHtml('nips.html',html)
    # html = readHtml('nips.html')

    url_kernel_list = getKernelUrl(html)

    writeListToTxt('url_list.txt',url_kernel_list)

    if not os.path.exists('pdf_download'):
                os.mkdir('pdf_download')
    os.chdir(os.path.join(os.getcwd(),'pdf_download'))

    for url in url_kernel_list[:]:
        print(url)
        getFile(url)
        
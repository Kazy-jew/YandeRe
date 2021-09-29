# 图片id列表的生成和管理
# multi_pages：根据输入的日期区间生成该区间内的图片列表文件.txt
# remove_deleted & rewrite 更斯图片列表文件(去除已被从yande.re上删除的图片id)
import requests
import os
import urllib
from lxml import html
from colorama import Fore, Style
from termcolor import colored, cprint
import dategen

curt_year = dategen.read_year()


def multi_pages(date):
    # 生成原始id列表(多文件)和合并原始列表后的初始列表(单文件)，返回输入的日期
    download_folder = 'current_dl'
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      'Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277'}
    proxy_url = {'http': 'socks5://127.0.0.1:7890'}
    multi_date_list = []
    for n in date:
        id_list = []
        # 已经下载完成的列表不重复下载
        if os.path.exists('./current_dl/{}-{}.txt'.format(curt_year, n)):
            with open('./current_dl/{}-{}.txt'.format(curt_year, n)) as p:
                multi_date_list += p.read().splitlines()
            print('{}-{}...already exists'.format(curt_year, n))
        else:
            for i in range(1, 38):
                url = 'https://yande.re/post?page={}&tags=date%3A{}-{}'.format(i, curt_year, n)
                page_ = requests.get(url, headers=headers, proxies=proxy_url)
                tree = html.fromstring(page_.content)
                mark_tag = tree.xpath('//*[@id="post-list"]/div[2]/div[4]/p/text()')
                if not mark_tag:
                    id_list += tree.xpath('//*[@id="post-list-posts"]/li/@id')
                elif mark_tag == ['Nobody here but us chickens!']:
                    id_list = [w.replace('p', '') for w in id_list]
                    break
            multi_date_list += id_list
            with open(os.path.join(download_folder, '{}.txt'.format(url.split('%3A')[-1])), 'w') as f:
                for item in id_list:
                    f.write('{}\n'.format(item))
            print('{}...done'.format(url.split('%3A')[-1]))
    with open(os.path.join(download_folder, '{}_{}.txt'.format(date[0], date[-1])), 'w') as fa:
        for item in multi_date_list:
            fa.write('{}\n'.format(item))
    return date


def remove_deleted(img_id):
    # 确定图片未下载成功的原因：若源已经不存在则输出删除的信息，否则为本地原因
    id_to_remove = []
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/73.0.3683.103 Safari/537.36'}
    proxy_url = None #{'http': 'http://127.0.0.1:7890'}
    for _ in img_id:
        url = 'https://yande.re/post/show/{}'.format(_)
        page = requests.get(url, headers=headers, proxies=proxy_url)
        tree = html.fromstring(page.content)
        deleted_info = tree.xpath('//*[@id="post-view"]/div[1]/text()')
        image_info = tree.xpath('//*[@id="image"]')
        if image_info:
            print(Fore.RED + 'Warning !\n',
                  Fore.BLUE + 'Image {} still exists \
                  but failed to be downloaded too many times, '.format(colored(_, 'green')),
                  Fore.BLUE + 'please check manually')
            print(Style.RESET_ALL)
        else:
            print('{}:'.format(_), deleted_info[0])
            # 原post已经删除，需要从列表中去除
            id_to_remove.append(_)
    if len(img_id) == len(id_to_remove):
        # 所有的图片网站上原post已经删除
        return True
    else:
        # 存在未下载成功的图片，返回该图片id列表
        return list(set(img_id)-set(id_to_remove))


def rewrite(date, new_list):
    # 更新初始列表文件，将源已删除的图片id去除
    with open('./current_dl/{}_{}.txt'.format(date[0], date[-1]), 'w') as rw:
        for _ in new_list:
            rw.write('{}\n'.format(_))
    print('List updated')
    return

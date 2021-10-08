# main program of yande.re downloader
# MMP 我对yande.re的更新失望了, 几天前的日期几乎要更新几次...update每月一更好了...

import dategen
import download
import idlist
import move
import readid
import update
from importlib import reload


def downloader(date, original_id, id_list, eigenvalue):
    # original_id: 初始id列表
    # id_list: 当前列表(需要下载的列表)
    # eigenvalue的值(1 or 2)用来区别1:初次下载时/ 2: update时, 下载完成后文件夹的创建和文件的移动
    original_list = original_id
    count_num = 0
    fin = True
    while id_list:
        download.download_core(id_list)
        readid.check_dl(date)
        id_list = readid.remain_id()
        count_num += 1
        print('Retry times left:', 4 - count_num)
        if count_num == 4:
            fin = idlist.remove_deleted(id_list)   # id_list为未下载的图片id
            break
    if fin is True:
        print('All images downloaded successfully')
        renewed_list = list(set(original_list) - set(id_list))
        idlist.rewrite(date, renewed_list)
        if eigenvalue == 1:
            move.move(date)
        else:
            move.u_move(date)
        update.flush_update(date)
    else:
        print('Please check the info above')
        tsuzuku = input("Do you want to proceed category with broken dl? s to proceed any else to quit:")
        if tsuzuku == 's':
            if eigenvalue == 1:
                move.move(date)
            else:
                move.u_move(date)
            update.flush_update(date)
        else:
            return


class Options:


    @staticmethod
    def many_dates():
        date = dategen.input_date()
        idlist.multi_pages(date)
        original_id = readid.get_id(date)
        id_list = original_id
        eigenvalue = 1
        # fin = True
        sgl = input('Enter s to start or q to quit: \n(If encountered disk space issue and reselected date range,'
                    'enter q to quit and select "download remaining")')
        if sgl == 's':
            downloader(date, original_id, id_list, eigenvalue)
            # count_num = 0
            # while id_list:
            #     download.download_core(id_list)
            #     readid.check_dl(date)
            #     id_list = readid.remain_id()
            #     count_num += 1
            #     print('Retry times left:', 3-count_num)
            #     if count_num == 3:
            #         fin = idlist.remove_deleted(id_list)
            #         break
            # if fin is True:
            #     print('All images downloaded successfully')
            #     renewed_list = list(set(original_list) - set(id_list))
            #     # print(len(renewed_list), len(original_id), get_remain_id)
            #     idlist.rewrite(date, renewed_list)
            #     move.move(date)
            #     update.flush_update(date)
            # else:
            #     print('Please check the info above')
        elif sgl == 'q':
            print('download aborted')
            return
        else:
            print('invalid input !')

    @staticmethod
    def check_fail():
        eigenvalue = 1
        with open('./current_dl/dl_date.txt', 'r') as r:
            date = r.read().splitlines()
        original_id = readid.check_dl(date)
        get_remain_id = readid.remain_id()
        downloader(date, original_id, get_remain_id, eigenvalue)

    @staticmethod
    def update_check():
        eigenvalue = 2
        date = dategen.input_date()
        idlist.multi_pages(date)
        original_id = update.update(date)
        get_update_id = readid.get_id(date)
        downloader(date, original_id, get_update_id, eigenvalue)

    @staticmethod
    def update_check_fail():
        eigenvalue = 2
        with open('./current_dl/dl_date.txt', 'r') as r:
            date = r.read().splitlines()
        original_id = readid.check_dl(date)
        get_remain_id = readid.remain_id()
        downloader(date, original_id, get_remain_id, eigenvalue)


print('  Welcome to Yande.re Downloader !  ')
print('------------------------------------------')
print('|****************************************|')
print('|*** 1.download  2.download remaining ***|')
print('|*** 3.update    4.update remaining *****|')
print('|*** 5.set year  6.exit               ***|')
print('|****************************************|')
print('------------------------------------------')
while True:
    choice = input('select option: ')
    if choice == '1':
        Options.many_dates()
    elif choice == '2':
        Options.check_fail()
    elif choice == '3':
        Options.update_check()
    elif choice == '4':
        Options.update_check_fail()
    elif choice == '5':
        set_year = input('please enter za year:')
        with open('./current_dl/current_year.txt', 'w') as f:
            f.write('{}'.format(set_year))
        reload(dategen)
        reload(idlist)
        reload(move)
        reload(readid)
        reload(update)
    elif choice == '6':
        exit()
    else:
        print('invalid input !')

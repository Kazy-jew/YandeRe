# 归档
import os
import shutil
import dategen

curt_year = dategen.read_year()


def move(date):
    path = 'C:\\Users\\tokisaki\\Downloads\\'
    list1 = os.listdir(path)
    list2 = []
    for i in list1:
        if i.startswith('yande.re') and (not i.endswith('crdownload')):
            list2.append(i)
    for m in date:
        with open('./current_dl/{}-{}.txt'.format(curt_year, m)) as r:
            pairli = r.read().splitlines()
        folder = m.replace('-', '.')
        if not os.path.exists(os.path.join(path, folder)):
            os.makedirs(os.path.join(path, folder))
        for item in list2:
            name_id = item.split(' ')[1]
            if name_id in pairli:
                shutil.move(os.path.join(path, item), os.path.join(path, folder))
    return


def u_move(date):
    path = 'C:\\Users\\tokisaki\\Downloads\\'
    list1 = os.listdir(path)
    list2 = []
    for i in list1:
        if i.startswith('yande.re') and (not i.endswith('crdownload')):
            list2.append(i)
    folder = 'update_{}-{}'.format(date[0].replace('-', ''), date[-1].replace('-', ''))
    if not os.path.exists(os.path.join(path, folder)):
        os.makedirs(os.path.join(path, folder))
    with open('./current_dl/{}_{}.txt'.format(date[0], date[-1])) as r:
        pairli = r.read().splitlines()
    for item in list2:
        name_id = item.split(' ')[1]
        if name_id in pairli:
            shutil.move(os.path.join(path, item), os.path.join(path, folder))
    return


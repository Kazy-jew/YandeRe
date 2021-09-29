# read id, update id, remain id
import os
import dategen

curt_year = dategen.read_year()


def get_id(date):
    id_list = []
    # get_id是为了覆盖datelist里原有的初始id列表，原因是磁盘空间有限时，为了后续文件的归档合并，重新选择一部分日期下载
    if date:
        with open('./current_dl/dl_date.txt', 'w') as dl:
            for _ in date:
                dl.write('{}\n'.format(_))
        with open('./current_dl/{}_{}.txt'.format(date[0], date[-1])) as f1:
            id_list += f1.read().splitlines()
    else:
        print('No date file!')
    return id_list


def raw_id(o_date):
    # raw_id为直接从原始id列表合并的初始列表
    raw_list = []
    with open('./current_dl/{}_{}.txt'.format(o_date[0], o_date[-1])) as k:
        raw_list += k.read().splitlines()
    return raw_list


def remain_id():
    # 未下载的id列表
    remain_list = []
    with open('./current_dl/remain_dl.txt') as r:
        remain_list += r.read().splitlines()
    return remain_list


def update_id(date):
    update_list = []
    for _ in date:
        list_update = os.listdir('./updated_list')
        # 2021年更改点
        if 'img_list_{}-{}.txt'.format(curt_year, _) in list_update:
            with open('./updated_list/img_list_{}-{}.txt'.format(curt_year, _)) as r:
                update_list += r.read().splitlines()
    if len(update_list) > 0:
        print('update start...')
    return update_list


def rewrite_id(date, new_list):
    # 更新初始列表文件，将源已删除的图片id去除
    with open('./current_dl/{}_{}.txt'.format(date[0], date[-1]), 'w') as rw:
        for _ in new_list:
            rw.write('{}\n'.format(_))
    print('List renewed')
    return


def check_dl(d_date):     # list3：初始id列表，list2: 已下载的id列表，返回初始列表
    path = 'C:\\Users\\tokisaki\\Downloads'
    list1 = os.listdir(path)
    list2 = []
    list3 = []
    for name in list1:
        if name.startswith('yande.re') and (not name.endswith('crdownload')):
            new_id = name.split(' ')[1]
            list2.append(new_id)
    with open('./current_dl/{}_{}.txt'.format(d_date[0], d_date[-1])) as k:
        list3 += k.read().splitlines()
    diff = list(set(list3) - set(list2))
    if len(diff) <= 10:
        print('remain to be downloaded', diff)
    else:
        print('{} items remain'.format(len(diff)))
    if diff:
        with open('./current_dl/remain_dl.txt', 'w') as m:
            for _ in diff:
                m.write('{}\n'.format(_))
    else:
        with open('./current_dl/remain_dl.txt', 'w') as m:
            for _ in diff:
                m.write('{}\n'.format(_))
        print('No images to download')
    return list3

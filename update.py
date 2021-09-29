# 更新有关
import re
import os
import dategen

curt_year = dategen.read_year()


def update(date):
    all_list = []
    for i in date:
        with open('./current_dl/{}-{}.txt'.format(curt_year, i)) as p:
            li1 = p.read().splitlines()
        # 2021年更改点
        with open('./namelist_date/nl_{}-{}.txt'.format(curt_year, i)) as q:
            li2 = q.read().splitlines()
        updated_img = list(set(li1) - set(li2))
        all_list += updated_img
        if updated_img:
            # 2021年更改点
            with open('./updated_list/img_list_{}-{}.txt'.format(curt_year, i), 'w') as r:
                for _ in updated_img:
                    r.write('{}\n'.format(_))
        else:
            print('date {} no image updated'.format(i))
    with open('./current_dl/{}_{}.txt'.format(date[0], date[-1]), 'w') as f:
        for _ in all_list:
            f.write('{}\n'.format(_))
    return all_list


def flush_update(date):
    for _ in date:
        # 2021更改点
        os.replace('./current_dl/{}-{}.txt'.format(curt_year, _), './namelist_date/nl_{}-{}.txt'.format(curt_year, _))
        # os.replace('./current_dl/{}-{}.txt'.format(curt_year, _), './namelist_date/nl_{}.txt'.format(_))
    return


def flush_all():
    list1 = os.listdir('./current_dl')
    list2 = []
    for i in list1:
        if i.startswith('{}'.format(curt_year)):
            list2.append(i)
    for j in list2:
        date = re.sub(r'\.txt$', '', '{}-{}'.format(j.split('-')[-2], j.split('-')[-1]))
        with open('./current_dl/{}'.format(j)) as r:
            list3 = r.read().splitlines()
        # 2021更改点
        with open('./namelist_date/nl_{}-{}.txt'.format(curt_year, date), 'w') as f:
            for _ in list3:
                f.write('{}\n'.format(_))
    return


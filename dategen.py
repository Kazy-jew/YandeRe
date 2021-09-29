# generate period needed
# 生成所需要的日期区间
from datetime import date, timedelta


# 设定年份
def read_year():
    with open('./current_dl/current_year.txt', 'r') as f:
        yr = f.read()
    return yr


curt_year = read_year()


def date_list(start_date, end_date):
    delta = end_date - start_date
    date_lis = []
    for i in range(delta.days + 1):
        date_lis.append(str(start_date + timedelta(days=i)))
    date_year = [w.replace('{}-'.format(curt_year), '') for w in date_lis]
    with open('./current_dl/dl_date.txt', 'w') as f:
        for _ in date_lis:
            f.write('{}\n'.format(_))
    return date_year


def input_date():
    d = [x for x in input('please input a date range(month, date, month, date): ').split()]
    date_m = date_list(date(int(curt_year), int('{:>2}'.format(d[0])), int('{:>2}'.format(d[1]))),
                      date(int(curt_year), int('{:>2}'.format(d[2])), int('{:>2}'.format(d[3]))))
    print(date_m)
    return date_m


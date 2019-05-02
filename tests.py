import datetime

date_1 = datetime.datetime.strptime('2020-09-20', '%Y-%m-%d').date()
date_2 = datetime.datetime.strptime('2020-05-20', '%Y-%m-%d').date()

print(date_1)
print(date_1 > date_2)

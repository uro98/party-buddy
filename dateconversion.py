import datetime


def end_time(date, time):
    try:
        datetime_object = datetime.datetime.strptime(date + " " + time, '%Y-%m-%d %H')
    except ValueError:
        datetime_object = datetime.datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M')

    return datetime_object + datetime.timedelta (hours = 5)


if __name__=='__main__':
    print(end_time("2018-04-18", "20"))
    print(end_time("2018-04-18", "20:30"))

import datetime


def start_time(date, time):
    try:
        return datetime.datetime.strptime(date + " " + time, '%Y-%m-%d %H')
    except ValueError:
        return datetime.datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M')

def end_time(date, time):
    try:
        datetime_object = datetime.datetime.strptime(date + " " + time, '%Y-%m-%d %H')
    except ValueError:
        datetime_object = datetime.datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M')

    EndDate = datetime_object + datetime.timedelta(hours = 5)
    return EndDate


if __name__=='__main__':
    print(end_time("2018-04-18", "20"))
    print(end_time("2018-04-18", "20:30"))

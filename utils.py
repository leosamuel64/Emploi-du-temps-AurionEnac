import datetime


def get_current_info():
    year, week_num, day_of_week = datetime.date.today().isocalendar()
    return week_num, year

def getUTCDayWWeekNumber(week, year):
    a = datetime.datetime.utcnow()
    b = datetime.datetime.now()
    return datetime.datetime.strptime(f'{year}-{week}-1-UTC', "%Y-%W-%w-%Z") - (a-b)

def getWeekPlus1(day):
    #Not 7 day, only 6 (aurion load ics for 6 days)
    return day + datetime.timedelta(days=6)

def getWeekNumPlus1(week, year):
    monday = getUTCDayWWeekNumber(week, year)
    year, week_num, day_of_week = (monday + datetime.timedelta(days=7)).isocalendar()
    return week_num, year

def build_week(number, avoid):
    current_info = get_current_info()
    current_week = current_info[0] - 1

    if current_week == 0:
        current_week = 1

    return_list = []
    current_year = current_info[1]
    n = 0
    while n < number:
        if current_week not in avoid:
            n += 1
            week = [current_week, current_year]
            return_list.append(week)  
        current_week, current_year = getWeekNumPlus1(current_week, current_year)

    return return_list
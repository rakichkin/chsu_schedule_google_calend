import datetime
from bs4 import BeautifulSoup
from ScheduleSubject import ScheduleSubject

DATE_FORMAT = '%d.%m.%Y %H:%M'


def parse_chsu_page():
    with open("schedule_html.txt") as file:
        text = file.read()

    soup = BeautifulSoup(text, 'html.parser')
    days = soup.find_all(attrs={'class': 'raspisane_week_day_block'})

    schedule_subjects = list()
    for day in days:
        title_text = day.find(attrs={'class': 'raspisane_week_day_title'}).text
        date_str = title_text[title_text.find('/') + 2:]
        table_rows = day.find('table').find('tbody').find_all('tr')
        for row in table_rows:
            cols = row.find_all('td')

            subj_name = cols[1].text

            time_range_str = str(cols[0].text)
            start_time_str = time_range_str[0:time_range_str.find('-')]
            end_time_str = time_range_str[time_range_str.find('-')+1:]

            start_datetime_str = date_str + ' ' + start_time_str
            end_datetime_str = date_str + ' ' + end_time_str

            subj = ScheduleSubject(
                subj_name,
                datetime.datetime.strptime(start_datetime_str, DATE_FORMAT),
                datetime.datetime.strptime(end_datetime_str, DATE_FORMAT)
            )
            schedule_subjects.append(subj)

    return schedule_subjects

import datetime


class ScheduleSubject:
    def __init__(self, subject_name: str, start_time: datetime.datetime, end_time: datetime.datetime):
        self.subject_name = subject_name
        self.start_time = start_time
        self.end_time = end_time

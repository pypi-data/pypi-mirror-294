class Crontab:
    def __init__(
        self,
        minute: str = '*',
        hour: str = '*',
        day_of_week: str = '*',
        day_of_month: str = '*',
        month_of_year: str = '*',
    ) -> None:
        self.minute = minute
        self.hour = hour
        self.day_of_week = day_of_week
        self.day_of_month = day_of_month
        self.month_of_year = month_of_year

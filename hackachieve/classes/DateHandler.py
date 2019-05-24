from datetime import datetime


class DateHandler:

    def get_date_difference(date1, date2, type):
        date1_combined = None
        date2_combined = None

        if type is 'days':
            date1_combined = datetime.combine(date1, datetime.min.time())
            date2_combined = datetime.combine(date2, datetime.min.time())

        return (date1_combined - date2_combined).days

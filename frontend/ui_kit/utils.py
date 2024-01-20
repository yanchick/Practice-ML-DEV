from datetime import datetime

import pytz


# Default timezone is 'Europe/Moscow'
def format_timestamp(timestamp_str, timezone='Europe/Moscow'):
    utc_time = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S')
    utc_time = utc_time.replace(tzinfo=pytz.UTC)
    local_time = utc_time.astimezone(pytz.timezone(timezone))
    return local_time.strftime('%B %d, %Y, %H:%M')

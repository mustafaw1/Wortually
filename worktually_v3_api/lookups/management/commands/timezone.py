from pytz import timezone
from datetime import datetime

import pytz

# Time format
time_format = "%d-%b-%Y %H:%M:%S"


# Get the current time in the user's timezone
def print_time_in_user_timezone(user_timezone):
    now_utc = datetime.now(timezone("UTC"))
    user_time = now_utc.astimezone(timezone(user_timezone))
    print(user_time.strftime(time_format))
    print("the supported timezones by the pytz module:", pytz.all_timezones, "\n")


# Example usage
user_timezone = "Asia/kolkata"  # Replace with the user's timezone
print_time_in_user_timezone(user_timezone)

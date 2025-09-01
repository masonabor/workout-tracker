from datetime import datetime, timedelta

rest_time_form = datetime.strptime('00:01:30', '%H:%M:%S')
rest_time = timedelta(minutes=rest_time_form.minute, seconds=rest_time_form.second)

print(rest_time)
print(type(rest_time))
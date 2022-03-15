import datetime, time

def get_uptime():
    delta = datetime.datetime.utcnow() - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    uptime = ("{} days, {:0=2}:{:0=2}:{:0=2}".format(days, hours, minutes, seconds))
    return uptime
from datetime import datetime, timedelta

today = datetime.today()
five_d_ago = today - timedelta(days=5)

print("Today's date:", today.strftime('%Y-%m-%d'))
print("5 days ago from today's date:", five_d_ago.strftime('%Y-%m-%d'))


import time
import datetime

print(time.localtime())

#newDate = datetime.date(2000,1,1)
#print(newDate)

# todayDate = datetime(2000,1,1)
# print(todayDate)

futuredate = datetime.now() + timedelta(days=10)
print(futuredate)
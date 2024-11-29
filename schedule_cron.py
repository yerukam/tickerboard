from crontab import CronTab
my_cron = CronTab(user='pvalluri09')

# job = my_cron.new(command='/Users/pvalluri09/Desktop/pvalluri09/Work/college/packages/intraday-stock/venv/bin/python /Users/pvalluri09/Desktop/pvalluri09/Work/college/packages/intraday-stock/main.py > /tmp/logs.log 2 > /tmp/err.log')
job = my_cron.new(command='/Users/pvalluri09/Desktop/pvalluri09/Work/college/packages/intraday-stock/venv/bin/python /Users/pvalluri09/Desktop/pvalluri09/Work/college/packages/intraday-stock/test.py > /tmp/logs.log')
# job = my_cron.new(command='echo "Hello world" > /tmp/hello.log')
job.minute.every(1)
my_cron.write()
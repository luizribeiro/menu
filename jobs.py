from apscheduler.scheduler.blocking import BlockingScheduler

scheduler = BlockingScheduler()


@scheduler.scheduled_job("interval", minutes=3)
def timed_job() -> None:
    print("This job runs every three minutes")


scheduler.start()

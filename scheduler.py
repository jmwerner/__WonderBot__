
from wonderbot import main

if __name__ == '__main__':

    from apscheduler.schedulers.blocking import BlockingScheduler
    sched = BlockingScheduler()

    sched.add_job(main, 'interval', id='wonderbot', seconds=60)

    sched.start()

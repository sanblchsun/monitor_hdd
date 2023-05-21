from mail import send_mail
import psutil
from config import config
import time


def step_send_mail():
    step_mail = 0
    while True:
        hdd = psutil.disk_usage('/')
        hdd_free = hdd.free
        if step_mail == 0 or step_mail >= 3600 * 5:
            step_mail = 1
            try:
                send_mail.send_email_with_attachment(Reply_To_e_mail=config.Reply_To_e_mail,
                                                   firma=config.firma,
                                                   full_name=config.full_name,
                                                   priority=config.priority,
                                                   description=f"{config.description}: {round(config.min_free_memory/10737418240,9)} Гбайт,"
                                                               f" сейчас: {round(hdd_free/10737418240,9)} Гбайт")
            except Exception as e:
                pass
        if hdd_free > config.min_free_memory:
            return
        time.sleep(60)
        step_mail += 1
        print("step_send_mail")


def monitor_hdd():
    while True:
        hdd = psutil.disk_usage('/')
        hdd_free = hdd.free
        if hdd_free < config.min_free_memory:
            break
        time.sleep(60)


if __name__ == '__main__':
    while True:
        monitor_hdd()
        step_send_mail()



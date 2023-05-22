from mail import send_mail
import psutil
from config import config
import time
import logging
import logging.handlers

rfh = logging.handlers.RotatingFileHandler(filename='log.log',
                                           mode='a',
                                           maxBytes=5*1024,
                                           backupCount=2,
                                           encoding=None,
                                           delay=False)

logging.basicConfig(
                    level=logging.INFO,
                    format="%(asctime)s %(message)s",
                    datefmt="%y-%m-%d %H:%M:%S",
                    handlers=[
                        rfh
                    ])

logger = logging.getLogger('app')

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
                logging.info("Было отправлено сообщение")
            except Exception as e:
                logging.info(f"Ошибка почтовой службы; {e}")
        if hdd_free > config.min_free_memory:
            return
        time.sleep(60)
        logging.info(f"\n    {hdd_free} (текущее)\n"
                     f"    {config.min_free_memory} (пороговое)  КРИТИЧНО")
        step_mail += 1
        print("step_send_mail")


def monitor_hdd():
    while True:
        hdd = psutil.disk_usage('/')
        hdd_free = hdd.free
        if hdd_free < config.min_free_memory:
            logging.info(f"\n    {hdd_free} (текущее)\n"
                         f"    {config.min_free_memory} (пороговое)  КРИТИЧНО")
            break
        time.sleep(60)
        logging.info(f"\n    {hdd_free} (текущее)\n"
                     f"    {config.min_free_memory} (пороговое)")



if __name__ == '__main__':
    while True:
        monitor_hdd()
        step_send_mail()



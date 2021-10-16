from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler

import config
import constants
from app import get_menu
from utils import Email, send_email

scheduler = BlockingScheduler()


def _email_next_week_menu(recipient: str) -> None:
    date = datetime.now(config.get_timezone()) + timedelta(weeks=+1)
    lunch_menu, dinner_menu = get_menu(date)

    html_content = "<ul>"
    text_content = ""
    for i, day in enumerate(constants.DAYS):
        text_content += f"# {day}\n"
        text_content += f"* **Lunch:** {lunch_menu[i]}\n"
        text_content += f"* **Dinner:** {dinner_menu[i]}\n\n"

        html_content += f"<li><b>{day}</b></li>"
        html_content += "<ul>"
        html_content += f"<li><b>Lunch:</b> {lunch_menu[i]}</li>"
        html_content += f"<li><b>Dinner:</b> {dinner_menu[i]}</li>"
        html_content += "</ul>"
    html_content += "</ul>"

    send_email(
        Email(
            sender="Rosie <rosie@thepromisedlan.club>",
            recipients=[r for r in config.get_recipients() if recipient in r],
            subject="Next week menu",
            body=text_content,
            html=html_content,
        )
    )


@scheduler.scheduled_job("cron", day_of_week="fri", hour=5)
def email_next_week_menu_to_luiz() -> None:
    _email_next_week_menu("luiz")


@scheduler.scheduled_job("cron", day_of_week="mon", hour=5)
def email_next_week_menu_to_karin() -> None:
    _email_next_week_menu("karin")


scheduler.start()

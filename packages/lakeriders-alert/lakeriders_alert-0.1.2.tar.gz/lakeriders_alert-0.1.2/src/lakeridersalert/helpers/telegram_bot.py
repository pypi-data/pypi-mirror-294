from datetime import datetime

import requests


def sort_and_format_slots(slots, now=None):
    """
    Sort slots dictionary ({ datetime: count }) by weekday and time.
    Format them as [number_of_weeks_ahead, weekday, time, count]
    """
    sorted_datetimes = sorted(
        [(datetime.fromisoformat(dt), count) for dt, count in slots.items()],
        key=lambda x: x[0].timestamp(),
    )
    current_week = int((now if now is not None else datetime.now()).strftime("%W"))

    return [
        [int(dt.strftime("%W")) - current_week, dt.strftime("%A"), dt.hour, count]
        for dt, count in sorted_datetimes
    ]


def _format_n_slots_text(n):
    if n == 1:
        return "1 slot"
    else:
        return f"{n} slots"


def _format_week_text(n):
    if n == 0:
        return "this week"
    elif n == 1:
        return "next week"
    else:
        return f"in {n} weeks"


def notify_to_telegram(available_slots, token, chat_id):
    text = "*** NEW SLOTS AVAILABLE! ***"

    # Format slot info as [weekday, time, count]. Sort slots by weekday and time

    formatted_slots = sort_and_format_slots(available_slots)

    for [plus_week, day, time, count] in formatted_slots:
        text += f"\n{_format_n_slots_text(count)} available at {time} on {day} {_format_week_text(plus_week)}"

    response = requests.post(
        url=f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id": chat_id, "text": text},
    )

    if response.status_code == 404:
        raise Exception("Wrong bot token or chat ID")

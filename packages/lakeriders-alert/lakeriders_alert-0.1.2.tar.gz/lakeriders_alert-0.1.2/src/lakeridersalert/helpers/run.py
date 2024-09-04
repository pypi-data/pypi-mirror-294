from datetime import datetime
from time import sleep
from zoneinfo import ZoneInfo

from ..constants import POLLING_INTERVAL, RUN_WITH_LOGS
from ..helpers.web import (
    create_browser_session,
    get_reservations_html,
    InvalidCredentialsError,
)
from ..helpers.calendar_entries import (
    extract_calendar_entries,
    find_available_slots,
    write_calendar_entries_to_db,
)
from ..helpers.telegram_bot import notify_to_telegram


def run_once(email, password, token, chat_id, session=None, retries=0):
    if retries > 0:
        if RUN_WITH_LOGS:
            print(f"Sleep {2**retries} seconds before retrying")
        sleep(2**retries)
    browser_session = create_browser_session() if session is None else session
    try:
        html = get_reservations_html(
            session=browser_session, email=email, password=password
        )
    # TODO: Narrow down error class
    except Exception as e:
        if isinstance(e, InvalidCredentialsError):
            raise e
        # Crete new browser session when retrying to avoid any other type of error (like RemoteDisconnected errors)
        return run_once(
            email=email,
            password=password,
            token=token,
            chat_id=chat_id,
            session=None,
            retries=retries + 1,
        )

    calendar_entries = extract_calendar_entries(html)
    slots = find_available_slots(calendar_entries)
    if slots is not None:
        notify_to_telegram(available_slots=slots, token=token, chat_id=chat_id)
    write_calendar_entries_to_db(calendar_entries)

    return browser_session


# Polling should be run only between 7am and midnight
def run_once_conditionally(email, password, token, chat_id, session=None):
    now = datetime.now(ZoneInfo("Europe/Zurich"))
    if now.hour >= 7:
        return run_once(
            email=email,
            password=password,
            token=token,
            chat_id=chat_id,
            session=session,
        )
    else:
        return session


def run_in_loop(email, password, token, chat_id):
    browser_session = run_once_conditionally(
        email=email, password=password, token=token, chat_id=chat_id
    )
    sleep(POLLING_INTERVAL)
    while True:
        run_once_conditionally(
            session=browser_session,
            email=email,
            password=password,
            token=token,
            chat_id=chat_id,
        )
        sleep(POLLING_INTERVAL)

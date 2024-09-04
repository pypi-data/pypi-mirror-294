import sqlite3
import re

from ..constants import CANCELLED, FREE, EMPTY, DB_NAME, RUN_WITH_LOGS


def extract_calendar_entries(html):
    # Extract events from the HTML response
    events_text = re.search(r"events\: \[(.*)\]", html, re.DOTALL).group(1)
    trimmed_text = re.sub(r"\n|\t", "", events_text)
    events = re.findall(r"\{.*?\}", trimmed_text)

    """
        We store the calendar entries in a dictionary { [key]: value }, where:
            * key: str
                Date + time of the session in ISO format. E.g.: '2024-08-12T18:00:00'
            * value: str.
                Names of the participants of the session, separated by commas.
                If a session has been cancelled, the name used is 'CANCELLED'
                If a session is free, the name used is 'FREE
                E.g.: 'Bond J.,Norbert E.,FREE,CANCELLED'
    """
    calendar_entries = {}
    for event in events:
        # Events have the formats:
        #   "{title: 'Bond J.',start: '2024-06-03T18:00:00',end: '2024-06-03T19:00:00',color: '#D3D3D3',description: 'Reservé par Bond J.'}"
        #   "{title: ' ',start: '2024-06-03T18:00:00',end: '2024-06-03T19:00:00',color: '#D3D3D3',description: 'Reservé par  '}"
        #   "{title: 'Place disponible',color: '#82BCF3',url: '?reserver=43966',start: '2024-09-18T19:00:00',end: '2024-09-18T20:00:00',description: 'Cliquez pour réserver entre 19:00 et 20:00'}"
        #   "{title: 'Session annulée',color: '#BF0000',start: '2024-09-18T20:00:00',end: '2024-09-18T21:00:00',description: 'La session est annulée.'}"
        name = re.search("title: '(.*?)'", event).group(1)
        if name == "Session annulée":
            name = CANCELLED
        elif name == "Place disponible":
            name = FREE
        elif name == " ":
            name = EMPTY
        datetime = re.search("start: '(.*?)'", event).group(1)
        if datetime in calendar_entries:
            calendar_entries[datetime] += f",{name}"
        else:
            calendar_entries[datetime] = name

    return calendar_entries


def write_calendar_entries_to_db(calendar_entries):
    conn = sqlite3.connect(f"{DB_NAME}")
    cursor = conn.cursor()

    for datetime in calendar_entries:
        cursor.execute(
            """
            SELECT members
            FROM calendar
            WHERE datetime = ?
        """,
            (datetime,),
        )
        old_members_array = cursor.fetchall()

        if len(old_members_array) == 0:
            # No previous entry exists
            cursor.execute(
                """
                INSERT INTO calendar (datetime, members)
                VALUES (?, ?)
            """,
                (datetime, calendar_entries[datetime]),
            )
        else:
            # Overwrite previous entry
            cursor.execute(
                """
                UPDATE calendar
                SET members = ?
                WHERE datetime = ?
            """,
                (calendar_entries[datetime], datetime),
            )

    conn.commit()
    conn.close()


def count_slots_available(new_members: str, old_members: str) -> int:
    new_free_slots = new_members.count(FREE)
    old_free_slots = old_members.count(FREE)

    return max(new_free_slots - old_free_slots, 0)


def find_available_slots(calendar_entries):
    conn = sqlite3.connect(f"{DB_NAME}")
    cursor = conn.cursor()

    result = {}
    has_available_slots = False

    for datetime in calendar_entries:
        cursor.execute(
            """
            SELECT members
            FROM calendar
            WHERE datetime = ?
        """,
            (datetime,),
        )
        old_members_entry = cursor.fetchone()

        if old_members_entry is None:
            # The DB hasn't been populated for this datetime.
            continue
        else:
            old_members = old_members_entry[0]

        if count := count_slots_available(calendar_entries[datetime], old_members):
            has_available_slots = True
            result[datetime] = count

    conn.close()

    if RUN_WITH_LOGS:
        print(
            "* No new slots available :("
            if has_available_slots is False
            else "* Available slots found! :D"
        )

    return result if has_available_slots else None

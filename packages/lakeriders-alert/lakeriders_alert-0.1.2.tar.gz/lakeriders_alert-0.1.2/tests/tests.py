from unittest import TestCase
from datetime import datetime

from lakeridersalert.helpers.calendar_entries import extract_calendar_entries, count_slots_available
from lakeridersalert.helpers.telegram_bot import sort_and_format_slots
from .test_data import html as test_html, calendar_entries_dict as test_calendar_entries


class TestExtractCalendarEntries(TestCase):
    def test_extract_calendar_entries_all_cases(self):
        self.assertEqual(extract_calendar_entries(test_html), test_calendar_entries)


class TestCountSlotsAvailable(TestCase):
    def test_count_one_when_full(self):
        new_members = "Agatha C.,William T.,Robin H.,FREE"
        old_members = "Robin H.,William T.,Agatha C.,Donald D."
        self.assertEqual(count_slots_available(new_members, old_members), 1)

    def test_count_one_when_some_cancelled(self):
        new_members = "William T.,Robin H.,FREE"
        old_members = "Robin H.,William T.,Agatha C.,CANCELLED"
        self.assertEqual(count_slots_available(new_members, old_members), 1)

    def test_count_one_when_more_free(self):
        new_members = "Donald D.,FREE,FREE,FREE"
        old_members = "FREE,FREE,Agatha C.,Donald D."
        self.assertEqual(count_slots_available(new_members, old_members), 1)

    def test_count_zero_when_some_reserved(self):
        new_members = "Agatha C.,William T.,Robin H.,Donald D."
        old_members = "Robin H.,William T.,Agatha C.,FREE"
        self.assertEqual(count_slots_available(new_members, old_members), 0)

    def test_count_zero_when_members_changed(self):
        new_members = "Michael J.,Femke B.,Isina I.,Michael P."
        old_members = "Robin H.,William T.,Agatha C.,Donald D."
        self.assertEqual(count_slots_available(new_members, old_members), 0)

    def test_count_two_when_more_free(self):
        new_members = "FREE,FREE,FREE,FREE"
        old_members = "Robin H.,William T.,FREE,FREE"
        self.assertEqual(count_slots_available(new_members, old_members), 2)


class TestSortAndFormatSlots(TestCase):
    def test_sort_as_expected(self):
        slots = {
            "2024-08-16T18:00:00": 3,
            "2024-08-20T20:00:00": 1,
            "2024-08-12T19:00:00": 2,
            "2024-08-12T18:00:00": 1,
        }
        mocked_now = datetime.fromisoformat("2024-08-16T18:00:00")
        expected = [
            [0, "Monday", 18, 1],
            [0, "Monday", 19, 2],
            [0, "Friday", 18, 3],
            [1, "Tuesday", 20, 1],
        ]
        self.assertEqual(sort_and_format_slots(slots, mocked_now), expected)

import copy
import unittest
from datetime import date, datetime, timezone, timedelta
from validator import validate_deadlines

BASE = dict(calendarId='a', uid='1', title='HW 1', due='2026-10-30T23:59:00-05:00')

def check(**changes):
    return validate_deadlines([{**BASE, **changes}])[0]

class ValidatorTests(unittest.TestCase):
    def test_utc_conversion(self):
        self.assertEqual(check()['normalizedDue'], '2026-10-31T04:59:00.000Z')
    def test_trim_title(self):
        self.assertEqual(check(title=' HW 1 ')['title'], 'HW 1')
    def test_blank_title(self):
        self.assertIn('Missing title', check(title=' ')['issues'])
    def test_missing_date(self):
        self.assertIn('Missing due date', check(due=None)['issues'])
    def test_nonsense_date(self):
        self.assertEqual(check(due='tomorrow')['status'], 'needs_review')
    def test_timezone_free_string(self):
        self.assertIsNone(check(due='2026-10-30T23:59:00')['normalizedDue'])
    def test_impossible_date(self):
        self.assertIn('Invalid due date', check(due='2026-02-30T12:00:00Z')['issues'])
    def test_leap_day(self):
        self.assertEqual(check(due='2028-02-29T12:00:00Z')['status'], 'valid')
    def test_duplicate(self):
        self.assertIn('Duplicate', validate_deadlines([BASE, dict(BASE)])[1]['issues'][0])
    def test_conflicting_date(self):
        other = {**BASE, 'due':'2026-11-01T12:00:00Z'}
        self.assertIn('Conflicting', validate_deadlines([BASE, other])[1]['issues'][0])
    def test_separate_calendars(self):
        self.assertEqual(validate_deadlines([BASE, {**BASE, 'calendarId':'b'}])[1]['status'], 'valid')
    def test_no_mutation(self):
        records = [copy.deepcopy(BASE)]
        before = copy.deepcopy(records)
        validate_deadlines(records)
        self.assertEqual(records, before)
    def test_missing_identifiers(self):
        row = {'title':'HW', 'due':BASE['due']}
        self.assertEqual(validate_deadlines([row, dict(row)])[1]['status'], 'valid')
    def test_impossible_clock(self):
        self.assertEqual(check(due='2026-10-30T25:00:00Z')['status'], 'needs_review')

if __name__ == '__main__':
    unittest.main()

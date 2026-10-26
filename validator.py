import re
from datetime import date, datetime, timezone


def normalize_due(due):
    """Return (UTC ISO timestamp or None, list of review issues)."""
    if due is None or due == "":
        return None, ["Missing due date"]
    if isinstance(due, str):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})", due):
            return None, ["Use a full timestamp with seconds and an explicit UTC offset"]
        if due[-1] != 'Z' and (int(due[-5:-3]) > 23 or int(due[-2:]) > 59):
            return None, ["Invalid due date"]
        try:
            value = datetime.fromisoformat(due.replace('Z', '+00:00'))
        except ValueError:
            return None, ["Invalid due date"]
    else:
        return None, ["Invalid due date"]
    if value.tzinfo is None or value.utcoffset() is None:
        return None, ["Missing time zone: review before import"]
    try:
        normalized = value.astimezone(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    except (ValueError, OverflowError):
        return None, ["Invalid due date"]
    return normalized, []


def validate_deadlines(records):
    """Validate imported dictionaries without changing the input.

    Accepts due as an ISO string or None. Original keys
    remain intact. Duplicate detection needs both calendarId and uid.
    """
    if not isinstance(records, list):
        raise TypeError('Expected a list of dictionaries')
    seen = {}
    results = []
    for record in records:
        if not isinstance(record, dict):
            raise TypeError('Each record must be a dictionary')
        title = record.get('title', '')
        title = title.strip() if isinstance(title, str) else ''
        issues = [] if title else ['Missing title']
        due = record.get('due')
        normalized, date_issues = normalize_due(due)
        issues.extend(date_issues)
        calendar_id = record.get('calendarId')
        uid = record.get('uid')
        if isinstance(calendar_id, str) and calendar_id and isinstance(uid, str) and uid:
            key = (calendar_id, uid)
            fingerprint = (title, due)
            if key in seen:
                kind = 'Duplicate' if seen[key] == fingerprint else 'Conflicting'
                issues.append(kind + ' record: review before import')
            else:
                seen[key] = fingerprint
        results.append({**record, 'title': title, 'normalizedDue': normalized,
                        'issues': issues, 'status': 'needs_review' if issues else 'valid'})
    return results

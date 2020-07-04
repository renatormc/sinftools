from datetime import datetime, timedelta
import re


def string(cell):
    return str(cell.value)


def timestamp(cell):
    try:
        res = re.search(r'(.+)\(UTC-\d\)', cell.value)
        return datetime.strptime(res.group(1), "%d/%m/%Y %H:%M:%S")
    except:
        return None


def integer(cell):
    try:
        return int(cell.value)
    except:
        return None


def participant(item):
    try:
        value = item if isinstance(item, str) else item.value
        parts = re.split(r'\s+', value)
        n = len(parts)
        if n >= 2:
            return {'identifier': parts[0].strip(), 'name': " ".join(parts[1:]).strip()}
        elif n == 1:
            return {'identifier': parts[0].strip(), 'name': None}
        else:
            return {'identifier': None, 'name': None}
    except:
        return {'identifier': None, 'name': None}


def participants(cell):
    try:
        return [participant(item) for item in cell.value.split("\n")]
    except:
        return []


def parties(item):
    try:
        ret = []
        value = item if isinstance(item, str) else item.value
        parts = value.split("\n")
        for part in parts:
            peaces = part.split(":")
            if len(peaces) == 2:
                item = {'role': peaces[0].strip()}
                item.update(participant(peaces[1].strip()))
                ret.append(item)
        return ret
    except:
        return []


def contact_entries(item):
    ret = []
    value = item if isinstance(item, str) else item.value
    parts = value.split("\n")
    for part in parts:
        peaces = part.split(":")
        if len(peaces) == 2:
            item = {'category': peaces[0].strip(), 'value': peaces[1].strip()}
            ret.append(item)
    return ret
    return []


def duration(cell):
    try:
        parts = cell.value.split(":")
        return timedelta(hours=int(parts[0]), minutes=int(parts[1]), seconds=int(parts[2]))
    except:
        return None


def attachment(cell):
    try:
        return cell.hyperlink.target
    except:
        return None

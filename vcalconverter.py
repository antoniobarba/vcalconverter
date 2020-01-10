import argparse
import sys
import codecs

class Event:
    def __init__(self, start = None, end = None, created = None, description = None, summary = None, location = None):
        self.start = start
        self.end = end
        self.created = created
        self.description = description
        self.location = location
        self.summary = summary

    def toICS(self):
        return f'''BEGIN:VEVENT
DTSTART:{self.start}
DTEND:{self.end}
CREATED:{self.created}
DESCRIPTION:{self.description}
LOCATION:{self.location}
SUMMARY:{self.summary}
END:VEVENT'''

    def toVCS(self):
        return f'''BEGIN:VEVENT
DTSTART:{self.start}
DTEND:{self.end}
CREATED:{self.created}
DESCRIPTION;ENCODING=QUOTED-PRINTABLE:{self.description}
LOCATION:{self.location}
SUMMARY:{self.summary}
END:VEVENT'''

class Calendar:

    def toICS(self):
        expEvents = '\n'.join([x.toICS() for x in self.events])
        return f'''BEGIN:VCALENDAR
PRODID:-//Antonio Barba//VCalConverter Beta//EN
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:Converted with VCalConverter Beta
X-WR-TIMEZONE:Europe/Rome
BEGIN:VTIMEZONE
TZID:Europe/Rome
X-LIC-LOCATION:Europe/Rome
BEGIN:DAYLIGHT
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
TZNAME:CEST
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
TZNAME:CET
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE
{expEvents}
END:VCALENDAR'''

    def toVCS(self):
        expEvents = '\n'.join([x.toICS() for x in self.events])
        return f'''BEGIN:VCALENDAR
VERSION:1.0
PRODID:-//Antonio Barba//VCalConverter Beta//1.0//EN
{expEvents}
END:VCALENDAR

'''
        
    def __init__(self, fileName, charEncoding="UTF-8"):
        self.events = []
        with open(fileName, encoding=charEncoding) as file:
            inEvent = False
            tmp = {'start': None, 'end': None, 'created': None, 'description': None, 'location': None, 'summary': None}
            for line in file.readlines():
                if line.startswith('BEGIN:VEVENT'):
                    inEvent = True
                if inEvent:
                    if line.startswith('END:VEVENT'):
                        inEvent = False
                        self.events.append(Event(start=tmp['start'],
                                                 end=tmp['end'],
                                                 created=tmp['created'],
                                                 description=tmp['description'],
                                                 location=tmp['location'],
                                                 summary=tmp['summary']))
                        tmp = {'start': None, 'end': None, 'created': None, 'description': None, 'location': None, 'summary': None}
            
                    elif line.startswith('SUMMARY'):
                        tmp['summary'] = line[line.index(':')+1 : -1]
                    elif line.startswith('DTSTART'):
                        tmp['start'] = line[line.index(':')+1 : -1]
                    elif line.startswith('DTEND'):
                        tmp['end'] = line[line.index(':')+1 : -1]
                    elif line.startswith('LOCATION'):
                        tmp['location'] = line[line.index(':')+1 : -1]
                    elif line.startswith('DESCRIPTION'):
                        tmp['description'] = line[line.index(':')+1 : -1]
                    elif line.startswith('CREATED'):
                        tmp['created'] = line[line.index(':')+1 : -1]
                        
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)
        
parser = argparse.ArgumentParser(description="Convert iCal (*.ics) file format to vCalendar (*.vcs)")
parser.add_argument('fileName', type=str, help="Path to the file to be converted")
args = parser.parse_args()
cal = Calendar(args.fileName)
uprint(cal.toICS())

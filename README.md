# vcalconverter
Conversion Tool from iCalendar (\*.ics) to vCalendar (\*.vcs) file formats

## Requirements
Python 3.6 or newer (tested on Windows, but it should work on Linux and Mac too with minimal changes if any)

## Usage
python vcalconverter.py \<fileName\>
  
Output: The converted calendar in vCal format, on the standard output

## Example:

- Export your calendar from Google Calendar in iCal format, save it as test.ics
- Convert it like this:
python vcalconverter.py /path/to/test.ics > /path/to/conversionresult.vcs

The file will be converted and the output redirected from the stdout to a regular file.
Then you can import your converted calendar data into a legacy application, like older versions of Outlook or Palm Desktop to sync with an old Palm Powered PDA.

## Known limitations
- Timezones are not properly supported
- There is some code in place for the inverse conversion (vcs to ics), but it's not tested nor finished
- I made this script for my own use to sync Google Calendar with my old Palm handheld, so I don't plan on expanding its capabilities beyond a certain point, of course any contribution to the code will be appreciated

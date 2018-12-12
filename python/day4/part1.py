import fileinput
import re

pattern = re.compile(r'\[(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) (?P<hour>\d{2}):(?P<minute>\d{2})\] (?P<action>.+)')

start_pattern = re.compile(r'Guard #(?P<guard>\d+) begins shift')

class Shift:
	__init__(guard, month, day):
		self.guard = guard
		self.month = month
		self.day = day
		self.sleeps = []


lines = [line for lineinput.input()]
lines.sort()


sleep = None
for line in lines:
	year,month,day,hour,minute,action = pattern.match(line).groups()

	m = start_pattern.match(action)

	if m == None:
		if action == 'falls asleep':
			sleep = (minute, 60)
		else if action == 'wakes up':
			sleep = (sleep[0], minute)
	else:
		guard = m.group('guard')
		shift = Shift(guard, month, day)



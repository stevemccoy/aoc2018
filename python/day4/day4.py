import fileinput
import re

pattern = re.compile(r'\[(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) (?P<hour>\d{2}):(?P<minute>\d{2})\] (?P<action>.+)')

start_pattern = re.compile(r'Guard #(?P<guard>\d+) begins shift')

class Shift:
	def __init__(self, guard, month, day):
		self.guard = guard
		self.month = month
		self.day = day
		self.sleeps = []

class Guard:
	def __init__(self, gid):
		self.gid = gid
		self.totalSleep = 0
		self.whenSleeping = dict.fromkeys([i for i in range(60)], 0)

	def add_sleep(self, minFrom, minTo):
		for m in range(minFrom, minTo, 1):
			self.whenSleeping[m] += 1
		self.totalSleep += (minTo - minFrom)


def read_shifts(lines):
	all_shifts = []
	sleep = None
	guard = None
	shift = None

	for line in lines:
		year,month,day,hour,minute,action = pattern.match(line).groups()
		m = start_pattern.match(action)
		if m == None:
			if action == 'falls asleep':
				sleep = (int(minute), 60)
			elif action == 'wakes up':
				sleep = (sleep[0], int(minute))
				shift.sleeps.append(sleep)
		else:
			if not shift is None:
				all_shifts.append(shift)
				shift = None
				guard = None

			guard = m.group('guard')
			shift = Shift(guard, month, day)

	all_shifts.append(shift)
	return all_shifts


def find_guard(guard_id, guard_dict):
	if guard_id in guard_dict:
		return guard_dict[guard_id]
	else:
		guard = Guard(guard_id)
		guard_dict[guard_id] = guard
		return guard


def pivot_dictionary(d):
	result = dict()
	for k,v in d.items():
		if not v in result:
			result[v] = []
		result[v].append(k)
	return result



lines = [line for line in fileinput.input()]
lines.sort()

all_shifts = read_shifts(lines)
all_guards = dict()

for shift in all_shifts:
	guard = find_guard(shift.guard, all_guards)
	for sleep in shift.sleeps:
		guard.add_sleep(sleep[0], sleep[1])

# Get guard with the most sleep.
sleepy_guard = None
sleep_minutes = 0
for guard in all_guards.values():
	if guard.totalSleep > sleep_minutes:
		sleep_minutes = guard.totalSleep
		sleepy_guard = guard

print(sleepy_guard.gid)

# When is this guard most likely asleep?
# whenSleeping = min -> freq
# transform to freq -> [min,...]

when_sleeping = pivot_dictionary(sleepy_guard.whenSleeping)

print(when_sleeping)

# Which guard is most frequently asleep on the same minute?

max_frequency = 0
minute = None
freq = None
result = []
for guard in all_guards.values():
	minute, freq = max(guard.whenSleeping.items(), key = lambda item: item[1])
	if freq > max_frequency:
		max_frequency = freq
		result.append((guard.gid, minute, freq))

print(result)







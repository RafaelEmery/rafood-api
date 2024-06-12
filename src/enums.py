from enum import Enum


class DayType(Enum):
	WEEKDAY = 'weekday'
	WEEKEND = 'weekend'
	HOLIDAY = 'holiday'


class Day(Enum):
	MONDAY = 'monday'
	TUESDAY = 'tuesday'
	WEDNESDAY = 'wednesday'
	THURSDAY = 'thursday'
	FRIDAY = 'friday'
	SATURDAY = 'saturday'
	SUNDAY = 'sunday'

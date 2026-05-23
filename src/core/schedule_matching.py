from datetime import datetime

from sqlalchemy import Integer, Time, and_, case, cast, extract, or_

from src.enums import Day, DayType


def day_name_to_index(column: object) -> object:
	"""
	Map a Day enum string column (e.g. 'monday') to 0–6 for ordered comparisons in SQL.

	Consider the Day enum to map the day name to an index.
	"""
	return case(
		*((column == day.value, index) for index, day in enumerate(Day)),  # type: ignore[arg-type]
		else_=-1,
	)


def current_day_index(reference_time: datetime) -> object:
	"""
	ISO weekday as 0–6 (Monday=0), matching Python Day enum order.

	Consider the reference time to get the current day index.
	"""
	return cast(extract('isodow', reference_time), Integer) - 1  # type: ignore[arg-type]


def current_day_type(reference_time: datetime) -> object:
	"""
	Weekday vs weekend from reference_time (ISO Saturday/Sunday → weekend).

	Consider the reference time to get the current day type.
	"""
	return case(
		(extract('isodow', reference_time).in_([6, 7]), DayType.WEEKEND.value),  # type: ignore[arg-type]
		else_=DayType.WEEKDAY.value,
	)


def current_day_name(reference_time: datetime) -> object:
	"""
	Day enum string for reference_time (e.g. 'wednesday').

	Consider the reference time to get the current day name.
	"""
	return case(
		*(
			(extract('isodow', reference_time) == index + 1, day.value)  # type: ignore[arg-type]
			for index, day in enumerate(Day)
		),
		else_=Day.MONDAY.value,
	)


def day_in_range(start_day_col: object, end_day_col: object, reference_time: datetime) -> object:
	"""
	True when reference_time's weekday falls in [start_day, end_day] on the week circle.

	Consider the reference time to check if the day is in the range.
	Handles wrap-around (e.g. friday → monday): if start > end, the range crosses Sunday.
	"""
	current = current_day_index(reference_time)
	start_idx = day_name_to_index(start_day_col)
	end_idx = day_name_to_index(end_day_col)

	# Normal range (mon → fri) or wrap-around (fri → mon)
	return or_(
		and_(start_idx <= current, current <= end_idx),  # type: ignore[operator]
		and_(start_idx > end_idx, or_(current >= start_idx, current <= end_idx)),  # type: ignore[operator]
	)


def schedule_time_in_range(
	start_time_col: object, end_time_col: object, reference_time: datetime
) -> object:
	"""
	True when reference_time's clock time is between start_time and end_time (inclusive).

	Consider the reference time to check if the time is in the range.
	"""
	current_time = cast(reference_time, Time)

	return and_(start_time_col <= current_time, current_time <= end_time_col)

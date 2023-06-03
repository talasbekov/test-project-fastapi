# Define the number of days in each month as a list
days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def convert_days(days):
    def is_leap_year(year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    years = days // 365
    months = 0
    remaining_days = days % 365

    # Adjust for leap years
    for year in range(years):
        if is_leap_year(year + 1):
            remaining_days -= 1

    # Calculate the months and remaining days
    for i, days_in_current_month in enumerate(days_in_month):
        if remaining_days >= days_in_current_month:
            months += 1
            remaining_days -= days_in_current_month
        else:
            break

    return years, months, remaining_days

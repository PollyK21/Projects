from datetime import date, timedelta, datetime


def get_birthdays_per_week(users):
    # сьогоднішня дата
    today = date.today()
    today_year = today.year

    # дата через тиждень
    next_week = date.today() + timedelta(weeks=1)


    birthdays = {}

    
    for user in users:
        name = user['name']
        birthday = user['birthday']

        # міняємо рік на поточний (якщо рік записний минулий чи дата народження)
        new_b = birthday.replace(year=today_year)
        #якщо при цьому дата др вже минула в цьому році додаємо рік щоб визначити наступний др
        if today > new_b:
            new_b = new_b.replace(year=today_year + 1)

        # якщо др в наступному тижні
        if today <= new_b < next_week:
            # якщо припадає на сб, нд
            if new_b.weekday() in [5, 6]:
                # перевіряємо чи створений список для понеділка
                if 'Monday' not in birthdays:
                    birthdays['Monday'] = []
                # додаємо имʼя до дня тижня
                birthdays['Monday'].append(name)

            # те саме для інших днів тижня
            else:
                day = new_b.strftime('%A')
                if day not in birthdays:
                    birthdays[day] = []
                birthdays[day].append(name)

    print(birthdays)        
    return birthdays


# users_list = [
#     {"name": "Bill Gates", "birthday": datetime(1955, 10, 28).date()},
#     {"name": "Steve Jobs", "birthday": datetime(1955, 12, 3).date()},
#     {"name": "Mark Zuckerberg", "birthday": datetime(1984, 5, 14).date()},
#     {"name": "Elon Musk", "birthday": datetime(1971, 12, 6).date()},
#     {"name": "Jeff Bezos", "birthday": datetime(1964, 12, 2).date()},
#     # Додайте інших користувачів за необхідністю
# ]

# get_birthdays_per_week(users_list)


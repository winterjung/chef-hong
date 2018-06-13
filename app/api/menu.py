from enum import Enum

from app.api import request
from app.api.formatter import DefaultFormatter
from app.api.utils import (assert_daily_menus, assert_places, day_to_weekday,
                           grouper, listify, now)


def generate_combined_menu():
    # table
    pq = request.pq()
    table = request.table(pq)

    # 소스: week_menus -> length: 6 * 11
    # 열: weekdays, dates -> length: 6
    days = request.days(table)
    daily_menus = request.daily_menus(table)
    week_menus = grouper(daily_menus, len(days))
    weekdays, dates = request.divide_days(days)

    # 행: times, places -> length: 11
    times = request.rows(table)
    places = request.refine_place()

    # 장소 정보
    subtitles = request.slim_subtitles(request.subtitles(table))
    place_info = request.refine_place_info(subtitles)

    assert_daily_menus(days, times, daily_menus)
    assert_places(places, times, subtitles)

    rows = zip(week_menus, places, place_info, times)
    for week_menu, place, info, time in rows:
        for daily_menu, weekday, date in zip(week_menu, weekdays, dates):
            yield {
                'date': date,
                'weekday': weekday,
                'place': place,
                'place_info': info,
                'time': time,
                'text': daily_menu,
            }


def update_all_menu():
    all_menu = Menu()
    for menu in generate_combined_menu():
        all_menu.add_menu(menu)
    return all_menu


class Weekday(Enum):
    월요일 = 0
    화요일 = 1
    수요일 = 2
    목요일 = 3
    금요일 = 4
    토요일 = 5
    일요일 = 6


class Chef:
    def __init__(self, duration=3600, formatter=DefaultFormatter):
        """
        cache = {
            '3.점심.학생회관.False': {
                'text': ...,
                'create_at': ...,
            }
        }
        """
        self.all_menu = update_all_menu()
        self.cache = {}
        self.duration = duration
        self.formatter = formatter
        self.create_at = now()

    def _get(self, weekday, time, place, simplify):
        if self.is_outdated():
            self.all_menu = update_all_menu()

        key = '{}.{}.{}.{}'.format(weekday, time, place, simplify)
        if key not in self.cache or self.is_timeout(key):
            menu = self.all_menu.day(weekday).time(time).place(place)
            text = menu.format(self.formatter).text(simplify)

            self.cache[key] = {
                'text': text,
                'create_at': now(),
            }

        return self.cache[key]['text']

    def is_outdated(self):
        return self.create_at + self.duration < now()

    def is_timeout(self, key):
        return self.cache[key]['create_at'] + self.duration < now()

    def is_closed(self, name):
        return name == '일요일'

    def closed(self):
        return '오늘은 쉽니다. (야옹)\n- 셰프 홍'

    def order(self, day, *, time=None, place=None, simplify=True):
        """
        >>> order('오늘')
        오늘의 간략화된 식단

        >>> order('오늘', simplify=False)
        오늘의 전체 식단

        >>> order('오늘', time='점심')
        오늘의 전체 점심 식단

        >>> order('오늘', place='신기숙사')
        오늘의 전체 신기숙사 식단
        """
        # time이나 place가 있다면 전체 식단 반환하기위해
        if any((time, place)):
            simplify = False

        # 오늘 -> 0...6 -> 월요일...일요일
        weekday = day_to_weekday(day)
        name = Weekday(weekday).name

        if self.is_closed(name):
            return self.closed()

        text = self._get(name, time, place, simplify)
        if simplify:
            text += '\n\n{}의 간략한 식단입니다. (야옹)'.format(day)
        return text


class Menu:
    def __init__(self, menus=None):
        """
        Parameters
        ----------
        menus : list, optional

        Attributes
        ----------
        _menus : list[dict[str, str]]

        dict : {
            'date': date,
            'weekday': weekday,
            'place': place,
            'place_info': place_info,
            'time': time,
            'text': daily_menu,
        }
        """
        self._menus = []

        if menus is not None:
            self.add_menus(menus)

    def add_menus(self, menus):
        for menu in listify(menus):
            if isinstance(menu, dict):
                self.add_menu(menu)

    def add_menu(self, menu):
        self._menus.append(menu)

    def day(self, weekday):
        """
        Parameters
        ----------
        weekday : str, e.g. 월요일, 화요일
        """
        if weekday is None:
            return self

        filtered = [menu for menu in self._menus
                    if menu['weekday'] == weekday]
        return Menu(menus=filtered)

    def time(self, name):
        if name is None:
            return self

        filtered = [menu for menu in self._menus
                    if name in menu['time']]
        return Menu(menus=filtered)

    def place(self, name):
        if name is None:
            return self

        filtered = [menu for menu in self._menus
                    if menu['place'] == name]
        return Menu(menus=filtered)

    def format(self, formatter):
        self.formatter = formatter
        return self

    def text(self, simplify):
        places = self._assemble(simplify)
        weekday, date = self._weekday_and_date()
        text = self.formatter.format(places=places,
                                     weekday=weekday,
                                     date=date)
        return text.strip()

    def _assemble(self, simplify):
        # TODO: 더 가독성 있게 개선
        already = []
        places = []
        for menu in self._menus:
            text = menu['text']
            if simplify:
                text = self._simplify(text)

            time = dict(name=menu['time'], text=text)
            name = menu['place_info']

            if name not in already:
                already.append(name)
                places.append(dict(name=name, time=list()))

            idx = already.index(name)
            places[idx]['time'].append(time)
        return places

    def _simplify(self, text, count=5, cond=None):
        separated = text.split('\n')
        filtered = list(filter(cond, separated))
        return '\n'.join(filtered[:count])

    def _weekday_and_date(self):
        weekday = set(menu['weekday'] for menu in self._menus).pop()
        date = set(menu['date'] for menu in self._menus).pop()
        return weekday, date

    def __repr__(self):
        weekday = set(menu['weekday'] for menu in self._menus)
        place = set(menu['place'] for menu in self._menus)

        return '<Menu of {}*{}>'.format(weekday, place)


chef = Chef()

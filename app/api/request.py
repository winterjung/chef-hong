import itertools
import re

import requests
from pyquery import PyQuery

PLACE_RULE = dict(
    학생회관=2,
    남문관=4,
    교직원=2,
    신기숙사=3)


def pq(url=None):
    if url is None:
        url = 'http://apps.hongik.ac.kr/food/food.php'
    res = requests.get(url)
    return PyQuery(res.text)


def table(pq):
    table = pq('.weekly-menu-list')
    return table


def days(table):
    """요일과 날짜를 반환함

    >>> days(table(pq()))
    ('월요일(2018.02.26)', ..., '토요일(2018.03.03)')
    """
    ths = table('thead')('th')
    contents = (th.text_content() for th in ths)
    days = filter(is_day_of_the_week, contents)
    return tuple(days)


def divide_days(days):
    """요일과 날짜로 분리함

    >>> divide_days(['월요일(2018.02.26)'])
    ('월요일', '(2018.02.26)')
    """
    weekdays = []
    dates = []
    for day in days:
        weekday, date = divide_day(day)
        weekdays.append(weekday)
        dates.append(date)

    return weekdays, dates


def divide_day(day):
    pattern = re.compile(r"""
        (
            [(]    # 여는 괄호
            [^)]+  # ')'가 오기 전까지 모든 문자
            [)]    # 닫는 괄호
        )
        """, re.VERBOSE)
    weekday, date, *_ = pattern.split(day)
    return weekday, date


def is_day_of_the_week(text):
    return '요일' in text


def daily_menus(table):
    """daily-menu 클래스로 되어있는 메뉴를 반환함
    len(menus)는 6의 배수(월요일~토요일)임
    """
    menus = table('.daily-menu')
    menus = (trim(menu.text_content()) for menu in menus)
    return tuple(menus)


def trim(text):
    return (text
            .replace('\r', '')
            .replace('\t', '')
            .strip('\n'))


def subtitles(table):
    """식당 이름과 부가 정보를 반환함"""
    subtitles = table('.subtitle')
    subtitles = (trim(title.text_content()) for title in subtitles)
    return tuple(subtitles)


def remove_bracket_content(text):
    pattern = re.compile(r"""
        (
            [(]    # 여는 괄호
            [^)]+  # ')'가 오기 전까지 모든 문자
            [)]    # 닫는 괄호
        )
        """, re.VERBOSE)
    return re.sub(pattern, '', text)


def slim_subtitles(subtitles):
    slim = (remove_bracket_content(title) for title in subtitles)
    return tuple(slim)


def rows(table):
    ths = table('tbody')('th')
    rows = (th.text_content() for th in ths)
    return tuple(rows)


def refine_place():
    """PLACE_RULE을 토대로 장소를 행의 수와 같게 만들어 반환한다.

    Examples
    --------
    >>> refine_place()
    ('학생회관', '학생회관', '남문관', '남문관', ...)
    """
    places = PLACE_RULE.items()

    repeated = map(_repeat, places)
    places = itertools.chain.from_iterable(repeated)

    return tuple(places)


def refine_place_info(subtitles):
    counts = PLACE_RULE.values()

    repeated = map(_repeat, zip(subtitles, counts))
    place_info = itertools.chain.from_iterable(repeated)
    return tuple(place_info)


def _repeat(p):
    return itertools.repeat(*p)

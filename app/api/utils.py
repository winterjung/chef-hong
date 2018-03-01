import itertools
from datetime import datetime, timedelta


def listify(obj):
    if obj is None:
        return []
    if isinstance(obj, (list, tuple)):
        return obj
    return [obj]


def grouper(iterable, n, fillvalue=None):
    """
    Example
    -------
    >>> grouper('ABCDEFG', 3, 'x')
    ABC DEF Gxx
    """
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def now():
    return int(datetime.utcnow().timestamp())


def day_to_weekday(day):
    """
    Example
    -------
    >>> day_to_weekday('오늘')
    0  # 월요일
    >>> day_to_weekday('내일')
    1  # 화요일
    """
    delta_mapping = {
        '오늘': timedelta(hours=9),
        '내일': timedelta(days=1, hours=9),
    }
    now = datetime.utcnow() + delta_mapping.get(day)
    weekday = now.weekday()
    return weekday


def assert_daily_menus(days, times, daily_menus):
    """한 주의 식단과 행(점심, 저녁), 열(월화수목금토) 정합성 검사

    Parameters
    ----------
    days : tuple
        날짜 정보(열) e.g. (월요일(2018.03.02), ...)
    times : tuple
        시간 정보(행) e.g. (점심, 저녁, ...)
    daily_menus : tuple
        한 주의 식단 text 정보

    Example
    -------
    >>> assert len(days) == 6
    >>> assert len(times) == 11
    >>> assert len(daily_menus) == 66
    """
    assert len(days) * len(times) == len(daily_menus)


def assert_places(places, times, subtitles):
    """장소 정보와 행(점심, 저녁) 정합성 검사

    Parameters
    ----------
    places : odict_items
        장소와 장소가 가진 행의 수 e.g. 학생회관은 점심, 저녁, 신기숙사는 아침, 점심, 저녁
    times : tuple
        시간 정보(행) e.g. (점심, 저녁, ...)
    subtitles : tuple
        장소 정보 e.g. 학생회관식당 / 11:00~14:00, 17:00~19:00

    Example
    -------
    >>> assert len(places) == 11
    >>> assert len(times) == 11
    >>> assert len(places) == 4
    >>> assert len(subtitles) == 4
    """
    assert len(places) == len(times)
    assert len(set(places)) == len(subtitles)

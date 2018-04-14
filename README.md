# Chef Hong

[![license]](/LICENSE)
[![travis]](https://travis-ci.org/JungWinter/chef-hong)
[![codecov]](https://codecov.io/gh/JungWinter/chef-hong)

---

<b>[Chef Hong]</b>은 [chatterbox]를 사용하여 제작한 카카오톡 챗봇으로 <b>홍익대학교 학식알리미</b> 역할을 맡고 있습니다.

## History

**학식알리미 Chef Hong**의 주요 변경 사항이 기록되어 있습니다.

### [1.2.0]

> 2018-04-14
- Fixture를 분리하고 Test case 개선
- Alembic, SQLAlchemy 사용

### [1.1.6]

> 2018-03-16
- 간략한 식단 안내가 전체 식단 보기에도 적용되는 문제 수정

### [1.1.5]

> 2018-03-16
- [pytest-mock]을 사용해 `python-logstash-async`의 로깅이 테스트에 영향을 주던 문제 수정
- `chef.cache`를 볼 수 있도록 `util` 엔드포인트를 추가

### [1.1.4]

> 2018-03-12
- 간략한 식단 안내에 `오늘`이라고 고정된 문구를 `오늘`, `내일`이라고 적절하게 출력하도록 변경

### [1.1.3]

> 2018-03-12
- 간략한 식단 안내 문구를 추가하는 행위를 `chatter.py`에서 `menu.py`의 `Chef`가 담당하도록 변경

### [1.1.2]

> 2018-03-06
- 메뉴 업데이트 주기를 1시간으로 수정

### [1.1.1]

> 2018-03-03
- [gunicorn], [requests] 의존성 추가
- 로깅 에러 수정

### [1.1.0]

> 2018-03-02
- [python-logstash-async]를 사용한 로깅 추가

### [1.0.1]

> 2018-03-02
- README에 뱃지 추가
- isort 적용
- 일요일 휴무 메시지 적용

### [1.0.0]

> 2018-03-01

:tada:


[Chef Hong]: https://github.com/JungWinter/chef-hong
[license]: https://img.shields.io/badge/license-MIT-blue.svg
[travis]: https://travis-ci.org/JungWinter/chef-hong.svg
[codecov]: https://codecov.io/gh/JungWinter/chef-hong/branch/master/graph/badge.svg
[chatterbox]: https://github.com/JungWinter/chatterbox

[1.0.0]: https://github.com/JungWinter/chef-hong/commit/65044dfb2a949aae19bda5e8614e227a902ee0cf
[1.0.1]: https://github.com/JungWinter/chef-hong/compare/v1.0.0...v1.0.1
[1.1.0]: https://github.com/JungWinter/chef-hong/compare/v1.0.1...v1.1.0
[1.1.1]: https://github.com/JungWinter/chef-hong/compare/v1.1.0...v1.1.1
[1.1.2]: https://github.com/JungWinter/chef-hong/compare/v1.1.1...v1.1.2
[1.1.3]: https://github.com/JungWinter/chef-hong/compare/v1.1.2...v1.1.3
[1.1.4]: https://github.com/JungWinter/chef-hong/compare/v1.1.3...v1.1.4
[1.1.5]: https://github.com/JungWinter/chef-hong/compare/v1.1.4...v1.1.5
[1.1.6]: https://github.com/JungWinter/chef-hong/compare/v1.1.5...v1.1.6
[1.2.0]: https://github.com/JungWinter/chef-hong/compare/v1.1.6...v1.2.0

[python-logstash-async]: https://github.com/eht16/python-logstash-async
[gunicorn]: http://gunicorn.org/
[requests]: https://github.com/requests/requests
[pytest-mock]: https://github.com/pytest-dev/pytest-mock/

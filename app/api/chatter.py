from chatterbox import Chatter, Keyboard, MessageButton, Text

chatter = Chatter(fallback=True)


@chatter.base(name='홈')
def home_keyboard():
    home_buttons = ['오늘의 식단', '다른 식단 보기', '다른 기능']
    return Keyboard(home_buttons)


@chatter.rule(action='다른 기능', src='홈', dest='기타')
def etc(data):
    text = Text('안녕하세요! 학식알리미 셰프 홍입니다. 무엇을 도와드릴까요?')
    buttons = Keyboard(['자기소개', '추가될 기능', '취소'])
    return text + buttons


@chatter.rule(action='다른 식단 보기', src='홈', dest='다른식단')
def other(data):
    text = Text('구현중입니다! 조금만 기다려주세요. (야옹)')
    msg_button = MessageButton(label='이번주 식단 보기',
                               url='http://apps.hongik.ac.kr/food/food.php')
    keyboard = Keyboard(['내일의 식단', '이번주 식단'])
    return text + msg_button + keyboard


@chatter.rule(action=['내일의 식단', '이번주 식단'], src='다른식단', dest='홈')
def other_step2(data):
    text = Text('')
    keyboard = chatter.home()
    return text + keyboard


@chatter.rule(action='오늘의 식단', src='홈', dest='오늘식단')
def today(data):
    text = Text('')
    keyboard = Keyboard(['전체 식단', '점심', '신기숙사'])
    return text + keyboard


@chatter.rule(action=['전체 식단', '점심', '신기숙사'], src='오늘식단', dest='홈')
def today_step2(data):
    text = Text('')
    keyboard = chatter.home()
    return text + keyboard


@chatter.rule(action='자기소개', src='기타', dest='홈')
def intro(data):
    text = Text(
        '학식알리미 셰프 홍은 여기서 개발되고 있어요! '
        '기능 제안, 버그 제보는 언제나 환영합니다. (최고)\n'
        '개발자 분들이 (별) 눌러주시길 기대할게요!')
    msg_button = MessageButton(label='이동하기',
                               url='https://github.com/jungwinter/chef-hong')
    keyboard = chatter.home()
    return text + msg_button + keyboard


@chatter.rule(action='추가될 기능', src='기타', dest='홈')
def roadmap(data):
    text = Text(
        '앞으로 다양한 기능이 추가 될 예정입니다!\n'
        '* 학식 사진으로 보기\n'
        '* 커뮤니티\n'
        '* 이 달의 최고 학식러\n'
        '\n'
        '기능 제안은 언제나 환영합니다! 개발자에게 연락해주세요!')
    msg_button = MessageButton(label='개발자 트위터',
                               url='https://twitter.com/res_tin')
    keyboard = chatter.home()
    return text + msg_button + keyboard


@chatter.rule(action='취소', src='*', dest='홈')
def cancel(data):
    text = Text('취소하셨습니다.')
    return text + chatter.home()

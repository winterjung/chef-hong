from chatterbox import Chatter, Keyboard, MessageButton, Text

chatter = Chatter(fallback=True)


@chatter.base(name='홈')
def home_keyboard():
    home_buttons = ['자기소개', '사이트로 이동하기']
    return Keyboard(home_buttons)


@chatter.rule(action='자기소개', src='홈', dest='소개')
def intro(data):
    text = Text('안녕하세요! 무엇을 도와드릴까요?')
    buttons = Keyboard(['오늘의 날씨', '취소'])
    return text + buttons


@chatter.rule(action='오늘의 날씨', src='소개', dest='홈')
def weather(data):
    text = Text('오늘은 하루종일 맑겠습니다.')
    keyboard = chatter.home()
    return text + keyboard


@chatter.rule(action='사이트로 이동하기', src='홈', dest='홈')
def web(data):
    text = Text('자세한 정보를 보고싶으면 사이트로 이동해주세요!')
    msg_button = MessageButton(label='이동하기',
                               url='https://github.com/jungwinter/chatterbox')
    keyboard = chatter.home()
    return text + msg_button + keyboard


@chatter.rule(action='취소', src='*', dest='홈')
def cancel(data):
    text = Text('취소하셨습니다.')
    return text + chatter.home()

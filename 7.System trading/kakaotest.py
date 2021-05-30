import requests

# 커스텀 템플릿 주소 : https://kapi.kakao.com/v2/api/talk/memo/send
talk_url = "https://kapi.kakao.com/v2/api/talk/memo/send"

# 사용자 토큰
token = '24506e4cd6be7aef5c29dfe652252d0b'
header = {
    "Authorization": "Bearer {본인의 사용자 토큰 넣기}".format(
        token=token
    )
}

# 메시지 template id와 정의했던 ${name}을 JSON 형식으로 값으로 입력
payload = {
    'template_id' : {27291},
    'template_args' : '{"name": "테스트 제목"}'
}

# 카카오톡 메시지 전송
res = requests.post(talk_url, data=payload, headers=header)

if res.json().get('result_code') == 0:
    print('메시지를 성공적으로 보냈습니다.')
else:
    print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(res.json()))
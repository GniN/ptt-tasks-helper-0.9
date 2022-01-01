from PyPtt import PTT
from shared import Bot, to_csv, to_file_path
import json

ptt_bot = Bot()

def getUser(id):
    try:
        user = ptt_bot.get_user(id)
        return user
    except PTT.exceptions.NoSuchUser:
        print('無此使用者')
        return None
    except Exception as e:
        print(e)
        print('其他錯誤')
        return None

with open(to_file_path('07_vote_checker.json'), encoding='utf-8') as json_file:
    data = json.load(json_file)

board_name = data['board_name']
post_number = int(data['post_number'])

output_rows = ['id,修正後id,正確id,登入次數,有效文章數,退文文章數,上次登入ip,上次登入日期,帳號認證,罰單狀況,編號,支持或反對']

print('正在解析文章')

post_info = ptt_bot.get_post(
        board_name,
        post_index=post_number)

print('解析文章成功')

rows = post_info.content

support_rows = post_info.content.split('----------支持----------')[1].split('----------反對----------')[0].split('\n')
against_rows = post_info.content.split('----------反對----------')[1].split('----------總計----------')[0].split('\n')

print(f'共有{len(support_rows + against_rows)}用戶筆資料')

index = 1

for row in support_rows + against_rows:
    print(f'正在查詢第{index}筆資料')

    cols = row.split(' ')
    cols = list(filter(('').__ne__, cols))
    if len(cols) < 2:
        continue
    
    # '1.hsuan0904
    number_and_id = cols[0]

    vote_number = number_and_id.split('.')[0]
    id = number_and_id.split('.')[1]

    user = getUser(id)
    user_info_list = [id]
    if user is not None:
        real_id = user.id.split(' ')[0]
        if real_id == id:
            user_info_list.append('')
        else:    
            user_info_list.append(real_id)

        # 認證
        verify_text = ''
        if user.account_verified == False:
            verify_text = '尚未通過認證'

        # 罰單
        violation_text = ''
        signature_file_first_line = user.signature_file.split('\n')[0]
        if '此人違規' in signature_file_first_line:
            violation_text = signature_file_first_line

        support_or_against_text = ''
        if row in support_rows:
            support_or_against_text = '支持'
        if row in against_rows:
            support_or_against_text = '反對'

        
        user_info_list.append(real_id) #正確id
        user_info_list.append( str(user.login_time) ) #登入次數
        user_info_list.append( str(user.legal_post) ) #有效文章數
        user_info_list.append( str(user.illegal_post) ) #退文文章數
        user_info_list.append( str(user.last_ip) ) #上次登入ip
        user_info_list.append( str(user.last_login) ) #上次登入日期
        user_info_list.append( str(verify_text) ) #認證
        user_info_list.append( str(signature_file_first_line) ) #資訊列第一行
        user_info_list.append( str(vote_number) ) #投票編號
        user_info_list.append( str(support_or_against_text) ) #支持或反對
    
    output_rows.append(','.join(user_info_list))

    index = index + 1

to_csv(output_rows, '07_vote_checker.csv')

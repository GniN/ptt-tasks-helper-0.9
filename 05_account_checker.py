from PyPtt import PTT
from shared import Bot, to_csv, to_file_path

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


f = open(to_file_path('05_account_checker.txt'), 'r', encoding='utf-8')

index = 1

output_rows = ['id,修正後id,正確id,登入次數,有效文章數,退文文章數,上次登入ip,上次登入日期,帳號認證,罰單狀況']

for id in f:
    print(f'正在查詢第{index}筆資料')
    id = id.replace('\n', '')
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
        
        user_info_list.append(real_id) #正確id
        user_info_list.append( str(user.login_time) ) #登入次數
        user_info_list.append( str(user.legal_post) ) #有效文章數
        user_info_list.append( str(user.illegal_post) ) #退文文章數
        user_info_list.append( str(user.last_ip) ) #上次登入ip
        user_info_list.append( str(user.last_login) ) #上次登入日期
        user_info_list.append( str(verify_text) ) #認證
        user_info_list.append( str(signature_file_first_line) ) #認證        
    
    output_rows.append(','.join(user_info_list))

    index = index + 1


to_csv(output_rows, '05_account_checker.csv')

# '  此人違規 尚未繳交罰單 (已累計 1 次)'
# '\n此人違規 尚未繳交罰單 (已累計 1 次)'
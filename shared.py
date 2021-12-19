from PyPtt import PTT
import os, sys
import websockets.client

# determine if the application is a frozen `.exe` (e.g. pyinstaller --onefile) 
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
# or a script file (e.g. `.py` / `.pyw`)
elif __file__:
    application_path = os.path.dirname(__file__)

def Bot():
    f = open(os.path.join(application_path, "secrets.txt"), "r", encoding='utf-8')
    secretsRow = f.readline()
    secretsRowInfos = secretsRow.split(':')

    ptt_id = secretsRowInfos[0]
    password = secretsRowInfos[1]

    ptt_bot = PTT.API()
    try:
        ptt_bot.login(ptt_id, password)
    except PTT.exceptions.LoginError:
        ptt_bot.log('登入失敗')
        return None
    except PTT.exceptions.WrongIDorPassword:
        ptt_bot.log('帳號密碼錯誤')
        return None
    except PTT.exceptions.LoginTooOften:
        ptt_bot.log('請稍等一下再登入')
        return None
    ptt_bot.log('登入成功')

    return ptt_bot

def to_file_path(filename):
    return os.path.join(application_path, filename)

def to_csv(output_rows, filename):
    output_file = open(filename, "w", encoding="utf_8_sig")
    for row in output_rows:
        output_file.write(row + "\n")
    output_file.close()

filter_map = {
    # 搜尋關鍵字    / ?
    'KEYWORD': PTT.data_type.post_search_type.KEYWORD,
    # 搜尋作者      a
    'AUTHOR': PTT.data_type.post_search_type.AUTHOR,
    # 搜尋推文數    Z
    'PUSH': PTT.data_type.post_search_type.PUSH,
    # 搜尋標記      G
    'MARK': PTT.data_type.post_search_type.MARK,
    # 搜尋稿酬      A
    'MONEY': PTT.data_type.post_search_type.MONEY,
}

def to_search_list(filters):
    return [(filter_map[filter['type']], filter['value']) for filter in filters]
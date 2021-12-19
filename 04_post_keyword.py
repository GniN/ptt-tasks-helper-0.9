from PyPtt import PTT
from shared import Bot, to_csv, to_file_path
import json

ptt_bot = Bot()

with open(to_file_path('04_post_keyword.json'), encoding='utf-8') as json_file:
    data = json.load(json_file)


index = 0
board_name = data['board_name']
post_number = int(data['post_number'])
keywords = data['keywords']

output_rows = ['id,樓層,內容,時間,ip,推噓箭頭,重複出現']

print('正在解析文章')

post_info = ptt_bot.get_post(
        board_name,
        post_index=post_number)

print('解析文章成功')

author_list = []

floor_number = 0
for push in post_info.push_list:
    floor_number = floor_number + 1
    if len(keywords) > 0 and (not any(keyword in push.content for keyword in keywords)):
        continue

    push_type = ''
    if push.type == PTT.data_type.push_type.PUSH:
        push_type = '推'
    if push.type == PTT.data_type.push_type.BOO:
        push_type = '噓'
    if push.type == PTT.data_type.push_type.ARROW:
        push_type = '箭頭'

    has_shown = '否'
    if push.author in author_list:
        has_shown = '是'

    output_rows.append(
        ','.join([
            push.author,
            str(floor_number), 
            push.content, 
            str(push.time), 
            str(push.ip), 
            push_type,
            has_shown])
    )

    author_list.append(push.author)


to_csv(output_rows, '04_post_keyword.csv')
from PyPtt import PTT
from shared import Bot, to_csv, to_search_list, to_file_path
import json

ptt_bot = Bot()

with open(to_file_path('02_keyword_posts_in_board.json'), encoding='utf-8') as json_file:
    data = json.load(json_file)

index = 0
filters = data['filters']
board_name = data['board_name']
start_index = int(data['start_index'])

if start_index <= 0:
    print(f'start_index 必須大於0')
    exit()

output_rows = ['id,文章日期,文章標題,文章編號,ip,link,推,噓,箭頭']

search_list = to_search_list(filters)

newest_index = ptt_bot.get_newest_index(
    PTT.data_type.index_type.BBS,
    board_name,
    search_list=search_list)

print(f'找到 {newest_index} 篇文章')

for current_index in range(start_index, newest_index + 1):
    print(f'正在解析 {current_index}/{newest_index} 篇文章')
    post_info = ptt_bot.get_post(
        board_name,
        post_index=current_index,
        search_list=search_list)
    author_id = post_info.author.split(' ')[0]

    # PTT.data_type.push_type.PUSH
    # [ x for x in a if x == 1]

    push_type_list = list(map(lambda p: p.type, post_info.push_list))

    push_count = len([p for p in push_type_list if p == PTT.data_type.push_type.PUSH])
    boo_count = len([p for p in push_type_list if p == PTT.data_type.push_type.BOO])
    arrow_count = len([p for p in push_type_list if p == PTT.data_type.push_type.ARROW])

    output_rows.append(
        ','.join([
            author_id,
            str(post_info.date),
            str(post_info.title),
            str(post_info.aid),
            str(post_info.ip),
            str(post_info.web_url),
            str(push_count),
            str(boo_count),
            str(arrow_count),
            ])
    )
    

to_csv(output_rows, '02_keyword_posts_in_board.csv')
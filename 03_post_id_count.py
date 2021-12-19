from PyPtt import PTT
from shared import Bot, to_csv, to_file_path
import json

ptt_bot = Bot()

with open(to_file_path('03_post_id_count.json'), encoding='utf-8') as json_file:
    data = json.load(json_file)

index = 0
board_name = data['board_name']
post_number = int(data['post_number'])
ids = data['ids']

output_rows = ['id,出現次數,出現樓層']

print('正在解析文章')

post_info = ptt_bot.get_post(
        board_name,
        post_index=post_number)

author_push_map = {}

print('解析文章成功')

floor_number = 0
for push in post_info.push_list:
    floor_number = floor_number + 1
    if push.author not in ids:
        continue
    if push.author in author_push_map:
        author_push_map[push.author]['count'] = author_push_map[push.author]['count'] + 1
        author_push_map[push.author]['floor_numbers'].append(str(floor_number))
    else:
        author_push_map[push.author] = {'count': 1, 'floor_numbers': [str(floor_number)]}

for author in author_push_map:
    floor_number_string = '，'.join(author_push_map[author]['floor_numbers'])

    output_rows.append(
        ','.join([author, str(author_push_map[author]['count']), floor_number_string])
    )

to_csv(output_rows, '03_post_id_count.csv')
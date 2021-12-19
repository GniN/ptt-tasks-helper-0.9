from PyPtt import PTT
from shared import Bot, to_csv, to_file_path
import json

ptt_bot = Bot()



with open(to_file_path('01_id_posts_in_board.json'), encoding='utf-8') as json_file:
    data = json.load(json_file)


id_list = data['ids']
board_name = data['board_name']

output_rows = ['id,現存文章數,最新文章日期,最新文章標題,ip,link']

index = 0
for id in id_list:
    index = index + 1
    search_list = [
        (PTT.data_type.post_search_type.AUTHOR, id),
    ]

    try:    
        newest_index = ptt_bot.get_newest_index(
            PTT.data_type.index_type.BBS,
            board_name,
            search_list=search_list)
    except:
        output_rows.append(f'{id}')
        continue

    print(f'正在處理第{index}/{len(id_list)}筆資料: {id} 在 {board_name} 最新文章編號 {newest_index}')

    if newest_index > 0:
        print(f'正在解析文章')
        post = ptt_bot.get_post(
            board_name,
            post_index=newest_index,
            search_list=search_list
        )

        output_rows.append(
            ','.join([id, str(newest_index), str(post.date), str(post.title), str(post.ip), str(post.web_url)])
        )
    else:
        output_rows.append('id,')
    

to_csv(output_rows, '01_id_posts_in_board.csv')
## 帳號密碼
請將帳號密碼放在secrets.txt，格式如下
```
hsuan0904:mysupersafepassword
```

## 情況一

輸入：指定看板, 一排ID
輸出：ID, 現存文章數, 最新文章日期, 最新文章標題

輸入請放在
01_id_posts_in_board.txt

### 輸入檔案內容
```json
{
    "board_name": "image",
    "ids": [
        "hsuan0904",
        "hsuan0904"
    ]
}
```

## 情況二

輸入：指定看板, 指定標題關鍵字

輸出：ID, 文章日期, 文章標題, 推, 噓, 箭頭 等文章資訊

輸入請放在 
02_keyword_posts_in_board.json
```json
{
    "board_name": "image",
    "start_index": 1,
    "filters": [
        { "type": "KEYWORD", "value": "如果" }
    ]
}
```

支援的filter type如下
```
    # 搜尋關鍵字    / ?
    'KEYWORD'
    # 搜尋作者      a
    'AUTHOR'
    # 搜尋推文數    Z
    'PUSH'
    # 搜尋標記      G
    'MARK'
    # 搜尋稿酬      A
    'MONEY'
```


## 情況三

輸入：指定看板, 指定文章編號, 一排ID

輸出：ID, 出現次數, 出現樓層(可能有一串), 推文類型

輸入請放在 
03_post_id_count.txt

```json
{
    "board_name": "turtlesoup",
    "post_number": 33629,
    "ids": [
        "hsuan0904"
    ]
}
```

## 情況四

輸入：指定看板, 指定文章編號, 指定關鍵字

輸出：ID, 樓層, 內容, 時間, ip

輸入請放在 
04_post_keyword.txt

```json
{
    "board_name": "turtlesoup",
    "post_number": 33636,
    "keywords": [
        "金魚",
        "可達鴨"
    ]
}

```

## 情況五

輸入：一排ID

輸出：ID, 登入次數, 有效文章數, 退文文章數, 是否通過認證等資訊

輸入請放在 
05_account_checker.txt

```python
turtlesoup:33636:[活動] # 看板名稱:文章編號，請用分號分隔
```

## 附註
如果有pyptt尚未提供的功能，可以先做再自己的branch，並用以下方式安裝
```
pip install git+https://github.com/GniN/PyPtt.git
```
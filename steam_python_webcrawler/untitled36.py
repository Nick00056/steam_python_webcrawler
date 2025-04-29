import requests
from bs4 import BeautifulSoup
import time

# Steam搜尋頁面URL
url = "https://store.steampowered.com/search/"

# 設定HTTP標頭指定語系為繁體中文
headers = {
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}

# 搜尋條件設定
params = {
    "sort_by": "Price_ASC",  # 依價格由低到高排序
    "specials": 1,           # 只篩選特價商品
    "ndl": 1,                
    "start": 0,              # 起始索引位置
    "count": 10              # 每次取得10筆資料
}

# 建立一個Session保持連線
session = requests.Session()

# 控制是否繼續抓取的開關
keep_going = True

# 遊戲編號初始值
game_number = 1

# 進入抓取迴圈
while keep_going:
    time.sleep(0.5)  # 每次請求間隔0.5秒避免過快被封鎖

    # 發送GET請求
    response = session.get(url, headers=headers, params=params)
    
    # 更新start參數往後抓取下一批遊戲
    params["start"] += 10

    if response.status_code == 200:
        # 解析HTML網頁內容
        soup = BeautifulSoup(response.text, "html.parser")

        # 找出所有遊戲項目
        game_list = soup.find_all("a", class_="search_result_row ds_collapse_flag")

        # 逐一處理每款遊戲
        for game in game_list:
            # 如果已經抓到100款遊戲則停止
            if game_number > 100:
                keep_going = False
                break

            # 取得遊戲名稱
            title = game.find("span", class_="title")
            if title:
                print(f"第 {game_number} 個 遊戲名稱:", title.text)
            else:
                print("沒有找到遊戲名稱")
                continue

            # 取得遊戲連結
            link = game["href"]
            print("遊戲連結:", link)

            # 取得價格資訊
            final_price = game.find("div", class_="discount_final_price")
            discount = game.find("div", class_="discount_pct")
            original_price = game.find("div", class_="discount_original_price")

            # 取得發售日期
            release_date = game.find("div", class_="col search_released responsive_secondrow")

            # 取得評價資訊
            review = game.find("span", class_="search_review_summary")

            if final_price:
                # 清理並處理現在價格
                now_price = final_price.text.strip().replace(" ", "")
                price_num = now_price[4:]  # 去除貨幣符號與多餘字元
                
                # 若價格高於11元則停止繼續抓取
                if float(price_num) > 11:
                    keep_going = False
                    break

                # 顯示原價與現價
                if original_price:
                    print("原始價格:", original_price.text.strip())
                else:
                    print("原始價格: 無原價資訊")

                print("最終價格:", now_price)

                # 顯示折扣資訊
                if discount:
                    print("折扣為:", discount.text.strip())
                else:
                    print("折扣為: 無折扣資訊")

                # 顯示發售日期
                if release_date:
                    print("發行日期:", release_date.text.strip())
                else:
                    print("發行日期: 未知")

                # 根據折扣比例給出購買建議
                if discount:
                    discount_text = discount.text.strip()
                    discount_text = discount_text.replace("-", "").replace("%", "")
                    if discount_text.isdigit():
                        if int(discount_text) >= 50:
                            print("推薦程度: 建議購買")
                        else:
                            print("推薦程度: 可再觀望")
                    else:
                        print("推薦程度: 折扣格式錯誤")
                else:
                    print("推薦程度: 無折扣資訊")
            else:
                print("價格資訊: 未找到")

            # 顯示用戶評價
            if review:
                review_text = review.get("data-tooltip-html").replace("<br>", "").strip()
                print("遊戲評價:", review_text)
            else:
                print("遊戲評價: 無評價資訊")

            print("=" * 70)
            game_number += 1
    else:
        print("連線失敗")
#感謝教授撥空觀看

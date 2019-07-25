Python Appplication 1: card_Scrape.py 運用Selenium執行動態網頁的自動化操作，並運用Webdriver來控制Chrome 瀏覽器，尋找到標的卡片群組網頁擷取其 HTML，再運用PyQuery 解析各卡圖檔、網址、評等及賀詞等資訊。運用Request請求各卡圖檔，並依其原有檔名將全數百項縮圖儲存於local個人檔案資料夾。另外，運用csv 套件將全數百項卡片資訊，如卡片主題、圖檔網址、評等及賀詞儲存於一csv格式檔案以方便搜尋。

Python Appplication 2: python socket programming 的應用程式，實現的是簡單的多人聊天室的例子，就是允許多個人同時一起聊天，每個人傳送的訊息所有人都能接收到，類似於 QQ 群的功能，而不是點對點的 QQ 好友之間的聊天。
實現的有兩部分：
ChatRoom_server.py: 聊天伺服器，負責與使用者建立 Socket 連線，並將某個使用者傳送的訊息廣播到所有線上的使用者。
ChatRoom_client.py: 使用者聊天客戶端，可以輸入聊天的內容併發送，同時可以顯示其他使用者的訊息記錄。

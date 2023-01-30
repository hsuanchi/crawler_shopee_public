# 蝦皮爬蟲 + 賣家競品分析

## How to use：

1. install requirement
```
$ pip3 install -r requirement.txt
```

2. 修改 main.py 裡面的 input_shop_ids，放入自己想追蹤的店家
```
    user_dict = {
        'a0025071@gmail.com': {
            'user_info': {
                'Email': 'a0025071@gmail.com',
                'Name': 'Max',
            },
            'input_shop_name': [
                "fulinxuan",
                "pat6116xx",
                "join800127",
                "...."
            ],
            'input_product_ids': []
        }
    }
```


## Code-base structure

```
.
├── CHANGELOG.md
├── README.md
├── config
│   └── config.py
├── log
│   └── live_shopee_20xx-xx-xx.log
├── main.py
├── requirements.txt
└── view
    ├── api_v4_get_product_detail.py
    ├── api_v4_get_shop_detail.py
    ├── check_ip_pool.py
    ├── clean_data.sql
    ├── csv
    │   ├── pdp_detail.csv
    │   └── shop_detail.csv
    └── utils.py
```

## About Concurrency Programming

* [【Python教學】淺談 Concurrency Programming (多線程/多進程/協程比較)](https://www.maxlist.xyz/2020/04/09/concurrency-programming/)
* [【Python教學】淺談 GIL & Thread-safe & Atomic](https://www.maxlist.xyz/2020/03/15/gil-thread-safe-atomic/)
* [【Python教學】淺談 Coroutine 協程使用方法](https://www.maxlist.xyz/2020/03/29/python-coroutine/)
* [【Python教學】Async IO Design Patterns 範例程式](https://www.maxlist.xyz/2020/04/03/async-io-design-patterns-python/)
* [【實戰篇】 解析 Python 之父寫的 web crawler 異步爬蟲](https://www.maxlist.xyz/2020/04/05/async-python-crawler-snippets/)


## 計畫原由

最近老姐在經營蝦皮賣家，為了找到在蝦皮上最佳銷售策略，所以寫了這篇蝦皮賣家競品分析。

此次的目標很簡單，掌握競品情報來提高自己銷售業績：

  1. 數千個商品，上架優先順序策略
  2. 商品訂價策略
  3. 掌握競品營運狀況

首先我們挑選出蝦皮上同產業的競品商家，寫爬蟲程式取得相關公開數據，計算出競品總營業額 (銷售數量 x 銷售單價)。

<img src="https://github.com/hsuanchi/crawler_shopee_public/blob/master/img/00_競品整體餅圖-480x327.png" width="400">

### ㄧ. 上架商品優先順序策略
在儀表板中，點擊圓圈圈可以看到商品的資訊(如下圖)
<img src="https://github.com/hsuanchi/crawler_shopee_public/blob/master/img/shopee_BCG.jpg">

##### ▍引流款 (低價，高需求)
引流款的意義在於衝評價或是利用免運門檻來提高客單價進行收單。
<img src="https://github.com/hsuanchi/crawler_shopee_public/blob/master/img/02_引流款.png">

##### ▍地雷款 (低價，低需求)
地雷款基本上此區商品不是主要營收來源，上架商品順序的話，會建議盡量先避開此區商品。
<img src="https://github.com/hsuanchi/crawler_shopee_public/blob/master/img/03_地雷款.png">

##### ▍價值款 (高價，低需求)
價值款產品還需搭配銷銷售數量或售總交額來交叉看，如果是初期賣家建議在此區挑選銷售數量較多的先上架(如下圖)，既可以兼顧衝評價與銷售額。
<img src="https://github.com/hsuanchi/crawler_shopee_public/blob/master/img/04_價值款.png">
上架順序：價值款和引流款的優先順序可視個人依比例調整，但盡量避免先上地雷區的產品。

### 二. 商品訂價策略
此次要上架的商品是 1尺6 的七星劍，如下圖在左上輸入商品名稱和類型後，可以看到資料庫內此商品銷售總金額為 5,000 元，其中產品訂價在 270 ~ 350 之間。

Step 1 輸入商品名稱 & 商品類型：七星劍和 1尺6
Step 2 確認近期交易過商品訂價：價錢落在 270 ~ 350 之間
Step 3 查看 HashTag 和免運活動：點擊競品商品名稱可以看到資訊
<img src="https://github.com/hsuanchi/crawler_shopee_public/blob/master/img/05_蝦皮競品訂價.png">

### 三. 掌握競品數據
#### 1. 競品日銷售
##### ▍知己知彼，掌握對手每日銷售狀況

可以選擇指定商家，例如下圖點擊 金龍佛具 4/12日 3,750元，下方欄位則會列出金龍佛具 4/12 日所有銷售商品和類型出來。快速掌握競品每日銷售狀況
<img src="https://github.com/hsuanchi/crawler_shopee_public/blob/master/img/06_蝦皮賣家日銷售狀況.png">

#### 2. 競品週銷售
##### ▍情境題 – 週末是否影響業績？

週日和週一的銷售狀況表現最差，而週四和週五銷售狀態佳。如果你遇到週日銷售較差，別擔心大家 (佛具產業) 都跟你一樣。
<img src="https://github.com/hsuanchi/crawler_shopee_public/blob/master/img/07_週銷售額.png">

#### 3. 競品月銷售
##### ▍情境題 – 逢四天連假，競品業績如何？

這次的連假 (4/2~4/4 號)，可以看到競品銷售狀況表現佳，僅有最後一天 4/4 號的銷售低於水平。
<img src="https://github.com/hsuanchi/crawler_shopee_public/blob/master/img/08_月銷售額.png">

#### 4. 競品銷售相關數據
從公開資料中可以獲得總體營收、上架商品數和上架商品均價，而預測客單價和預測客戶購買商品數則是用其他綜合數據推測出來，與實際數字多少會有誤差。

* 總營收
* 上架商品數
* 上架商品均價
* 預測客單價
* 預測客戶購買商品數
<img src="https://github.com/hsuanchi/crawler_shopee_public/blob/master/img/09_蝦皮競品銷售.png">

#### 5. 商品評價數據
評分系統的資料可從 API 拉出來，從資料中可以看出蝦皮除了有使用者介面上的星等 (rating_star) 評價 (1~5分) 外，還額外將評價區分成優良評價 (rating_good)、中立評價 (rating_normal) 和負面評價 (rating_bad)

* 平均評分 (rating_star)
* 優良評價 (rating_good)
* 中立評價 (rating_normal)
* 負面評價 (rating_bad)
猜測在搜尋商品排名中，這三欄應該影響商品排名的重要參數之一，不然不會額外再獨立欄位出來。
<img src="https://github.com/hsuanchi/crawler_shopee_public/blob/master/img/10_蝦皮競品整體狀況.png">

### 最後
##### ▍回顧本篇我們介紹了的內容：

1. 上架商品優先順序策略
    * 引流款 (低價，高需求)
    * 地雷款 (低價，低需求)
    * 價值款 (高價，低需求)
2. 商品訂價策略
3. 掌握競品數據
    * 日銷售
    * 週銷售
    * 月銷售
4. 銷售相關數據
5. 商品評價數據

本篇同步發佈至部落格[【數據分析】蝦皮賣家競品分析｜Max行銷誌](https://www.maxlist.xyz/2020/04/14/shopee-crawler/)

# 📚 Week 3 練習題系統

> **完整的 MultiIndex、GroupBy、Pivot Table 實戰練習**
>
> 包含 37 道精心設計的題目，從基礎到挑戰，涵蓋所有核心技能

---

## 🎯 系統概覽

本練習系統包含 **4 個主要文件**，提供完整的學習路徑：

| 文件 | 題數 | 難度分布 | 預計時間 |
|------|------|---------|---------|
| **Exercise_01** | 12 題 | 🟢×4 🟡×4 🔴×4 | 2-4 小時 |
| **Exercise_02** | 15 題 | 🟢×5 🟡×6 🔴×4 | 3-5 小時 |
| **Exercise_03** | 10 題 | 🟢×3 🟡×4 🔴×3 | 2-3 小時 |
| **Solutions** | 37 題解答 | 完整詳解 | 參考用 |

**總計：37 題 | 預計完成時間：7-12 小時**

---

## 📁 文件結構

```
exercises/
├── README.md                                    # 📘 本文件
├── Exercise_01_MultiIndex_12_Questions.md      # 🎯 MultiIndex 練習（12 題）
├── Exercise_02_GroupBy_15_Questions.md         # 🎯 GroupBy 練習（15 題）
├── Exercise_03_Pivot_10_Questions.md           # 🎯 Pivot Table 練習（10 題）
└── Solutions_Complete.md                       # 📖 完整解答（37 題）
```

---

## 📝 Exercise 01: MultiIndex 實戰（12 題）

**檔案：** `Exercise_01_MultiIndex_12_Questions.md`

### 內容涵蓋

#### 🟢 基礎題（1-4 題）
- ✅ 使用 `groupby()` 自動建立 MultiIndex
- ✅ 使用 `from_tuples()` 手動建立 MultiIndex
- ✅ 使用 `.loc[]` 進行單層與雙層切片
- ✅ 理解 MultiIndex 的索引結構

#### 🟡 進階題（5-8 題）
- ✅ 使用 `IndexSlice` 進行複雜範圍選取
- ✅ 使用 `.xs()` 跨層選取資料
- ✅ 使用 `stack()` / `unstack()` 轉換寬窄表
- ✅ 使用 `swaplevel()` 與 `sort_index()` 調整索引順序

#### 🔴 挑戰題（9-12 題）
- ✅ 建立三層 MultiIndex（時間 × 地區 × 類別）
- ✅ 結合 GroupBy 進行複雜聚合
- ✅ 生成包含小計與總計的報表
- ✅ 建立動態 MultiIndex 儀表板函數

### 學習目標

完成此練習後，你將能夠：
- 熟練建立與操作 MultiIndex
- 理解 MultiIndex 與 Excel 樞紐表的對應關係
- 掌握多層索引的切片技巧
- 能夠處理複雜的多維度資料分析

---

## 📝 Exercise 02: GroupBy 進階實戰（15 題）

**檔案：** `Exercise_02_GroupBy_15_Questions.md`

### 內容涵蓋

#### 🟢 基礎題（1-5 題）
- ✅ 基礎 `groupby()` + 單一聚合函數
- ✅ 使用 `.agg([...])` 多函數聚合
- ✅ 使用字典形式的 `agg()` 對不同欄位應用不同函數
- ✅ 計算分組後的衍生指標
- ✅ 時間序列分組與月度趨勢分析

#### 🟡 進階題（6-11 題）
- ✅ 使用 **Named Aggregation** 命名聚合
- ✅ 使用 `transform()` 進行組內計算（百分比、標準化）
- ✅ 比較 `transform()` vs `apply()` 的效能差異
- ✅ 使用 `filter()` 篩選符合條件的組
- ✅ 結合 `filter()` 與 `transform()`

#### 🔴 挑戰題（12-15 題）
- ✅ 自訂聚合函數（眾數、加權平均等）
- ✅ 實作複雜商業邏輯（RFM 客戶分群模型）
- ✅ 多層 GroupBy 分析（時間 × 地區 × 類別）
- ✅ 計算同比成長率（YoY）與環比成長率（MoM）

### 學習目標

完成此練習後，你將能夠：
- 掌握 GroupBy 的核心方法（agg, transform, filter, apply）
- 能夠建立自訂聚合函數
- 理解組內計算與組間比較的差異
- 能夠實作複雜的資料分析模型

---

## 📝 Exercise 03: Pivot Table 透視表實戰（10 題）

**檔案：** `Exercise_03_Pivot_10_Questions.md`

### 內容涵蓋

#### 🟢 基礎題（1-3 題）
- ✅ 建立基本 `pivot_table()`（單維度、雙維度）
- ✅ 使用 `margins=True` 新增總計列與欄
- ✅ 同時顯示多個值與多個聚合函數

#### 🟡 進階題（4-7 題）
- ✅ 多函數聚合透視表
- ✅ 計算百分比透視表（列、欄、總計百分比）
- ✅ 使用 `stack()` / `unstack()` 轉換寬窄表
- ✅ 使用 `melt()` 進行逆透視（寬表變長表）

#### 🔴 挑戰題（8-10 題）
- ✅ 建立動態透視表生成函數
- ✅ 建立綜合儀表板（多個關聯透視表）
- ✅ 使用 `.style` API 套用條件格式與視覺化

### 學習目標

完成此練習後，你將能夠：
- 熟練使用 `pivot_table()` 與 `crosstab()`
- 掌握寬窄表轉換技巧
- 能夠建立專業的商業報表
- 理解 pandas 透視表與 Excel 樞紐表的對應關係

---

## 📖 Solutions_Complete.md

**檔案：** `Solutions_Complete.md`

### 解答結構

每題包含 **8 個部分**：

1. **題目回顧** - 快速回顧題目要求
2. **解題思路** - 3-5 個步驟的解題邏輯
3. **完整代碼** - 可直接執行的完整代碼（含註釋）
4. **輸出結果** - 預期的執行結果範例
5. **代碼說明** - 逐行解釋關鍵代碼
6. **知識點總結** - 該題涉及的核心知識點
7. **常見錯誤** - 初學者容易犯的錯誤與正確做法
8. **延伸練習** - 進階練習建議

### 解答示範

```markdown
## 🟢 題 1：建立地區 × 產品類別 MultiIndex

### 題目回顧
建立「客戶州別 × 產品類別」的雙層索引...

### 解題思路
1. 載入資料：載入 orders, order_items, products, customers
2. 合併資料：使用 merge 連接多張表
3. 建立 MultiIndex：使用 groupby 自動建立
4. 計算總額：對 price 欄位加總
5. 輸出結果：查看索引結構

### 完整代碼
```python
import pandas as pd
# ... 完整可執行代碼 ...
```

### 輸出結果
```
customer_state  product_category_name
SP              cama_mesa_banho          $254,567.89
                beleza_saude             $198,765.43
...
```

### 代碼說明
- Line 5-8：載入四張資料表
- Line 11：使用 merge() 連接訂單與客戶
...

### 知識點總結
✅ MultiIndex 建立方式 1：groupby 自動建立
✅ merge 連接多張表
...

### 常見錯誤
❌ 錯誤 1：忘記指定 how='left'
✅ 正確做法：...

### 延伸練習
1. 轉換為 DataFrame 並重置索引
2. 計算每個州別的產品類別數量
...
```

---

## 🚀 使用指南

### 📖 推薦學習路徑

#### 階段 1：基礎建立（Week 1）
1. 閱讀 `Exercise_01_MultiIndex_12_Questions.md` 基礎題（1-4 題）
2. 動手實作，嘗試獨立完成
3. 對照 `Solutions_Complete.md` 檢視解答
4. 重點關注「知識點總結」與「常見錯誤」

#### 階段 2：進階技巧（Week 2）
1. 完成 Exercise 01 進階題（5-8 題）
2. 完成 Exercise 02 基礎+進階題（1-11 題）
3. 練習建立自己的函數與工具
4. 嘗試「延伸練習」

#### 階段 3：實戰挑戰（Week 3）
1. 完成所有挑戰題（🔴）
2. 完成 Exercise 03 全部題目
3. 自己建立一個完整的資料分析項目
4. 整合 MultiIndex、GroupBy、Pivot Table

### 💡 學習技巧

#### ✅ DO（建議做法）
- ✅ **先思考再看答案**：嘗試獨立解題至少 15 分鐘
- ✅ **動手實作**：必須親自執行代碼，不要只看
- ✅ **理解而非記憶**：理解背後的邏輯，而非死記語法
- ✅ **筆記重點**：記錄常見錯誤與關鍵知識點
- ✅ **舉一反三**：完成延伸練習，應用到不同資料集

#### ❌ DON'T（避免做法）
- ❌ **直接看答案**：不經思考直接看解答
- ❌ **只看不做**：只閱讀代碼而不執行
- ❌ **跳過基礎題**：直接挑戰困難題目
- ❌ **忽略錯誤**：遇到錯誤不深入理解原因
- ❌ **孤立學習**：不將技能整合應用

### 🎯 完成檢核表

複製以下檢核表到你的筆記，追蹤學習進度：

```markdown
## Exercise 01: MultiIndex（12 題）
- [ ] 題 1：建立 MultiIndex
- [ ] 題 2：from_tuples
- [ ] 題 3：loc 單層切片
- [ ] 題 4：loc 雙層切片
- [ ] 題 5：IndexSlice
- [ ] 題 6：xs 跨層選取
- [ ] 題 7：stack/unstack
- [ ] 題 8：swaplevel
- [ ] 題 9：三層 MultiIndex
- [ ] 題 10：複雜聚合
- [ ] 題 11：報表生成
- [ ] 題 12：動態儀表板

## Exercise 02: GroupBy（15 題）
- [ ] 題 1-5：基礎聚合
- [ ] 題 6：Named Aggregation
- [ ] 題 7-8：Transform
- [ ] 題 9：Transform vs Apply
- [ ] 題 10-11：Filter
- [ ] 題 12：自訂聚合函數
- [ ] 題 13：加權平均
- [ ] 題 14：多層分析
- [ ] 題 15：RFM 模型

## Exercise 03: Pivot Table（10 題）
- [ ] 題 1-3：基礎透視表
- [ ] 題 4-5：多函數聚合
- [ ] 題 6-7：寬窄表轉換
- [ ] 題 8：動態透視表函數
- [ ] 題 9：綜合儀表板
- [ ] 題 10：條件格式
```

---

## 📊 資料集說明

### Olist 巴西電商資料

所有練習使用 **Olist 巴西電商公開資料集**，包含：

| 資料表 | 筆數 | 說明 |
|--------|------|------|
| `olist_orders_dataset.csv` | 99,441 | 訂單主檔 |
| `olist_order_items_dataset.csv` | 112,650 | 訂單明細 |
| `olist_products_dataset.csv` | 32,951 | 產品資訊 |
| `olist_customers_dataset.csv` | 99,441 | 客戶資訊 |
| `olist_sellers_dataset.csv` | 3,095 | 賣家資訊 |
| `olist_order_reviews_dataset.csv` | 99,224 | 訂單評價 |

**資料路徑：**
```python
base_path = '/mnt/data/datasets/ecommerce/olist/'
```

### 資料欄位說明

#### 訂單表（orders）
- `order_id`：訂單 ID
- `customer_id`：客戶 ID
- `order_status`：訂單狀態
- `order_purchase_timestamp`：購買時間

#### 訂單明細表（order_items）
- `order_id`：訂單 ID
- `order_item_id`：訂單項目 ID
- `product_id`：產品 ID
- `seller_id`：賣家 ID
- `price`：商品價格
- `freight_value`：運費

#### 產品表（products）
- `product_id`：產品 ID
- `product_category_name`：產品類別

#### 客戶表（customers）
- `customer_id`：客戶 ID
- `customer_unique_id`：客戶唯一 ID
- `customer_state`：客戶所在州

---

## 🔗 相關資源

### 課程資料
- 📘 **Day01_MultiIndex_Complete_Guide.md** - MultiIndex 完整教學
- 📘 **Day02_GroupBy_Advanced.md** - GroupBy 進階教學
- 📘 **Day03_Pivot_Table_Master.md** - Pivot Table 精通指南

### 官方文件
- [pandas MultiIndex 官方文件](https://pandas.pydata.org/docs/user_guide/advanced.html)
- [pandas GroupBy 官方文件](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [pandas Reshaping 官方文件](https://pandas.pydata.org/docs/user_guide/reshaping.html)

### 延伸學習
- Week 4: 時間序列分析
- Week 5: 資料清理與前處理
- Week 6: 視覺化與報表設計

---

## ❓ 常見問題（FAQ）

### Q1: 我應該按順序完成所有題目嗎？
**A:** 建議按順序完成基礎題與進階題，但挑戰題可以根據興趣選擇。確保基礎扎實後再挑戰困難題目。

### Q2: 完成一題需要多少時間？
**A:**
- 基礎題：5-10 分鐘
- 進階題：10-20 分鐘
- 挑戰題：20-30 分鐘

如果超過預計時間，可以參考「解題思路」獲得提示。

### Q3: 我的答案與解答不同，是錯的嗎？
**A:** 不一定！pandas 通常有多種方法達成同樣目標。只要：
- ✅ 結果正確
- ✅ 邏輯清晰
- ✅ 效能合理

你的答案就是有效的。可以比較不同方法的優缺點。

### Q4: 遇到錯誤該怎麼辦？
**A:**
1. 仔細閱讀錯誤訊息
2. 檢查資料型態與索引結構
3. 參考解答中的「常見錯誤」章節
4. 使用 `print()` 與 `.info()` 檢視中間結果

### Q5: 如何驗證答案正確性？
**A:**
1. 檢查結果的資料型態（Series, DataFrame, MultiIndex）
2. 檢查資料筆數是否符合預期
3. 使用 `.head()`, `.tail()` 查看資料
4. 計算總和、平均等統計量驗證邏輯

### Q6: 可以使用 AI 輔助學習嗎？
**A:** 可以！但建議：
- ✅ 先獨立思考至少 15 分鐘
- ✅ 使用 AI 解釋錯誤訊息
- ✅ 請 AI 解釋複雜的語法
- ❌ 不要直接要求 AI 給出完整答案

---

## 📞 支援與反饋

### 發現錯誤？
如果您發現題目或解答有錯誤，請：
1. 記錄錯誤位置（檔案名稱與行號）
2. 描述問題與預期行為
3. 提供改進建議

### 有建議？
歡迎提供：
- 新題目建議
- 難度調整建議
- 解答改進建議
- 延伸資源推薦

---

## 🎓 完成後的下一步

恭喜完成 Week 3 的所有練習！你已經掌握：

### ✅ 核心技能
- MultiIndex 多層索引的建立與操作
- GroupBy 分組聚合與組內計算
- Pivot Table 透視表與寬窄轉換
- 複雜資料分析與報表生成

### 🚀 進階方向

#### 方向 1：深化技能
- 挑戰更大的資料集（百萬筆以上）
- 優化代碼效能（向量化、避免迴圈）
- 建立可重用的分析模組

#### 方向 2：整合應用
- 結合視覺化（matplotlib, seaborn, plotly）
- 建立自動化報表系統
- 開發互動式儀表板（Streamlit, Dash）

#### 方向 3：實戰項目
- 分析真實商業資料
- 參加 Kaggle 競賽
- 建立個人資料分析作品集

---

## 📜 授權與使用

本練習系統為教學用途設計，歡迎：
- ✅ 個人學習使用
- ✅ 教學分享使用
- ✅ 修改與改進

請保留原作者資訊並註明出處。

---

**準備好了嗎？開始你的 pandas 進階之旅！💪**

祝學習順利！🎉

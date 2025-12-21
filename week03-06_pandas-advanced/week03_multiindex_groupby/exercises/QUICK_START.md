# ⚡ 快速開始指南

> 5 分鐘快速上手 Week 3 練習題系統

---

## 🎯 系統簡介

**37 道題目 | 3 大主題 | 完整解答**

```
📦 Week 3 練習題系統
├── 🎯 Exercise 01: MultiIndex（12 題）
├── 🎯 Exercise 02: GroupBy（15 題）
├── 🎯 Exercise 03: Pivot Table（10 題）
└── 📖 Solutions: 完整解答（37 題）
```

---

## 🚀 立即開始

### Step 1: 檢查資料集

確認 Olist 資料集路徑正確：

```python
import pandas as pd
import os

base_path = '/mnt/data/datasets/ecommerce/olist/'

# 檢查資料集是否存在
required_files = [
    'olist_orders_dataset.csv',
    'olist_order_items_dataset.csv',
    'olist_products_dataset.csv',
    'olist_customers_dataset.csv',
]

for file in required_files:
    filepath = os.path.join(base_path, file)
    if os.path.exists(filepath):
        print(f"✅ {file}")
    else:
        print(f"❌ {file} - 找不到檔案")
```

### Step 2: 選擇起點

根據你的程度選擇起點：

| 你的程度 | 建議起點 | 預計時間 |
|---------|---------|---------|
| 🌱 初學者 | Exercise 01, 題 1-4 | 30-60 分鐘 |
| 🌿 有基礎 | Exercise 01, 題 5-8 | 1-2 小時 |
| 🌳 進階者 | Exercise 02, 題 1-5 | 1-2 小時 |
| 🌲 高手 | 挑戰題（🔴） | 2-3 小時 |

### Step 3: 開始第一題

**📝 Exercise 01, 題 1：建立地區 × 產品類別 MultiIndex**

1. 打開 `Exercise_01_MultiIndex_12_Questions.md`
2. 閱讀題目 1 的情境與任務
3. 嘗試獨立完成（15 分鐘）
4. 卡住了？查看「提示」區塊
5. 完成後對照 `Solutions_Complete.md` 的解答

---

## 📋 3 種使用模式

### 模式 1：循序漸進（推薦新手）

```
Day 1-2: Exercise 01 基礎題（1-4）
Day 3-4: Exercise 01 進階題（5-8）
Day 5-6: Exercise 01 挑戰題（9-12）
Day 7-9: Exercise 02 基礎+進階（1-11）
...
```

### 模式 2：主題學習（推薦有基礎）

```
Week 1: 完成所有 MultiIndex 題目（Exercise 01）
Week 2: 完成所有 GroupBy 題目（Exercise 02）
Week 3: 完成所有 Pivot Table 題目（Exercise 03）
```

### 模式 3：挑戰模式（推薦進階者）

```
直接挑戰所有 🔴 挑戰題：
- Exercise 01: 題 9-12
- Exercise 02: 題 12-15
- Exercise 03: 題 8-10
```

---

## 💡 學習技巧

### ✅ 5 個高效學習法則

#### 1️⃣ **先思考後查答案**
```
❌ 直接看解答
✅ 思考 15 分鐘 → 查提示 → 再思考 10 分鐘 → 對照解答
```

#### 2️⃣ **動手實作**
```
❌ 只看代碼
✅ 親自執行 → 修改參數 → 觀察結果變化
```

#### 3️⃣ **筆記重點**
```
記錄：
- 新學到的方法
- 常見錯誤
- 最佳實踐
- 待研究的主題
```

#### 4️⃣ **舉一反三**
```
完成一題後：
- 嘗試不同的參數
- 應用到其他欄位
- 結合其他方法
- 完成延伸練習
```

#### 5️⃣ **建立知識地圖**
```
MultiIndex
├── 建立方式
│   ├── groupby 自動建立
│   ├── from_tuples
│   ├── from_arrays
│   └── from_product
├── 切片方式
│   ├── .loc[]
│   ├── IndexSlice
│   └── .xs()
└── 轉換方式
    ├── stack/unstack
    └── swaplevel
```

---

## 🎯 第一天學習計劃

**目標：完成 Exercise 01 的前 4 題（基礎題）**

### ⏰ 時間分配（共 2 小時）

```
09:00-09:15  環境準備 & 資料檢查
09:15-09:45  題 1：建立 MultiIndex（30 分鐘）
09:45-10:15  題 2：from_tuples（30 分鐘）
10:15-10:25  休息 ☕
10:25-10:50  題 3：loc 單層切片（25 分鐘）
10:50-11:15  題 4：loc 雙層切片（25 分鐘）
11:15-11:30  複習 & 筆記整理
```

### 📝 檢核點

- [ ] 能夠使用 `groupby()` 建立 MultiIndex
- [ ] 能夠使用 `from_tuples()` 手動建立 MultiIndex
- [ ] 能夠使用 `.loc[]` 進行單層切片
- [ ] 能夠使用 `.loc[('A', 'B')]` 進行雙層切片
- [ ] 理解 MultiIndex 的索引結構

---

## 📊 進度追蹤

### 方法 1：使用檢核表

複製到筆記：

```markdown
## 我的學習進度

### Exercise 01: MultiIndex
- [ ] ✅ 題 1 (完成日期: ____)
- [ ] ✅ 題 2 (完成日期: ____)
- [ ] ✅ 題 3 (完成日期: ____)
...

### 學習筆記
- 今天學到：____
- 遇到困難：____
- 明天計劃：____
```

### 方法 2：使用試算表

| 日期 | 題目 | 狀態 | 時間 | 困難點 | 心得 |
|------|------|------|------|--------|------|
| 2024-12-11 | Ex01-Q1 | ✅ | 25 分 | merge 順序 | 理解連接邏輯 |
| 2024-12-11 | Ex01-Q2 | ✅ | 20 分 | tuple 格式 | 注意逗號 |
| ... | ... | ... | ... | ... | ... |

---

## 🆘 遇到問題？

### 常見問題速查

#### Q: 執行代碼出現 `FileNotFoundError`
```python
# ❌ 錯誤
base_path = '/wrong/path/'

# ✅ 正確
base_path = '/mnt/data/datasets/ecommerce/olist/'

# 或使用相對路徑
base_path = '../../../data/olist/'
```

#### Q: `KeyError` 錯誤
```python
# ❌ MultiIndex 錯誤切片
sales['SP', 'eletronicos']

# ✅ 正確
sales.loc[('SP', 'eletronicos')]
```

#### Q: 合併後資料筆數不對
```python
# ❌ 預設 inner join
df = orders.merge(customers, on='customer_id')

# ✅ 使用 left join 保留所有訂單
df = orders.merge(customers, on='customer_id', how='left')
```

#### Q: 找不到解答對應的題目
```python
# 解答文件結構：
# Part 1: MultiIndex 解答（題 1-12）
#   → 對應 Exercise_01_MultiIndex_12_Questions.md
# Part 2: GroupBy 解答（題 13-27）
#   → 對應 Exercise_02_GroupBy_15_Questions.md
#     （題號 13-27 = 原 Exercise 02 的題 1-15）
# Part 3: Pivot Table 解答（題 28-37）
#   → 對應 Exercise_03_Pivot_10_Questions.md
#     （題號 28-37 = 原 Exercise 03 的題 1-10）
```

---

## 🎉 完成里程碑

### 🏆 成就系統

| 成就 | 條件 | 獎勵 |
|------|------|------|
| 🌱 入門者 | 完成 Exercise 01 基礎題（1-4） | 掌握 MultiIndex 基礎 |
| 🌿 進階者 | 完成 Exercise 01 全部（1-12） | 掌握 MultiIndex 進階 |
| 🌳 熟練者 | 完成 Exercise 01-02 全部（27 題） | 掌握 GroupBy 核心 |
| 🌲 專家 | 完成全部 37 題 | 成為 pandas 進階使用者 |
| 💎 大師 | 完成全部 + 所有延伸練習 | pandas 大師級技能 |

### 📜 學習證明

完成所有題目後，你可以：

1. **建立作品集**
   - 將解題代碼整理成 Jupyter Notebook
   - 上傳到 GitHub
   - 附上說明與心得

2. **分享經驗**
   - 撰寫學習心得文章
   - 在社群分享學習歷程
   - 幫助其他學習者

3. **應用實戰**
   - 使用學到的技能分析真實資料
   - 參加 Kaggle 競賽
   - 建立自己的資料分析項目

---

## 📚 推薦資源

### 官方文件
- [pandas MultiIndex](https://pandas.pydata.org/docs/user_guide/advanced.html)
- [pandas GroupBy](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [pandas Reshaping](https://pandas.pydata.org/docs/user_guide/reshaping.html)

### 延伸閱讀
- Week 2: Excel 進階與 pandas 基礎
- Week 4: 時間序列分析
- Week 5: 資料清理與前處理

---

## ✅ 準備完成檢核

開始前確認：

- [ ] ✅ 已安裝 pandas（版本 >= 1.3.0）
- [ ] ✅ 已確認資料集路徑正確
- [ ] ✅ 已閱讀 README.md
- [ ] ✅ 已準備好筆記本（實體或數位）
- [ ] ✅ 已規劃學習時間（每天至少 1 小時）

**一切就緒？開始你的學習之旅！** 🚀

---

## 💬 最後的建議

> **"學習最好的方式就是實作。不要害怕犯錯，每個錯誤都是學習的機會。"**

### 三個心態調整

1. **耐心**：每題花時間思考，不要急著看答案
2. **好奇**：嘗試不同的方法，探索 pandas 的能力
3. **堅持**：遇到困難是正常的，堅持下去就會進步

### 下一步行動

1. **現在**：打開 `Exercise_01_MultiIndex_12_Questions.md`
2. **今天**：完成前 2 題
3. **本週**：完成 Exercise 01 全部
4. **本月**：完成全部 37 題

**準備好了嗎？Let's go!** 💪

# Week 5: Apply/Transform/Agg 深度應用系統

## 📋 課程概述

這是一套完整的 Pandas **Apply、Transform、Agg** 三大核心功能的深度教學系統，涵蓋：

- **4 份教學指南**（Day 09-12）
- **37 道練習題**（Easy/Medium/Hard 三個難度）
- **完整的客戶分析系統**（整合三大方法）
- **詳細的解答與對標**

### 學習目標

完成本課程後，你將能夠：

✓ 設計複雜的會員評級系統（Apply）
✓ 實現組內相對分析（Transform）
✓ 生成多維度聚合報表（Agg）
✓ 構建完整的 RFM 客戶分析系統
✓ 從 Excel 轉換複雜邏輯到 Python
✓ 優化代碼性能（Apply vs 向量化）

---

## 📚 課程結構

### 教學指南（4 份）

| 文件 | 時長 | 主要內容 |
|------|------|---------|
| **Day09_Apply_Deep_Dive_Guide.md** | 2-3h | Series/DataFrame apply、自訂函數、15 個案例 |
| **Day10_Transform_Guide.md** | 2.5-3h | Transform 基礎、標準化、排名、10 個案例 |
| **Day11_Agg_Named_Guide.md** | 2.5-3h | Named Agg、自訂聚合、報表生成、12 個案例 |
| **Day12_Practice_Integration.md** | 3-4h | 完整客戶分析系統（RFM、分群、流失預警） |

**總學習時間**: 10-13 小時

### 練習題系統（3 份）

| 文件 | 題數 | 難度分佈 |
|------|------|---------|
| **Exercise_07_Apply_15_Questions.md** | 15 | 🟢5 + 🟡6 + 🔴4 |
| **Exercise_08_Transform_10_Questions.md** | 10 | 🟢3 + 🟡4 + 🔴3 |
| **Exercise_09_Agg_12_Questions.md** | 12 | 🟢4 + 🟡5 + 🔴3 |

**總題數**: 37 道

### 輔助資源（3 份）

- **Solutions_Complete.md** - 前 5 題詳細解答
- **QUICK_START.md** - 快速開始指南
- **INDEX.md** - 完整題目索引

---

## 🎯 核心概念對比

### Apply vs Transform vs Agg

```
操作          輸入      輸出形狀    典型用途
═══════════════════════════════════════════════════════
Apply        Series    標量或Series  複雜邏輯、轉換
Transform    Series    Series(保持)  組內相對計算
Agg          Series    標量         統計聚合
```

### 實例對比

```python
data = pd.DataFrame({
    'city': ['北京', '北京', '北京', '上海', '上海'],
    'sales': [100, 150, 120, 200, 180]
})

# Apply: 複雜邏輯分類
data['level'] = data['sales'].apply(
    lambda x: '高' if x > 150 else '低'
)  # 返回 Series，5 行

# Transform: 廣播城市平均
data['city_avg'] = data.groupby('city')['sales'].transform('mean')
  # 返回 Series，5 行，值重複

# Agg: 統計聚合
result = data.groupby('city')['sales'].agg('mean')
  # 返回 Series，2 行，每個城市一行
```

---

## 📖 推薦學習路徑

### 初級（Week 1）

1. **Day 09: Apply 基礎** (2小時)
   - Series.apply 簡單函數
   - 字符串清洗案例
   - 基本性能認識

2. **Day 10: Transform 基礎** (2小時)
   - Transform 核心概念
   - 組內平均廣播
   - 簡單排名

3. **練習**: Exercise 07 (Easy) + Exercise 08 (Easy)

### 中級（Week 2）

4. **Day 09: Apply 進階** (1小時)
   - DataFrame.apply(axis=1)
   - 會員評級系統
   - RFM 評分

5. **Day 10: Transform 進階** (1小時)
   - Z-score 標準化
   - 組內排名
   - 異常值檢測

6. **Day 11: Named Agg 基礎** (1.5小時)
   - 基本語法
   - 多欄位聚合
   - 簡單報表

7. **練習**: Exercise 07 (Medium) + Exercise 08 (Medium) + Exercise 09 (Easy)

### 高級（Week 3）

8. **Day 11: Named Agg 進階** (1小時)
   - 自訂聚合函數
   - 加權平均
   - 複雜報表

9. **Day 12: 完整整合** (3-4小時)
   - RFM 分析系統
   - 客戶分群
   - 流失預警
   - 行銷建議

10. **練習**: Exercise 07 (Hard) + Exercise 08 (Hard) + Exercise 09 (Medium/Hard) + Solutions 對標

---

## 🎓 關鍵知識點

### Apply（複雜邏輯）

**何時使用：**
- ✓ 多條件判斷（IF-THEN-ELSE）
- ✓ 自訂複雜轉換
- ✓ 處理特殊邏輯

**不用 Apply 的時候：**
- ❌ 簡單數學運算 → 直接向量化
- ❌ 字符串操作 → 使用 .str 方法
- ❌ 簡單分類 → 使用 pd.cut/pd.qcut

### Transform（相對計算）

**核心特性：**
- ✓ 保持原始行數
- ✓ 自動廣播
- ✓ 適合組內相對

**典型應用：**
- 組內平均廣播
- Z-score 標準化
- 排名計算
- 占比計算

### Agg（聚合統計）

**Named Agg 優勢：**
- ✓ 列名清晰
- ✓ 易於訪問
- ✓ 代碼可維護

**多層聚合：**
- 多分組列
- 多聚合函數
- 多源欄位

---

## 💡 實戰案例

### 1. 會員等級評定（Apply）

```python
def assign_member_level(row):
    if row['total_spent'] >= 5000 and row['orders'] >= 10:
        return '白金'
    elif row['total_spent'] >= 2000 or row['orders'] >= 5:
        return '黃金'
    else:
        return '銀牌'

customer_data['level'] = customer_data.apply(assign_member_level, axis=1)
```

### 2. 客戶排名（Transform）

```python
# 計算每個城市內的客戶排名
customer_data['city_rank'] = customer_data.groupby('city')['total_spent'].transform(
    lambda x: x.rank(ascending=False)
)

# 計算城市內的百分位
customer_data['city_percentile'] = customer_data.groupby('city')['total_spent'].transform(
    lambda x: x.rank(pct=True) * 100
)
```

### 3. 聚合報表（Agg）

```python
# 按地區生成銷售報表
region_report = sales_data.groupby('region').agg(
    total_revenue=('amount', 'sum'),
    num_customers=('customer_id', 'nunique'),
    avg_order_value=('amount', 'mean'),
    num_transactions=('amount', 'count')
)
```

### 4. 完整 RFM 系統（整合三者）

見 **Day12_Practice_Integration.md**

---

## 🔧 技術棧需求

### 必須
- Python 3.7+
- Pandas 1.0+
- NumPy 1.15+

### 推薦
- Jupyter Notebook（練習）
- VS Code（代碼編寫）
- Matplotlib（可視化）

### 數據源
- Olist 巴西電商真實數據集
- 提供：orders、customers、products、order_items 等

---

## 📊 效能參考

### Apply vs 向量化

```
簡單運算 (乘法):
  Apply:      0.2156 秒
  Vectorized: 0.0012 秒
  性能提升:   179.7 倍 ⚡

分類運算:
  Apply:      0.1845 秒
  Vectorized: 0.0018 秒
  性能提升:   102.5 倍 ⚡

條件賦值:
  Apply:      0.1923 秒
  Vectorized: 0.0015 秒
  性能提升:   128.2 倍 ⚡

(基於 100,000 行數據測試)
```

### 建議

- **10K 行以下**: Apply 可接受
- **10K-100K**: 考慮向量化
- **100K+**: 必須向量化

---

## ✅ 檢查清單

使用本課程前，確認你已掌握：

- [ ] GroupBy 基本操作 (groupby.agg, groupby.sum 等)
- [ ] Series vs DataFrame 的區別
- [ ] 基本的 Lambda 函數
- [ ] Pandas 索引和切片
- [ ] 缺失值處理 (fillna, dropna)

完成本課程後，你能：

- [ ] 設計複雜的 apply 函數
- [ ] 理解 transform 的廣播機制
- [ ] 使用 Named Agg 生成清晰的報表
- [ ] 實現完整的 RFM 分析
- [ ] 優化代碼性能

---

## 📞 常見問題

**Q: Apply 和 Transform 的區別？**
A: Apply 對每個組應用函數，Transform 應用後保持原始形狀並廣播回去。

**Q: 何時使用 Named Agg？**
A: 當你需要多個聚合函數時，Named Agg 使列名更清晰。

**Q: 我應該總是使用 Apply 嗎？**
A: 不，簡單操作優先向量化，性能可快 100 倍。

**Q: 如何優化 Apply 的性能？**
A: 考慮向量化，或使用 numba/cython 加速。

---

## 📝 更新日誌

| 版本 | 日期 | 更新內容 |
|------|------|---------|
| 1.0 | 2025-12-11 | 首次發佈，包含 4 份教學和 37 道練習 |

---

## 📞 技術支持

遇到問題？

1. 查看 **QUICK_START.md** 快速開始
2. 參考 **Solutions_Complete.md** 解答示例
3. 查看 **INDEX.md** 題目分類索引
4. 重新閱讀相關教學章節

---

## 📄 許可證

本教材供學習使用。

---

**最後更新**: 2025-12-11
**作者**: Data Analysis Teaching System
**版本**: 1.0 - 完整版

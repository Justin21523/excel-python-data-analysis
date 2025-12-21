# Project 3: Inventory Optimization System
庫存優化系統 - Week 18

## 項目概述

Inventory Optimization System 是一個全面的庫存管理解決方案，提供需求預測、庫存優化、成本分析和自動補充建議。

## 主要功能

1. **需求預測** (Demand Forecasting)
   - 移動平均法
   - 指數平滑法
   - 趨勢分析

2. **庫存優化** (Inventory Optimization)
   - 經濟訂單量（EOQ）
   - 安全庫存計算
   - 訂單點計算

3. **成本分析** (Cost Analysis)
   - 持有成本
   - 訂購成本
   - 總成本優化

4. **ABC 分類** (ABC Classification)
   - 高價值產品
   - 中等價值產品
   - 低價值產品

5. **自動補充** (Automatic Replenishment)
   - 補充建議
   - 緊急性評估
   - 預計到貨時間

## 安裝

```bash
cd project3_inventory_optimizer
pip install -r requirements.txt
```

## 使用

```bash
python main.py --config config.yaml
```

## 主要計算公式

### 經濟訂單量（EOQ）

```
EOQ = √(2 × D × S / H)

其中：
- D = 年需求量
- S = 每次訂購成本
- H = 年持有成本率
```

### 安全庫存（Safety Stock）

```
SS = Z × σ × √L

其中：
- Z = 服務水平係數（如 95% 對應 1.65）
- σ = 需求標準差
- L = 訂購提前期（天）
```

### 訂單點（Reorder Point）

```
ROP = D × L + SS

其中：
- D = 日均需求
- L = 提前期（天）
- SS = 安全庫存
```

## 輸出

- 補充建議清單
- 庫存優化報告
- 成本分析
- 產品分類

## 配置示例

```yaml
optimization:
  service_level: 0.95  # 95% 服務水平
  review_period: 30    # 30天評估周期

abc_analysis:
  a_threshold: 80      # A 類：80% 銷售額
  b_threshold: 95      # B 類：95% 銷售額
```

## 常見指標

- **庫存周轉率**：銷售成本 / 平均庫存
- **持有成本**：平均庫存 × 單位成本 × 成本率
- **缺貨率**：缺貨次數 / 總訂購次數
- **訂購成本**：年訂購次數 × 單次成本

---

**版本**：1.0.0

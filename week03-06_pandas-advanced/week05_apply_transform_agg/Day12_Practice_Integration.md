# Day 12: 實踐整合 - 完整客戶分析系統 (3-4 小時)

## 📚 目錄
1. [項目概述](#項目概述)
2. [數據準備與探索](#數據準備與探索)
3. [功能1: RFM 分析引擎](#功能1-rfm-分析引擎)
4. [功能2: 客戶分群系統](#功能2-客戶分群系統)
5. [功能3: 價值分析模塊](#功能3-價值分析模塊)
6. [功能4: 流失預警系統](#功能4-流失預警系統)
7. [功能5: 行銷建議引擎](#功能5-行銷建議引擎)
8. [最終儀表板](#最終儀表板)

---

## 項目概述

### 目標

建立完整的**客戶分析系統**，整合 Apply、Transform 和 Agg 三大核心方法：

- **Apply**: 複雜的會員評級邏輯
- **Transform**: 組內相對排名和標準化
- **Agg**: 多維度聚合報表生成

### 核心場景

在線零售平台需要：
1. 識別高價值客戶（RFM 分析）
2. 自動分群並標記特徵
3. 評估客戶生命週期價值
4. 預警潛在流失客戶
5. 生成個性化行銷建議

### 技術棧

```
數據加載 → 數據清理 → RFM 計算 → 分群評估 → 流失預警 → 行銷建議 → 報表輸出
   ↓          ↓         ↓          ↓         ↓         ↓        ↓
加載器     NaN 處理    Apply      Transform  Apply    Apply    Agg
```

---

## 數據準備與探索

### 2.1 加載和初始探索

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from olist.datasets import load_datasets

# 加載核心數據集
print("=" * 60)
print("客戶分析系統 - 數據加載")
print("=" * 60)

orders_df = load_datasets('orders')
order_items_df = load_datasets('order_items')
order_payments_df = load_datasets('order_payments')
customers_df = load_datasets('customers')
sellers_df = load_datasets('sellers')
products_df = load_datasets('products')
product_categories_df = load_datasets('product_categories')

# 探索數據
print(f"\n訂單數量: {len(orders_df):,}")
print(f"客戶數量: {len(customers_df):,}")
print(f"訂單項目數: {len(order_items_df):,}")
print(f"時間跨度: {orders_df['order_purchase_timestamp'].min()} 至 {orders_df['order_purchase_timestamp'].max()}")

# 查看數據質量
print("\n缺失值檢查:")
for col in orders_df.columns:
    missing = orders_df[col].isna().sum()
    if missing > 0:
        print(f"  {col}: {missing} ({missing/len(orders_df)*100:.2f}%)")
```

### 2.2 構建統一的客戶交易表

```python
# 構建完整的客戶交易視圖
print("\n" + "=" * 60)
print("構建客戶交易視圖")
print("=" * 60)

# 第一步：合併訂單和支付信息
order_payment = order_payments_df.groupby('order_id')['payment_value'].sum().reset_index()
order_payment.columns = ['order_id', 'total_payment']

# 第二步：加入訂單和客戶信息
customer_orders = orders_df[['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp']].merge(
    order_payment,
    on='order_id',
    how='left'
)

# 第三步：加入訂單項目詳情
order_items_detail = order_items_df.groupby('order_id').agg({
    'product_id': 'count',
    'price': 'sum'
}).reset_index()
order_items_detail.columns = ['order_id', 'num_items', 'items_total_price']

customer_orders = customer_orders.merge(
    order_items_detail,
    on='order_id',
    how='left'
)

# 第四步：加入客戶信息
customer_orders = customer_orders.merge(
    customers_df[['customer_id', 'customer_state', 'customer_city']],
    on='customer_id',
    how='left'
)

# 驗證合併結果
print(f"合併後記錄數: {len(customer_orders):,}")
print(f"唯一客戶數: {customer_orders['customer_id'].nunique():,}")
print(f"平均每客戶訂單數: {len(customer_orders) / customer_orders['customer_id'].nunique():.2f}")

print("\n交易表樣本:")
print(customer_orders.head())

# 數據驗證
print("\n數據驗證:")
print(f"NaN 支付值: {customer_orders['total_payment'].isna().sum()}")
print(f"NaN 項目數: {customer_orders['num_items'].isna().sum()}")
print(f"NaN 客戶州: {customer_orders['customer_state'].isna().sum()}")
```

---

## 功能1: RFM 分析引擎

### 3.1 RFM 基礎計算

```python
print("\n" + "=" * 60)
print("功能1: RFM 分析引擎")
print("=" * 60)

# 定義參考日期（使用數據集中最晚的日期）
reference_date = orders_df['order_purchase_timestamp'].max()
print(f"\n參考日期: {reference_date}")

# 計算 RFM 指標
rfm_data = []

for customer_id in customer_orders['customer_id'].unique():
    customer_data = customer_orders[customer_orders['customer_id'] == customer_id]

    # R: 最近性（天數）
    last_purchase = customer_data['order_purchase_timestamp'].max()
    recency = (reference_date - last_purchase).days

    # F: 頻率（購買次數）
    frequency = customer_data['order_id'].nunique()

    # M: 金額（總消費額）
    monetary = customer_data['total_payment'].sum()

    rfm_data.append({
        'customer_id': customer_id,
        'recency': recency,
        'frequency': frequency,
        'monetary': monetary
    })

rfm_df = pd.DataFrame(rfm_data)

print(f"\nRFM 數據統計:")
print(rfm_df[['recency', 'frequency', 'monetary']].describe())

# 驗證
print(f"\n樣本 RFM 數據:")
print(rfm_df.head(10))
```

### 3.2 RFM 五分位分級

```python
# 對每個 RFM 維度進行五分位分級（1-5，5為最優）

print("\nRFM 五分位分級...")

# R: 最近性（低日數 = 高分）
rfm_df['R_score'] = pd.qcut(
    rfm_df['recency'],
    q=5,
    labels=[5, 4, 3, 2, 1],  # 反轉：最近的客戶得 5 分
    duplicates='drop'
)

# F: 頻率（高頻率 = 高分）
rfm_df['F_score'] = pd.qcut(
    rfm_df['frequency'].rank(method='first'),
    q=5,
    labels=[1, 2, 3, 4, 5],
    duplicates='drop'
)

# M: 金額（高消費 = 高分）
rfm_df['M_score'] = pd.qcut(
    rfm_df['monetary'].rank(method='first'),
    q=5,
    labels=[1, 2, 3, 4, 5],
    duplicates='drop'
)

# 轉換為數值類型便於計算
rfm_df['R_score'] = rfm_df['R_score'].astype(int)
rfm_df['F_score'] = rfm_df['F_score'].astype(int)
rfm_df['M_score'] = rfm_df['M_score'].astype(int)

# 計算總分
rfm_df['rfm_score'] = rfm_df['R_score'] + rfm_df['F_score'] + rfm_df['M_score']

print(f"分級完成!")
print(f"\nRFM 分佈統計:")
print(f"R_score: {rfm_df['R_score'].value_counts().sort_index().to_dict()}")
print(f"F_score: {rfm_df['F_score'].value_counts().sort_index().to_dict()}")
print(f"M_score: {rfm_df['M_score'].value_counts().sort_index().to_dict()}")

# 樣本展示
print(f"\nRFM 五分位樣本:")
print(rfm_df[['customer_id', 'recency', 'R_score', 'frequency', 'F_score', 'monetary', 'M_score', 'rfm_score']].head(15))
```

### 3.3 RFM 分群 (使用 Apply)

```python
# 使用 apply 進行複雜的 RFM 分群邏輯

print("\nRFM 分群分配...")

def assign_rfm_segment(row):
    """
    根據 RFM 評分分配客戶分群

    分群策略：
    - Champions: R>=4, F>=4, M>=4 (最佳客戶)
    - Loyal Customers: F>=4, M>=3 (忠實客戶)
    - Potential Loyalists: R>=4, F>=3, M>=3 (潛在忠實客戶)
    - At Risk: R<=2, F>=3 (流失風險)
    - Lost: R<=1, F<=1 (已流失)
    - Need Attention: R>=3, F<=2, M<=2 (需要關注)
    - Promising: R>=3, F>=2, M>=2 (有潛力)
    """
    r, f, m = row['R_score'], row['F_score'], row['M_score']

    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    elif f >= 4 and m >= 3:
        return 'Loyal Customers'
    elif r >= 4 and f >= 3 and m >= 3:
        return 'Potential Loyalists'
    elif r <= 2 and f >= 3:
        return 'At Risk'
    elif r <= 1 and f <= 1:
        return 'Lost'
    elif r >= 3 and f <= 2 and m <= 2:
        return 'Need Attention'
    elif r >= 3 and f >= 2 and m >= 2:
        return 'Promising'
    else:
        return 'Other'

# 應用分群邏輯
rfm_df['rfm_segment'] = rfm_df.apply(assign_rfm_segment, axis=1)

# 統計分群分佈
segment_dist = rfm_df['rfm_segment'].value_counts()
print(f"\nRFM 分群分佈:")
for segment, count in segment_dist.items():
    pct = count / len(rfm_df) * 100
    print(f"  {segment:20} {count:6,} 人 ({pct:5.2f}%)")

print(f"\n分群樣本:")
print(rfm_df[['customer_id', 'recency', 'frequency', 'monetary', 'rfm_segment']].sample(15))
```

---

## 功能2: 客戶分群系統

### 4.1 計算分群特徵

```python
print("\n" + "=" * 60)
print("功能2: 客戶分群系統")
print("=" * 60)

# 計算每個客戶的詳細特徵
customer_features = customer_orders.groupby('customer_id').agg(
    total_spent=('total_payment', 'sum'),
    num_orders=('order_id', 'nunique'),
    avg_order_value=('total_payment', 'mean'),
    num_items_purchased=('num_items', 'sum'),
    avg_items_per_order=('num_items', 'mean'),
    customer_state=('customer_state', 'first'),
    first_purchase_date=('order_purchase_timestamp', 'min'),
    last_purchase_date=('order_purchase_timestamp', 'max')
).reset_index()

# 計算客戶生命週期（天）
customer_features['customer_lifetime_days'] = (
    customer_features['last_purchase_date'] - customer_features['first_purchase_date']
).dt.days

# 計算購買間隔
customer_features['avg_days_between_orders'] = (
    customer_features['customer_lifetime_days'] / (customer_features['num_orders'] - 1)
).fillna(0)

print(f"客戶特徵計算完成: {len(customer_features)} 個客戶")
print(f"\n客戶特徵統計:")
print(customer_features[[
    'total_spent', 'num_orders', 'avg_order_value',
    'customer_lifetime_days', 'avg_days_between_orders'
]].describe())
```

### 4.2 計算相對排名 (使用 Transform)

```python
# 使用 transform 計算客戶在全體中的相對位置

print("\n計算相對排名...")

# 全局百分位排名
customer_features['spent_percentile'] = customer_features['total_spent'].rank(pct=True) * 100
customer_features['frequency_percentile'] = customer_features['num_orders'].rank(pct=True) * 100
customer_features['recency_percentile'] = (
    1 - rfm_df.set_index('customer_id').loc[customer_features['customer_id'], 'recency'].rank(pct=True)
) * 100

# 按州的相對排名
customer_features['state_spent_rank'] = (
    customer_features.groupby('customer_state')['total_spent'].transform(
        lambda x: x.rank(ascending=False)
    ).astype(int)
)

customer_features['state_spent_percentile'] = (
    customer_features.groupby('customer_state')['total_spent'].transform(
        lambda x: x.rank(pct=True) * 100
    )
)

print("相對排名計算完成!")
print(f"\n樣本排名數據:")
print(customer_features[[
    'customer_id', 'total_spent', 'spent_percentile',
    'state_spent_rank', 'state_spent_percentile'
]].head(15))
```

### 4.3 群體特徵分析 (使用 Agg)

```python
# 合併 RFM 和特徵數據
customer_complete = customer_features.merge(
    rfm_df[['customer_id', 'rfm_segment', 'rfm_score']],
    on='customer_id'
)

# 按分群計算特徵聚合
segment_profile = customer_complete.groupby('rfm_segment').agg(
    num_customers=('customer_id', 'count'),
    avg_spent=('total_spent', 'mean'),
    median_spent=('total_spent', 'median'),
    total_revenue=('total_spent', 'sum'),
    avg_orders=('num_orders', 'mean'),
    avg_order_value=('avg_order_value', 'mean'),
    avg_lifetime_days=('customer_lifetime_days', 'mean'),
    avg_days_between_orders=('avg_days_between_orders', 'mean')
).reset_index()

print("\n分群特徵聚合（使用 Named Agg）:")
segment_profile = customer_complete.groupby('rfm_segment').agg(
    customer_count=('customer_id', 'count'),
    total_segment_revenue=('total_spent', 'sum'),
    avg_customer_value=('total_spent', 'mean'),
    median_customer_value=('total_spent', 'median'),
    avg_frequency=('num_orders', 'mean'),
    avg_monetary=('total_spent', 'mean'),
    avg_lifetime_days=('customer_lifetime_days', 'mean')
).reset_index()

segment_profile['pct_of_customers'] = (
    segment_profile['customer_count'] / segment_profile['customer_count'].sum() * 100
)
segment_profile['pct_of_revenue'] = (
    segment_profile['total_segment_revenue'] / segment_profile['total_segment_revenue'].sum() * 100
)

print(segment_profile.to_string())
```

---

## 功能3: 價值分析模塊

### 5.1 客戶生命週期價值 (CLV) 估算

```python
print("\n" + "=" * 60)
print("功能3: 價值分析模塊")
print("=" * 60)

# 估算 CLV（Customer Lifetime Value）

def calculate_clv_metrics(row):
    """
    計算客戶生命週期價值相關指標

    使用公式：
    CLV = ARPU * Gross Margin * Customer Lifetime
    其中：
    - ARPU = Average Revenue Per User (年度)
    - Gross Margin = 毛利率（假設為 30%）
    - Customer Lifetime = 客戶預期保留期（2-3 年）
    """
    total_spent = row['total_spent']
    num_orders = row['num_orders']
    lifetime_days = max(row['customer_lifetime_days'], 1)  # 避免除以 0

    # 年度消費額
    annual_revenue = (total_spent / max(lifetime_days, 1)) * 365

    # 假設毛利率 30%，預期保留期 2 年
    gross_margin = 0.30
    expected_lifetime_years = 2

    # 估算 CLV
    estimated_clv = annual_revenue * gross_margin * expected_lifetime_years

    return {
        'annual_revenue': annual_revenue,
        'estimated_clv': estimated_clv,
        'clv_tier': 'N/A'  # 暫時賦值，稍後計算
    }

# 應用 CLV 計算（使用 apply）
clv_results = customer_complete.apply(calculate_clv_metrics, axis=1, result_type='expand')
customer_complete = pd.concat([customer_complete, clv_results], axis=1)

# 分級
customer_complete['clv_tier'] = pd.qcut(
    customer_complete['estimated_clv'],
    q=4,
    labels=['Tier D (Low)', 'Tier C (Medium)', 'Tier B (High)', 'Tier A (Premium)'],
    duplicates='drop'
)

print("CLV 計算完成!")
print(f"\nCLV 分佈:")
print(customer_complete['clv_tier'].value_counts())
print(f"\nCLV 統計:")
print(customer_complete[['annual_revenue', 'estimated_clv']].describe())

print(f"\n高價值客戶樣本（Top 10 CLV）:")
print(customer_complete.nlargest(10, 'estimated_clv')[[
    'customer_id', 'total_spent', 'num_orders', 'annual_revenue', 'estimated_clv', 'clv_tier', 'rfm_segment'
]])
```

### 5.2 價值與風險矩陣

```python
# 建立客戶價值與風險矩陣

# 計算流失風險評分（基於 RFM）
def calculate_risk_score(row):
    """
    計算流失風險分數（0-100，越高越危險）
    """
    recency = row['recency']
    frequency = row['frequency']
    monetary = row['monetary']

    risk = 0

    # 最近性風險（30%權重）
    if recency > 180:
        risk += 30
    elif recency > 90:
        risk += 15
    elif recency > 30:
        risk += 5

    # 頻率風險（40%權重）
    if frequency <= 1:
        risk += 40
    elif frequency <= 3:
        risk += 20
    elif frequency <= 5:
        risk += 10

    # 金額風險（30%權重）
    if monetary < customer_complete['total_spent'].quantile(0.25):
        risk += 30
    elif monetary < customer_complete['total_spent'].quantile(0.50):
        risk += 15
    elif monetary < customer_complete['total_spent'].quantile(0.75):
        risk += 5

    return min(risk, 100)

customer_complete['churn_risk_score'] = rfm_df.set_index('customer_id').loc[
    customer_complete['customer_id']
].apply(calculate_risk_score, axis=1).values

# 分級
customer_complete['risk_level'] = pd.cut(
    customer_complete['churn_risk_score'],
    bins=[0, 25, 50, 75, 100],
    labels=['Low', 'Medium', 'High', 'Critical'],
    include_lowest=True
)

# 矩陣分析
value_risk_matrix = customer_complete.groupby(['clv_tier', 'risk_level']).agg(
    customer_count=('customer_id', 'count'),
    avg_clv=('estimated_clv', 'mean'),
    total_revenue=('total_spent', 'sum')
).reset_index()

print("\n價值與風險矩陣:")
print(value_risk_matrix.to_string())

# 關鍵客戶識別：高價值、高風險
at_risk_vips = customer_complete[
    (customer_complete['clv_tier'] == 'Tier A (Premium)') &
    (customer_complete['risk_level'].isin(['High', 'Critical']))
]

print(f"\n高價值高風險客戶（需主動保留）: {len(at_risk_vips)} 人")
print(f"累計價值: ${at_risk_vips['estimated_clv'].sum():,.0f}")
```

---

## 功能4: 流失預警系統

### 6.1 流失預警分級

```python
print("\n" + "=" * 60)
print("功能4: 流失預警系統")
print("=" * 60)

def assign_churn_alert_level(row):
    """
    使用 Apply 進行複雜的流失預警邏輯

    等級定義：
    - RED (緊急): 可能在 30 天內流失，且曾經是高價值客戶
    - ORANGE (警告): 已經沒有購買 60 天或以上
    - YELLOW (監控): 近期活動減少，但還未成為高風險
    - GREEN (正常): 定期購買，風險低
    """
    recency = row['recency']
    frequency = row['frequency']
    monetary = row['monetary']
    rfm_segment = row['rfm_segment']
    avg_days_between = row['avg_days_between_orders']

    # 參考值
    avg_frequency = customer_complete['num_orders'].mean()
    median_monetary = customer_complete['total_spent'].median()

    # RED (緊急)
    if recency > 60 and monetary > median_monetary and rfm_segment in ['Champions', 'Loyal Customers']:
        return 'RED'

    # ORANGE (警告)
    if recency > avg_days_between * 2 and frequency >= 3:
        return 'ORANGE'

    if recency > 90:
        return 'ORANGE'

    # YELLOW (監控)
    if recency > 30 and recency <= 90:
        if frequency >= 5 or monetary >= median_monetary:
            return 'YELLOW'

    # GREEN (正常)
    return 'GREEN'

customer_complete['churn_alert'] = customer_complete.apply(
    assign_churn_alert_level,
    axis=1
)

# 統計
alert_dist = customer_complete['churn_alert'].value_counts()
print("\n流失預警分佈:")
for alert, count in alert_dist.items():
    pct = count / len(customer_complete) * 100
    print(f"  {alert:10} {count:6,} 人 ({pct:5.2f}%)")

# 按警告級別分析
alert_analysis = customer_complete.groupby('churn_alert').agg(
    num_customers=('customer_id', 'count'),
    avg_recency=('recency', 'mean'),
    avg_frequency=('num_orders', 'mean'),
    avg_revenue=('total_spent', 'mean'),
    total_at_risk=('estimated_clv', 'sum')
).reset_index()

print("\n警告級別分析:")
print(alert_analysis.to_string())

# 展示 RED 級別客戶（需立即行動）
red_alert_customers = customer_complete[customer_complete['churn_alert'] == 'RED']

print(f"\nRED 級別客戶（需立即保留）: {len(red_alert_customers)} 人")
print(f"累計風險價值: ${red_alert_customers['estimated_clv'].sum():,.0f}")

print(f"\nRED 級別客戶樣本:")
print(red_alert_customers[[
    'customer_id', 'recency', 'num_orders', 'total_spent',
    'estimated_clv', 'rfm_segment', 'churn_alert'
]].head(20))
```

---

## 功能5: 行銷建議引擎

### 7.1 個性化行銷建議

```python
print("\n" + "=" * 60)
print("功能5: 行銷建議引擎")
print("=" * 60)

def generate_marketing_recommendation(row):
    """
    根據客戶特徵生成個性化行銷建議

    使用複雜邏輯實現多維度決策
    """
    rfm_segment = row['rfm_segment']
    churn_alert = row['churn_alert']
    clv_tier = row['clv_tier']
    frequency = row['num_orders']
    avg_order = row['avg_order_value']

    recommendations = []
    channels = []
    offers = []

    # 基於 RFM 分群的基礎建議
    if rfm_segment == 'Champions':
        recommendations.append('VIP 尊享計劃')
        channels.append('Personal Email')
        offers.append('20% VIP 折扣')

    elif rfm_segment == 'Loyal Customers':
        recommendations.append('忠實客戶獎勵')
        channels.append('Email/SMS')
        offers.append('15% 會員折扣')

    elif rfm_segment == 'Potential Loyalists':
        recommendations.append('升級培養計劃')
        channels.append('Email')
        offers.append('10% 滿額折扣')

    elif rfm_segment == 'At Risk':
        recommendations.append('流失挽留活動')
        channels.append('SMS/Phone')
        offers.append('25% 特別優惠')

    elif rfm_segment == 'Lost':
        recommendations.append('重新激活活動')
        channels.append('Email/Ads')
        offers.append('30% 回饋折扣')

    # 基於警告級別的補充建議
    if churn_alert == 'RED':
        recommendations.append('高優先級保留')
        if 'Phone' not in channels:
            channels.append('Phone')
        offers.insert(0, '專屬客服跟進')

    elif churn_alert == 'ORANGE':
        recommendations.append('重新激活')
        offers.insert(0, '限時優惠碼')

    # 基於消費習慣的交叉銷售建議
    if frequency >= 10:
        recommendations.append('高頻購買者計劃')
        offers.append('每次購買返現')

    if avg_order >= customer_complete['avg_order_value'].quantile(0.75):
        recommendations.append('高客單價對象')
        offers.append('滿額升級禮遇')

    return pd.Series({
        'recommendations': ' | '.join(recommendations),
        'marketing_channels': ' | '.join(channels),
        'suggested_offers': ' | '.join(offers)
    })

# 應用行銷建議引擎
marketing_recs = customer_complete.apply(generate_marketing_recommendation, axis=1)
customer_complete = pd.concat([customer_complete, marketing_recs], axis=1)

print("行銷建議生成完成!")

print(f"\n建議樣本（不同分群）:")
for segment in customer_complete['rfm_segment'].unique():
    sample = customer_complete[customer_complete['rfm_segment'] == segment].iloc[0]
    print(f"\n分群: {segment}")
    print(f"  推薦: {sample['recommendations']}")
    print(f"  渠道: {sample['marketing_channels']}")
    print(f"  優惠: {sample['suggested_offers']}")
```

### 7.2 營銷活動優先級

```python
# 為營銷活動設定優先級

def calculate_campaign_priority(row):
    """計算營銷活動優先級（1-5，5 為最高）"""
    priority = 0

    # CLV 權重 (40%)
    if row['clv_tier'] == 'Tier A (Premium)':
        priority += 2
    elif row['clv_tier'] == 'Tier B (High)':
        priority += 1.5
    elif row['clv_tier'] == 'Tier C (Medium)':
        priority += 1

    # 流失風險權重 (50%)
    if row['churn_alert'] == 'RED':
        priority += 2.5
    elif row['churn_alert'] == 'ORANGE':
        priority += 2
    elif row['churn_alert'] == 'YELLOW':
        priority += 1

    # 回購潛力權重 (10%)
    if row['rfm_segment'] == 'Potential Loyalists':
        priority += 0.5

    return min(priority, 5)

customer_complete['campaign_priority'] = customer_complete.apply(
    calculate_campaign_priority,
    axis=1
)

# 按優先級分組分析
priority_analysis = customer_complete.groupby(
    pd.cut(customer_complete['campaign_priority'], bins=[0, 1, 2, 3, 4, 5],
           labels=['Very Low', 'Low', 'Medium', 'High', 'Critical'])
).agg(
    customer_count=('customer_id', 'count'),
    total_value=('estimated_clv', 'sum'),
    avg_clv=('estimated_clv', 'mean')
).reset_index()

print("\n營銷活動優先級分佈:")
print(priority_analysis.to_string())
```

---

## 最終儀表板

### 8.1 綜合報表生成

```python
print("\n" + "=" * 60)
print("最終儀表板")
print("=" * 60)

# 1. 客戶總體情況
print("\n【1】客戶總體情況")
print("-" * 60)
total_customers = len(customer_complete)
total_revenue = customer_complete['total_spent'].sum()
avg_clv = customer_complete['estimated_clv'].mean()
retention_rate = (customer_complete['churn_alert'] == 'GREEN').sum() / total_customers * 100

print(f"總客戶數:        {total_customers:,}")
print(f"總交易金額:      ${total_revenue:,.0f}")
print(f"平均客戶價值:    ${avg_clv:,.0f}")
print(f"健康客戶率:      {retention_rate:.1f}%")
print(f"可保留風險客戶:  {(customer_complete['churn_alert'].isin(['RED', 'ORANGE'])).sum():,}")

# 2. RFM 分群分佈
print("\n【2】RFM 分群分佈")
print("-" * 60)
rfm_summary = customer_complete.groupby('rfm_segment').agg(
    num_customers=('customer_id', 'count'),
    total_revenue=('total_spent', 'sum'),
    avg_clv=('estimated_clv', 'mean')
).sort_values('total_revenue', ascending=False)

for idx, row in rfm_summary.iterrows():
    pct = row['num_customers'] / total_customers * 100
    value_pct = row['total_revenue'] / total_revenue * 100
    print(f"{idx:20} {row['num_customers']:6,} 人 ({pct:5.1f}%) | 收入 ${row['total_revenue']:10,.0f} ({value_pct:5.1f}%) | CLV ${row['avg_clv']:8,.0f}")

# 3. 流失風險分析
print("\n【3】流失風險分析")
print("-" * 60)
alert_summary = customer_complete.groupby('churn_alert').agg(
    num_customers=('customer_id', 'count'),
    avg_recency=('recency', 'mean'),
    total_at_risk_value=('estimated_clv', 'sum')
).sort_values('total_at_risk_value', ascending=False)

for idx, row in alert_summary.iterrows():
    pct = row['num_customers'] / total_customers * 100
    print(f"{idx:10} {row['num_customers']:6,} 人 ({pct:5.1f}%) | 平均最近性 {row['avg_recency']:6.0f} 天 | 風險價值 ${row['total_at_risk_value']:12,.0f}")

# 4. CLV 分級分佈
print("\n【4】客戶價值分佈")
print("-" * 60)
clv_summary = customer_complete.groupby('clv_tier').agg(
    num_customers=('customer_id', 'count'),
    total_clv=('estimated_clv', 'sum'),
    avg_clv=('estimated_clv', 'mean')
).sort_values('total_clv', ascending=False)

for idx, row in clv_summary.iterrows():
    pct = row['num_customers'] / total_customers * 100
    value_pct = row['total_clv'] / customer_complete['estimated_clv'].sum() * 100
    print(f"{idx:20} {row['num_customers']:6,} 人 ({pct:5.1f}%) | CLV ${row['total_clv']:12,.0f} ({value_pct:5.1f}%) | 平均 ${row['avg_clv']:8,.0f}")

# 5. 地理分佈 Top 10
print("\n【5】Top 10 地區（按收入）")
print("-" * 60)
geo_summary = customer_complete.groupby('customer_state').agg(
    num_customers=('customer_id', 'count'),
    total_revenue=('total_spent', 'sum'),
    avg_clv=('estimated_clv', 'mean')
).sort_values('total_revenue', ascending=False).head(10)

for idx, (state, row) in enumerate(geo_summary.iterrows(), 1):
    pct = row['total_revenue'] / total_revenue * 100
    print(f"{idx:2}. {state:3} {row['num_customers']:6,} 人 | 收入 ${row['total_revenue']:10,.0f} ({pct:5.1f}%) | 平均 CLV ${row['avg_clv']:8,.0f}")

# 6. 營銷活動優先級
print("\n【6】營銷活動優先級分佈")
print("-" * 60)
priority_summary = customer_complete.groupby(
    pd.cut(customer_complete['campaign_priority'],
           bins=[0, 1, 2, 3, 4, 5],
           labels=['Very Low (0-1)', 'Low (1-2)', 'Medium (2-3)', 'High (3-4)', 'Critical (4-5)'])
).agg(
    num_customers=('customer_id', 'count'),
    total_value=('estimated_clv', 'sum'),
    avg_priority=('campaign_priority', 'mean')
)

for idx, row in priority_summary.iterrows():
    print(f"{idx:20} {row['num_customers']:6,} 人 | 價值 ${row['total_value']:12,.0f} | 優先級 {row['avg_priority']:4.2f}")
```

### 8.2 導出分析結果

```python
# 導出關鍵結果供下一步使用

# 1. 完整的客戶分析表
output_customer_analysis = customer_complete[[
    'customer_id', 'customer_state',
    'total_spent', 'num_orders', 'avg_order_value',
    'customer_lifetime_days',
    'recency', 'frequency', 'monetary',
    'rfm_segment', 'rfm_score',
    'clv_tier', 'estimated_clv',
    'churn_alert', 'churn_risk_score',
    'campaign_priority',
    'recommendations', 'marketing_channels', 'suggested_offers'
]].sort_values('estimated_clv', ascending=False)

print("\n分析結果已保存!")

# 2. 高風險客戶清單（需立即行動）
high_risk = customer_complete[
    (customer_complete['churn_alert'].isin(['RED', 'ORANGE'])) &
    (customer_complete['estimated_clv'] > 0)
].sort_values('estimated_clv', ascending=False)

print(f"\n高風險客戶清單已生成: {len(high_risk)} 人")
print(f"需要保留的客戶價值: ${high_risk['estimated_clv'].sum():,.0f}")

# 3. 增長機會客戶清單
growth_opportunity = customer_complete[
    (customer_complete['rfm_segment'] == 'Potential Loyalists') |
    (customer_complete['rfm_segment'] == 'Promising')
].sort_values('estimated_clv', ascending=False)

print(f"\n增長機會客戶清單已生成: {len(growth_opportunity)} 人")
print(f"潛在增長價值: ${growth_opportunity['estimated_clv'].sum():,.0f}")

# 最終統計
print("\n" + "=" * 60)
print("分析完成！")
print("=" * 60)
print(f"✓ 分析客戶數: {len(customer_complete):,}")
print(f"✓ 總交易金額: ${total_revenue:,.0f}")
print(f"✓ 平均客戶價值: ${avg_clv:,.0f}")
print(f"✓ 需要保留的高風險客戶: {len(high_risk):,} 人 (${high_risk['estimated_clv'].sum():,.0f})")
print(f"✓ 增長機會客戶: {len(growth_opportunity):,} 人 (${growth_opportunity['estimated_clv'].sum():,.0f})")
```

---

## 完整代碼整合

此時，你已經擁有：
- ✓ RFM 分析引擎
- ✓ 客戶分群系統
- ✓ 價值分析模塊
- ✓ 流失預警系統
- ✓ 行銷建議引擎
- ✓ 綜合儀表板

### 推薦後續步驟

1. **可視化**: 使用 Matplotlib/Seaborn 繪製儀表板圖表
2. **驗證**: 通過 A/B 測試驗證建議的有效性
3. **優化**: 根據實際結果調整分群和風險評分算法
4. **自動化**: 將分析流程集成到每日/每週自動運行
5. **擴展**: 加入產品推薦、季節性分析等功能

---

## 學習檢查清單

- [ ] 理解完整的數據合併流程
- [ ] 掌握 RFM 分析的全套實現
- [ ] 能夠使用 Apply、Transform、Agg 進行複雜分析
- [ ] 理解客戶分群的業務邏輯
- [ ] 掌握 CLV 估算的方法
- [ ] 能夠設計流失預警系統
- [ ] 理解行銷建議的決策邏輯
- [ ] 能夠生成可視化的分析報告

---

**建立時間**: 2025-12-11
**版本**: 1.0
**狀態**: 完整版

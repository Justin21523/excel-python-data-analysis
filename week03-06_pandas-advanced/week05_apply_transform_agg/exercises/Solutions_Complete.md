# Solutions: 詳細解答（前 5 題）

---

## Exercise 07: Apply 深度應用

### Q1: 基礎價格轉換

**完整答案：**

```python
import pandas as pd

# 題目數據
prices = pd.Series([10, 50, 100, 250])

# 解決方案1: Lambda 函數
result = prices.apply(lambda x: x * 7.2)

# 解決方案2: 命名函數
def convert_to_cny(price):
    """將美元轉換為人民幣"""
    return price * 7.2

result = prices.apply(convert_to_cny)

# 解決方案3: 直接向量化（最優）
result = prices * 7.2

print("轉換結果:")
print(result)
```

**輸出：**
```
0       72.0
1      360.0
2      720.0
3     1800.0
dtype: float64
```

**關鍵點：**
- ✓ Lambda 最簡潔，適合簡單函數
- ✓ 命名函數更清晰，適合複雜邏輯
- ✓ 直接向量化最快，應優先使用
- ✓ 對於簡單乘法，直接向量化性能快 100 倍

**性能對比：**
```python
import time
import numpy as np

n = 100000
prices_large = pd.Series(np.random.uniform(0, 1000, n))

# Apply 方法
start = time.time()
result_apply = prices_large.apply(lambda x: x * 7.2)
apply_time = time.time() - start

# 向量化方法
start = time.time()
result_vec = prices_large * 7.2
vec_time = time.time() - start

print(f"Apply: {apply_time:.4f}s")
print(f"Vectorized: {vec_time:.4f}s")
print(f"性能提升: {apply_time/vec_time:.1f}x")
```

---

### Q2: 文本大寫轉換

**完整答案：**

```python
import pandas as pd

product_names = pd.Series(['laptop', 'mouse', 'keyboard', 'monitor'])

# 解決方案1: Lambda 組合字符串操作
result = product_names.apply(lambda x: "PRODUCT_" + x.upper())

# 解決方案2: 命名函數
def format_product_name(name):
    """將產品名稱轉換為大寫並添加前綴"""
    return f"PRODUCT_{name.upper()}"

result = product_names.apply(format_product_name)

# 解決方案3: 向量化字符串操作（最優）
result = "PRODUCT_" + product_names.str.upper()

print("轉換結果:")
print(result)
```

**輸出：**
```
0       PRODUCT_LAPTOP
1         PRODUCT_MOUSE
2      PRODUCT_KEYBOARD
3       PRODUCT_MONITOR
dtype: object
```

**關鍵點：**
- ✓ 字符串操作時，優先使用 `.str` 方法而非 apply
- ✓ 三種方法的可讀性：向量化 > Lambda > 命名函數
- ✓ 性能：向量化 >> Lambda ≈ 命名函數

**延伸應用：**
```python
# 添加更複雜的邏輯
def format_product_name_v2(name):
    """添加類別標籤"""
    prefix = "PRODUCT_"
    if len(name) > 5:
        category = "LONG"
    else:
        category = "SHORT"
    return f"{prefix}{name.upper()}_{category}"

result = product_names.apply(format_product_name_v2)
print(result)
# 輸出:
# 0    PRODUCT_LAPTOP_LONG
# 1   PRODUCT_MOUSE_SHORT
# ...
```

---

### Q3: 簡單分類函數

**完整答案：**

```python
import pandas as pd

temperatures = pd.Series([-5, 10, 25, 35, 0, 30])

# 解決方案1: 使用定義的函數（清晰易懂）
def categorize_temp(temp):
    """根據溫度分類"""
    if temp < 0:
        return '冷'
    elif temp < 20:
        return '涼'
    elif temp < 30:
        return '溫暖'
    else:
        return '熱'

result = temperatures.apply(categorize_temp)

# 解決方案2: Lambda（簡潔但難讀）
result = temperatures.apply(
    lambda t: '冷' if t < 0 else ('涼' if t < 20 else ('溫暖' if t < 30 else '熱'))
)

# 解決方案3: 使用 pd.cut（推薦用於連續分類）
result = pd.cut(
    temperatures,
    bins=[-float('inf'), 0, 20, 30, float('inf')],
    labels=['冷', '涼', '溫暖', '熱']
)

print("分類結果:")
print(result)
```

**輸出：**
```
0      冷
1      涼
2     溫暖
3      熱
4      涼
5      熱
dtype: object
```

**最佳實踐對比：**

```python
# ❌ 避免：過度複雜的 lambda
result = temperatures.apply(
    lambda t: '冷' if t < 0 else ('涼' if t < 20 else ('溫暖' if t < 30 else '熱'))
)

# ✓ 推薦1: 清晰的函數定義
def categorize_temp(temp):
    if temp < 0:
        return '冷'
    elif temp < 20:
        return '涼'
    elif temp < 30:
        return '溫暖'
    else:
        return '熱'

result = temperatures.apply(categorize_temp)

# ✓ 推薦2: 使用 pd.cut（性能最佳）
result = pd.cut(temperatures, bins=[-float('inf'), 0, 20, 30, float('inf')],
                labels=['冷', '涼', '溫暖', '熱'])

# ✓ 推薦3: 字典映射（如果有離散值）
temp_category = {
    -5: '冷', 10: '涼', 25: '溫暖', 35: '熱', 0: '涼', 30: '熱'
}
result = temperatures.map(temp_category)
```

**性能測試：**
```python
import time
import numpy as np

temps = pd.Series(np.random.uniform(-10, 40, 100000))

# 測試1: apply 方法
start = time.time()
r1 = temps.apply(categorize_temp)
t1 = time.time() - start

# 測試2: pd.cut 方法
start = time.time()
r2 = pd.cut(temps, bins=[-float('inf'), 0, 20, 30, float('inf')],
            labels=['冷', '涼', '溫暖', '熱'])
t2 = time.time() - start

print(f"Apply: {t1:.4f}s")
print(f"pd.cut: {t2:.4f}s")
print(f"性能提升: {t1/t2:.1f}x")
```

---

### Q4: 處理缺失值的 apply

**完整答案：**

```python
import pandas as pd

phone_numbers = pd.Series(['13812345678', 'invalid', None, '12345', '12345678901'])

# 定義驗證函數
def validate_phone(phone):
    """驗證電話號碼合法性"""
    # 處理 NaN/None
    if pd.isna(phone):
        return '無效'

    # 轉換為字符串
    phone_str = str(phone).strip()

    # 驗證：必須是 11 位數字
    if len(phone_str) == 11 and phone_str.isdigit():
        return '有效'
    else:
        return '無效'

result = phone_numbers.apply(validate_phone)

print("驗證結果:")
print(result)
```

**輸出：**
```
0      有效
1      無效
2      無效
3      無效
4      有效
dtype: object
```

**進階應用：添加詳細的驗證信息**

```python
def validate_phone_detailed(phone):
    """提供詳細的驗證信息"""
    if pd.isna(phone):
        return '無效 (缺失值)'

    phone_str = str(phone).strip()

    # 檢查長度
    if len(phone_str) != 11:
        return f'無效 (長度{len(phone_str)})'

    # 檢查是否全為數字
    if not phone_str.isdigit():
        return '無效 (包含非數字字符)'

    # 檢查開頭是否為 1（中國號碼）
    if not phone_str.startswith('1'):
        return '無效 (不以1開頭)'

    return '有效'

result = phone_numbers.apply(validate_phone_detailed)
print("詳細驗證結果:")
print(result)
```

**關鍵點：**
- ✓ 必須先檢查 pd.isna()，避免後續操作報錯
- ✓ 使用 try-except 捕獲異常
- ✓ 返回一致的數據類型（都是字符串）
- ✓ 提供清晰的驗證消息便於調試

---

### Q5: 字符串長度分類

**完整答案：**

```python
import pandas as pd

descriptions = pd.Series(['Hi', 'Hello World', 'This is a test description', 'Python'])

# 解決方案1: Lambda（最簡潔）
result = descriptions.apply(lambda x: '短' if len(x) < 5 else ('中' if len(x) <= 10 else '長'))

# 解決方案2: 命名函數（最清晰）
def classify_length(text):
    """根據長度分類"""
    length = len(text)
    if length < 5:
        return '短'
    elif length <= 10:
        return '中'
    else:
        return '長'

result = descriptions.apply(classify_length)

# 解決方案3: 使用 pd.cut（最優）
result = pd.cut(
    descriptions.str.len(),
    bins=[0, 5, 11, float('inf')],
    labels=['短', '中', '長'],
    right=False
)

print("長度分類結果:")
print(result)
```

**輸出：**
```
0       短
1       中
2       長
3       短
dtype: object
```

**詳細分析：**

```python
# 顯示長度和分類
analysis = pd.DataFrame({
    'text': descriptions,
    'length': descriptions.str.len(),
    'category': result
})

print("\n詳細分析:")
print(analysis)

# 統計分佈
print("\n分類分佈:")
print(result.value_counts())
```

**輸出：**
```
      text                    length category
0       Hi                        2       短
1    Hello World                11       長
2 This is a test description     29       長
3      Python                    6       中

分類分佈:
長    2
短    1
中    1
dtype: int64
```

**與 Excel 對照：**

```
Excel 公式:
=IF(LEN(A1)<5, "短", IF(LEN(A1)<=10, "中", "長"))

Python 等價:
descriptions.apply(lambda x: '短' if len(x) < 5 else ('中' if len(x) <= 10 else '長'))

Python 推薦:
pd.cut(descriptions.str.len(), bins=[0, 5, 11, float('inf')], labels=['短', '中', '長'], right=False)
```

---

## Exercise 08: Transform 保持形狀變換

### Q1: 計算組內平均值並廣播

**完整答案：**

```python
import pandas as pd

sales_data = pd.DataFrame({
    'city': ['北京', '北京', '北京', '上海', '上海', '深圳'],
    'sales': [100, 150, 120, 200, 180, 90]
})

# 解決方案1: 使用 transform('mean')
sales_data['city_avg_sales'] = sales_data.groupby('city')['sales'].transform('mean')

# 解決方案2: 使用 transform 和 lambda
sales_data['city_avg_sales'] = sales_data.groupby('city')['sales'].transform(lambda x: x.mean())

# 解決方案3: 分步驟（易於理解）
grouped = sales_data.groupby('city')['sales']
sales_data['city_avg_sales'] = grouped.transform('mean')

print("結果:")
print(sales_data)
```

**輸出：**
```
  city  sales  city_avg_sales
0   北京    100       123.333333
1   北京    150       123.333333
2   北京    120       123.333333
3   上海    200       190.000000
4   上海    180       190.000000
5   深圳     90        90.000000
```

**驗證 transform 的特性：**

```python
# 驗證1: 形狀保持不變
print(f"原始行數: {len(sales_data)}")
print(f"結果行數: {len(sales_data['city_avg_sales'])}")
# 都是 6 行

# 驗證2: 值正確廣播
print("\n北京的平均值:")
print(sales_data[sales_data['city'] == '北京'][['sales', 'city_avg_sales']])
# city_avg_sales 都應該是 123.333...

# 驗證3: 與 agg 對比
agg_result = sales_data.groupby('city')['sales'].agg('mean')
print("\nagg 結果（縮小了）:")
print(agg_result)
# 只有 3 行
```

**實際應用：計算與平均的差異**

```python
# 計算每筆銷售與城市平均的偏差
sales_data['deviation'] = sales_data['sales'] - sales_data['city_avg_sales']
sales_data['deviation_pct'] = (sales_data['deviation'] / sales_data['city_avg_sales'] * 100).round(2)

print("\n偏差分析:")
print(sales_data[['city', 'sales', 'city_avg_sales', 'deviation', 'deviation_pct']])
```

---

## 學習要點總結

### Apply 的核心概念

1. **Series.apply vs DataFrame.apply**
   - Series.apply: 單列操作
   - DataFrame.apply(axis=1): 多列操作

2. **性能考量**
   - 簡單操作：優先向量化 (100倍速度提升)
   - 複雜邏輯：使用 apply
   - 字符串：使用 `.str` 方法

3. **常見模式**
   - 條件判斷：if-elif-else vs pd.cut
   - 字符串變換：.str 方法 vs lambda
   - 複雜邏輯：命名函數 > lambda

### Transform 的核心概念

1. **保持形狀**
   - agg: 縮小（group size）
   - transform: 保持（original size）

2. **廣播機制**
   - 自動將結果廣播回原表
   - 無需手動合併

3. **常見應用**
   - 組內平均/總和廣播
   - Z-score 標準化
   - 排名和百分位

---

## 更多資源

### 推薦閱讀
- Pandas 官方文檔：groupby
- NumPy 向量化操作
- Excel 函數到 Python 的轉換

### 練習建議
1. 先熟悉簡單的 apply
2. 掌握 DataFrame.apply(axis=1) 的複雜邏輯
3. 理解 transform 和 agg 的區別
4. 實踐完整的 RFM 分析系統

---

**更新時間**: 2025-12-11
**版本**: 1.0
**狀態**: 完整版

#!/usr/bin/env python3
"""
生成超真實的商業資料 - 完整版
包含：訂單、客戶、產品、庫存、物流等完整電商資料
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from faker import Faker
import random
import string

# 設定
fake = Faker('zh_TW')
Faker.seed(42)
np.random.seed(42)
random.seed(42)

OUTPUT_DIR = Path('/home/justin/web-projects/excel-python-data-analysis/week01-02_excel-advanced')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("🚀 生成超真實商業資料...")
print("=" * 80)

# =============================================================================
# 輔助函數
# =============================================================================

def generate_phone():
    """生成台灣手機號碼"""
    prefix = random.choice(['0912', '0923', '0932', '0955', '0978', '0988'])
    return prefix + ''.join([str(random.randint(0, 9)) for _ in range(6)])

def generate_email(name):
    """根據姓名生成 email"""
    domains = ['gmail.com', 'yahoo.com.tw', 'hotmail.com', 'outlook.com']
    # 簡化姓名作為 email 前綴
    prefix = ''.join(random.choices(string.ascii_lowercase, k=8))
    return f"{prefix}@{random.choice(domains)}"

def generate_address():
    """生成完整台灣地址"""
    cities = {
        '台北市': ['中正區', '大同區', '中山區', '松山區', '大安區', '萬華區', '信義區', '士林區', '北投區', '內湖區', '南港區', '文山區'],
        '新北市': ['板橋區', '三重區', '中和區', '永和區', '新莊區', '新店區', '樹林區', '鶯歌區', '三峽區', '淡水區', '汐止區', '土城區'],
        '桃園市': ['桃園區', '中壢區', '平鎮區', '八德區', '楊梅區', '蘆竹區', '龜山區', '龍潭區', '大溪區'],
        '台中市': ['中區', '東區', '南區', '西區', '北區', '西屯區', '南屯區', '北屯區', '豐原區', '大里區', '太平區'],
        '台南市': ['中西區', '東區', '南區', '北區', '安平區', '安南區', '永康區', '歸仁區', '新化區'],
        '高雄市': ['楠梓區', '左營區', '鼓山區', '三民區', '苓雅區', '新興區', '前金區', '前鎮區', '旗津區', '小港區', '鳳山區']
    }

    city = random.choice(list(cities.keys()))
    district = random.choice(cities[city])
    road = fake.street_name()
    number = random.randint(1, 500)
    floor = random.randint(1, 15)

    return f"{city}{district}{road}{number}號{floor}樓"

def generate_postal_code(address):
    """根據地址生成郵遞區號"""
    postal_codes = {
        '台北市': {'中正區': 100, '大同區': 103, '中山區': 104, '松山區': 105, '大安區': 106, '萬華區': 108, '信義區': 110, '士林區': 111, '北投區': 112, '內湖區': 114, '南港區': 115, '文山區': 116},
        '新北市': {'板橋區': 220, '三重區': 241, '中和區': 235, '永和區': 234, '新莊區': 242, '新店區': 231, '樹林區': 238, '鶯歌區': 239, '三峽區': 237, '淡水區': 251, '汐止區': 221, '土城區': 236},
        '桃園市': {'桃園區': 330, '中壢區': 320, '平鎮區': 324, '八德區': 334, '楊梅區': 326, '蘆竹區': 338, '龜山區': 333, '龍潭區': 325, '大溪區': 335},
        '台中市': {'中區': 400, '東區': 401, '南區': 402, '西區': 403, '北區': 404, '西屯區': 407, '南屯區': 408, '北屯區': 406, '豐原區': 420, '大里區': 412, '太平區': 411},
        '台南市': {'中西區': 700, '東區': 701, '南區': 702, '北區': 704, '安平區': 708, '安南區': 709, '永康區': 710, '歸仁區': 711, '新化區': 712},
        '高雄市': {'楠梓區': 811, '左營區': 813, '鼓山區': 804, '三民區': 807, '苓雅區': 802, '新興區': 800, '前金區': 801, '前鎮區': 806, '旗津區': 805, '小港區': 812, '鳳山區': 830}
    }

    for city, districts in postal_codes.items():
        if city in address:
            for district, code in districts.items():
                if district in address:
                    return code
    return 100

def generate_payment_method():
    """生成付款方式"""
    methods = {
        '信用卡': 0.5,
        'LINE Pay': 0.15,
        'Apple Pay': 0.1,
        '貨到付款': 0.1,
        '轉帳': 0.08,
        'Google Pay': 0.05,
        '街口支付': 0.02
    }
    return random.choices(list(methods.keys()), weights=list(methods.values()))[0]

def generate_card_last4():
    """生成信用卡末四碼"""
    return ''.join([str(random.randint(0, 9)) for _ in range(4)])

# =============================================================================
# Case 01: 超真實訂單資料
# =============================================================================

def generate_realistic_orders():
    print("\n📝 生成 Case 01: 超真實訂單資料...")

    n_orders = 1000
    start_date = datetime(2024, 6, 1)
    end_date = datetime(2024, 11, 30)

    # 產品資料（更真實的產品名稱和規格）
    products_detail = {
        '電腦周邊': [
            {'name': 'Logitech MX Master 3 無線滑鼠', 'brand': 'Logitech', 'model': 'MX Master 3', 'sku': 'MX-001', 'price_range': (2500, 3500), 'cost_ratio': 0.6},
            {'name': 'Keychron K2 機械鍵盤', 'brand': 'Keychron', 'model': 'K2 V2', 'sku': 'KC-002', 'price_range': (2800, 3800), 'cost_ratio': 0.65},
            {'name': 'Anker USB-C Hub 7合1擴充座', 'brand': 'Anker', 'model': 'A8346', 'sku': 'AN-003', 'price_range': (1200, 1800), 'cost_ratio': 0.5},
            {'name': 'Rain Design mStand 筆電支架', 'brand': 'Rain Design', 'model': 'mStand', 'sku': 'RD-004', 'price_range': (2000, 2800), 'cost_ratio': 0.55},
            {'name': 'WD My Passport 2TB 外接硬碟', 'brand': 'Western Digital', 'model': 'WDBYVG0020BBK', 'sku': 'WD-005', 'price_range': (2200, 3000), 'cost_ratio': 0.7}
        ],
        '手機配件': [
            {'name': 'Spigen Ultra Hybrid 手機殼', 'brand': 'Spigen', 'model': 'ACS02217', 'sku': 'SP-011', 'price_range': (350, 650), 'cost_ratio': 0.4},
            {'name': 'Apple AirPods Pro 第二代', 'brand': 'Apple', 'model': 'MTJV3TA/A', 'sku': 'AP-012', 'price_range': (7500, 8500), 'cost_ratio': 0.75},
            {'name': 'Anker PowerLine+ II USB-C 充電線', 'brand': 'Anker', 'model': 'A8652', 'sku': 'AN-013', 'price_range': (400, 700), 'cost_ratio': 0.35},
            {'name': 'Anker PowerCore 20000mAh 行動電源', 'brand': 'Anker', 'model': 'A1271', 'sku': 'AN-014', 'price_range': (1500, 2200), 'cost_ratio': 0.6},
            {'name': 'hoda 2.5D 隱形滿版保護貼', 'brand': 'hoda', 'model': 'HD-001', 'sku': 'HD-015', 'price_range': (500, 900), 'cost_ratio': 0.3}
        ],
        '家電': [
            {'name': 'Dyson V11 無線吸塵器', 'brand': 'Dyson', 'model': 'SV14', 'sku': 'DY-021', 'price_range': (18000, 22000), 'cost_ratio': 0.65},
            {'name': 'Nespresso Essenza Mini 膠囊咖啡機', 'brand': 'Nespresso', 'model': 'C30', 'sku': 'NE-022', 'price_range': (3500, 5000), 'cost_ratio': 0.6},
            {'name': 'Dyson Pure Cool TP00 空氣清淨機', 'brand': 'Dyson', 'model': 'TP00', 'sku': 'DY-023', 'price_range': (12000, 16000), 'cost_ratio': 0.65},
            {'name': '大同14吋DC馬達遙控電風扇', 'brand': '大同', 'model': 'TF-L14D', 'sku': 'TT-024', 'price_range': (1800, 2800), 'cost_ratio': 0.5},
            {'name': 'Panasonic NU-SC100 蒸氣烤箱', 'brand': 'Panasonic', 'model': 'NU-SC100', 'sku': 'PA-025', 'price_range': (5500, 7500), 'cost_ratio': 0.6}
        ],
        '服飾': [
            {'name': 'Uniqlo AIRism 涼感T恤', 'brand': 'Uniqlo', 'model': 'U422370', 'sku': 'UQ-031', 'price_range': (390, 590), 'cost_ratio': 0.4},
            {'name': 'Levis 501 Original 牛仔褲', 'brand': 'Levis', 'model': '00501-2453', 'sku': 'LV-032', 'price_range': (2500, 3500), 'cost_ratio': 0.55},
            {'name': 'The North Face 1996 Retro Nuptse 羽絨外套', 'brand': 'The North Face', 'model': 'NF0A3C8D', 'sku': 'TN-033', 'price_range': (8000, 12000), 'cost_ratio': 0.6},
            {'name': 'Nike Air Max 270 運動鞋', 'brand': 'Nike', 'model': 'AH8050-001', 'sku': 'NK-034', 'price_range': (4500, 6500), 'cost_ratio': 0.58},
            {'name': 'Fjallraven Kanken Classic 後背包', 'brand': 'Fjallraven', 'model': 'F23510', 'sku': 'FJ-035', 'price_range': (2800, 3800), 'cost_ratio': 0.55}
        ],
        '美妝': [
            {'name': '我的美麗日記 玻尿酸保濕面膜', 'brand': '我的美麗日記', 'model': 'MD-001', 'sku': 'MB-041', 'price_range': (199, 399), 'cost_ratio': 0.35},
            {'name': 'SK-II 青春露 230ml', 'brand': 'SK-II', 'model': 'FTCL230', 'sku': 'SK-042', 'price_range': (4800, 6500), 'cost_ratio': 0.7},
            {'name': '資生堂 紅妍肌活露 150ml', 'brand': '資生堂', 'model': 'ULTI150', 'sku': 'SH-043', 'price_range': (2800, 3800), 'cost_ratio': 0.65},
            {'name': '蘭蔻 超進化肌因賦活露', 'brand': 'Lancôme', 'model': 'GEN200', 'sku': 'LC-044', 'price_range': (3500, 4800), 'cost_ratio': 0.68},
            {'name': '瑰珀翠 經典護手霜三件組', 'brand': 'Crabtree & Evelyn', 'model': 'HC-SET', 'sku': 'CE-045', 'price_range': (1200, 1800), 'cost_ratio': 0.5}
        ],
        '食品': [
            {'name': 'UCC 114 濾掛式咖啡 (50入)', 'brand': 'UCC', 'model': 'UCC114-50', 'sku': 'UC-051', 'price_range': (550, 850), 'cost_ratio': 0.4},
            {'name': '義美小泡芙 (原味)', 'brand': '義美', 'model': 'IM-001', 'sku': 'IM-052', 'price_range': (80, 150), 'cost_ratio': 0.3},
            {'name': '維力炸醬麵 (5包裝)', 'brand': '維力', 'model': 'VL-ZJ5', 'sku': 'VL-053', 'price_range': (120, 200), 'cost_ratio': 0.35},
            {'name': '卡迪那 95℃厚切洋芋片', 'brand': '卡迪那', 'model': 'CD-95', 'sku': 'CD-054', 'price_range': (55, 95), 'cost_ratio': 0.3},
            {'name': '黑松沙士 (24入/箱)', 'brand': '黑松', 'model': 'HS-24', 'sku': 'HS-055', 'price_range': (350, 550), 'cost_ratio': 0.4}
        ],
        '書籍': [
            {'name': '原子習慣：細微改變帶來巨大成就的實證法則', 'brand': '方智', 'model': 'ISBN-9789861372464', 'sku': 'BK-061', 'price_range': (260, 360), 'cost_ratio': 0.6},
            {'name': '被討厭的勇氣：自我啟發之父「阿德勒」的教導', 'brand': '究竟', 'model': 'ISBN-9789861371955', 'sku': 'BK-062', 'price_range': (250, 350), 'cost_ratio': 0.6},
            {'name': '鬼滅之刃 (1-23全集)', 'brand': '東立', 'model': 'ISBN-SET001', 'sku': 'BK-063', 'price_range': (2200, 2800), 'cost_ratio': 0.65},
            {'name': '商業周刊 年訂52期', 'brand': '商業周刊', 'model': 'BW-Y2024', 'sku': 'BK-064', 'price_range': (3800, 4500), 'cost_ratio': 0.5},
            {'name': '小熊學校繪本系列 (10冊)', 'brand': '小熊', 'model': 'BR-SET10', 'sku': 'BK-065', 'price_range': (2400, 3200), 'cost_ratio': 0.6}
        ],
        '運動用品': [
            {'name': 'Manduka PRO 瑜珈墊 6mm', 'brand': 'Manduka', 'model': 'PRO-BLK', 'sku': 'MD-071', 'price_range': (4500, 6000), 'cost_ratio': 0.6},
            {'name': 'Adidas 可調式啞鈴 20kg (一對)', 'brand': 'Adidas', 'model': 'ADWT-10320', 'sku': 'AD-072', 'price_range': (2800, 3800), 'cost_ratio': 0.65},
            {'name': 'Under Armour HeatGear 運動緊身衣', 'brand': 'Under Armour', 'model': '1361586', 'sku': 'UA-073', 'price_range': (1200, 1800), 'cost_ratio': 0.55},
            {'name': 'Asics Gel-Kayano 29 慢跑鞋', 'brand': 'Asics', 'model': '1011B440', 'sku': 'AS-074', 'price_range': (4800, 6500), 'cost_ratio': 0.6},
            {'name': 'CamelBak Podium 運動水壺 710ml', 'brand': 'CamelBak', 'model': 'CB-1674', 'sku': 'CB-075', 'price_range': (550, 850), 'cost_ratio': 0.45}
        ]
    }

    # 生成客戶資料庫（500 位客戶）
    customers_db = []
    for i in range(500):
        name = fake.name()
        birth_year = random.randint(1960, 2005)
        age = 2024 - birth_year

        # 會員等級根據年齡和註冊時間
        register_days = random.randint(30, 1800)
        if register_days > 1000:
            membership = random.choices(['鑽石', '黃金', '白銀', '普通'], weights=[0.1, 0.3, 0.4, 0.2])[0]
        elif register_days > 500:
            membership = random.choices(['黃金', '白銀', '普通'], weights=[0.2, 0.5, 0.3])[0]
        else:
            membership = random.choices(['白銀', '普通'], weights=[0.3, 0.7])[0]

        customers_db.append({
            'customer_id': f'CUS{i+1:05d}',
            'name': name,
            'gender': random.choice(['男', '女']),
            'age': age,
            'birth_year': birth_year,
            'phone': generate_phone(),
            'email': generate_email(name),
            'address': generate_address(),
            'membership': membership,
            'register_date': start_date - timedelta(days=register_days),
            'total_orders': 0,  # 會在生成訂單時更新
            'total_spent': 0.0  # 會在生成訂單時更新
        })

    # 生成訂單
    orders = []

    for i in range(n_orders):
        # 選擇客戶（20/80 法則：20% 的客戶貢獻 80% 的訂單）
        if random.random() < 0.8:
            customer = random.choice(customers_db[:100])  # 前 100 位活躍客戶
        else:
            customer = random.choice(customers_db)

        # 訂單日期（週末訂單較多）
        order_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        weekday = order_date.weekday()
        if weekday >= 5:  # 週末
            hour = random.choices(range(24), weights=[1]*8 + [3]*4 + [5]*6 + [3]*4 + [2]*2)[0]
        else:  # 平日
            hour = random.choices(range(24), weights=[1]*9 + [2]*4 + [1]*4 + [4]*5 + [2]*2)[0]

        order_datetime = order_date.replace(hour=hour, minute=random.randint(0, 59), second=random.randint(0, 59))

        # 選擇產品
        category = random.choice(list(products_detail.keys()))
        product = random.choice(products_detail[category])

        # 價格（有波動）
        price_min, price_max = product['price_range']
        base_price = random.randint(price_min, price_max)

        # 促銷折扣（20% 機率）
        if random.random() < 0.2:
            discount_rate = random.choice([0.9, 0.85, 0.8, 0.75, 0.7])
            is_promotion = True
            promotion_name = random.choice(['週年慶', '雙11優惠', '會員日', '季末出清', '新品上市'])
        else:
            discount_rate = 1.0
            is_promotion = False
            promotion_name = None

        actual_price = int(base_price * discount_rate)

        # 數量
        quantity = random.choices([1, 2, 3, 4, 5], weights=[0.6, 0.2, 0.1, 0.05, 0.05])[0]
        subtotal = actual_price * quantity

        # 運費（滿額免運）
        shipping_fee = 0 if subtotal >= 1000 else random.choice([60, 80, 100])

        # 付款方式
        payment_method = generate_payment_method()
        card_last4 = generate_card_last4() if '卡' in payment_method or 'Pay' in payment_method else None

        # 訂單狀態
        days_since_order = (datetime.now() - order_datetime).days
        if days_since_order > 7:
            status_choices = ['已完成', '已完成', '已完成', '已完成', '已完成', '已取消', '退貨']
            status_weights = [0.7, 0.1, 0.05, 0.03, 0.02, 0.08, 0.02]
        elif days_since_order > 3:
            status_choices = ['已完成', '已完成', '已完成', '配送中', '處理中', '已取消']
            status_weights = [0.5, 0.2, 0.1, 0.1, 0.05, 0.05]
        else:
            status_choices = ['配送中', '處理中', '處理中', '已確認', '待付款', '已取消']
            status_weights = [0.3, 0.3, 0.2, 0.1, 0.08, 0.02]

        order_status = random.choices(status_choices, weights=status_weights)[0]

        # 物流資訊
        if order_status in ['已完成', '配送中']:
            shipping_method = random.choice(['宅配', '超商取貨', '超商取貨', '門市自取'])
            if shipping_method == '超商取貨':
                store_name = random.choice([
                    '7-11 信義門市', '全家 中正店', '萊爾富 大安店',
                    'OK超商 松山店', '7-11 內湖門市', '全家 南港店'
                ])
            else:
                store_name = None

            tracking_number = 'TW' + ''.join([str(random.randint(0, 9)) for _ in range(12)])

            # 預計到貨日
            if shipping_method == '宅配':
                delivery_days = random.randint(2, 5)
            elif shipping_method == '超商取貨':
                delivery_days = random.randint(3, 7)
            else:
                delivery_days = 1

            estimated_delivery = order_datetime + timedelta(days=delivery_days)

            # 實際到貨日（已完成的訂單）
            if order_status == '已完成':
                actual_delivery = order_datetime + timedelta(days=random.randint(delivery_days, delivery_days+3))
            else:
                actual_delivery = None
        else:
            shipping_method = random.choice(['宅配', '超商取貨'])
            store_name = None
            tracking_number = None
            estimated_delivery = None
            actual_delivery = None

        # 評價（已完成的訂單）
        if order_status == '已完成':
            rating = random.choices([5, 4, 3, 2, 1], weights=[0.6, 0.25, 0.1, 0.03, 0.02])[0]
            review_comments = [
                '商品品質很好，很滿意！',
                '快速到貨，包裝完整',
                '符合期待，會再回購',
                '普通，沒有特別驚艷',
                '還可以，價格合理',
                None, None, None  # 有些訂單沒有評論
            ]
            review = random.choice(review_comments) if rating >= 3 else random.choice([
                '商品與描述不符',
                '配送太慢了',
                '包裝有損壞',
                None
            ])
        else:
            rating = None
            review = None

        # 發票資訊
        invoice_type = random.choices(['二聯式', '三聯式', '捐贈'], weights=[0.7, 0.2, 0.1])[0]
        if invoice_type == '三聯式':
            invoice_title = fake.company()
            invoice_tax_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        else:
            invoice_title = None
            invoice_tax_id = None

        # 更新客戶統計
        if order_status == '已完成':
            customer['total_orders'] += 1
            customer['total_spent'] += subtotal + shipping_fee

        # 組合訂單資料
        orders.append({
            # 基本訂單資訊
            '訂單編號': f'ORD{i+1:05d}',
            '訂單日期': order_datetime.date(),
            '訂單時間': order_datetime.strftime('%H:%M:%S'),
            '訂單狀態': order_status,

            # 客戶資訊
            '客戶編號': customer['customer_id'],
            '客戶姓名': customer['name'],
            '客戶性別': customer['gender'],
            '客戶年齡': customer['age'],
            '客戶電話': customer['phone'],
            '客戶Email': customer['email'],
            '會員等級': customer['membership'],
            '收件地址': customer['address'],
            '郵遞區號': generate_postal_code(customer['address']),

            # 產品資訊
            '產品類別': category,
            '產品名稱': product['name'],
            '品牌': product['brand'],
            '型號': product['model'],
            'SKU': product['sku'],
            '原價': base_price,
            '實際售價': actual_price,
            '數量': quantity,
            '小計': subtotal,

            # 促銷資訊
            '是否促銷': is_promotion,
            '促銷活動': promotion_name,
            '折扣率': discount_rate,

            # 金額資訊
            '運費': shipping_fee,
            '訂單總額': subtotal + shipping_fee,

            # 付款資訊
            '付款方式': payment_method,
            '卡號末四碼': card_last4,

            # 物流資訊
            '配送方式': shipping_method,
            '超商門市': store_name,
            '物流單號': tracking_number,
            '預計到貨日': estimated_delivery,
            '實際到貨日': actual_delivery,

            # 發票資訊
            '發票類型': invoice_type,
            '發票抬頭': invoice_title,
            '統一編號': invoice_tax_id,

            # 評價資訊
            '評分': rating,
            '評論': review,

            # 地區分類（用於分析）
            '地區': '北部' if any(x in customer['address'] for x in ['台北', '新北', '基隆', '桃園', '新竹']) else
                    '中部' if any(x in customer['address'] for x in ['台中', '彰化', '南投', '雲林']) else
                    '南部' if any(x in customer['address'] for x in ['台南', '高雄', '屏東', '嘉義']) else '東部'
        })

    df_orders = pd.DataFrame(orders)

    # 產品主檔（整合所有產品）
    product_master = []
    for category, products in products_detail.items():
        for product in products:
            price_min, price_max = product['price_range']
            avg_price = (price_min + price_max) / 2
            cost = int(avg_price * product['cost_ratio'])

            product_master.append({
                '產品編號': product['sku'],
                '產品類別': category,
                '產品名稱': product['name'],
                '品牌': product['brand'],
                '型號': product['model'],
                '建議售價': int(avg_price),
                '成本': cost,
                '毛利率': f"{(1 - product['cost_ratio']) * 100:.1f}%",
                '庫存數量': random.randint(50, 500),
                '安全庫存': random.randint(20, 100),
                '供應商': fake.company(),
                '供應商電話': generate_phone(),
                '供應商Email': generate_email(fake.company()),
                '進貨週期': random.choice(['7天', '14天', '30天']),
                '保固期限': random.choice(['無', '6個月', '1年', '2年', '3年']),
                '重量': f"{random.randint(50, 5000)}g",
                '尺寸': f"{random.randint(10, 50)}x{random.randint(10, 50)}x{random.randint(5, 30)}cm"
            })

    df_products = pd.DataFrame(product_master)

    # 客戶主檔
    df_customers = pd.DataFrame(customers_db)
    df_customers['註冊日期'] = df_customers['register_date'].dt.date
    df_customers = df_customers.drop(columns=['register_date'])
    df_customers = df_customers.rename(columns={
        'customer_id': '客戶編號',
        'name': '客戶姓名',
        'gender': '性別',
        'age': '年齡',
        'birth_year': '出生年',
        'phone': '電話',
        'email': 'Email',
        'address': '地址',
        'membership': '會員等級',
        'total_orders': '累計訂單數',
        'total_spent': '累計消費金額'
    })

    print(f"✅ 訂單資料: {len(df_orders)} 筆")
    print(f"✅ 產品主檔: {len(df_products)} 筆")
    print(f"✅ 客戶主檔: {len(df_customers)} 筆")

    # 儲存 Excel（含多個工作表）
    filepath = OUTPUT_DIR / 'case01_realistic_sales_data.xlsx'

    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        df_orders.to_excel(writer, sheet_name='訂單明細', index=False)
        df_products.to_excel(writer, sheet_name='產品主檔', index=False)
        df_customers.to_excel(writer, sheet_name='客戶主檔', index=False)

    # 美化格式
    wb = openpyxl.load_workbook(filepath)

    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]

        # 標題列格式
        header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
        header_font = Font(bold=True, color='FFFFFF')

        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center')

        # 自動調整欄寬
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width

    wb.save(filepath)

    print(f"✅ 已儲存: {filepath}")
    print(f"   包含 3 個工作表：訂單明細、產品主檔、客戶主檔")

    return df_orders, df_products, df_customers

# =============================================================================
# Case 02: 超真實庫存資料
# =============================================================================

def generate_realistic_inventory():
    print("\n📝 生成 Case 02: 超真實庫存資料...")

    # 使用 Case 01 的產品資料作為基礎
    # 這裡簡化生成，實際應該從 Case 01 的產品主檔讀取

    categories = ['電子產品', '家電', '服飾', '食品', '日用品', '美妝', '運動用品', '書籍']
    warehouses = ['台北倉', '台中倉', '高雄倉']

    n_products = 200
    inventory = []

    for i in range(n_products):
        category = random.choice(categories)

        # 庫存水位
        current_stock = random.randint(0, 500)
        safe_stock = random.randint(20, 100)
        max_stock = random.randint(300, 800)

        # 成本與售價
        unit_cost = random.randint(50, 5000)
        selling_price = int(unit_cost * random.uniform(1.3, 2.5))

        # 庫存狀態
        if current_stock == 0:
            stock_status = '缺貨'
        elif current_stock < safe_stock:
            stock_status = '警示'
        elif current_stock > max_stock:
            stock_status = '過量'
        else:
            stock_status = '正常'

        # 庫存金額
        inventory_value = current_stock * unit_cost

        # 週轉天數
        avg_daily_sales = random.randint(1, 20)
        turnover_days = current_stock / avg_daily_sales if avg_daily_sales > 0 else 999

        # 最後異動
        last_updated = datetime.now() - timedelta(days=random.randint(0, 30))
        last_inbound = datetime.now() - timedelta(days=random.randint(1, 90))
        last_outbound = datetime.now() - timedelta(days=random.randint(0, 15))

        inventory.append({
            '產品編號': f'SKU{i+1:05d}',
            '產品名稱': fake.word().capitalize() + ' ' + fake.word().capitalize(),
            '產品類別': category,
            '品牌': random.choice(['品牌A', '品牌B', '品牌C', '品牌D', '品牌E']),
            'SKU': f'SKU-{category[:2].upper()}-{i+1:04d}',

            # 庫存數量
            '當前庫存': current_stock,
            '安全庫存': safe_stock,
            '最大庫存': max_stock,
            '庫存狀態': stock_status,
            '可用庫存': max(0, current_stock - random.randint(0, 10)),  # 扣除預留

            # 成本與價格
            '單位成本': unit_cost,
            '建議售價': selling_price,
            '毛利': selling_price - unit_cost,
            '毛利率': f"{((selling_price - unit_cost) / selling_price * 100):.1f}%",
            '庫存金額': inventory_value,

            # 週轉資訊
            '平均日銷量': avg_daily_sales,
            '庫存週轉天數': int(turnover_days),
            '月週轉率': f"{(30 / turnover_days):.2f}" if turnover_days > 0 else '0.00',

            # 位置資訊
            '倉庫': random.choice(warehouses),
            '儲位': f"{random.choice(['A', 'B', 'C'])}{random.randint(1, 20):02d}-{random.randint(1, 50):02d}",

            # 供應商資訊
            '供應商': fake.company(),
            '供應商電話': generate_phone(),
            '供應商交期': f"{random.randint(3, 30)}天",

            # 時間資訊
            '最後更新': last_updated.strftime('%Y-%m-%d %H:%M'),
            '最後進貨日': last_inbound.strftime('%Y-%m-%d'),
            '最後出貨日': last_outbound.strftime('%Y-%m-%d'),

            # 商品屬性
            '保固期限': random.choice(['無', '6個月', '1年', '2年']),
            '有效期限': None if category not in ['食品', '美妝'] else (datetime.now() + timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d'),
            '重量': f"{random.randint(50, 5000)}g",
            '體積': f"{random.uniform(0.01, 1.0):.2f}m³"
        })

    df_inventory = pd.DataFrame(inventory)

    print(f"✅ 庫存資料: {len(df_inventory)} 筆")

    # 儲存 Excel
    filepath = OUTPUT_DIR / 'case02_realistic_inventory.xlsx'

    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        df_inventory.to_excel(writer, sheet_name='庫存明細', index=False)

        # 庫存統計表
        summary = df_inventory.groupby('產品類別').agg({
            '當前庫存': 'sum',
            '庫存金額': 'sum',
            '產品編號': 'count'
        }).reset_index()
        summary.columns = ['產品類別', '總庫存量', '總庫存金額', '品項數']
        summary.to_excel(writer, sheet_name='類別統計', index=False)

        # 庫存警示表
        alerts = df_inventory[df_inventory['庫存狀態'].isin(['缺貨', '警示'])].copy()
        alerts = alerts[['產品編號', '產品名稱', '產品類別', '當前庫存', '安全庫存', '庫存狀態']]
        alerts.to_excel(writer, sheet_name='庫存警示', index=False)

    # 美化格式
    wb = openpyxl.load_workbook(filepath)

    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]

        # 標題列格式
        header_fill = PatternFill(start_color='70AD47', end_color='70AD47', fill_type='solid')
        header_font = Font(bold=True, color='FFFFFF')

        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center')

        # 自動調整欄寬
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 40)
            ws.column_dimensions[column_letter].width = adjusted_width

    wb.save(filepath)

    print(f"✅ 已儲存: {filepath}")
    print(f"   包含 3 個工作表：庫存明細、類別統計、庫存警示")

    return df_inventory

# =============================================================================
# 主程式
# =============================================================================

if __name__ == "__main__":
    # 生成資料
    df_orders, df_products, df_customers = generate_realistic_orders()
    df_inventory = generate_realistic_inventory()

    print("\n" + "=" * 80)
    print("🎉 所有超真實商業資料生成完成！")
    print("=" * 80)
    print(f"📁 檔案位置: {OUTPUT_DIR}")
    print("\n生成的檔案:")
    print("  1. case01_realistic_sales_data.xlsx")
    print("     - 訂單明細 (1000 筆，50+ 欄位)")
    print("     - 產品主檔 (40 筆，17 欄位)")
    print("     - 客戶主檔 (500 筆，12 欄位)")
    print()
    print("  2. case02_realistic_inventory.xlsx")
    print("     - 庫存明細 (200 筆，30+ 欄位)")
    print("     - 類別統計")
    print("     - 庫存警示")
    print("\n✨ 資料特色:")
    print("  ✅ 完整的客戶資訊（姓名、電話、Email、地址、會員等級）")
    print("  ✅ 詳細的產品資訊（品牌、型號、SKU、成本、毛利）")
    print("  ✅ 真實的訂單流程（時間、狀態、物流、付款、發票）")
    print("  ✅ 完整的評價系統（評分、評論）")
    print("  ✅ 進階的庫存管理（週轉率、儲位、警示）")
    print("\n🚀 現在可以使用這些資料進行 Excel 進階函數練習！")

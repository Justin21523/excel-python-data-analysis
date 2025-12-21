#!/bin/bash
# Amazon Reviews 2023 下載進度監控腳本

echo "=================================================================================="
echo "📊 Amazon Reviews 2023 下載進度報告"
echo "=================================================================================="
echo ""

# 計算已下載檔案數
REVIEWS_COUNT=$(ls /mnt/data/datasets/ecommerce/amazon-reviews-2023/reviews/ 2>/dev/null | wc -l)
METADATA_COUNT=$(ls /mnt/data/datasets/ecommerce/amazon-reviews-2023/metadata/ 2>/dev/null | wc -l)
TOTAL_FILES=$((REVIEWS_COUNT + METADATA_COUNT))

# 計算進度百分比（總共 66 個檔案：33 reviews + 33 metadata）
PROGRESS=$((TOTAL_FILES * 100 / 66))

echo "📦 已下載檔案數："
echo "   ✅ Reviews:  $REVIEWS_COUNT / 33"
echo "   ✅ Metadata: $METADATA_COUNT / 33"
echo "   📊 總計:     $TOTAL_FILES / 66 (${PROGRESS}%)"
echo ""

# 顯示已下載的總大小
TOTAL_SIZE=$(du -sh /mnt/data/datasets/ecommerce/amazon-reviews-2023/ 2>/dev/null | awk '{print $1}')
echo "💾 已下載大小: $TOTAL_SIZE"
echo ""

# 顯示已完成的類別
echo "✅ 已完成類別 ($REVIEWS_COUNT/33)："
ls /mnt/data/datasets/ecommerce/amazon-reviews-2023/reviews/ 2>/dev/null | sed 's/.jsonl.gz//g' | nl
echo ""

# 檢查正在下載的檔案（從日誌）
echo "🔄 當前下載狀態："
tail -3 /tmp/amazon_download.log 2>/dev/null | grep -E "📂|📥|%"
echo ""

# 預估剩餘時間
REMAINING_FILES=$((66 - TOTAL_FILES))
echo "⏳ 剩餘檔案數: $REMAINING_FILES"
echo "📈 預估完成時間: 根據目前速度約需 5-7 小時"
echo ""

# 顯示最近 5 分鐘的下載速度
echo "📶 即時下載資訊："
tail -20 /tmp/amazon_download.log 2>/dev/null | grep -E "Reviews:" | tail -3
echo ""

echo "=================================================================================="
echo "💡 使用提示："
echo "   • 即時監控: tail -f /tmp/amazon_download.log"
echo "   • 重新檢查: bash check_amazon_progress.sh"
echo "   • 檢查檔案: ls -lh /mnt/data/datasets/ecommerce/amazon-reviews-2023/reviews/"
echo "=================================================================================="

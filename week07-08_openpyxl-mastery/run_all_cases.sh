#!/bin/bash

# Week 7-8 openpyxl 完全掌握 - 批量執行腳本
# 執行所有 14 個案例

set -e

echo "=========================================="
echo "Week 7-8: openpyxl 完全掌握"
echo "批量執行所有案例"
echo "=========================================="
echo ""

# 設定開始時間
START_TIME=$(date +%s)

# 案例列表
cases=(
    "case01_styled_monthly_report.py"
    "case02_multi_sheet_consolidation.py"
    "case03_conditional_formatting.py"
    "case04_dynamic_chart_generation.py"
    "case05_formula_injection.py"
    "case06_template_based_reports.py"
    "case07_data_validation.py"
    "case08_executive_summary.py"
    "case09_cell_merging.py"
    "case10_sheet_protection.py"
    "case11_hyperlinks_comments.py"
    "case12_image_insertion.py"
    "case13_full_automation_system.py"
    "case14_pandas_excel_integration.py"
)

# 執行計數
total=${#cases[@]}
success=0
failed=0

# 執行每個案例
for ((i=0; i<total; i++)); do
    case_file=${cases[$i]}
    case_num=$((i+1))

    echo "[$case_num/$total] 執行 $case_file..."
    echo "----------------------------------------"

    if python3 "$case_file" 2>&1; then
        echo "✓ $case_file 執行成功"
        ((success++))
    else
        echo "✗ $case_file 執行失敗"
        ((failed++))
    fi

    echo ""
done

# 計算執行時間
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
MINUTES=$((DURATION / 60))
SECONDS=$((DURATION % 60))

# 輸出統計摘要
echo "=========================================="
echo "執行統計摘要"
echo "=========================================="
echo "總案例數：$total"
echo "成功數：$success"
echo "失敗數：$failed"
echo "執行時間：${MINUTES}分${SECONDS}秒"
echo ""

if [ $failed -eq 0 ]; then
    echo "✅ 所有案例執行完成！"
    exit 0
else
    echo "⚠️  部分案例執行失敗，請檢查上述錯誤訊息"
    exit 1
fi

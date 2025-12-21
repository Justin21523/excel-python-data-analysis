#!/bin/bash

# Week 15-20 Capstone Projects - 批次執行腳本
# Usage: bash run_all.sh [sequential|parallel]

set -e  # 遇到錯誤時停止

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
START_TIME=$(date +%s)
MODE="${1:-parallel}"  # 默認並行執行

# 項目列表
PROJECTS=(
    "project1_sales_intelligence"
    "project2_customer_insights"
    "project3_inventory_optimizer"
    "project4_operations_monitor"
    "project5_executive_dashboard"
)

# 結果記錄
declare -A RESULTS
declare -a SUCCESS_PROJECTS
declare -a FAILED_PROJECTS

# 函數定義

print_header() {
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}Week 15-20 Capstone Projects - 開始執行${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${YELLOW}執行模式: $MODE${NC}"
    echo -e "${YELLOW}項目數: ${#PROJECTS[@]}${NC}"
    echo ""
}

print_project_header() {
    local project=$1
    local index=$2
    local total=$3

    echo -e "${BLUE}[$index/$total] 執行 $project...${NC}"
}

run_project() {
    local project=$1
    local project_dir="${SCRIPT_DIR}/${project}"
    local main_file="${project_dir}/main.py"

    # 檢查 main.py 是否存在
    if [ ! -f "$main_file" ]; then
        echo -e "${RED}✗ $project: main.py 不存在${NC}"
        FAILED_PROJECTS+=("$project")
        RESULTS[$project]="FAILED: main.py 不存在"
        return 1
    fi

    # 進入項目目錄
    cd "$project_dir"

    # 執行項目
    if python main.py > /tmp/${project}.log 2>&1; then
        echo -e "${GREEN}✓ $project 執行成功${NC}"
        SUCCESS_PROJECTS+=("$project")
        RESULTS[$project]="SUCCESS"
        return 0
    else
        echo -e "${RED}✗ $project 執行失敗${NC}"
        FAILED_PROJECTS+=("$project")
        RESULTS[$project]="FAILED"

        # 顯示錯誤信息
        if [ -f /tmp/${project}.log ]; then
            echo -e "${RED}  錯誤摘要:${NC}"
            tail -n 10 /tmp/${project}.log | sed 's/^/    /'
        fi

        return 1
    fi

    # 返回上級目錄
    cd "$SCRIPT_DIR"
}

run_sequential() {
    local index=1

    for project in "${PROJECTS[@]}"; do
        print_project_header "$project" "$index" "${#PROJECTS[@]}"
        run_project "$project"
        ((index++))
        echo ""
    done
}

run_parallel() {
    local pids=()
    local index=1

    for project in "${PROJECTS[@]}"; do
        # 最多同時執行 3 個項目
        while [ $(jobs -r | wc -l) -ge 3 ]; do
            sleep 1
        done

        # 後台執行項目
        (
            print_project_header "$project" "$index" "${#PROJECTS[@]}"
            run_project "$project"
        ) &

        pids+=($!)
        ((index++))
    done

    # 等待所有後台任務完成
    for pid in "${pids[@]}"; do
        wait $pid || true
    done
}

print_summary() {
    local end_time=$(date +%s)
    local elapsed=$((end_time - START_TIME))
    local success_count=${#SUCCESS_PROJECTS[@]}
    local failed_count=${#FAILED_PROJECTS[@]}
    local total=$((success_count + failed_count))

    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}執行摘要${NC}"
    echo -e "${BLUE}============================================================${NC}"

    echo -e "${GREEN}成功: $success_count/$total${NC}"
    echo -e "${RED}失敗: $failed_count/$total${NC}"
    echo -e "${YELLOW}用時: ${elapsed} 秒${NC}"

    echo ""
    echo "詳細結果:"

    for project in "${PROJECTS[@]}"; do
        local status=${RESULTS[$project]:-"UNKNOWN"}

        if [[ $status == "SUCCESS" ]]; then
            echo -e "  ${GREEN}✓${NC} $project: $status"
        else
            echo -e "  ${RED}✗${NC} $project: $status"
        fi
    done

    echo ""

    if [ $failed_count -eq 0 ]; then
        echo -e "${GREEN}所有項目執行成功！${NC}"
        return 0
    else
        echo -e "${RED}有 $failed_count 個項目執行失敗。${NC}"
        return 1
    fi
}

cleanup() {
    # 清理臨時文件
    rm -f /tmp/project*.log
}

# 主程序

# 檢查 Python
if ! command -v python &> /dev/null; then
    echo -e "${RED}錯誤：未找到 Python${NC}"
    exit 1
fi

echo "Python 版本:"
python --version
echo ""

# 進入腳本目錄
cd "$SCRIPT_DIR"

# 檢查 requirements
if [ ! -f requirements_all.txt ]; then
    echo -e "${YELLOW}警告：requirements_all.txt 不存在${NC}"
    echo -e "${YELLOW}嘗試安裝依賴...${NC}"
    pip install pandas numpy openpyxl matplotlib seaborn PyYAML
fi

# 打印頭部
print_header

# 根據模式執行
case $MODE in
    sequential)
        run_sequential
        ;;
    parallel)
        run_parallel
        ;;
    *)
        echo -e "${RED}未知的執行模式: $MODE${NC}"
        echo "用法: $0 [sequential|parallel]"
        exit 1
        ;;
esac

# 打印摘要
echo ""
print_summary
RESULT=$?

# 清理
cleanup

# 返回結果
exit $RESULT

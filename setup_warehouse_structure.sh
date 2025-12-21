#!/bin/bash

# ==============================================================================
# Excel to Python Advanced Analytics - AI_WAREHOUSE 3.0 結構設定腳本
# ==============================================================================
#
# 這個腳本會：
# 1. 在 /mnt/c/ai_projects/ 建立專案目錄
# 2. 在 /mnt/data/datasets/ecommerce/ 建立資料集目錄
# 3. 設定正確的環境變數
# 4. 將當前專案移動到正確位置（可選）
#
# 使用方式：
#   chmod +x setup_warehouse_structure.sh
#   ./setup_warehouse_structure.sh
#
# ==============================================================================

set -e  # 遇到錯誤立即停止

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===================================================================${NC}"
echo -e "${BLUE}  Excel to Python Advanced Analytics${NC}"
echo -e "${BLUE}  AI_WAREHOUSE 3.0 結構設定${NC}"
echo -e "${BLUE}===================================================================${NC}"

# ==============================================================================
# 1. 檢查磁碟是否存在
# ==============================================================================

echo -e "\n${YELLOW}[1/6] 檢查磁碟掛載...${NC}"

if [ ! -d "/mnt/c" ]; then
    echo -e "${RED}❌ /mnt/c 不存在！請確認 2TB NVMe 已正確掛載。${NC}"
    exit 1
fi

if [ ! -d "/mnt/data" ]; then
    echo -e "${RED}❌ /mnt/data 不存在！請確認 4TB NVMe 已正確掛載。${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 磁碟掛載檢查通過${NC}"

# ==============================================================================
# 2. 建立專案目錄結構
# ==============================================================================

echo -e "\n${YELLOW}[2/6] 建立專案目錄結構...${NC}"

# 專案目錄（在 /mnt/c）
PROJECT_DIR="/mnt/c/ai_projects/excel-python-data-analysis"
mkdir -p "$PROJECT_DIR"
echo -e "${GREEN}✅ 建立專案目錄：${PROJECT_DIR}${NC}"

# 快取目錄（在 /mnt/c）
CACHE_DIR="/mnt/c/ai_cache"
mkdir -p "$CACHE_DIR/huggingface"
mkdir -p "$CACHE_DIR/pip"
mkdir -p "$CACHE_DIR/torch"
mkdir -p "$CACHE_DIR/kaggle"
echo -e "${GREEN}✅ 建立快取目錄：${CACHE_DIR}${NC}"

# 資料集目錄（在 /mnt/data）
DATASET_DIR="/mnt/data/datasets/ecommerce"
mkdir -p "$DATASET_DIR/kaggle"
mkdir -p "$DATASET_DIR/uci"
mkdir -p "$DATASET_DIR/huggingface"
mkdir -p "$DATASET_DIR/synthetic"
mkdir -p "$DATASET_DIR/raw"
mkdir -p "$DATASET_DIR/processed"
echo -e "${GREEN}✅ 建立資料集目錄：${DATASET_DIR}${NC}"

# ==============================================================================
# 3. 設定環境變數
# ==============================================================================

echo -e "\n${YELLOW}[3/6] 設定環境變數...${NC}"

ENV_FILE="$HOME/.bashrc"

# 檢查是否已經設定過
if grep -q "AI_WAREHOUSE 3.0" "$ENV_FILE"; then
    echo -e "${YELLOW}⚠️  環境變數已存在於 $ENV_FILE${NC}"
else
    echo -e "\n# ============================================" >> "$ENV_FILE"
    echo -e "# AI_WAREHOUSE 3.0 - Excel Python Data Analysis" >> "$ENV_FILE"
    echo -e "# ============================================" >> "$ENV_FILE"
    echo -e "export PROJECT_ROOT=\"$PROJECT_DIR\"" >> "$ENV_FILE"
    echo -e "export DATASET_ROOT=\"$DATASET_DIR\"" >> "$ENV_FILE"
    echo -e "" >> "$ENV_FILE"
    echo -e "# HuggingFace & PyTorch Cache" >> "$ENV_FILE"
    echo -e "export HF_HOME=\"$CACHE_DIR/huggingface\"" >> "$ENV_FILE"
    echo -e "export TRANSFORMERS_CACHE=\"$CACHE_DIR/huggingface\"" >> "$ENV_FILE"
    echo -e "export TORCH_HOME=\"$CACHE_DIR/torch\"" >> "$ENV_FILE"
    echo -e "export XDG_CACHE_HOME=\"$CACHE_DIR\"" >> "$ENV_FILE"
    echo -e "" >> "$ENV_FILE"
    echo -e "# Kaggle" >> "$ENV_FILE"
    echo -e "export KAGGLE_CONFIG_DIR=\"$CACHE_DIR/kaggle\"" >> "$ENV_FILE"
    echo -e "" >> "$ENV_FILE"

    echo -e "${GREEN}✅ 環境變數已寫入 $ENV_FILE${NC}"
fi

# 立即載入環境變數
export PROJECT_ROOT="$PROJECT_DIR"
export DATASET_ROOT="$DATASET_DIR"
export HF_HOME="$CACHE_DIR/huggingface"
export TRANSFORMERS_CACHE="$CACHE_DIR/huggingface"
export TORCH_HOME="$CACHE_DIR/torch"
export XDG_CACHE_HOME="$CACHE_DIR"
export KAGGLE_CONFIG_DIR="$CACHE_DIR/kaggle"

echo -e "${GREEN}✅ 環境變數已載入${NC}"

# ==============================================================================
# 4. 複製專案檔案
# ==============================================================================

echo -e "\n${YELLOW}[4/6] 複製專案檔案...${NC}"

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "$CURRENT_DIR" != "$PROJECT_DIR" ]; then
    echo -e "${BLUE}當前位置：${CURRENT_DIR}${NC}"
    echo -e "${BLUE}目標位置：${PROJECT_DIR}${NC}"

    read -p "是否要將專案移動到 AI_WAREHOUSE 結構？(y/N): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}複製檔案中...${NC}"
        rsync -av --progress \
            --exclude 'venv' \
            --exclude '__pycache__' \
            --exclude '*.pyc' \
            --exclude '.git' \
            --exclude 'datasets/*/.*' \
            "$CURRENT_DIR/" "$PROJECT_DIR/"

        echo -e "${GREEN}✅ 專案已複製到：${PROJECT_DIR}${NC}"
        echo -e "${YELLOW}⚠️  請手動刪除舊位置的檔案：${CURRENT_DIR}${NC}"
    else
        echo -e "${YELLOW}⚠️  跳過移動，繼續使用當前位置${NC}"
        PROJECT_DIR="$CURRENT_DIR"
    fi
else
    echo -e "${GREEN}✅ 專案已在正確位置${NC}"
fi

# ==============================================================================
# 5. 設定 Python 虛擬環境
# ==============================================================================

echo -e "\n${YELLOW}[5/6] 設定 Python 虛擬環境...${NC}"

cd "$PROJECT_DIR"

if [ ! -d "venv" ]; then
    echo -e "${BLUE}建立虛擬環境...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ 虛擬環境已建立${NC}"
fi

# 啟動虛擬環境並安裝套件
echo -e "${BLUE}安裝 Python 套件...${NC}"
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}✅ Python 套件安裝完成${NC}"

# ==============================================================================
# 6. 建立符號連結
# ==============================================================================

echo -e "\n${YELLOW}[6/6] 建立符號連結...${NC}"

# 在專案目錄建立指向資料集的符號連結
if [ ! -L "$PROJECT_DIR/datasets_link" ]; then
    ln -s "$DATASET_DIR" "$PROJECT_DIR/datasets_link"
    echo -e "${GREEN}✅ 建立符號連結：datasets_link -> $DATASET_DIR${NC}"
fi

# ==============================================================================
# 完成
# ==============================================================================

echo -e "\n${GREEN}===================================================================${NC}"
echo -e "${GREEN}  ✅ 設定完成！${NC}"
echo -e "${GREEN}===================================================================${NC}"

echo -e "\n${BLUE}專案資訊：${NC}"
echo -e "  專案目錄：${GREEN}$PROJECT_DIR${NC}"
echo -e "  資料集目錄：${GREEN}$DATASET_DIR${NC}"
echo -e "  快取目錄：${GREEN}$CACHE_DIR${NC}"

echo -e "\n${BLUE}下一步：${NC}"
echo -e "  1. 重新載入環境變數：${YELLOW}source ~/.bashrc${NC}"
echo -e "  2. 切換到專案目錄：${YELLOW}cd $PROJECT_DIR${NC}"
echo -e "  3. 啟動虛擬環境：${YELLOW}source venv/bin/activate${NC}"
echo -e "  4. 下載資料集：${YELLOW}python datasets/download_datasets_warehouse.py --all${NC}"

echo -e "\n${BLUE}環境變數已設定：${NC}"
echo -e "  PROJECT_ROOT=$PROJECT_ROOT"
echo -e "  DATASET_ROOT=$DATASET_ROOT"
echo -e "  HF_HOME=$HF_HOME"

echo -e "\n${GREEN}🎉 開始你的資料分析之旅！${NC}"

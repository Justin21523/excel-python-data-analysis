#!/bin/bash

# ==============================================================================
# Data Analysis Environment Setup - data_env
# ==============================================================================
#
# 這個腳本會：
# 1. 從 ai_env 匯出套件列表（除了 numpy）
# 2. 建立新的 conda 環境 data_env
# 3. 安裝所有需要的資料分析套件
# 4. 設定正確的環境變數（AI_WAREHOUSE 3.0）
#
# 使用方式：
#   chmod +x setup_data_env.sh
#   ./setup_data_env.sh
#
# ==============================================================================

set -e

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}===================================================================${NC}"
echo -e "${BLUE}  Data Analysis Environment Setup${NC}"
echo -e "${BLUE}  建立 data_env conda 環境${NC}"
echo -e "${BLUE}===================================================================${NC}"

# ==============================================================================
# 1. 檢查 ai_env 是否存在
# ==============================================================================

echo -e "\n${YELLOW}[1/5] 檢查 ai_env 環境...${NC}"

if ! conda env list | grep -q "ai_env"; then
    echo -e "${RED}❌ ai_env 環境不存在！${NC}"
    echo -e "${YELLOW}將使用預設套件列表建立 data_env${NC}"
    USE_AI_ENV=false
else
    echo -e "${GREEN}✅ ai_env 環境存在${NC}"
    USE_AI_ENV=true
fi

# ==============================================================================
# 2. 匯出 ai_env 套件列表（除了 numpy）
# ==============================================================================

if [ "$USE_AI_ENV" = true ]; then
    echo -e "\n${YELLOW}[2/5] 從 ai_env 匯出套件列表...${NC}"

    # 匯出套件列表
    conda list -n ai_env --export > /tmp/ai_env_packages.txt

    # 移除 numpy 相關套件（因為要使用最新版本）
    grep -v "numpy" /tmp/ai_env_packages.txt > /tmp/data_env_packages.txt || true

    echo -e "${GREEN}✅ 套件列表已匯出${NC}"
    echo -e "${BLUE}   總套件數：$(wc -l < /tmp/ai_env_packages.txt)${NC}"
    echo -e "${BLUE}   過濾後套件數：$(wc -l < /tmp/data_env_packages.txt)${NC}"
fi

# ==============================================================================
# 3. 建立 data_env 環境
# ==============================================================================

echo -e "\n${YELLOW}[3/5] 建立 data_env 環境...${NC}"

if conda env list | grep -q "data_env"; then
    echo -e "${YELLOW}⚠️  data_env 已存在！${NC}"
    read -p "是否要刪除並重新建立？(y/N): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}刪除舊環境...${NC}"
        conda env remove -n data_env -y
    else
        echo -e "${YELLOW}保留現有環境，跳過建立步驟${NC}"
        exit 0
    fi
fi

# 建立新環境（Python 3.11）
echo -e "${BLUE}建立 Python 3.11 環境...${NC}"
conda create -n data_env python=3.11 -y

echo -e "${GREEN}✅ data_env 環境已建立${NC}"

# ==============================================================================
# 4. 安裝套件
# ==============================================================================

echo -e "\n${YELLOW}[4/5] 安裝資料分析套件...${NC}"

# 啟動環境
source $(conda info --base)/etc/profile.d/conda.sh
conda activate data_env

# 安裝核心套件
echo -e "${BLUE}安裝核心套件...${NC}"
conda install -y -c conda-forge \
    numpy \
    pandas \
    scipy \
    scikit-learn \
    matplotlib \
    seaborn \
    jupyter \
    notebook \
    jupyterlab

# 安裝 Excel 相關套件
echo -e "${BLUE}安裝 Excel 相關套件...${NC}"
pip install openpyxl xlrd xlsxwriter

# 安裝資料下載套件
echo -e "${BLUE}安裝資料下載套件...${NC}"
pip install kaggle ucimlrepo datasets

# 安裝視覺化套件
echo -e "${BLUE}安裝視覺化套件...${NC}"
pip install plotly kaleido

# 安裝商業分析套件
echo -e "${BLUE}安裝商業分析套件...${NC}"
pip install mlxtend

# 安裝自動化套件
echo -e "${BLUE}安裝自動化套件...${NC}"
pip install schedule pyyaml python-pptx reportlab

# 安裝開發工具
echo -e "${BLUE}安裝開發工具...${NC}"
pip install black flake8 pytest ipython

# 如果有 ai_env 的套件列表，安裝額外套件
if [ "$USE_AI_ENV" = true ] && [ -f /tmp/data_env_packages.txt ]; then
    echo -e "${BLUE}安裝 ai_env 的額外套件...${NC}"
    # 這裡可以選擇性安裝一些套件
    # conda install -y --file /tmp/data_env_packages.txt
    echo -e "${YELLOW}⚠️  跳過完整複製，僅安裝核心套件${NC}"
fi

echo -e "${GREEN}✅ 所有套件安裝完成${NC}"

# ==============================================================================
# 5. 設定環境變數
# ==============================================================================

echo -e "\n${YELLOW}[5/5] 設定環境變數...${NC}"

# 取得 conda 環境路徑
ENV_PATH=$(conda info --envs | grep "data_env" | awk '{print $NF}')
ENV_VARS_DIR="$ENV_PATH/etc/conda/activate.d"
mkdir -p "$ENV_VARS_DIR"

# 建立啟動腳本
cat > "$ENV_VARS_DIR/env_vars.sh" << 'EOF'
#!/bin/bash

# AI_WAREHOUSE 3.0 環境變數
export PROJECT_ROOT="/mnt/c/ai_projects/excel-python-data-analysis"
export DATASET_ROOT="/mnt/data/datasets/ecommerce"

# HuggingFace & PyTorch Cache
export HF_HOME="/mnt/c/ai_cache/huggingface"
export TRANSFORMERS_CACHE="/mnt/c/ai_cache/huggingface"
export TORCH_HOME="/mnt/c/ai_cache/torch"
export XDG_CACHE_HOME="/mnt/c/ai_cache"

# Kaggle
export KAGGLE_CONFIG_DIR="/mnt/c/ai_cache/kaggle"

# Jupyter
export JUPYTER_CONFIG_DIR="/mnt/c/ai_cache/jupyter"

echo "✅ AI_WAREHOUSE 3.0 環境變數已載入"
echo "   PROJECT_ROOT: $PROJECT_ROOT"
echo "   DATASET_ROOT: $DATASET_ROOT"
EOF

# 建立停用腳本
ENV_DEACTIVATE_DIR="$ENV_PATH/etc/conda/deactivate.d"
mkdir -p "$ENV_DEACTIVATE_DIR"

cat > "$ENV_DEACTIVATE_DIR/env_vars.sh" << 'EOF'
#!/bin/bash

# 清除環境變數
unset PROJECT_ROOT
unset DATASET_ROOT
unset HF_HOME
unset TRANSFORMERS_CACHE
unset TORCH_HOME
unset XDG_CACHE_HOME
unset KAGGLE_CONFIG_DIR
unset JUPYTER_CONFIG_DIR
EOF

# 設定權限
chmod +x "$ENV_VARS_DIR/env_vars.sh"
chmod +x "$ENV_DEACTIVATE_DIR/env_vars.sh"

echo -e "${GREEN}✅ 環境變數已設定${NC}"

# ==============================================================================
# 完成
# ==============================================================================

echo -e "\n${GREEN}===================================================================${NC}"
echo -e "${GREEN}  ✅ data_env 環境設定完成！${NC}"
echo -e "${GREEN}===================================================================${NC}"

# 顯示套件資訊
echo -e "\n${BLUE}已安裝套件：${NC}"
conda list -n data_env | grep -E "pandas|numpy|scipy|scikit-learn|matplotlib|seaborn|jupyter|openpyxl"

echo -e "\n${BLUE}環境資訊：${NC}"
echo -e "  環境名稱：${GREEN}data_env${NC}"
echo -e "  Python 版本：${GREEN}$(conda run -n data_env python --version)${NC}"
echo -e "  環境路徑：${GREEN}$ENV_PATH${NC}"

echo -e "\n${BLUE}使用方式：${NC}"
echo -e "  啟動環境：${YELLOW}conda activate data_env${NC}"
echo -e "  停用環境：${YELLOW}conda deactivate${NC}"
echo -e "  啟動 Jupyter：${YELLOW}conda activate data_env && jupyter lab${NC}"

echo -e "\n${BLUE}下一步：${NC}"
echo -e "  1. 啟動環境：${YELLOW}conda activate data_env${NC}"
echo -e "  2. 下載資料集：${YELLOW}python datasets/download_datasets_warehouse.py --priority${NC}"
echo -e "  3. 開始學習：${YELLOW}jupyter lab${NC}"

echo -e "\n${GREEN}🎉 開始你的資料分析之旅！${NC}"

# 清理暫存檔案
rm -f /tmp/ai_env_packages.txt /tmp/data_env_packages.txt

#!/bin/bash
# ============================================================================
# Week 21+ ML/DL 環境設置腳本
# 在現有 data_env 中安裝所有機器學習/深度學習套件
# ============================================================================

set -e  # 遇到錯誤立即退出

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     Week 21+ ML/DL 環境設置                                  ║"
echo "║     安裝 PyTorch, HuggingFace Transformers, XGBoost 等       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# 確保 conda 初始化
source ~/miniconda3/etc/profile.d/conda.sh

# 激活 data_env 環境
echo "🔧 激活 data_env 環境..."
conda activate data_env

# 確認 Python 版本
echo ""
echo "📊 當前 Python 版本："
python --version

# 安裝 ML/DL 核心套件
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "第 1 步：安裝深度學習框架 (PyTorch)"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "🔥 安裝 PyTorch (CPU 版本，適合筆記本學習)..."
# CPU 版本，體積較小，適合學習
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "第 2 步：安裝 NLP 工具 (HuggingFace)"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "🤗 安裝 HuggingFace Transformers & Datasets..."
pip install transformers datasets tokenizers accelerate

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "第 3 步：安裝經典機器學習套件"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📦 安裝 XGBoost, LightGBM, CatBoost..."
pip install xgboost lightgbm catboost

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "第 4 步：安裝實驗追蹤工具"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📈 安裝 Weights & Biases (W&B) 和 MLflow..."
pip install wandb mlflow

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "第 5 步：安裝進階 ML 工具"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "🔬 安裝 Optuna (超參數優化), SHAP (模型解釋), imbalanced-learn..."
pip install optuna shap imbalanced-learn

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "第 6 步：安裝推薦系統套件"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "⭐ 安裝 Surprise (協同過濾), implicit (ALS), mlxtend (購物籃分析)..."
pip install scikit-surprise implicit mlxtend

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "第 7 步：安裝時間序列套件"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📅 安裝 Prophet (Facebook), statsmodels, pmdarima (Auto ARIMA)..."
pip install prophet statsmodels pmdarima

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "第 8 步：安裝深度學習輔助工具"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "⚡ 安裝 PyTorch Lightning (簡化訓練), torchmetrics..."
pip install pytorch-lightning torchmetrics

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "第 9 步：安裝 NLP 進階工具"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📝 安裝 spaCy (NLP), gensim (Word2Vec), nltk, textblob..."
pip install spacy gensim nltk textblob

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "第 10 步：安裝圖神經網絡套件"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "🕸️  安裝 PyTorch Geometric (GNN)..."
pip install torch-geometric

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "第 11 步：安裝其他實用工具"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "🛠️  安裝 tqdm (進度條), joblib (並行), pyyaml..."
pip install tqdm joblib pyyaml

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "驗證安裝"
echo "════════════════════════════════════════════════════════════════"
echo ""
python -c "
import sys
print('✅ Python:', sys.version.split()[0])

# 檢查核心套件
packages = [
    ('torch', 'PyTorch'),
    ('transformers', 'HuggingFace Transformers'),
    ('xgboost', 'XGBoost'),
    ('lightgbm', 'LightGBM'),
    ('catboost', 'CatBoost'),
    ('sklearn', 'scikit-learn'),
    ('wandb', 'Weights & Biases'),
    ('mlflow', 'MLflow'),
    ('optuna', 'Optuna'),
    ('shap', 'SHAP'),
    ('surprise', 'Surprise'),
    ('implicit', 'Implicit'),
    ('prophet', 'Prophet'),
    ('statsmodels', 'Statsmodels'),
    ('pytorch_lightning', 'PyTorch Lightning'),
    ('spacy', 'spaCy'),
    ('gensim', 'Gensim'),
    ('torch_geometric', 'PyTorch Geometric'),
]

print('\n📦 已安裝套件檢查：\n')
for module, name in packages:
    try:
        mod = __import__(module)
        version = getattr(mod, '__version__', 'unknown')
        print(f'  ✅ {name:30s} {version}')
    except ImportError:
        print(f'  ❌ {name:30s} 未安裝')

# 檢查 PyTorch CUDA 支援
import torch
print(f'\n🔥 PyTorch CUDA 可用: {torch.cuda.is_available()}')
print(f'   PyTorch 版本: {torch.__version__}')
"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "生成 requirements_ml.txt"
echo "════════════════════════════════════════════════════════════════"
echo ""
pip freeze > /home/justin/web-projects/excel-python-data-analysis/requirements_ml.txt
echo "✅ 已生成 requirements_ml.txt (包含所有已安裝套件)"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    ✅ 安裝完成！                             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 環境資訊："
echo "   Python: $(python --version)"
echo "   Conda 環境: data_env"
echo "   套件列表: requirements_ml.txt"
echo ""
echo "🚀 下一步："
echo "   1. 執行測試腳本: python test_ml_environment.py"
echo "   2. 開始 Week 21 課程"
echo "   3. 查看完整課程規劃: cat ~/.llm_provider/plans/distributed-cooking-wadler.md"
echo ""

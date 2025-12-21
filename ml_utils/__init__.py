"""
ml_utils - Week 21-44 機器學習/深度學習共用工具庫

這個套件包含 Week 21-44 所有課程共用的工具函數，
涵蓋資料處理、模型訓練、評估、部署等各個環節。

模組結構：
- data_processing: 資料載入、前處理、特徵工程
- modeling: 模型訓練、超參數優化、早停等
- evaluation: 評估指標、視覺化、模型比較
- deployment: 模型保存、載入、推理
- visualization: 繪圖工具、儀表板生成

使用方式：
    from ml_utils.data_processing import load_olist_ml, create_features
    from ml_utils.evaluation import classification_report, plot_confusion_matrix
    from ml_utils.modeling import train_with_cv, hyperparameter_tuning
"""

__version__ = "1.0.0"
__author__ = "Justin (AI-Enhanced Learning Project)"

# 未來可在此處導入常用函數，方便 import
# from .data_processing import load_olist_ml, create_rfm_features
# from .evaluation import classification_metrics, plot_roc_curve

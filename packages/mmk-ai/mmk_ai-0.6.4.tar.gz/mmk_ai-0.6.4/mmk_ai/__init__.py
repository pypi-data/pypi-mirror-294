__version__ = "0.6.0"

# Modülleri içe aktar
from .data_preprocessing import load_csv, preprocess_data
from .visualization import univariate_visualization, bivariate_visualization, multivariate_visualization
from .model_training import train_model_threaded, optimize_hyperparameters, save_model, load_model
from .evaluation import evaluate_model
from .scoring import calculate_scores, plot_roc_curve

# Sabitleri tanımla
DEFAULT_SEED = 42

# Başlatma fonksiyonu
def init():
    print("mmk_ai package initialized")

# Başlatma işlemini gerçekleştir
init()

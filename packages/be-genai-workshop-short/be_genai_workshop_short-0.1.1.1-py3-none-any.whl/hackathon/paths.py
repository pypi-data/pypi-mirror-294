import os

_PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
_REPOSITORY_DIR = os.path.dirname(_PACKAGE_DIR)

EVALUATION_DIR = os.path.join(_PACKAGE_DIR, "evaluation")

REQUIREMENTS_COLAB_PATH = os.path.join(_REPOSITORY_DIR, "requirements_colab.txt")  # noqa E501
DOTENV_PATH = os.path.join(_REPOSITORY_DIR, ".env")
PRODUCT_REVIEWS_PATH = os.path.join(_PACKAGE_DIR, "data", "product_reviews.xlsx")  # noqa E501
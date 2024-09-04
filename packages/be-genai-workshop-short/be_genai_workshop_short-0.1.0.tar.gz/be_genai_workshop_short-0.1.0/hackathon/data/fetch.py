import pandas as pd
from hackathon.paths import PRODUCT_REVIEWS_PATH


def product_reviews():
    return pd.read_excel(PRODUCT_REVIEWS_PATH)
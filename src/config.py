import os

MODEL_NAME = 'deepseek-ai/DeepSeek-OCR'

CONFIG = {
    'dpi': 400,
    'base_size': 1024,
    'image_size': 640,
    'output_dir': './output',
    'images_dir': './images'
}

ELEMENT_NAMES = {
    'AL': 'Aluminum', 'V': 'Vanadium', 'FE': 'Iron', 'C': 'Carbon',
    'N': 'Nitrogen', 'O': 'Oxygen', 'Y': 'Yttrium', 'H': 'Hydrogen',
    'TI': 'Titanium', 'SI': 'Silicon', 'MN': 'Manganese', 'P': 'Phosphorus',
    'S': 'Sulfur', 'CR': 'Chromium', 'MO': 'Molybdenum', 'NI': 'Nickel',
    'CU': 'Copper', 'W': 'Tungsten', 'CO': 'Cobalt', 'NB': 'Niobium',
    'B': 'Boron', 'SN': 'Tin', 'ZN': 'Zinc', 'PB': 'Lead', 'ZR': 'Zirconium',
    'TA': 'Tantalum', 'HF': 'Hafnium', 'MG': 'Magnesium', 'CA': 'Calcium'
}

ELEMENTS = set(ELEMENT_NAMES.keys())

os.environ["CUDA_VISIBLE_DEVICES"] = '0'

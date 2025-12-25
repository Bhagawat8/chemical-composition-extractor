import sys
import os
from io import StringIO
import torch
from transformers import AutoModel, AutoTokenizer
from .config import MODEL_NAME, CONFIG

_model = None
_tokenizer = None


def load_model():
    global _model, _tokenizer
    
    if _model is not None:
        return _model, _tokenizer
    
    print("Loading DeepSeek-OCR model...")
    _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    _model = AutoModel.from_pretrained(
        MODEL_NAME, 
        _attn_implementation='flash_attention_2', 
        trust_remote_code=True, 
        use_safetensors=True
    )
    _model = _model.eval().cuda().to(torch.bfloat16)
    print("Model loaded")
    
    return _model, _tokenizer


def run_ocr(image_path, model=None, tokenizer=None):
    if model is None or tokenizer is None:
        model, tokenizer = load_model()
    
    prompt = "<image>\nFree OCR."
    os.makedirs(CONFIG['output_dir'], exist_ok=True)
    
    old_stdout = sys.stdout
    sys.stdout = captured = StringIO()
    
    try:
        result = model.infer(
            tokenizer, 
            prompt=prompt, 
            image_file=image_path, 
            output_path=CONFIG['output_dir'],
            base_size=CONFIG['base_size'], 
            image_size=CONFIG['image_size'], 
            crop_mode=True,
            save_results=True, 
            test_compress=True
        )
    finally:
        sys.stdout = old_stdout
    
    return result if result else captured.getvalue()


def run_ocr_on_all_images(image_paths, model=None, tokenizer=None):
    if model is None or tokenizer is None:
        model, tokenizer = load_model()
    
    all_text = []
    
    for i, img_path in enumerate(image_paths, 1):
        print(f"  OCR Page {i}/{len(image_paths)}...", end=" ")
        text = run_ocr(img_path, model, tokenizer)
        all_text.append(f"\n{'='*50}\nPAGE {i}\n{'='*50}\n{text}")
        print(f"{len(text)} chars")
    
    return '\n'.join(all_text)

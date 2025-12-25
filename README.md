# 🧪 Chemical Composition Extraction from Material Certificates

A document intelligence pipeline that extracts chemical composition data and other information from PDFs using DeepSeek-OCR, a vision-language model optimized for document understanding.

---

## 📖 Introduction

Material certificates are critical documents in manufacturing and supply chain management. They contain chemical composition tables that define the exact elemental makeup of metal alloys like Ti-6Al-4V (Titanium Grade 5). Manually extracting this data is tedious, error-prone, and does not scale.

This project automates the entire extraction process. You give it a PDF, it returns a clean CSV with element symbols, values, units, and metadata. No templates. No manual intervention.

The core challenge was not just OCR, but understanding document structure. Traditional OCR tools like Tesseract can read text, but they cannot understand that "6.53 - 6.54" under "AL" in a table means Aluminum content is in that range. We needed something smarter.

After evaluating multiple approaches including Tesseract with layout analysis and various open-source alternatives, we settled on DeepSeek-OCR. It is a vision-language model that understands documents the way humans do: visually. It outputs structured markdown with tables intact, which makes parsing significantly easier.

---

## 💻 System Requirements

### 🔧 Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| GPU | 16GB VRAM (T4) | 24GB VRAM (A10G) |
| System RAM | 16GB | 32GB |
| Storage | 20GB free | SSD preferred |

> **⚠️ GPU is mandatory.** DeepSeek-OCR is a 7-billion parameter vision-language model. CPU inference takes 10+ minutes per page with vanilla attention algorithm, making it inefficient.

---

### ⚡ Why Flash Attention is Default

We use Flash Attention 2.0 as the default attention mechanism for three reasons:

1. **💾 Memory efficiency**: Flash Attention reduces VRAM usage by 2-4x compared to standard attention, allowing the 7B model to fit on 16GB GPUs
2. **🚀 Speed**: 2-3x faster inference on supported hardware (Ampere architecture and newer)
3. **✅ No accuracy loss**: Flash Attention is mathematically equivalent to standard attention

> Flash Attention requires CUDA-capable GPU. On unsupported hardware, the model falls back to standard attention but may run out of memory.

---

### 💰 Estimated Processing Cost (A10G GPU)

Based on testing with AWS g5.xlarge instance ($1.006/hour for A10G):

| Metric | Value |
|--------|-------|
| ⏱️ Time per page | ~12-15 seconds |
| 📄 Pages per hour | ~240-300 |
| 💵 Cost per page | ~$0.003-0.004 |
| 📊 Cost per 100 pages | ~$0.35-0.40 |

> 📝 Model loading takes ~30 seconds on first run. Subsequent pages process faster with cached model.

---

## ✨ Core Features and Implementation

### 🔄 What This Pipeline Does

1. 📥 Takes any PDF file as input
2. 🖼️ Converts PDF pages to high-resolution images (400 DPI)
3. 🔃 Automatically corrects image orientation using Tesseract OSD
4. 👁️ Runs DeepSeek-OCR on each images individually to extract text with structure preserved
5. 🔗 Merged the OCR extracted text of all images.
6. 📊 Parses the OCR output to identify chemical composition tables
7. 🌍 Handles German number formats (comma as decimal separator) and other irregularity
8. 📋 Distinguishes between requirement values and actual test results
9. 📤 Exports clean CSV with element data and PDF's metadata

---

### 🎯 Key Technical Decisions

#### 🤔 Why DeepSeek-OCR over Tesseract?

Tesseract is excellent for clean, well-formatted text. But material certificates are messy. They have rotated pages, multi-column layouts, tables with merged cells, and stamps overlapping text. DeepSeek-OCR handles all of this because it processes the document as an image and understands layout contextually.

#### 🔄 Why Tesseract for Orientation Detection?

DeepSeek-OCR expects correctly oriented images. Scanned certificates are often rotated 90 or 270 degrees. Tesseract OSD is fast and reliable for detecting rotation. We use it purely for orientation detection, not for OCR.

#### 🔍 Why 400 DPI?

We tested 200, 300, and 400 DPI. At 200 DPI, small text became blurry and OCR accuracy dropped. At 400 DPI, we get consistently readable text without excessive file sizes.

#### 🌐 Handling German Number Formats

European certificates often use German notation: `0,004` instead of `0.004`. The parser detects comma-period patterns and converts appropriately.

---

## 📁 Project Structure

```
codebase/
    run.py                      # CLI entry point
    requirements.txt            # Python dependencies
    Dockerfile                  # Container configuration
    Submission_notebook.ipynb   # Jupyter notebook for interactive use
    README.md                   # This documentation
    .gitignore                  # Git ignore rules
    src/
        __init__.py             # Package exports
        config.py               # Settings and element lookup
        pdf_io.py               # PDF to image conversion
        ocr_engine.py           # DeepSeek model and inference
        parser.py               # Text parsing and extraction
        export.py               # DataFrame and CSV generation
        main.py                 # Pipeline orchestration
    data/
        input/                  # Place input PDFs here
    diagrams/                   # Flow diagrams
    tests/                      # Unit tests
    output/                     # Generated files
    images/                     # Converted page images
```

---

### 📝 File Descriptions

#### 🚀 `run.py`

Command-line entry point. Handles argument parsing and calls the main pipeline.

```bash
python run.py certificate.pdf -o results.csv --dpi 400
```

---

#### 📓 `Submission_notebook.ipynb`

Jupyter notebook version of the pipeline. Useful for:
- 🔧 Interactive development and debugging
- ☁️ Running on cloud platforms (Kaggle, SageMaker, Colab)
- 📊 Step-by-step execution with visual output
- ⚡ Quick prototyping without CLI setup

The notebook contains the same logic as the Python modules but in cell-by-cell format with inline outputs.

---

#### 📦 `requirements.txt`

All Python dependencies grouped by purpose:
- **Core**: torch, transformers
- **PDF**: pdf2image, Pillow
- **OCR**: pytesseract
- **Data**: pandas, numpy
- **Model**: einops, safetensors, accelerate

---

#### ⚙️ `src/config.py`

Configuration constants:
- Model name: `deepseek-ai/DeepSeek-OCR`
- DPI: 400 (configurable)
- Image size: 1024 base, 640 inference
- Element lookup table (24 elements)

---

#### 🖼️ `src/pdf_io.py`

PDF to image conversion with orientation fix:
- Uses pdf2image (Poppler wrapper)
- Tesseract OSD for rotation detection
- Saves as PNG for lossless quality

---

#### 👁️ `src/ocr_engine.py`

DeepSeek-OCR model management:
- Lazy loading with global cache
- Flash Attention 2.0 enabled
- bfloat16 precision for memory efficiency
- stdout capture for inference results

---

#### 🔍 `src/parser.py`

Text parsing and value extraction:
- Markdown table detection
- German number conversion
- Value type detection (exact, range, max, less-than)
- Element symbol recognition

---

#### 📤 `src/export.py`

Output generation:
- Pandas DataFrame creation
- Column ordering and sorting
- CSV export with metadata

---

#### 🎯 `src/main.py`

Pipeline orchestration:
- Coordinates all modules
- Progress logging
- Error handling
- CLI interface

---

## 🔄 High Level Workflow

```
                    +------------------+
                    |   📄 Input PDF   |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    | pdf_to_images()  |
                    | (400 DPI, PNG)   |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    | fix_orientation()|
                    | (Tesseract OSD)  |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    | run_ocr()        |
                    | (DeepSeek-OCR)   |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    | extract_         |
                    | composition()    |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    | create_dataframe |
                    | save_csv()       |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |  📊 Output CSV   |
                    +------------------+
```

> 💡 Each step has a single responsibility. If the CSV is wrong, check the parser. If parsing fails, check the OCR. If OCR is garbled, check orientation.

---

## 🛠️ Why These Tools

| Tool | Purpose | Why Chosen |
|------|---------|------------|
| 🤖 DeepSeek-OCR | Document OCR | Understands layout, outputs markdown tables |
| ⚡ Flash Attention | Attention mechanism | 2-3x faster, 2-4x less VRAM |
| 🔄 Tesseract OSD | Orientation detection | Fast, accurate, offline |
| 📄 pdf2image | PDF conversion | Reliable, handles edge cases |
| 📑 Poppler | PDF rendering | Industry standard, well-maintained |

---

## ⚠️ Constraints and Limitations

- **🖥️ GPU required**: CPU inference is too slow for practical use
- **📄 Single certificate per PDF**: Multi-certificate PDFs merge data incorrectly
- **🔤 Latin alphabet**: Element symbols must be in standard notation
- **🔍 OCR accuracy**: Values like 0.004 and 0.0004 can be confused on poor prints

---

## 🚀 Future Enhancements

- 📊 Confidence scores for extracted values
- 📑 Multi-certificate PDF support
- 🗄️ Batch processing with database output
- 🎯 Fine-tuned model for material certificates

---

## 📖 Usage

### 📥 Installation

```bash
# System dependencies
sudo apt-get install poppler-utils tesseract-ocr

# Python dependencies
pip install -r requirements.txt

# Flash Attention (requires GPU)
pip install flash-attn --no-build-isolation
```

---

### 💻 Command Line

```bash
python run.py certificate.pdf
python run.py certificate.pdf -o results.csv
python run.py certificate.pdf --dpi 300
```

---

### 🐍 Python Module

```python
from src import extract_chemical_composition

df = extract_chemical_composition("certificate.pdf")
print(df)
```

---

### 📓 Jupyter Notebook

Open `Submission_notebook.ipynb` and run cells sequentially. The notebook includes installation cells for cloud environments.

---

### 🐳 Docker

Build the Docker image:

```bash
docker build -t chemical-composition-extractor .
---

## 🛠️ Development Notes

This project started with Tesseract and OpenCV-based table detection. It worked for clean certificates but failed on rotated scans and unusual layouts.

The breakthrough came with vision-language models. DeepSeek-OCR understands documents visually and outputs structured markdown, making parsing straightforward.

> 💡 **Key debugging insight**: `model.infer()` prints to stdout instead of returning results. Capturing stdout solved the "None return" problem that consumed hours of debugging.

> 📝 **Lesson learned**: orientation matters more than resolution. A rotated high-res image produces worse OCR than a correctly oriented low-res image.

---

## 📚 References

- 🤖 **DeepSeek-OCR Model**: https://huggingface.co/deepseek-ai/DeepSeek-OCR
- 📄 **DeepSeek-VL2 Paper**: https://arxiv.org/abs/2412.10302
- ⚡ **Flash Attention Paper**: https://arxiv.org/abs/2205.14135
- 📖 **Transformers Library**: https://huggingface.co/docs/transformers

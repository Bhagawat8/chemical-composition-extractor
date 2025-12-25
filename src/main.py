import argparse
from pathlib import Path
from .pdf_io import pdf_to_images
from .ocr_engine import load_model, run_ocr_on_all_images
from .parser import extract_composition, extract_metadata
from .export import create_dataframe, save_csv, save_ocr_text


def extract_chemical_composition(pdf_path, output_csv=None):
    print("=" * 60)
    print("CHEMICAL COMPOSITION EXTRACTION PIPELINE")
    print("=" * 60)
    
    print("\n[Step 1] Converting PDF to images...")
    image_paths = pdf_to_images(pdf_path)
    
    print("\n[Step 2] Loading model and running OCR...")
    model, tokenizer = load_model()
    ocr_text = run_ocr_on_all_images(image_paths, model, tokenizer)
    print(f"  Total: {len(ocr_text)} chars")
    
    save_ocr_text(ocr_text)
    
    print("\n[Step 3] Parsing chemical composition...")
    composition = extract_composition(ocr_text)
    metadata = extract_metadata(ocr_text)
    
    if not composition:
        print("  No composition found")
        return None
    
    df = create_dataframe(composition, metadata)
    
    print("\n[Step 4] Saving results...")
    save_csv(df, output_csv)
    
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)
    
    return df


def main():
    parser = argparse.ArgumentParser(description='Extract chemical composition from material certificates')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('-o', '--output', help='Output CSV file path', default=None)
    
    args = parser.parse_args()
    
    if not Path(args.pdf_path).exists():
        print(f"Error: File not found: {args.pdf_path}")
        return 1
    
    df = extract_chemical_composition(args.pdf_path, args.output)
    
    if df is not None and not df.empty:
        print("\nExtracted data:")
        print(df.to_string())
        return 0
    else:
        return 1


if __name__ == '__main__':
    exit(main())

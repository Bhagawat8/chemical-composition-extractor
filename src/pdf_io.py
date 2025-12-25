import os
from pathlib import Path
from pdf2image import convert_from_path
import pytesseract
from .config import CONFIG


def fix_orientation(img):
    try:
        osd = pytesseract.image_to_osd(img)
        rotation = 0
        for line in osd.split('\n'):
            if 'Rotate:' in line:
                rotation = int(line.split(':')[1].strip())
                break
        
        if rotation == 90:
            img = img.rotate(-90, expand=True)
        elif rotation == 180:
            img = img.rotate(180, expand=True)
        elif rotation == 270:
            img = img.rotate(-270, expand=True)
        
        return img
    except:
        return img


def pdf_to_images(pdf_path, dpi=None, output_dir=None):
    dpi = dpi or CONFIG['dpi']
    output_dir = output_dir or CONFIG['images_dir']
    
    os.makedirs(output_dir, exist_ok=True)
    pdf_name = Path(pdf_path).stem
    
    print(f"Converting: {pdf_path} (DPI: {dpi})")
    
    images = convert_from_path(pdf_path, dpi=dpi)
    print(f"  Pages: {len(images)}")
    
    saved_paths = []
    for i, img in enumerate(images, 1):
        img = fix_orientation(img)
        img_path = f"{output_dir}/{pdf_name}_page_{i}.png"
        img.save(img_path, 'PNG')
        saved_paths.append(img_path)
        print(f"  Page {i} saved")
    
    return saved_paths

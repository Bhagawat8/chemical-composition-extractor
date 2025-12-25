import re
from .config import ELEMENTS, ELEMENT_NAMES


def german_to_float(text):
    if not text:
        return None
    text = str(text).strip().replace(' ', '')
    if '.' in text and ',' in text:
        text = text.replace('.', '').replace(',', '.')
    elif ',' in text:
        text = text.replace(',', '.')
    try:
        return float(text)
    except:
        return None


def parse_value(text):
    if not text:
        return None, None, None
    
    text = str(text).strip()
    text = re.sub(r'(\d),(\d)', r'\1.\2', text)
    
    m = re.search(r'(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)', text)
    if m:
        return float(m.group(1)), float(m.group(2)), 'range'
    
    m = re.search(r'max\s*[:\s]*(\d+\.?\d*)', text, re.I)
    if m:
        return float(m.group(1)), None, 'max'
    
    m = re.search(r'[<≤]\s*(\d+\.?\d*)', text)
    if m:
        return float(m.group(1)), None, 'less_than'
    
    m = re.search(r'(\d+\.?\d*)', text)
    if m:
        return float(m.group(1)), None, 'exact'
    
    return None, None, None


def extract_composition(text):
    results = []
    
    rows = []
    for line in text.split('\n'):
        if '|' in line and not re.match(r'^[\|\s\-:]+$', line.strip()):
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if cells:
                rows.append(cells)
    
    header_idx, header_row = None, None
    for i, row in enumerate(rows):
        if sum(1 for c in row if c.upper().strip() in ELEMENTS) >= 3:
            header_idx, header_row = i, row
            break
    
    if header_row:
        elem_map = {j: c.upper().strip() for j, c in enumerate(header_row) if c.upper().strip() in ELEMENTS}
        
        for row_idx in range(header_idx + 1, len(rows)):
            row = rows[row_idx]
            if sum(1 for c in row if c.upper().strip() in ELEMENTS) >= 3:
                continue
            
            row_type = 'actual'
            first = row[0].upper() if row else ''
            if 'TOP' in first:
                row_type = 'top'
            elif 'BOTTOM' in first:
                row_type = 'bottom'
            elif any(x in first for x in ['REQ', 'MIN', 'MAX', 'SPEC']):
                row_type = 'requirement'
            
            for col_idx, elem in elem_map.items():
                if col_idx < len(row):
                    val, max_val, vtype = parse_value(row[col_idx])
                    if val is not None:
                        entry = {
                            'element_symbol': elem,
                            'element_name': ELEMENT_NAMES.get(elem, elem),
                            'value': val,
                            'unit': 'wt.%',
                            'value_type': vtype,
                            'sample_position': row_type
                        }
                        if max_val is not None:
                            entry['max_value'] = max_val
                        results.append(entry)
    
    if re.search(r'ti[-\s]?remainder', text, re.I):
        results.append({
            'element_symbol': 'TI',
            'element_name': 'Titanium',
            'value': None,
            'unit': 'wt.%',
            'value_type': 'balance',
            'sample_position': 'actual'
        })
    
    return results


def extract_metadata(text):
    info = {}
    m = re.search(r'(Ti-6Al-4V|TI-6AL-4V)', text, re.I)
    if m:
        info['alloy'] = m.group(1).upper()
    m = re.search(r'Heat\s*(?:№|No\.?)[:\s]*([0-9\-]+)', text, re.I)
    if m:
        info['heat_no'] = m.group(1)
    return info

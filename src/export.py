import pandas as pd
from datetime import datetime


def create_dataframe(composition, metadata):
    if not composition:
        return pd.DataFrame()
    
    for item in composition:
        item.update(metadata)
    
    df = pd.DataFrame(composition)
    
    cols = ['element_symbol', 'element_name', 'value', 'max_value', 'unit', 
            'value_type', 'sample_position', 'alloy', 'heat_no']
    df = df[[c for c in cols if c in df.columns] + [c for c in df.columns if c not in cols]]
    df = df.sort_values(['element_symbol', 'sample_position']).reset_index(drop=True)
    
    return df


def save_csv(df, output_path=None):
    if output_path is None:
        output_path = f"chemical_composition_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    df.to_csv(output_path, index=False)
    print(f"Saved: {output_path}")
    print(f"  Entries: {len(df)}")
    if not df.empty:
        print(f"  Elements: {', '.join(sorted(df['element_symbol'].unique()))}")
    
    return output_path


def save_ocr_text(text, output_path='merged_ocr.txt'):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return output_path

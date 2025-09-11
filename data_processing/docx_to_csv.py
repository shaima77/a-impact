"""
סקריפט להמרת קובץ Word של דרישות רישוי ל-CSV
"""

import os
import sys
import polars as pl
from docx import Document
import re

def extract_requirements_from_docx(docx_path):
    """חילוץ דרישות מקובץ Word"""
    
    try:
        doc = Document(docx_path)
        requirements = []
        current_requirement = {}
        
        print(f"Processing document: {docx_path}")
        
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            
            if not text:
                continue
                
            # זיהוי כותרת דרישה חדשה
            if text and len(text) > 10:
                # אם יש לנו דרישה קודמת, שמור אותה
                if current_requirement.get('title'):
                    requirements.append(current_requirement.copy())
                    current_requirement = {}
                
                # התחל דרישה חדשה
                current_requirement = {
                    'title': text[:200],  # מגביל אורך כותרת
                    'description': text,
                    'authority': extract_authority(text),
                    'category': extract_category(text),
                    'priority': determine_priority(text),
                    'estimated_cost': '',
                    'processing_time': ''
                }
        
        # הוסף את הדרישה האחרונה
        if current_requirement.get('title'):
            requirements.append(current_requirement)
            
        print(f"Extracted {len(requirements)} requirements")
        return requirements
        
    except Exception as e:
        print(f"Error processing DOCX: {e}")
        return []

def extract_authority(text):
    """חילוץ רשות מוסמכת מהטקסט"""
    
    authorities = [
        'משרד הבריאות',
        'העירייה המקומית',
        'רשות הכבאות',
        'המשטרה',
        'משרד הפנים',
        'משרד התחבורה',
        'רשות המסים',
        'ביטוח לאומי',
        'משרד הכלכלה',
        'משרד העבודה',
        'רשות הרדיו',
        'חברת הגז',
        'רשות החשמל'
    ]
    
    text_lower = text.lower()
    
    for authority in authorities:
        if authority.lower() in text_lower:
            return authority
            
    # חיפוש דפוסים נוספים
    if 'עירייה' in text_lower or 'רשות מקומית' in text_lower:
        return 'העירייה המקומית'
    elif 'בריאות' in text_lower:
        return 'משרד הבריאות'
    elif 'כבאות' in text_lower or 'אש' in text_lower:
        return 'רשות הכבאות'
    elif 'משטרה' in text_lower:
        return 'המשטרה'
    elif 'גז' in text_lower:
        return 'חברת הגז/יועץ מוסמך'
    
    return 'לא צוין'

def extract_category(text):
    """זיהוי קטגוריית הדרישה"""
    
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['רישיון עסק', 'פתיחת עסק', 'עסק']):
        return 'רישיון עסק'
    elif any(word in text_lower for word in ['בריאות', 'תברואה', 'מזון']):
        return 'בריאות ותברואה'
    elif any(word in text_lower for word in ['אש', 'כבאות', 'בטיחות אש']):
        return 'בטיחות אש'
    elif any(word in text_lower for word in ['גז', 'בטיחות גז']):
        return 'בטיחות גז'
    elif any(word in text_lower for word in ['אלכוהול', 'משקאות חריפים']):
        return 'רישיון אלכוהול'
    elif any(word in text_lower for word in ['בנייה', 'תכנון']):
        return 'תכנון ובנייה'
    elif any(word in text_lower for word in ['מס', 'מסים', 'ארנונה']):
        return 'מיסוי'
    elif any(word in text_lower for word in ['עובדים', 'עבודה']):
        return 'העסקת עובדים'
    
    return 'כללי'

def determine_priority(text):
    """קביעת עדיפות הדרישה"""
    
    text_lower = text.lower()
    
    # עדיפות גבוהה
    high_priority_keywords = [
        'רישיון עסק', 'חובה', 'אסור', 'אישור כיבוי אש',
        'רישיון בריאות', 'בטיחות גז', 'משקאות חריפים'
    ]
    
    # עדיפות בינונית
    medium_priority_keywords = [
        'מומלץ', 'רצוי', 'יש לשקול', 'בהתאם לצורך'
    ]
    
    for keyword in high_priority_keywords:
        if keyword in text_lower:
            return 'high'
            
    for keyword in medium_priority_keywords:
        if keyword in text_lower:
            return 'medium'
    
    return 'low'

def save_to_csv(requirements, output_path):
    """שמירה ל-CSV"""
    
    try:
        df = pl.DataFrame(requirements)
        df.write_csv(output_path)
        print(f"Saved {len(requirements)} requirements to {output_path}")
        return True
        
    except Exception as e:
        print(f"Error saving CSV: {e}")
        return False

def main():
    """פונקציה ראשית"""
    
    # נתיבי קבצים
    docx_path = "../18-07-2022_4.2A.docx"  # הקובץ המקורי
    csv_path = "licensing_requirements.csv"
    
    # בדוק אם הקובץ קיים
    if not os.path.exists(docx_path):
        print(f"File not found: {docx_path}")
        print("Please ensure the Word document is in the correct location")
        return
    
    print("Starting DOCX to CSV conversion...")
    
    # חלץ דרישות
    requirements = extract_requirements_from_docx(docx_path)
    
    if not requirements:
        print("No requirements extracted. Please check the input file.")
        return
    
    # שמור ל-CSV
    if save_to_csv(requirements, csv_path):
        print("Conversion completed successfully!")
        print(f"Output file: {csv_path}")
    else:
        print("Failed to save CSV file")

if __name__ == "__main__":
    main()

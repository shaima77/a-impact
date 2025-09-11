"""
ניתוח וסיכום נתוני דרישות הרישוי
"""

import polars as pl
import json
from collections import Counter

def analyze_requirements(csv_path="licensing_requirements.csv"):
    """ניתוח נתוני הדרישות"""
    
    try:
        # קריאת הנתונים
        df = pl.read_csv(csv_path)
        print(f"Loaded {len(df)} requirements from {csv_path}")
        
        # ניתוח בסיסי
        print("\n=== בסיסי ===")
        print(f"סה\"כ דרישות: {len(df)}")
        
        # ניתוח לפי רשויות
        print("\n=== לפי רשויות ===")
        authority_counts = df['authority'].value_counts()
        for row in authority_counts.iter_rows():
            authority, count = row
            print(f"{authority}: {count}")
        
        # ניתוח לפי קטגוריות
        print("\n=== לפי קטגוריות ===")
        category_counts = df['category'].value_counts()
        for row in category_counts.iter_rows():
            category, count = row
            print(f"{category}: {count}")
        
        # ניתוח לפי עדיפות
        print("\n=== לפי עדיפות ===")
        priority_counts = df['priority'].value_counts()
        for row in priority_counts.iter_rows():
            priority, count = row
            priority_name = {
                'high': 'גבוהה',
                'medium': 'בינונית', 
                'low': 'נמוכה'
            }.get(priority, priority)
            print(f"{priority_name}: {count}")
        
        # חיפוש דרישות ספציפיות לסוגי עסקים
        print("\n=== דרישות לפי סוגי עסקים ===")
        business_keywords = {
            'מסעדה': ['מסעדה', 'מזון', 'אוכל', 'בישול'],
            'בר': ['בר', 'אלכוהול', 'משקאות חריפים', 'שתייה'],
            'בית קפה': ['קפה', 'משקאות', 'חלב', 'מאפים']
        }
        
        for business_type, keywords in business_keywords.items():
            relevant_reqs = []
            for keyword in keywords:
                # חיפוש במילות המפתח בעמודות title ו-description
                title_matches = df.filter(pl.col("title").str.contains(f"(?i){keyword}"))
                desc_matches = df.filter(pl.col("description").str.contains(f"(?i){keyword}"))
                
                # איחוד התוצאות
                matches = pl.concat([title_matches, desc_matches]).unique()
                relevant_reqs.extend(range(len(matches)))
            
            unique_reqs = list(set(relevant_reqs))
            print(f"{business_type}: {len(unique_reqs)} דרישות רלוונטיות")
        
        return df
        
    except Exception as e:
        print(f"Error analyzing data: {e}")
        return None

def create_business_type_mapping(df):
    """יצירת מיפוי דרישות לסוגי עסקים"""
    
    mapping = {
        'מסעדה': [],
        'בר': [],  
        'בית קפה': [],
        'מזון מהיר': []
    }
    
    # כללים למיפוי
    rules = {
        'מסעדה': [
            'מזון', 'אוכל', 'בישול', 'מטבח', 'בריאות', 'תברואה',
            'כיבוי אש', 'רישיון עסק', 'גז'
        ],
        'בר': [
            'אלכוהול', 'משקאות חריפים', 'בר', 'שתייה', 'לילה',
            'כיבוי אש', 'רישיון עסק', 'משטרה'
        ],
        'בית קפה': [
            'קפה', 'משקאות', 'חלב', 'מאפה', 'פשוט', 'קל',
            'כיבוי אש', 'רישיון עסק'
        ],
        'מזון מהיר': [
            'מהיר', 'טייק אווי', 'משלוח', 'פשוט', 'בסיסי',
            'מזון', 'כיבוי אש', 'רישיון עסק'
        ]
    }
    
    for business_type, keywords in rules.items():
        for i, row in enumerate(df.iter_rows(named=True)):
            title = str(row['title']).lower()
            description = str(row['description']).lower()
            
            # חיפוש מילות מפתח
            for keyword in keywords:
                if keyword in title or keyword in description:
                    if i not in mapping[business_type]:
                        mapping[business_type].append(i)
                    break
    
    # הוספת דרישות בסיסיות לכל סוג עסק
    basic_requirements = []
    for i, row in enumerate(df.iter_rows(named=True)):
        title = str(row['title']).lower()
        if any(word in title for word in ['רישיון עסק', 'כיבוי אש', 'בטיחות']):
            basic_requirements.append(i)
    
    # הוסף דרישות בסיסיות לכל סוג עסק
    for business_type in mapping:
        for req_id in basic_requirements:
            if req_id not in mapping[business_type]:
                mapping[business_type].append(req_id)
    
    return mapping

def save_analysis_results(df, mapping, output_file="analysis_results.json"):
    """שמירת תוצאות הניתוח"""
    
    results = {
        'total_requirements': len(df),
        'business_type_mapping': mapping,
        'statistics': {
            'by_authority': dict(df['authority'].value_counts().iter_rows()),
            'by_category': dict(df['category'].value_counts().iter_rows()),
            'by_priority': dict(df['priority'].value_counts().iter_rows())
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Analysis results saved to {output_file}")

def main():
    """פונקציה ראשית"""
    
    print("Starting requirements analysis...")
    
    # ניתוח הנתונים
    df = analyze_requirements()
    
    if df is not None:
        # יצירת מיפוי
        mapping = create_business_type_mapping(df)
        
        print(f"\n=== מיפוי לסוגי עסקים ===")
        for business_type, req_ids in mapping.items():
            print(f"{business_type}: {len(req_ids)} דרישות")
        
        # שמירת תוצאות
        save_analysis_results(df, mapping)
        
        print("\nAnalysis completed successfully!")
    else:
        print("Analysis failed!")

if __name__ == "__main__":
    main()

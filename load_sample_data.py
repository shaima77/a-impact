#!/usr/bin/env python
"""
סקריפט לטעינת נתוני מדגם למסד הנתונים
"""
import os
import sys
import csv
import django
from pathlib import Path

# הגדרת path למודולי Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'business_licensing.settings')
django.setup()

from questionnaire.models import BusinessType, LicensingRequirement


def load_business_types():
    """יצירת סוגי עסקים בסיסיים"""
    business_types = [
        {
            'name': 'מסעדה',
            'description': 'מסעדה או בית קפה עם הגשת אוכל מלא'
        },
        {
            'name': 'בר',
            'description': 'בר או פאב עם הגשת משקאות אלכוהוליים'
        },
        {
            'name': 'בית קפה',
            'description': 'בית קפה עם חטיפים קלים ומשקאות'
        },
        {
            'name': 'מזון מהיר',
            'description': 'מקום מזון מהיר או טייק אווי'
        },
        {
            'name': 'קייטרינג',
            'description': 'שירותי קייטרינג ואירועים'
        }
    ]
    
    print("יוצר סוגי עסקים...")
    created_types = {}
    
    for bt_data in business_types:
        business_type, created = BusinessType.objects.get_or_create(
            name=bt_data['name'],
            defaults={'description': bt_data['description']}
        )
        created_types[bt_data['name']] = business_type
        if created:
            print(f"✓ נוצר סוג עסק: {bt_data['name']}")
        else:
            print(f"○ קיים כבר: {bt_data['name']}")
    
    return created_types


def load_requirements_from_csv():
    """טעינת דרישות מקובץ CSV"""
    csv_file = Path(__file__).parent / 'data_processing' / 'restaurant_requirements_clean.csv'
    
    if not csv_file.exists():
        print(f"קובץ CSV לא נמצא: {csv_file}")
        return
    
    business_types = load_business_types()
    
    print(f"\nטוען דרישות מקובץ: {csv_file}")
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        requirements_created = 0
        requirements_skipped = 0
        
        for row in reader:
            # עיבוד הנתונים מה-CSV
            title = row.get('title', '').strip()
            description = row.get('description', '').strip()
            authority = row.get('authority', '').strip()
            
            if not title or len(title) < 10:
                requirements_skipped += 1
                continue
            
            # מיפוי קטגוריות
            category = row.get('category', 'general')
            if category not in ['restaurant', 'bar', 'health', 'safety', 'municipal', 'general']:
                category = 'general'
            
            # מיפוי עדיפות
            importance = row.get('importance', 'medium')
            priority_mapping = {'high': 'high', 'medium': 'medium', 'low': 'low'}
            priority = priority_mapping.get(importance, 'medium')
            
            # מאפיינים מיוחדים
            requires_gas = str(row.get('requires_gas', 'false')).lower() == 'true'
            meat_related = str(row.get('meat_related', 'false')).lower() == 'true'
            delivery_related = str(row.get('delivery_related', 'false')).lower() == 'true'
            outdoor_related = str(row.get('outdoor_related', 'false')).lower() == 'true'
            alcohol_related = str(row.get('alcohol_related', 'false')).lower() == 'true'
            
            # עיבוד שטח ותפוסה
            min_area = None
            max_area = None
            min_capacity = None
            max_capacity = None
            
            try:
                area_text = row.get('area_extracted', '').strip()
                if area_text and any(char.isdigit() for char in area_text):
                    # ניסיון לחלץ מספרים מהטקסט
                    import re
                    numbers = re.findall(r'\d+', area_text)
                    if numbers:
                        if 'עד' in area_text or 'מקסימום' in area_text:
                            max_area = int(numbers[0])
                        elif 'מ-' in area_text or 'מינימום' in area_text:
                            min_area = int(numbers[0])
                        else:
                            min_area = int(numbers[0])
                            
                capacity_text = row.get('capacity_extracted', '').strip()
                if capacity_text and any(char.isdigit() for char in capacity_text):
                    numbers = re.findall(r'\d+', capacity_text)
                    if numbers:
                        min_capacity = int(numbers[0])
            except:
                pass
            
            # עלות וזמן
            cost_estimate = row.get('cost_estimate', '').strip()
            if not cost_estimate:
                if priority == 'high':
                    cost_estimate = '1,000-5,000 ₪'
                elif priority == 'medium':
                    cost_estimate = '500-2,000 ₪'
                else:
                    cost_estimate = '100-1,000 ₪'
            
            processing_time = row.get('processing_time', '').strip()
            if not processing_time:
                if priority == 'high':
                    processing_time = '2-4 שבועות'
                elif priority == 'medium':
                    processing_time = '1-2 שבועות'
                else:
                    processing_time = 'עד שבוע'
            
            # יצירת הדרישה
            try:
                requirement, created = LicensingRequirement.objects.get_or_create(
                    title=title[:300],  # חיתוך אם הכותרת ארוכה מדי
                    defaults={
                        'description': description,
                        'authority': authority,
                        'category': category,
                        'priority': priority,
                        'min_area': min_area,
                        'max_area': max_area,
                        'min_capacity': min_capacity,
                        'max_capacity': max_capacity,
                        'requires_gas': requires_gas,
                        'meat_related': meat_related,
                        'delivery_related': delivery_related,
                        'outdoor_related': outdoor_related,
                        'alcohol_related': alcohol_related,
                        'estimated_cost': cost_estimate,
                        'processing_time': processing_time,
                    }
                )
                
                if created:
                    requirements_created += 1
                    # קישור לסוגי עסקים רלוונטיים
                    if category == 'restaurant':
                        requirement.business_types.add(
                            business_types['מסעדה'],
                            business_types['בית קפה'],
                            business_types['מזון מהיר']
                        )
                    elif category == 'bar':
                        requirement.business_types.add(business_types['בר'])
                    else:
                        # דרישות כלליות לכל הסוגים
                        for bt in business_types.values():
                            requirement.business_types.add(bt)
                    
                    if requirements_created % 10 == 0:
                        print(f"נוצרו {requirements_created} דרישות...")
                else:
                    requirements_skipped += 1
                    
            except Exception as e:
                print(f"שגיאה ביצירת דרישה: {title[:50]}... - {e}")
                requirements_skipped += 1
    
    print(f"\n✓ הושלמה טעינת הנתונים:")
    print(f"  - {requirements_created} דרישות נוצרו")
    print(f"  - {requirements_skipped} דרישות דולגו")


def create_sample_business_types():
    """יצירת סוגי עסקים נוספים למדגם"""
    additional_types = [
        'מאפייה',
        'גלידריה', 
        'בית מרקחת',
        'חנות יין',
        'דלפק אוכל',
        'משלוחי פיצה'
    ]
    
    print("\nיוצר סוגי עסקים נוספים...")
    for type_name in additional_types:
        business_type, created = BusinessType.objects.get_or_create(
            name=type_name,
            defaults={'description': f'עסק מסוג {type_name}'}
        )
        if created:
            print(f"✓ נוצר: {type_name}")


def main():
    """פונקציה ראשית"""
    print("=== טעינת נתוני מדגם למערכת ===\n")
    
    try:
        # טעינת סוגי עסקים
        business_types = load_business_types()
        
        # טעינת דרישות מ-CSV
        load_requirements_from_csv()
        
        # יצירת סוגי עסקים נוספים
        create_sample_business_types()
        
        print(f"\n=== סיכום ===")
        print(f"סוגי עסקים במערכת: {BusinessType.objects.count()}")
        print(f"דרישות רישוי במערכת: {LicensingRequirement.objects.count()}")
        print(f"\n✅ טעינת הנתונים הושלמה בהצלחה!")
        
    except Exception as e:
        print(f"\n❌ שגיאה בטעינת הנתונים: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
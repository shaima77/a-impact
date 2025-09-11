#!/usr/bin/env python
"""
סקריפט בדיקה מהירה למערכת הערכת רישוי עסקים
"""
import os
import sys
import django
from pathlib import Path

# הגדרת path למודולי Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'business_licensing.settings')
django.setup()

def test_models():
    """בדיקת המודלים"""
    try:
        from questionnaire.models import BusinessType, LicensingRequirement, BusinessAssessment, AssessmentReport
        
        print("📊 בדיקת מודלים...")
        
        # ספירת רשומות
        business_types_count = BusinessType.objects.count()
        requirements_count = LicensingRequirement.objects.count()
        assessments_count = BusinessAssessment.objects.count()
        reports_count = AssessmentReport.objects.count()
        
        print(f"   - סוגי עסקים: {business_types_count}")
        print(f"   - דרישות רישוי: {requirements_count}")
        print(f"   - הערכות עסקים: {assessments_count}")
        print(f"   - דוחות: {reports_count}")
        
        if business_types_count == 0:
            print("   ⚠️  אין סוגי עסקים - הריצו: python load_sample_data.py")
        
        if requirements_count == 0:
            print("   ⚠️  אין דרישות רישוי - הריצו: python load_sample_data.py")
        
        print("   ✅ המודלים עובדים תקין")
        return True
        
    except Exception as e:
        print(f"   ❌ שגיאה במודלים: {e}")
        return False

def test_ai_service():
    """בדיקת שירות AI"""
    try:
        print("\n🤖 בדיקת שירות AI...")
        
        # בדיקה בסיסית של ייבוא
        from services.ai_service import FlanT5ReportGenerator, get_ai_generator
        print("   ✅ הייבוא של שירות AI עובד")
        
        # ניסיון יצירת מופע (ללא טעינת המודל)
        print("   🔄 בודק יצירת מופע AI...")
        
        # זה יכול לקחת זמן רב בפעם הראשונה
        print("   ⚠️  שימו לב: טעינת המודל לראשונה יכולה לקחת מספר דקות")
        
        try:
            generator = get_ai_generator()
            print("   ✅ שירות AI נטען בהצלחה")
            
            # בדיקה קלה של הפונקציונליות
            test_business_data = {
                'business_name': 'מסעדת בדיקה',
                'business_type': 'מסעדה',
                'area_sqm': 100,
                'seating_capacity': 50,
                'uses_gas': True,
                'serves_meat': True,
                'offers_delivery': False,
                'has_outdoor_seating': False,
                'serves_alcohol': False,
            }
            
            test_requirements = [{
                'title': 'רישיון עסק בסיסי',
                'description': 'רישיון עסק מקומי',
                'authority': 'העירייה',
                'priority': 'high',
                'category': 'general',
                'estimated_cost': '500 ₪',
                'processing_time': '2 שבועות',
            }]
            
            print("   🔄 בודק יצירת דוח AI...")
            report = generator.generate_report(test_business_data, test_requirements)
            
            if report and len(report) > 100:
                print("   ✅ יצירת דוח AI עובדת תקין")
                print(f"   📝 אורך הדוח: {len(report)} תווים")
                return True
            else:
                print("   ⚠️  הדוח שנוצר קצר מהצפוי")
                return False
                
        except Exception as ai_error:
            print(f"   ⚠️  שגיאה ביצירת AI: {ai_error}")
            print("   💡 זה יכול לקרות אם אין מספיק זיכרון או חיבור אינטרנט")
            return False
        
    except ImportError as e:
        print(f"   ❌ שגיאה בייבוא שירות AI: {e}")
        print("   💡 נסו להתקין: pip install transformers torch")
        return False
    except Exception as e:
        print(f"   ❌ שגיאה כללית בשירות AI: {e}")
        return False

def test_views():
    """בדיקת Views"""
    try:
        print("\n🌐 בדיקת Views...")
        
        from questionnaire import views
        print("   ✅ ייבוא views עובד")
        
        # בדיקה שהפונקציות קיימות
        required_views = ['home', 'questionnaire', 'submit_assessment', 'view_report']
        for view_name in required_views:
            if hasattr(views, view_name):
                print(f"   ✅ {view_name} קיים")
            else:
                print(f"   ❌ {view_name} חסר")
                return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ שגיאה ב-views: {e}")
        return False

def test_templates():
    """בדיקת Templates"""
    try:
        print("\n📄 בדיקת Templates...")
        
        templates_dir = Path(__file__).parent / 'templates'
        required_templates = ['base.html', 'home.html', 'questionnaire.html', 'report.html']
        
        for template in required_templates:
            template_path = templates_dir / template
            if template_path.exists():
                print(f"   ✅ {template}")
            else:
                print(f"   ❌ {template} חסר")
                return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ שגיאה בבדיקת templates: {e}")
        return False

def test_static_files():
    """בדיקת קבצים סטטיים"""
    try:
        print("\n🎨 בדיקת קבצים סטטיים...")
        
        static_dir = Path(__file__).parent / 'static'
        if static_dir.exists():
            css_dir = static_dir / 'css'
            js_dir = static_dir / 'js'
            
            if css_dir.exists():
                print("   ✅ תיקיית CSS קיימת")
            else:
                print("   ⚠️  תיקיית CSS חסרה")
            
            if js_dir.exists():
                print("   ✅ תיקיית JS קיימת")
            else:
                print("   ⚠️  תיקיית JS חסרה")
        else:
            print("   ⚠️  תיקיית static חסרה")
        
        return True
        
    except Exception as e:
        print(f"   ❌ שגיאה בבדיקת קבצים סטטיים: {e}")
        return False

def main():
    """פונקציה ראשית"""
    print("🔍 בדיקת מערכת הערכת רישוי עסקים")
    print("=" * 50)
    
    tests = [
        test_models,
        test_views,
        test_templates,
        test_static_files,
        test_ai_service,  # בסוף כי זה לוקח הכי הרבה זמן
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"   ❌ שגיאה לא צפויה בבדיקה: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 תוצאות: {passed}/{total} בדיקות עברו בהצלחה")
    
    if passed == total:
        print("🎉 המערכת מוכנה לשימוש!")
        print("\n🚀 להפעלת השרת:")
        print("   python manage.py runserver")
        print("   ואז גלשו ל: http://127.0.0.1:8000")
    else:
        print("⚠️  יש בעיות שצריך לפתור")
        
        if passed >= total - 1:  # אם רק AI נכשל
            print("\n💡 טיפ: אם רק שירות ה-AI נכשל, המערכת עדיין יכולה לעבוד")
            print("   הדוחות יהיו בסיסיים יותר אבל המערכת תפעל")

if __name__ == '__main__':
    main()

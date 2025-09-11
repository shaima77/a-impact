#!/usr/bin/env python
"""
בדיקה פשוטה של החיבור ל-AI
"""
import os
import sys

# הוספת התיקייה הנוכחית לסיספתה
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ai_import():
    """בדיקת ייבוא שירות AI"""
    try:
        print("🔄 בודק ייבוא שירות AI...")
        from services.ai_service import FlanT5ReportGenerator
        print("✅ ייבוא שירות AI הצליח!")
        return True
    except ImportError as e:
        print(f"❌ שגיאה בייבוא: {e}")
        return False
    except Exception as e:
        print(f"❌ שגיאה כללית: {e}")
        return False

def test_basic_functionality():
    """בדיקה בסיסית של הפונקציונליות"""
    try:
        from services.ai_service import FlanT5ReportGenerator
        
        print("🔄 יוצר מופע של הגנרטור...")
        
        # נתונים פשוטים לבדיקה
        test_business = {
            'business_name': 'מסעדת בדיקה',
            'business_type': 'מסעדה',
            'area_sqm': 100,
            'seating_capacity': 50,
            'uses_gas': True,
            'serves_meat': False,
            'offers_delivery': False,
            'has_outdoor_seating': False,
            'serves_alcohol': False,
        }
        
        test_requirements = [{
            'title': 'רישיון עסק בסיסי',
            'description': 'רישיון עסק מהעירייה',
            'authority': 'העירייה',
            'priority': 'high',
            'category': 'general',
            'estimated_cost': '500 ₪',
            'processing_time': '2 שבועות',
        }]
        
        # ניסיון יצירת הגנרטור (ללא הרצה בפועל)
        generator = FlanT5ReportGenerator()
        print("✅ יצירת גנרטור הצליחה!")
        
        print("⚠️  הערה: טעינת המודל בפועל תקרה רק בפעם הראשונה שנריץ generate_report")
        print("   זה יכול לקחת כמה דקות ודורש חיבור אינטרנט")
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        print("\n💡 פתרונות אפשריים:")
        print("   1. וודאו שהתקנתם: pip install transformers torch")
        print("   2. וודאו שיש מספיק זיכרון פנוי (4GB+)")
        print("   3. וודאו שיש חיבור אינטרנט יציב")
        return False

def main():
    print("🧪 בדיקה פשוטה של שירות AI")
    print("=" * 40)
    
    # בדיקת ייבוא
    if not test_ai_import():
        print("\n❌ הייבוא נכשל - בדקו את התקנת התלויות")
        return
    
    # בדיקה בסיסית
    if test_basic_functionality():
        print("\n✅ שירות AI מוכן לפעולה!")
        print("\n📋 כדי לבדוק את החיבור המלא:")
        print("   1. הריצו את השרת: python manage.py runserver")
        print("   2. גלשו לשאלון: http://127.0.0.1:8000")
        print("   3. מלאו את השאלון וראו את הדוח AI")
    else:
        print("\n⚠️  יש בעיה עם שירות ה-AI")
        print("   המערכת תעבוד עם דוחות בסיסיים")

if __name__ == "__main__":
    main()

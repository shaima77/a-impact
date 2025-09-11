#!/usr/bin/env python
"""
סקריפט הגדרה מהיר למערכת הערכת רישוי עסקים
"""
import os
import sys
import subprocess
import platform

def run_command(command, description):
    """הרצת פקודה עם הודעה"""
    print(f"\n🔄 {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ {description} הושלם בהצלחה")
        return True
    else:
        print(f"❌ שגיאה ב-{description}: {result.stderr}")
        return False

def check_python_version():
    """בדיקת גרסת Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ נדרשת Python 3.8 או חדשה יותר")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} מותקנת")
    return True

def setup_virtual_environment():
    """יצירת והפעלת סביבה וירטואלית"""
    venv_path = "venv"
    
    if not os.path.exists(venv_path):
        if not run_command("python -m venv venv", "יצירת סביבה וירטואלית"):
            return False
    else:
        print("✅ סביבה וירטואלית כבר קיימת")
    
    # הוראות הפעלה
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    print(f"\n📋 להפעלת הסביבה הוירטואלית הריצו:")
    print(f"   {activate_cmd}")
    
    return True

def install_requirements():
    """התקנת תלויות"""
    if os.path.exists("requirements.txt"):
        return run_command("pip install -r requirements.txt", "התקנת תלויות Python")
    else:
        print("❌ קובץ requirements.txt לא נמצא")
        return False

def setup_database():
    """הכנת מסד הנתונים"""
    success = True
    success &= run_command("python manage.py makemigrations", "יצירת מיגרציות")
    success &= run_command("python manage.py migrate", "הרצת מיגרציות")
    return success

def load_sample_data():
    """טעינת נתוני מדגם"""
    if os.path.exists("load_sample_data.py"):
        return run_command("python load_sample_data.py", "טעינת נתוני מדגם")
    else:
        print("⚠️  קובץ load_sample_data.py לא נמצא - דולגים על טעינת נתונים")
        return True

def create_superuser():
    """יצירת משתמש מנהל"""
    print("\n🔑 יצירת משתמש מנהל למערכת...")
    print("   (אופציונלי - ניתן לדלג על ידי Ctrl+C)")
    try:
        result = subprocess.run("python manage.py createsuperuser", shell=True)
        if result.returncode == 0:
            print("✅ משתמש מנהל נוצר בהצלחה")
        return True
    except KeyboardInterrupt:
        print("\n⏭️  דולגים על יצירת משתמש מנהל")
        return True

def main():
    """פונקציה ראשית"""
    print("🚀 הגדרת מערכת הערכת רישוי עסקים עם AI")
    print("=" * 50)
    
    # בדיקות בסיס
    if not check_python_version():
        sys.exit(1)
    
    # שלבי ההגדרה
    steps = [
        (setup_virtual_environment, "הגדרת סביבה וירטואלית"),
        (install_requirements, "התקנת תלויות"),
        (setup_database, "הגדרת מסד נתונים"),
        (load_sample_data, "טעינת נתוני מדגם"),
        (create_superuser, "יצירת משתמש מנהל"),
    ]
    
    print(f"\n📋 הגדרה כוללת {len(steps)} שלבים:")
    for i, (_, description) in enumerate(steps, 1):
        print(f"   {i}. {description}")
    
    input("\n▶️  לחצו Enter להתחלה...")
    
    # הרצת השלבים
    for step_func, description in steps:
        if not step_func():
            print(f"\n❌ השלב '{description}' נכשל")
            response = input("האם להמשיך? (y/N): ")
            if response.lower() != 'y':
                print("🛑 ההגדרה הופסקה")
                sys.exit(1)
    
    # סיום מוצלח
    print("\n" + "=" * 50)
    print("🎉 ההגדרה הושלמה בהצלחה!")
    print("\n📋 שלבים נוספים:")
    print("   1. הפעילו את הסביבה הוירטואלית")
    
    if platform.system() == "Windows":
        print("      venv\\Scripts\\activate")
    else:
        print("      source venv/bin/activate")
    
    print("   2. הריצו את השרת:")
    print("      python manage.py runserver")
    print("   3. גלשו לכתובת: http://127.0.0.1:8000")
    
    print("\n🤖 מערכת ה-AI (Flan-T5) תורד ויטען בפעם הראשונה")
    print("   זה יכול לקחת מספר דקות בהתאם לחיבור האינטרנט")
    
    print("\n📚 לתיעוד מפורט ראו: README.md")
    print("🐛 לדיווח על בעיות: צרו issue ב-GitHub")

if __name__ == "__main__":
    main()

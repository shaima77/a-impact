# מערכת הערכת רישוי עסקים עם AI

## תיאור הפרויקט

מערכת חכמה לעזרה לבעלי עסקים בישראל להבין את דרישות הרישוי הרלוונטיות לעסק שלהם. 
המערכת מבוססת על Django ומשתמשת ב-Flan-T5 (מודל AI של Google) ליצירת דוחות מותאמים אישית.

## תכונות עיקריות

- ✅ **שאלון דיגיטלי אינטראקטיבי** - איסוף נתוני העסק
- ✅ **מנוע התאמה חכם** - מיפוי בין מאפייני העסק לדרישות רגולטוריות  
- ✅ **דוחות AI מותאמים אישית** - דוחות מפורטים בעברית נוצרים על ידי Flan-T5
- ✅ **עיבוד נתונים מקובץ Word** - המרה אוטומטית לפורמט מובנה
- ✅ **ממשק משתמש מודרני** - עיצוב responsive ונגיש

## דרישות מערכת

- Python 3.8+
- Django 4.2+
- PyTorch (עבור Flan-T5)
- זיכרון: לפחות 4GB RAM (8GB מומלץ)
- מקום פנוי: לפחות 2GB

## התקנה והרצה

### שלב 1: הכנת הסביבה
```bash
# שכפול המאגר
git clone <repository-url>
cd a-impact

# יצירת סביבה וירטואלית
python -m venv venv

# הפעלת הסביבה הוירטואלית
# ב-Windows:
venv\Scripts\activate
# ב-Linux/Mac:
source venv/bin/activate
```

### שלב 2: התקנת תלויות
```bash
pip install -r requirements.txt
```

**הערה**: התקנת PyTorch ו-Transformers עשויה לקחת מספר דקות בהתאם למהירות האינטרנט.

### שלב 3: הכנת מסד הנתונים
```bash
# הרצת מיגרציות
python manage.py migrate

# טעינת נתוני מדגם (אופציונלי)
python load_sample_data.py
```

### שלב 4: הרצת השרת
```bash
python manage.py runserver
```

המערכת תהיה זמינה בכתובת: http://127.0.0.1:8000/

## שימוש במערכת

1. **כניסה לשאלון**: גלשו ל-http://127.0.0.1:8000/
2. **מילוי פרטי העסק**: שם, סוג, שטח, תפוסה ומאפיינים מיוחדים
3. **קבלת דוח מותאם**: הדוח נוצר אוטומטית על ידי AI
4. **עיון בדרישות**: פירוט מלא לפי עדיפויות וקטגוריות

## ארכיטקטורת המערכת

```
a-impact/
├── manage.py                     # Django management
├── requirements.txt              # Python dependencies
├── load_sample_data.py          # Data loading script
├── business_licensing/           # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── questionnaire/               # Main Django app
│   ├── models.py               # Data models
│   ├── views.py                # Business logic
│   ├── urls.py                 # URL routing
│   └── migrations/
├── services/                   # AI services
│   ├── __init__.py
│   └── ai_service.py          # Flan-T5 integration
├── data_processing/           # Data processing scripts
│   ├── docx_to_csv.py        # Word to CSV converter
│   ├── analyze_data.py       # Data analysis
│   └── restaurant_requirements*.csv/json
├── templates/                # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── questionnaire.html
│   └── report.html
└── static/                  # CSS, JS, images
    ├── css/
    └── js/
```

## טכנולוגיות שבשימוש

### Backend
- **Django 4.2** - Framework ראשי
- **Python 3.8+** - שפת התכנות
- **SQLite** - מסד נתונים (ניתן לשדרג ל-PostgreSQL)

### AI & ML
- **Flan-T5 (Google)** - מודל שפה ליצירת דוחות
- **Hugging Face Transformers** - ספריית ML
- **PyTorch** - Framework למודלי ML

### Frontend
- **Bootstrap 5** - עיצוב responsive
- **JavaScript** - אינטראקטיביות
- **Font Awesome** - אייקונים

### עיבוד נתונים
- **python-docx** - קריאת קבצי Word
- **Polars** - עיבוד נתונים מהיר
- **CSV/JSON** - פורמטי נתונים

## אינטגרציה עם AI

### מודל Flan-T5
המערכת משתמשת ב-Flan-T5-base מ-Google, מודל שפה מתקדם שמתמחה במשימות הבנת טקסט ויצירה.

### יצירת דוחות חכמים
1. **ניתוח נתוני עסק** - המערכת מעבדת את נתוני השאלון
2. **בחירת דרישות רלוונטיות** - אלגוריתם סינון מתקדם
3. **יצירת prompt מובנה** - בניית בקשה למודל AI
4. **יצירת דוח** - המודל מייצר דוח מפורט בעברית
5. **עיצוב סופי** - הדוח מעוצב ומוצג למשתמש

### דוגמת Prompt
```
Create a comprehensive business licensing report in Hebrew for:
- Business: "מסעדת השוק"
- Type: מסעדה
- Area: 120 sqm
- Capacity: 80 seats
- Features: שימוש בגז, הגשת בשר

Write professional report including analysis, priorities, costs...
```

## פתרון בעיות נפוצות

### שגיאות התקנה
```bash
# אם יש בעיה עם PyTorch:
pip install torch --index-url https://download.pytorch.org/whl/cpu

# אם יש בעיה עם Transformers:
pip install transformers --no-deps
pip install tokenizers
```

### בעיות זיכרון
- **הפתרון**: השתמשו ב-flan-t5-small במקום flan-t5-base
- **עדכון**: בקובץ `services/ai_service.py` שנו את model_name ל-"google/flan-t5-small"

### המודל לא נטען
- **סיבה**: חיבור אינטרנט איטי
- **פתרון**: המתינו למידה מלאה של המודל (עד 10 דקות בפעם הראשונה)

## פיתוח ותרומה

### הוספת דרישות חדשות
1. ערכו את קובץ ה-CSV: `data_processing/restaurant_requirements_clean.csv`
2. הריצו: `python load_sample_data.py`

### שינוי מודל AI
```python
# בקובץ services/ai_service.py
generator = FlanT5ReportGenerator(model_name="google/flan-t5-large")
```

### הוספת שפות נוספות
- ערכו את ה-prompts בקובץ `ai_service.py`
- הוסיפו תמיכה ב-RTL ב-CSS

## בדיקות ואיכות

### הרצת בדיקות
```bash
python manage.py test
```

### בדיקת AI
```bash
python manage.py shell
>>> from services.ai_service import get_ai_generator
>>> generator = get_ai_generator()
>>> # בדיקות ידניות...
```

## תיעוד נוסף

- **API Documentation**: `/api/docs/` (אם מותקן)
- **Admin Panel**: `/admin/` (ליצירת superuser: `python manage.py createsuperuser`)
- **Logs**: בקובץ `django.log`

## רישיון וזכויות יוצרים

פרויקט זה נוצר למטרות לימוד ופיתוח. 
השימוש במודל Flan-T5 כפוף לתנאי Apache 2.0 License.

---

**פותח עם ❤️ באמצעות Cursor AI ו-Claude**

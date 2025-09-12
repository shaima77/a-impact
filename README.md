# מערכת הערכת רישוי עסקים עם AI

## תיאור הפרויקט

מערכת חכמה לעזרה לבעלי עסקים בישראל להבין את דרישות הרישוי הרלוונטיות לעסק שלהם. 
המערכת מבוססת על Django ומשתמשת ב-Perplexity API עם מודל Llama 3.1 Sonar ליצירת דוחות מדויקים ומותאמים אישית.

## תכונות עיקריות

- ✅ **שאלון דיגיטלי אינטראקטיבי** - איסוף נתוני העסק
- ✅ **מנוע התאמה חכם** - מיפוי בין מאפייני העסק לדרישות רגולטוריות  
- ✅ **דוחות AI מותאמים אישית** - דוחות מדויקים בעברית מבוססי הנתונים הספציפיים
- ✅ **בדיקת התאמה חכמה** - זיהוי סתירות בין גודל העסק לדרישות הרגולטוריות
- ✅ **עיבוד נתונים מקובץ Word** - המרה אוטומטית לפורמט מובנה
- ✅ **ממשק משתמש מודרני** - עיצוב responsive ונגיש
- ✅ **אמינות גבוהה** - המערכת מתבססת רק על הנתונים המקוריים ולא על ידע כללי

## דרישות מערכת

- Python 3.8+
- Django 4.2+
- חיבור אינטרנט (עבור Perplexity API)
- API Key של Perplexity
- זיכרון: לפחות 2GB RAM
- מקום פנוי: לפחות 500MB

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

### שלב 2.5: הגדרת Perplexity API
1. **השג API Key**:
   - גש ל-https://www.perplexity.ai/
   - צור חשבון ואמת את כתובת האימייל
   - עבור לתפריט API ויצור API key חדש
   - המודל בשימוש: `sonar` (Llama 3.1 Sonar)

2. **צור קובץ .env**:
```bash
# ביצירת קובץ .env בתיקיית הפרויקט
echo "PERPLEXITY_API_KEY=your-api-key-here" > .env
echo "PERPLEXITY_MODEL=sonar" >> .env
echo "DEBUG=True" >> .env
```

**חשוב**: החלף את `your-api-key-here` ב-API key האמיתי שלך!

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

## 🎯 היתרונות החדשים של המערכת

### דיוק מושלם
- **מבוסס על נתונים אמיתיים**: הדוחות נוצרים רק מהדרישות שבקובץ המקורי
- **זיהוי סתירות**: המערכת מזהה אם העסק לא עונה על דרישות שטח או תפוסה
- **פרטים מלאים**: כל דרישה כוללת רשות, עלות, זמן וכל הפרטים הרלוונטיים

### שקיפות מלאה
- **מקורות ברורים**: כל מידע בדוח מצוין עם המקור הספציפי
- **הסברים מפורטים**: למה דרישה רלוונטית או לא רלוונטית לעסק
- **ללא ידע כללי**: המערכת לא מוסיפה מידע שאינו מופיע בקובץ המקורי

### דוחות מקצועיים
- **מבנה עקבי**: תמצית מנהלים, דרישות, עלויות, תוכנית פעולה והמלצות
- **עלויות וזמנים מדויקים**: בהתבסס על הנתונים הרשמיים בלבד
- **המלצות מעשיות**: צעדים קונקרטיים לביצוע

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
│   └── ai_service.py          # Perplexity API integration
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
- **Perplexity API** - מודל שפה מתקדם ליצירת דוחות
- **Llama 3.1 Sonar** - מודל מתקדם עם גישה לאינטרנט בזמן אמת

### Frontend
- **Bootstrap 5** - עיצוב responsive
- **JavaScript** - אינטראקטיביות
- **Font Awesome** - אייקונים

### עיבוד נתונים
- **python-docx** - קריאת קבצי Word
- **Polars** - עיבוד נתונים מהיר
- **CSV/JSON** - פורמטי נתונים

## אינטגרציה עם AI

### Perplexity API + Llama 3.1 Sonar
המערכת משתמשת ב-Perplexity API עם מודל Llama 3.1 Sonar - מודל שפה מתקדם עם יכולת גישה לאינטרנט בזמן אמת.

### יצירת דוחות מדויקים
1. **ניתוח נתוני עסק** - המערכת מעבדת את נתוני השאלון
2. **בחירת דרישות רלוונטיות** - אלגוריתם סינון מתקדם מהקובץ המקורי
3. **העברת נתונים מפורטים** - כל פרט רלוונטי מהדרישות מועבר למודל
4. **יצירת דוח מבוסס נתונים** - המודל מייצר דוח מבוסס רק על הנתונים שסופקו
5. **עיצוב וזיהוי סתירות** - הדוח כולל זיהוי התאמות ואי-התאמות

### תהליך מתקדם לדיוק
- **העברת פרטי דרישות מלאים**: כותרת, תיאור, רשות, דרישות שטח/תפוסה, עדיפות, עלות וזמן
- **בדיקת התאמה לגודל עסק**: המודל בודק אם העסק עונה על הגבלות שטח ותפוסה
- **הוראות מפורשות**: המודל מקבל הוראה להתבסס רק על הנתונים שסופקו ולא על ידע כללי
- **זיהוי סתירות**: המודל מציין אם יש סתירה בין מאפייני העסק לדרישות

### דוגמת מבנה הנתונים שמועברים למודל
```
דרישות שנמצאו (6 סה"כ):
1. חוק רישוי עסקים – תנאי תברואה לבתי אוכל התשמ"ג 1983
   תיאור: עמידה בתקנות תברואה לבתי אוכל
   רשות: משרד הבריאות
   עדיפות: גבוהה
   עלות: לפי תעריף
   זמן: 2-4 שבועות

2. אישור משרד הבריאות למטבח
   תיאור: בדיקת תנאי היגיינה במטבח
   רשות: משרד הבריאות
   ...
```

## פתרון בעיות נפוצות

### שגיאות Perplexity API
```bash
# בדיקת חיבור API:
curl -X POST "https://api.perplexity.ai/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "sonar", "messages": [{"role": "user", "content": "test"}]}'
```

### בעיות API Key
- **שגיאה 401**: בדקו שה-API key נכון בקובץ `.env`
- **שגיאה 400**: בדקו את פורמט הבקשה וש `PERPLEXITY_MODEL=sonar`
- **שגיאה 429**: חרגתם ממכסת ה-API - המתינו או שדרגו את התוכנית

### בעיות חיבור
- **שגיאת חיבור**: בדקו חיבור אינטרנט
- **Timeout**: הגדילו את timeout בקובץ `ai_service.py`
- **SSL errors**: ייתכן ובעיה ברשת המקומית

## פיתוח ותרומה

### הוספת דרישות חדשות
1. ערכו את קובץ ה-CSV: `data_processing/restaurant_requirements_clean.csv`
2. הריצו: `python load_sample_data.py`

### שינוי מודל Perplexity
```python
# בקובץ services/ai_service.py - שנו את המודל
self.model = config('PERPLEXITY_MODEL', default='sonar')
# אפשרויות: 'sonar', 'llama-3.1-sonar-small-128k-online', וכו'
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
>>> from services.ai_service import generate_ai_report
>>> # בדיקת יצירת דוח עם נתונים מדגם
>>> report = generate_ai_report("מסעדת בדיקה", "מסעדה", 100, 50, [], [])
>>> print(report[:200])  # בדיקת תחילת הדוח
```

## תיעוד נוסף

- **API Documentation**: `/api/docs/` (אם מותקן)
- **Admin Panel**: `/admin/` (ליצירת superuser: `python manage.py createsuperuser`)
- **Logs**: בקובץ `django.log`

## רישיון וזכויות יוצרים

פרויקט זה נוצר למטרות לימוד ופיתוח. 
השימוש ב-Perplexity API כפוף לתנאי השימוש של Perplexity.

---

**פותח עם ❤️ באמצעות Cursor AI ו-Claude**

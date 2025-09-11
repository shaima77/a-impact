# מערכת הערכת רישוי עסקים

## התקנה והרצה

### שלב 1: יצירת סביבת עבודה וירטואלית
```bash
python -m venv venv
venv\Scripts\activate  # ב-Windows
```

### שלב 2: התקנת תלויות
```bash
pip install -r requirements.txt
```

### שלב 3: הרצת מיגרציות
```bash
python manage.py migrate
```

### שלב 4: הרצת השרת
```bash
python manage.py runserver
```

המערכת תהיה זמינה בכתובת: http://127.0.0.1:8000/

## מבנה הפרויקט

```
a-impact/
├── manage.py
├── requirements.txt
├── business_licensing/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── README.md
```

"""
ניתוח ועיבוד מתקדם של נתוני הרישוי עם Polars
הכנת הנתונים למערכת Django
"""

import polars as pl
import re
from typing import List, Dict, Any


def load_and_analyze_csv() -> pl.DataFrame:
    """
    טעינת וניתוח הנתונים מה-CSV
    """
    csv_path = "data_processing/licensing_requirements.csv"
    
    try:
        df = pl.read_csv(csv_path)
        print(f"נטענו {len(df)} רשומות מהקובץ")
        return df
    except Exception as e:
        print(f"שגיאה בטעינת הקובץ: {e}")
        return pl.DataFrame()


def clean_and_categorize_data(df: pl.DataFrame) -> pl.DataFrame:
    """
    ניקוי וקטלוג הנתונים
    """
    # ניקוי בסיסי
    df = df.with_columns([
        # הסרת מרכאות מיותרות וניקוי רווחים
        pl.col("title").str.replace_all(r'^"|"$', '').str.strip_chars(),
        pl.col("description").str.replace_all(r'^"|"$', '').str.strip_chars(),
        pl.col("authority").str.strip_chars(),
        
        # זיהוי קטגוריות
        pl.when(
            pl.col("title").str.to_lowercase().str.contains("מסעד|אוכל|מטבח|הגש")
        ).then(pl.lit("restaurant"))
        .when(
            pl.col("title").str.to_lowercase().str.contains("בר|משקאות|אלכוהול")
        ).then(pl.lit("bar"))
        .when(
            pl.col("title").str.to_lowercase().str.contains("בריאות|סניטרי|רפוא")
        ).then(pl.lit("health"))
        .when(
            pl.col("title").str.to_lowercase().str.contains("כבאות|בטיחות|אש")
        ).then(pl.lit("safety"))
        .when(
            pl.col("title").str.to_lowercase().str.contains("עירייה|רשות|עיר")
        ).then(pl.lit("municipal"))
        .otherwise(pl.lit("general"))
        .alias("category"),
        
        # זיהוי דרגת חשיבות
        pl.when(
            pl.col("title").str.to_lowercase().str.contains("חובה|חוק|נדרש|בטיחות")
        ).then(pl.lit("high"))
        .when(
            pl.col("title").str.to_lowercase().str.contains("מומלץ|עדיף|רצוי")
        ).then(pl.lit("medium"))
        .otherwise(pl.lit("low"))
        .alias("importance"),
        
        # חילוץ מספרי שטח וקיבולת באופן מתקדם יותר
        pl.col("title").str.extract_all(r"(\d+)\s*מ\"ר").list.join(",").alias("area_extracted"),
        pl.col("title").str.extract_all(r"(\d+)\s*(?:מקומות|אנשים|לקוחות)").list.join(",").alias("capacity_extracted"),
    ])
    
    return df


def create_restaurant_specific_data(df: pl.DataFrame) -> pl.DataFrame:
    """
    יצירת נתונים ספציפיים למסעדות
    """
    # סינון רק פריטים רלוונטיים למסעדות
    restaurant_df = df.filter(
        (pl.col("category") == "restaurant") |
        (pl.col("category") == "health") |
        (pl.col("category") == "safety") |
        (pl.col("title").str.to_lowercase().str.contains("מסעד|אוכל|מטבח|הגש|בר|משקאות"))
    )
    
    # הוספת מאפיינים ספציפיים למסעדות
    restaurant_df = restaurant_df.with_columns([
        # זיהוי אם נדרש גז
        pl.col("description").str.to_lowercase().str.contains("גז").alias("requires_gas"),
        
        # זיהוי אם מתייחס להגשת בשר
        pl.col("description").str.to_lowercase().str.contains("בשר|כשר|טרף").alias("meat_related"),
        
        # זיהוי אם מתייחס למשלוחים
        pl.col("description").str.to_lowercase().str.contains("משלוח|הבא|חלוק").alias("delivery_related"),
        
        # זיהוי אם מתייחס לישיבה בחוץ
        pl.col("description").str.to_lowercase().str.contains("חוץ|מרפסת|גן|רחוב").alias("outdoor_related"),
        
        # זיהוי אם מתייחס לאלכוהול
        pl.col("description").str.to_lowercase().str.contains("אלכוהול|משקאות|יין|בירה").alias("alcohol_related"),
    ])
    
    return restaurant_df


def export_for_django(df: pl.DataFrame):
    """
    יצוא הנתונים בפורמט המתאים ל-Django
    """
    # יצירת קובץ JSON למסעדות
    restaurant_data = df.select([
        "requirement_id",
        "title", 
        "description",
        "authority",
        "category",
        "importance",
        "requires_gas",
        "meat_related", 
        "delivery_related",
        "outdoor_related",
        "alcohol_related",
        "area_extracted",
        "capacity_extracted"
    ]).to_dicts()
    
    # שמירה בפורמט JSON
    import json
    with open("data_processing/restaurant_requirements.json", "w", encoding="utf-8") as f:
        json.dump(restaurant_data, f, ensure_ascii=False, indent=2)
    
    print(f"נשמרו {len(restaurant_data)} דרישות למסעדות ב-JSON")
    
    # יצירת CSV נקי למסעדות
    df.write_csv("data_processing/restaurant_requirements_clean.csv")
    print("נשמר גם CSV נקי")


def analyze_statistics(df: pl.DataFrame):
    """
    ניתוח סטטיסטיקות של הנתונים
    """
    print("\n=== ניתוח הנתונים ===")
    
    # סטטיסטיקות כלליות
    print(f"סך הכל דרישות: {len(df)}")
    
    # חלוקה לפי קטגוריות
    category_stats = df.group_by("category").agg(pl.len().alias("count")).sort("count", descending=True)
    print("\nחלוקה לפי קטגוריות:")
    print(category_stats)
    
    # חלוקה לפי חשיבות
    importance_stats = df.group_by("importance").agg(pl.len().alias("count")).sort("count", descending=True)
    print("\nחלוקה לפי חשיבות:")
    print(importance_stats)
    
    # מאפיינים מיוחדים
    special_features = df.select([
        pl.col("requires_gas").sum().alias("requires_gas"),
        pl.col("meat_related").sum().alias("meat_related"),
        pl.col("delivery_related").sum().alias("delivery_related"),
        pl.col("outdoor_related").sum().alias("outdoor_related"),
        pl.col("alcohol_related").sum().alias("alcohol_related"),
    ])
    print("\nמאפיינים מיוחדים:")
    print(special_features)


def main():
    """
    הפונקציה הראשית
    """
    print("מתחיל ניתוח נתוני הרישוי עם Polars...")
    
    # טעינת הנתונים
    df = load_and_analyze_csv()
    if df.is_empty():
        return
    
    # ניקוי והכנת הנתונים
    print("מנקה ומקטלג את הנתונים...")
    df_clean = clean_and_categorize_data(df)
    
    # יצירת נתונים ספציפיים למסעדות
    print("יוצר נתונים ספציפיים למסעדות...")
    restaurant_df = create_restaurant_specific_data(df_clean)
    
    # ניתוח סטטיסטיקות
    analyze_statistics(restaurant_df)
    
    # יצוא למערכת Django
    print("\nמייצא נתונים למערכת Django...")
    export_for_django(restaurant_df)
    
    print("\nהניתוח הושלם בהצלחה! ✅")


if __name__ == "__main__":
    main()

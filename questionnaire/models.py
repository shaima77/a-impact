from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class BusinessType(models.Model):
    """סוגי עסקים"""
    name = models.CharField(max_length=100, verbose_name="שם סוג העסק")
    description = models.TextField(blank=True, verbose_name="תיאור")
    
    class Meta:
        verbose_name = "סוג עסק"
        verbose_name_plural = "סוגי עסקים"
    
    def __str__(self):
        return self.name


class BusinessAssessment(models.Model):
    """הערכת עסק - תוצאות השאלון"""
    
    # פרטי העסק הבסיסיים
    business_name = models.CharField(max_length=200, verbose_name="שם העסק")
    business_type = models.ForeignKey(
        BusinessType, 
        on_delete=models.CASCADE, 
        verbose_name="סוג העסק"
    )
    
    # נתוני שטח ותפוסה
    area_sqm = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10000)],
        verbose_name="שטח במ״ר"
    )
    seating_capacity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        verbose_name="מספר מקומות ישיבה"
    )
    
    # מאפיינים מיוחדים
    uses_gas = models.BooleanField(default=False, verbose_name="משתמש בגז")
    serves_meat = models.BooleanField(default=False, verbose_name="מגיש בשר")
    offers_delivery = models.BooleanField(default=False, verbose_name="מציע משלוחים")
    has_outdoor_seating = models.BooleanField(default=False, verbose_name="יש ישיבה בחוץ")
    serves_alcohol = models.BooleanField(default=False, verbose_name="מגיש אלכוהול")
    
    # פרטי יצירה
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="נוצר בתאריך")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="עודכן בתאריך")
    
    class Meta:
        verbose_name = "הערכת עסק"
        verbose_name_plural = "הערכות עסקים"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.business_name} - {self.business_type}"


class LicensingRequirement(models.Model):
    """דרישות רישוי"""
    
    PRIORITY_CHOICES = [
        ('high', 'גבוהה'),
        ('medium', 'בינונית'), 
        ('low', 'נמוכה'),
    ]
    
    CATEGORY_CHOICES = [
        ('restaurant', 'מסעדה'),
        ('bar', 'בר'),
        ('health', 'בריאות'),
        ('safety', 'בטיחות'),
        ('municipal', 'עירונית'),
        ('general', 'כללי'),
    ]
    
    title = models.CharField(max_length=300, verbose_name="כותרת")
    description = models.TextField(verbose_name="תיאור")
    authority = models.CharField(max_length=200, blank=True, verbose_name="רשות מוסמכת")
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='general',
        verbose_name="קטגוריה"
    )
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='medium',
        verbose_name="עדיפות"
    )
    
    # תנאים למתן הרישוי
    min_area = models.IntegerField(null=True, blank=True, verbose_name="שטח מינימלי")
    max_area = models.IntegerField(null=True, blank=True, verbose_name="שטח מקסימלי")
    min_capacity = models.IntegerField(null=True, blank=True, verbose_name="תפוסה מינימלית")
    max_capacity = models.IntegerField(null=True, blank=True, verbose_name="תפוסה מקסימלית")
    
    # מאפיינים מיוחדים
    requires_gas = models.BooleanField(default=False, verbose_name="דורש גז")
    meat_related = models.BooleanField(default=False, verbose_name="קשור לבשר")
    delivery_related = models.BooleanField(default=False, verbose_name="קשור למשלוחים")
    outdoor_related = models.BooleanField(default=False, verbose_name="קשור לישיבה בחוץ")
    alcohol_related = models.BooleanField(default=False, verbose_name="קשור לאלכוהול")
    
    # נתוני עלות וזמן
    estimated_cost = models.CharField(max_length=100, blank=True, verbose_name="עלות משוערת")
    processing_time = models.CharField(max_length=100, blank=True, verbose_name="זמן טיפול")
    
    business_types = models.ManyToManyField(BusinessType, verbose_name="סוגי עסקים")
    
    class Meta:
        verbose_name = "דרישת רישוי"
        verbose_name_plural = "דרישות רישוי"
        ordering = ['priority', 'category']
    
    def __str__(self):
        return f"{self.get_category_display()} - {self.title[:50]}..."


class AssessmentReport(models.Model):
    """דוח הערכה שנוצר עבור עסק"""
    
    assessment = models.OneToOneField(
        BusinessAssessment, 
        on_delete=models.CASCADE,
        verbose_name="הערכת עסק"
    )
    relevant_requirements = models.ManyToManyField(
        LicensingRequirement,
        verbose_name="דרישות רלוונטיות"
    )
    ai_generated_content = models.TextField(
        blank=True,
        verbose_name="תוכן שנוצר על ידי AI"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="נוצר בתאריך")
    
    class Meta:
        verbose_name = "דוח הערכה"
        verbose_name_plural = "דוחות הערכה"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"דוח עבור {self.assessment.business_name}"
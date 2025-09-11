from django.contrib import admin
from .models import BusinessType, BusinessAssessment, LicensingRequirement, AssessmentReport


@admin.register(BusinessType)
class BusinessTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']


@admin.register(LicensingRequirement)
class LicensingRequirementAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'priority', 'authority']
    list_filter = ['category', 'priority', 'requires_gas', 'meat_related', 'delivery_related', 'alcohol_related']
    search_fields = ['title', 'description', 'authority']
    filter_horizontal = ['business_types']
    
    fieldsets = (
        ('מידע בסיסי', {
            'fields': ('title', 'description', 'authority', 'category', 'priority')
        }),
        ('תנאי שטח ותפוסה', {
            'fields': ('min_area', 'max_area', 'min_capacity', 'max_capacity')
        }),
        ('מאפיינים מיוחדים', {
            'fields': ('requires_gas', 'meat_related', 'delivery_related', 'outdoor_related', 'alcohol_related')
        }),
        ('עלות וזמן', {
            'fields': ('estimated_cost', 'processing_time')
        }),
        ('סוגי עסקים', {
            'fields': ('business_types',)
        }),
    )


@admin.register(BusinessAssessment)
class BusinessAssessmentAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'business_type', 'area_sqm', 'seating_capacity', 'created_at']
    list_filter = ['business_type', 'uses_gas', 'serves_meat', 'offers_delivery', 'serves_alcohol', 'created_at']
    search_fields = ['business_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('פרטי העסק', {
            'fields': ('business_name', 'business_type', 'area_sqm', 'seating_capacity')
        }),
        ('מאפיינים מיוחדים', {
            'fields': ('uses_gas', 'serves_meat', 'offers_delivery', 'has_outdoor_seating', 'serves_alcohol')
        }),
        ('מטא דאטה', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(AssessmentReport)
class AssessmentReportAdmin(admin.ModelAdmin):
    list_display = ['assessment', 'created_at']
    list_filter = ['created_at']
    search_fields = ['assessment__business_name']
    readonly_fields = ['created_at']
    filter_horizontal = ['relevant_requirements']
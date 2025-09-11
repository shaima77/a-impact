from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import models
from .models import BusinessType, BusinessAssessment, LicensingRequirement, AssessmentReport
from services.ai_service import generate_ai_report
import json
import logging

logger = logging.getLogger(__name__)


def home(request):
    """דף הבית"""
    return render(request, 'home.html')


def questionnaire(request):
    """עמוד השאלון"""
    business_types = BusinessType.objects.all()
    context = {
        'business_types': business_types
    }
    return render(request, 'questionnaire.html', context)


@require_http_methods(["POST"])
def submit_assessment(request):
    """קבלת נתוני השאלון ויצירת הערכה"""
    try:
        # קבלת נתונים מהטופס
        business_name = request.POST.get('business_name', '').strip()
        business_type_id = request.POST.get('business_type', '')
        area_sqm = request.POST.get('area_sqm', '')
        seating_capacity = request.POST.get('seating_capacity', '')
        
        # Debug - הדפסת הנתונים שהתקבלו
        print(f"DEBUG: business_name={business_name}")
        print(f"DEBUG: business_type_id={business_type_id}")
        print(f"DEBUG: area_sqm={area_sqm}")
        print(f"DEBUG: seating_capacity={seating_capacity}")
        print(f"DEBUG: POST data keys: {list(request.POST.keys())}")
        
        # מאפיינים מיוחדים
        uses_gas = request.POST.get('uses_gas', 'false') == 'true'
        serves_meat = request.POST.get('serves_meat', 'false') == 'true'
        offers_delivery = request.POST.get('offers_delivery', 'false') == 'true'
        has_outdoor_seating = request.POST.get('has_outdoor_seating', 'false') == 'true'
        serves_alcohol = request.POST.get('serves_alcohol', 'false') == 'true'
        
        # בדיקת תקינות נתונים
        if not all([business_name, business_type_id, area_sqm, seating_capacity]):
            messages.error(request, 'אנא מלאו את כל השדות הנדרשים')
            return redirect('questionnaire:questionnaire')
        
        try:
            area_sqm = int(area_sqm)
            seating_capacity = int(seating_capacity)
            
            if area_sqm <= 0 or seating_capacity <= 0:
                raise ValueError("מספרים חייבים להיות חיוביים")
                
        except ValueError:
            messages.error(request, 'אנא הזינו מספרים תקינים עבור השטח ומספר המקומות')
            return redirect('questionnaire:questionnaire')
        
        # קבלת סוג העסק
        try:
            # נסה למצוא לפי ID ראשון
            try:
                business_type = BusinessType.objects.get(pk=business_type_id)
                print(f"Found business type by ID: {business_type}")
            except (BusinessType.DoesNotExist, ValueError):
                # נסה למצוא לפי שם
                business_type = BusinessType.objects.get(name=business_type_id)
                print(f"Found business type by name: {business_type}")
        except BusinessType.DoesNotExist:
            # יצירת סוג עסק בסיסי אם לא קיים
            print(f"Creating new business type: {business_type_id}")
            business_type = BusinessType.objects.create(
                name=business_type_id,
                description=f"סוג עסק: {business_type_id}"
            )
        
        # יצירת הערכת עסק
        assessment = BusinessAssessment.objects.create(
            business_name=business_name,
            business_type=business_type,
            area_sqm=area_sqm,
            seating_capacity=seating_capacity,
            uses_gas=uses_gas,
            serves_meat=serves_meat,
            offers_delivery=offers_delivery,
            has_outdoor_seating=has_outdoor_seating,
            serves_alcohol=serves_alcohol
        )
        
        # מציאת דרישות רלוונטיות
        relevant_requirements = find_relevant_requirements(assessment)
        
        # יצירת דוח עם Perplexity AI
        print(f"Creating AI report for: {assessment.business_name}")
        
        # יצירת דוח עם Perplexity AI בלבד
        from services.ai_service import generate_ai_report
        ai_content = generate_ai_report(assessment, relevant_requirements)
        print("AI report generated successfully with Perplexity!")
        
        report = AssessmentReport.objects.create(
            assessment=assessment,
            ai_generated_content=ai_content
        )
        
        # קישור דרישות רלוונטיות לדוח
        if relevant_requirements:
            report.relevant_requirements.set(relevant_requirements)
        
        print(f"Report created successfully with ID: {report.id}")
        messages.success(request, f'🎉 השאלון נשלח בהצלחה! נמצאו {len(relevant_requirements)} דרישות רלוונטיות לעסק שלכם.')
        
        return redirect('questionnaire:view_report', report_id=report.id)
        
    except Exception as e:
        print(f"CRITICAL ERROR in submit_assessment: {e}")
        import traceback
        traceback.print_exc()
        messages.error(request, f'אירעה שגיאה: {str(e)}')
        return redirect('questionnaire:questionnaire')


def find_relevant_requirements(assessment):
    """מציאת דרישות רלוונטיות לעסק"""
    
    # התחלה עם כל הדרישות
    requirements = LicensingRequirement.objects.all()
    
    # סינון לפי סוג עסק (אם מוגדר)
    business_type_requirements = requirements.filter(
        business_types=assessment.business_type
    )
    
    # אם לא נמצאו דרישות ספציפיות לסוג העסק, נשתמש בדרישות כלליות
    if not business_type_requirements.exists():
        # נחפש לפי שם סוג העסק
        business_type_name = assessment.business_type.name.lower()
        if 'מסעדה' in business_type_name or 'restaurant' in business_type_name:
            requirements = requirements.filter(category__in=['restaurant', 'health', 'safety'])
        elif 'בר' in business_type_name or 'bar' in business_type_name:
            requirements = requirements.filter(category__in=['bar', 'safety'])
        elif 'קפה' in business_type_name or 'cafe' in business_type_name:
            requirements = requirements.filter(category__in=['restaurant', 'health'])
        else:
            requirements = requirements.filter(category__in=['general', 'safety'])
    else:
        requirements = business_type_requirements
    
    # סינון לפי שטח
    if assessment.area_sqm:
        requirements = requirements.filter(
            models.Q(min_area__isnull=True) | models.Q(min_area__lte=assessment.area_sqm)
        ).filter(
            models.Q(max_area__isnull=True) | models.Q(max_area__gte=assessment.area_sqm)
        )
    
    # סינון לפי תפוסה
    if assessment.seating_capacity:
        requirements = requirements.filter(
            models.Q(min_capacity__isnull=True) | models.Q(min_capacity__lte=assessment.seating_capacity)
        ).filter(
            models.Q(max_capacity__isnull=True) | models.Q(max_capacity__gte=assessment.seating_capacity)
        )
    
    # סינון לפי מאפיינים מיוחדים
    filtered_requirements = []
    for req in requirements:
        # בדיקת התאמה למאפיינים מיוחדים
        if req.requires_gas and not assessment.uses_gas:
            continue
        if req.meat_related and not assessment.serves_meat:
            continue
        if req.delivery_related and not assessment.offers_delivery:
            continue
        if req.outdoor_related and not assessment.has_outdoor_seating:
            continue
        if req.alcohol_related and not assessment.serves_alcohol:
            continue
            
        filtered_requirements.append(req)
    
    return filtered_requirements


def view_report(request, report_id):
    """הצגת דוח הערכה"""
    try:
        report = get_object_or_404(AssessmentReport, id=report_id)
        relevant_requirements = report.relevant_requirements.all()
        
        # קיבוץ דרישות לפי קטגוריה
        requirements_by_category = {}
        for req in relevant_requirements:
            category = req.get_category_display()
            if category not in requirements_by_category:
                requirements_by_category[category] = []
            requirements_by_category[category].append(req)
        
        # קיבוץ דרישות לפי עדיפות
        requirements_by_priority = {
            'high': relevant_requirements.filter(priority='high'),
            'medium': relevant_requirements.filter(priority='medium'),
            'low': relevant_requirements.filter(priority='low'),
        }
        
        context = {
            'report': report,
            'assessment': report.assessment,
            'relevant_requirements': relevant_requirements,
            'requirements_by_category': requirements_by_category,
            'requirements_by_priority': requirements_by_priority,
            'total_requirements': len(relevant_requirements),
        }
        
        return render(request, 'report.html', context)
        
    except AssessmentReport.DoesNotExist:
        messages.error(request, 'דוח לא נמצא')
        return redirect('questionnaire:home')


@csrf_exempt
def api_get_requirements(request):
    """API endpoint לקבלת דרישות בפורמט JSON"""
    if request.method == 'GET':
        try:
            business_type = request.GET.get('business_type', '')
            area = request.GET.get('area', '')
            capacity = request.GET.get('capacity', '')
            
            # Query basic requirements
            requirements = LicensingRequirement.objects.all()
            
            if business_type:
                requirements = requirements.filter(category=business_type)
            
            if area:
                try:
                    area_int = int(area)
                    requirements = requirements.filter(
                        models.Q(min_area__isnull=True) | models.Q(min_area__lte=area_int)
                    ).filter(
                        models.Q(max_area__isnull=True) | models.Q(max_area__gte=area_int)
                    )
                except ValueError:
                    pass
            
            # Convert to JSON
            requirements_data = []
            for req in requirements:
                requirements_data.append({
                    'id': req.id,
                    'title': req.title,
                    'description': req.description,
                    'authority': req.authority,
                    'category': req.get_category_display(),
                    'priority': req.get_priority_display(),
                    'estimated_cost': req.estimated_cost,
                    'processing_time': req.processing_time,
                })
            
            return JsonResponse({
                'success': True,
                'requirements': requirements_data,
                'count': len(requirements_data)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


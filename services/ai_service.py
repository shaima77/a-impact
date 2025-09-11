"""
שירות AI לייצור דוחות חכמים עם Perplexity API
"""
import logging
import requests
import json
from typing import Dict, List, Optional
from decouple import config

logger = logging.getLogger(__name__)


class PerplexityReportGenerator:
    """
    מחלקה לייצור דוחות בעזרת Perplexity API
    """
    
    def __init__(self, api_key: str = None, model: str = "sonar"):
        """
        אתחול שירות Perplexity
        
        Args:
            api_key: API key של Perplexity (יילקח מ-.env אם לא סופק)
            model: שם המודל (ברירת מחדל: sonar)
        """
        self.api_key = api_key or config('PERPLEXITY_API_KEY', default='')
        self.model = model or config('PERPLEXITY_MODEL', default='sonar')
        self.base_url = "https://api.perplexity.ai/chat/completions"
        
        if not self.api_key:
            logger.warning("Perplexity API key not found. Please set PERPLEXITY_API_KEY in .env file")
    
    def _make_request(self, messages: List[Dict]) -> str:
        """ביצוע בקשה ל-Perplexity API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages
            }
            
            # לוג הבקשה לדיבוג
            print(f"Sending request to Perplexity:")
            print(f"Model: {self.model}")
            print(f"Messages count: {len(messages)}")
            print(f"API Key configured: {'Yes' if self.api_key else 'No'}")
            print(f"First message preview: {str(messages[0])[:200]}...")
            
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Perplexity API request failed: {e}")
            # הדפס תגובה מפורטת לדיבוג
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_details = e.response.json()
                    logger.error(f"API Error Details: {error_details}")
                    print(f"API Error Details: {error_details}")
                except:
                    logger.error(f"API Response Text: {e.response.text}")
                    print(f"API Response Text: {e.response.text}")
            raise Exception(f"Perplexity API error: {e}")
        except KeyError as e:
            logger.error(f"Unexpected response format: {e}")
            raise Exception("Invalid response from Perplexity API")
    
    def generate_report(self, business_data: Dict, requirements: List[Dict]) -> str:
        """
        יצירת דוח מותאם אישית על בסיס נתוני העסק והדרישות
        
        Args:
            business_data: נתוני העסק מהשאלון
            requirements: רשימת דרישות רלוונטיות
            
        Returns:
            דוח טקסט מפורט ומותאם
        """
        try:
            if not self.api_key:
                raise Exception("API key not configured")
            
            # הכנת הודעות לAPI
            messages = self._create_messages(business_data, requirements)
            
            # יצירת הדוח עם Perplexity
            ai_content = self._make_request(messages)
            
            # החזרת התוכן הגולמי מ-Perplexity ללא עיצוב נוסף
            return ai_content
            
        except Exception as e:
            logger.error(f"Error generating report with Perplexity: {e}")
            raise Exception(f"Failed to generate AI report: {e}")
    
    def _create_messages(self, business_data: Dict, requirements: List[Dict]) -> List[Dict]:
        """
        יצירת הודעות לPerplexity API
        """
        business_name = business_data.get('business_name', 'העסק')
        business_type = business_data.get('business_type', 'עסק')
        area = business_data.get('area_sqm', 0)
        capacity = business_data.get('seating_capacity', 0)
        
        # מאפיינים מיוחדים
        features = []
        if business_data.get('uses_gas', False):
            features.append('שימוש בגז')
        if business_data.get('serves_meat', False):
            features.append('הגשת בשר')
        if business_data.get('offers_delivery', False):
            features.append('שירות משלוחים')
        if business_data.get('has_outdoor_seating', False):
            features.append('ישיבה בחוץ')
        if business_data.get('serves_alcohol', False):
            features.append('הגשת אלכוהול')
        
        features_text = ', '.join(features) if features else 'אין מאפיינים מיוחדים'
        
        # סיווג דרישות
        high_priority_reqs = [req for req in requirements if req.get('priority') == 'high']
        medium_priority_reqs = [req for req in requirements if req.get('priority') == 'medium']
        
        # יצירת רשימת דרישות מפורטת
        requirements_summary = []
        for i, req in enumerate(requirements[:15], 1):  # 15 הראשונות עם מספור
            title = req.get('title', '')[:200]  # כותרת מורחבת
            description = req.get('description', '')[:300]  # תיאור
            authority = req.get('authority', '')
            area_req = req.get('area_requirements', '')
            capacity_req = req.get('capacity_requirements', '')
            special_req = req.get('special_requirements', '')
            priority = req.get('priority', '')
            cost = req.get('cost_estimate', '')
            time = req.get('processing_time', '')
            
            if title:
                req_text = f"{i}. {title}"
                if description and description != title:
                    req_text += f"\n   תיאור: {description}"
                if authority:
                    req_text += f"\n   רשות: {authority}"
                if area_req:
                    req_text += f"\n   דרישות שטח: {area_req}"
                if capacity_req:
                    req_text += f"\n   דרישות תפוסה: {capacity_req}"
                if special_req:
                    req_text += f"\n   דרישות מיוחדות: {special_req}"
                if priority:
                    req_text += f"\n   עדיפות: {priority}"
                if cost:
                    req_text += f"\n   עלות: {cost}"
                if time:
                    req_text += f"\n   זמן: {time}"
                requirements_summary.append(req_text)
        
        requirements_text = '\n\n'.join(requirements_summary) if requirements_summary else "אין דרישות ספציפיות"
        
        user_message = f"""אני צריך עזרה ביצירת דוח רישוי עסקים לעסק בישראל:

פרטי העסק:
- שם: {business_name}
- סוג: {business_type}
- שטח: {area} מ"ר
- תפוסה: {capacity} מקומות ישיבה
- מאפיינים: {features_text}

דרישות שנמצאו ({len(requirements)} סה"כ):
{requirements_text}

אנא צור דוח מקצועי בעברית שמבוסס בדיוק על הדרישות שפורטו לעיל.

חשוב: 
- השתמש רק בדרישות המפורטות למעלה ולא במידע כללי
- שים לב במיוחד לדרישות שטח ותפוסה אם מצוינות
- בדוק אם העסק עונה על הגבלות שנקבעו בדרישות
- אם יש סתירה בין גודל העסק לדרישות - ציין זאת בבירור

הדוח צריך לכלול:
1. תמצית מנהלים - כולל בדיקה אם העסק עונה על הדרישות הבסיסיות
2. דרישות עיקריות - רק אלה שמופיעות ברשימה
3. הערכות עלויות וזמנים - על בסיס הדרישות הקיימות
4. תוכנית פעולה מעשית
5. המלצות והתראות אם יש בעיות

הדוח צריך להיות מקצועי, מדויק ומבוסס על הנתונים בלבד."""

        return [
            {
                "role": "system",
                "content": "אתה יועץ רישוי עסקים מומחה בישראל. אתה מנתח רק את הדרישות הספציפיות שנתונות לך ולא מוסיף מידע כללי מבחוץ. אם יש סתירה בין פרטי העסק לדרישות המפורטות - אתה מציין זאת בבירור. התשובות שלך תמיד בעברית, מדויקות ומבוססות רק על הנתונים שסופקו."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    
    def _format_requirements_for_prompt(self, requirements: List[Dict]) -> str:
        """עיצוב דרישות עבור ה-prompt"""
        if not requirements:
            return "אין דרישות בקטגוריה זו"
        
        formatted = []
        for req in requirements[:5]:  # מגביל ל-5 דרישות כדי לא להעמיס על המודל
            title = req.get('title', 'ללא כותרת')[:100]
            authority = req.get('authority', 'לא צוין')
            formatted.append(f"- {title} (רשות: {authority})")
        
        if len(requirements) > 5:
            formatted.append(f"ועוד {len(requirements) - 5} דרישות נוספות...")
        
        return '\n'.join(formatted)
    
    
    


# יחידה גלובלית של הגנרטור
_generator_instance = None

def get_ai_generator():
    """קבלת מופע יחיד של הגנרטור"""
    global _generator_instance
    if _generator_instance is None:
        _generator_instance = PerplexityReportGenerator()
    return _generator_instance

def generate_ai_report(business_assessment, requirements_list) -> str:
    """
    פונקציה נוחה ליצירת דוח AI
    
    Args:
        business_assessment: אובייקט BusinessAssessment מהמודל
        requirements_list: רשימת דרישות רלוונטיות
        
    Returns:
        דוח מפורט כטקסט
    """
    try:
        # המרת נתונים לפורמט מתאים
        business_data = {
            'business_name': business_assessment.business_name,
            'business_type': business_assessment.business_type.name,
            'area_sqm': business_assessment.area_sqm,
            'seating_capacity': business_assessment.seating_capacity,
            'uses_gas': business_assessment.uses_gas,
            'serves_meat': business_assessment.serves_meat,
            'offers_delivery': business_assessment.offers_delivery,
            'has_outdoor_seating': business_assessment.has_outdoor_seating,
            'serves_alcohol': business_assessment.serves_alcohol,
        }
        
        # המרת דרישות לפורמט מתאים
        requirements = []
        for req in requirements_list:
            requirements.append({
                'title': req.title,
                'description': req.description,
                'authority': req.authority,
                'priority': req.priority,
                'category': req.category,
                'estimated_cost': req.estimated_cost,
                'processing_time': req.processing_time,
            })
        
        # יצירת הדוח
        generator = get_ai_generator()
        return generator.generate_report(business_data, requirements)
        
    except Exception as e:
        logger.error(f"Error in AI report generation: {e}")
        # אין דוח גיבוי - רק Perplexity
        raise Exception(f"Failed to generate AI report: {e}")

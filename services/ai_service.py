"""
שירות AI לייצור דוחות חכמים עם Flan-T5
"""
import logging
from typing import Dict, List, Optional
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

logger = logging.getLogger(__name__)


class FlanT5ReportGenerator:
    """
    מחלקה לייצור דוחות בעזרת Flan-T5
    """
    
    def __init__(self, model_name: str = "google/flan-t5-base"):
        """
        אתחול המודל
        
        Args:
            model_name: שם המודל מ-Hugging Face (flan-t5-base מומלץ לאיזון בין ביצועים לזיכרון)
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._load_model()
    
    def _load_model(self):
        """טעינת המודל והטוקנייזר"""
        try:
            logger.info(f"Loading Flan-T5 model: {self.model_name}")
            self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
            self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()
            logger.info(f"Model loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
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
            # הכנת prompt מובנה
            prompt = self._create_prompt(business_data, requirements)
            
            # יצירת הדוח
            report = self._generate_text(prompt)
            
            # עיבוד נוסף של הדוח
            formatted_report = self._format_report(report, business_data, requirements)
            
            return formatted_report
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return self._fallback_report(business_data, requirements)
    
    def _create_prompt(self, business_data: Dict, requirements: List[Dict]) -> str:
        """
        יצירת prompt מובנה עבור המודל
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
        
        # דרישות בעדיפות גבוהה
        high_priority_reqs = [req for req in requirements if req.get('priority') == 'high']
        medium_priority_reqs = [req for req in requirements if req.get('priority') == 'medium']
        
        prompt = f"""
Create a comprehensive business licensing report in Hebrew for the following business:

Business Details:
- Name: {business_name}
- Type: {business_type}
- Area: {area} square meters
- Seating Capacity: {capacity} seats
- Special Features: {features_text}

High Priority Requirements ({len(high_priority_reqs)} items):
{self._format_requirements_for_prompt(high_priority_reqs)}

Medium Priority Requirements ({len(medium_priority_reqs)} items):
{self._format_requirements_for_prompt(medium_priority_reqs)}

Write a professional business licensing report in Hebrew that includes:
1. Executive summary
2. Critical requirements analysis
3. Action plan with priorities
4. Cost and timeline estimates
5. Practical recommendations

Use clear, business-friendly Hebrew language. Focus on practical guidance.
"""
        
        return prompt
    
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
    
    def _generate_text(self, prompt: str) -> str:
        """יצירת טקסט עם המודל"""
        try:
            # הכנת הקלט
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
            inputs = inputs.to(self.device)
            
            # יצירת הטקסט
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=800,
                    min_length=200,
                    temperature=0.7,
                    do_sample=True,
                    top_p=0.9,
                    no_repeat_ngram_size=3,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # פענוח התוצאה
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Error in text generation: {e}")
            raise
    
    def _format_report(self, ai_content: str, business_data: Dict, requirements: List[Dict]) -> str:
        """עיצוב סופי של הדוח"""
        business_name = business_data.get('business_name', 'העסק')
        
        # מבנה הדוח הסופי
        report = f"""
# דוח הערכת רישוי עסקים - {business_name}

## תמצית מנהלים

{ai_content}

## פירוט דרישות לפי עדיפות

### דרישות בעדיפות גבוהה
{self._format_requirements_section([r for r in requirements if r.get('priority') == 'high'])}

### דרישות בעדיפות בינונית  
{self._format_requirements_section([r for r in requirements if r.get('priority') == 'medium'])}

### דרישות בעדיפות נמוכה
{self._format_requirements_section([r for r in requirements if r.get('priority') == 'low'])}

## המלצות סופיות

בהתבסס על ניתוח הנתונים, מומלץ להתחיל בטיפול בדרישות בעדיפות גבוהה ולהמשיך בהתאם לעדיפויות.
יש להתייעץ עם יועץ מקצועי ולפנות לרשויות הרלוונטיות לקבלת מידע עדכני.

---
*דוח זה נוצר באמצעות AI ומבוסס על הנתונים שסופקו. יש להתייעץ עם יועץ מקצועי לאימות המידע.*
"""
        
        return report.strip()
    
    def _format_requirements_section(self, requirements: List[Dict]) -> str:
        """עיצוב קטע דרישות"""
        if not requirements:
            return "אין דרישות בקטגוריה זו."
        
        formatted = []
        for i, req in enumerate(requirements, 1):
            title = req.get('title', 'ללא כותרת')
            authority = req.get('authority', 'לא צוין')
            cost = req.get('estimated_cost', 'לא צוין')
            time = req.get('processing_time', 'לא צוין')
            
            formatted.append(f"""
{i}. **{title[:100]}**
   - רשות מוסמכת: {authority}
   - עלות משוערת: {cost}
   - זמן טיפול: {time}
""")
        
        return '\n'.join(formatted)
    
    def _fallback_report(self, business_data: Dict, requirements: List[Dict]) -> str:
        """דוח גיבוי במקרה של שגיאה ב-AI"""
        business_name = business_data.get('business_name', 'העסק')
        
        return f"""
# דוח הערכת רישוי עסקים - {business_name}

## תמצית

בוצעה הערכת רישוי עבור {business_name}.
נמצאו {len(requirements)} דרישות רלוונטיות לעסק.

## דרישות עיקריות

{self._format_requirements_section(requirements[:10])}

## המלצות

מומלץ לטפל בדרישות לפי סדר עדיפות ולהתייעץ עם יועץ מקצועי.

---
*דוח זה נוצר במצב חירום ללא שימוש ב-AI. לדוח מפורט יותר, נסו שוב מאוחר יותר.*
"""


# יחידה גלובלית של הגנרטור
_generator_instance = None

def get_ai_generator():
    """קבלת מופע יחיד של הגנרטור"""
    global _generator_instance
    if _generator_instance is None:
        _generator_instance = FlanT5ReportGenerator()
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
        # החזרת דוח גיבוי
        return f"""
# דוח הערכת רישוי עסקים - {business_assessment.business_name}

## שגיאה ביצירת דוח AI

אירעה שגיאה ביצירת הדוח החכם: {str(e)}

## סיכום בסיסי

נמצאו {len(requirements_list)} דרישות רלוונטיות לעסק שלכם.
אנא פנו ליועץ מקצועי לקבלת עזרה בתהליך הרישוי.

---
*דוח זה נוצר במצב חירום ללא AI*
"""

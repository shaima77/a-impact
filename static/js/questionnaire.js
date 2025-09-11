// Questionnaire JavaScript functionality

let currentStep = 1;
const totalSteps = 4;
let formData = {};

document.addEventListener('DOMContentLoaded', function() {
    initializeQuestionnaire();
    setupEventListeners();
    updateProgress();
});

function initializeQuestionnaire() {
    // Show first step
    showStep(1);
    
    // Initialize form data
    formData = {
        business_name: '',
        business_type: '',
        area_sqm: '',
        seating_capacity: '',
        features: {
            uses_gas: false,
            serves_meat: false,
            offers_delivery: false,
            has_outdoor_seating: false,
            serves_alcohol: false
        }
    };
}

function setupEventListeners() {
    // Business type selection
    const businessTypeOptions = document.querySelectorAll('[data-value]');
    businessTypeOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Remove previous selection
            businessTypeOptions.forEach(opt => opt.classList.remove('selected'));
            
            // Add selection to clicked option
            this.classList.add('selected');
            
            // Update hidden input
            document.getElementById('businessType').value = this.dataset.value;
            formData.business_type = this.dataset.value;
        });
    });
    
    // Feature selection
    const featureOptions = document.querySelectorAll('[data-feature]');
    featureOptions.forEach(option => {
        option.addEventListener('click', function() {
            const feature = this.dataset.feature;
            const isSelected = this.classList.contains('selected');
            
            if (isSelected) {
                this.classList.remove('selected');
                document.getElementById(feature).value = 'false';
                formData.features[feature] = false;
            } else {
                this.classList.add('selected');
                document.getElementById(feature).value = 'true';
                formData.features[feature] = true;
            }
        });
    });
    
    // Input field updates
    document.getElementById('businessName').addEventListener('input', function() {
        formData.business_name = this.value;
    });
    
    document.getElementById('areaSize').addEventListener('input', function() {
        formData.area_sqm = this.value;
    });
    
    document.getElementById('seatingCapacity').addEventListener('input', function() {
        formData.seating_capacity = this.value;
    });
}

function changeStep(direction) {
    const newStep = currentStep + direction;
    
    // Validate current step before moving forward
    if (direction > 0 && !validateCurrentStep()) {
        return;
    }
    
    // Check boundaries
    if (newStep < 1 || newStep > totalSteps) {
        return;
    }
    
    // Update current step
    currentStep = newStep;
    
    // Show new step
    showStep(currentStep);
    
    // Update progress
    updateProgress();
    
    // Update review if on last step
    if (currentStep === totalSteps) {
        updateReview();
    }
}

function showStep(stepNumber) {
    // Hide all steps
    const steps = document.querySelectorAll('.form-step');
    steps.forEach(step => step.classList.remove('active'));
    
    // Show current step
    const currentStepElement = document.getElementById(`step${stepNumber}`);
    if (currentStepElement) {
        currentStepElement.classList.add('active');
        
        // Scroll to top
        currentStepElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    // Update navigation buttons
    updateNavigationButtons();
}

function updateNavigationButtons() {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    
    // Previous button
    if (currentStep === 1) {
        prevBtn.style.display = 'none';
    } else {
        prevBtn.style.display = 'inline-block';
    }
    
    // Next/Submit buttons
    if (currentStep === totalSteps) {
        nextBtn.style.display = 'none';
        submitBtn.style.display = 'inline-block';
    } else {
        nextBtn.style.display = 'inline-block';
        submitBtn.style.display = 'none';
    }
}

function updateProgress() {
    const progressBar = document.getElementById('progressBar');
    const stepCounter = document.getElementById('stepCounter');
    
    const progressPercent = (currentStep / totalSteps) * 100;
    progressBar.style.width = progressPercent + '%';
    
    stepCounter.textContent = `שלב ${currentStep} מתוך ${totalSteps}`;
}

function validateCurrentStep() {
    switch (currentStep) {
        case 1:
            const businessName = document.getElementById('businessName').value.trim();
            const businessType = document.getElementById('businessType').value;
            
            if (!businessName) {
                showError('אנא הזינו שם עסק');
                return false;
            }
            
            if (!businessType) {
                showError('אנא בחרו סוג עסק');
                return false;
            }
            
            return true;
            
        case 2:
            const areaSize = document.getElementById('areaSize').value;
            const seatingCapacity = document.getElementById('seatingCapacity').value;
            
            if (!areaSize || areaSize < 1) {
                showError('אנא הזינו שטח תקין');
                return false;
            }
            
            if (!seatingCapacity || seatingCapacity < 1) {
                showError('אנא הזינו מספר מקומות ישיבה תקין');
                return false;
            }
            
            return true;
            
        case 3:
            // Features are optional, so always valid
            return true;
            
        default:
            return true;
    }
}

function updateReview() {
    const reviewContent = document.getElementById('reviewContent');
    
    // Get selected features
    const selectedFeatures = [];
    Object.keys(formData.features).forEach(key => {
        if (formData.features[key]) {
            const featureNames = {
                uses_gas: 'שימוש בגז',
                serves_meat: 'הגשת בשר',
                offers_delivery: 'שירות משלוחים',
                has_outdoor_seating: 'ישיבה בחוץ',
                serves_alcohol: 'הגשת אלכוהול'
            };
            selectedFeatures.push(featureNames[key]);
        }
    });
    
    // Get business type name
    const businessTypeNames = {
        'מסעדה': 'מסעדה',
        'בר': 'בר/פאב',
        'בית קפה': 'בית קפה',
        'מזון מהיר': 'מזון מהיר',
        restaurant: 'מסעדה',
        bar: 'בר/פאב',
        cafe: 'בית קפה',
        fast_food: 'מזון מהיר'
    };
    
    const businessTypeName = businessTypeNames[formData.business_type] || formData.business_type;
    
    reviewContent.innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <h5><i class="fas fa-store text-primary"></i> פרטי העסק</h5>
                <ul class="list-unstyled">
                    <li><strong>שם העסק:</strong> ${formData.business_name}</li>
                    <li><strong>סוג העסק:</strong> ${businessTypeName}</li>
                </ul>
            </div>
            <div class="col-md-6">
                <h5><i class="fas fa-ruler-combined text-success"></i> מידות ותפוסה</h5>
                <ul class="list-unstyled">
                    <li><strong>שטח:</strong> ${formData.area_sqm} מ"ר</li>
                    <li><strong>מקומות ישיבה:</strong> ${formData.seating_capacity}</li>
                </ul>
            </div>
        </div>
        
        <hr>
        
        <h5><i class="fas fa-cogs text-info"></i> מאפיינים מיוחדים</h5>
        ${selectedFeatures.length > 0 ? 
            `<ul class="list-unstyled">
                ${selectedFeatures.map(feature => `<li><i class="fas fa-check text-success"></i> ${feature}</li>`).join('')}
            </ul>` : 
            '<p class="text-muted">לא נבחרו מאפיינים מיוחדים</p>'
        }
    `;
}

function showError(message) {
    // Remove any existing error alerts
    const existingAlert = document.querySelector('.alert-danger');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    // Create new error alert
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show mt-3';
    alert.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert after current step
    const currentStepElement = document.querySelector('.form-step.active');
    currentStepElement.appendChild(alert);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

// Form submission handling
document.getElementById('questionnaireForm').addEventListener('submit', function(e) {
    if (!validateCurrentStep()) {
        e.preventDefault();
        return;
    }
    
    // Final validation before submit
    const businessName = document.getElementById('businessName').value.trim();
    const businessType = document.getElementById('businessType').value;
    const areaSize = document.getElementById('areaSize').value;
    const seatingCapacity = document.getElementById('seatingCapacity').value;
    
    if (!businessName || !businessType || !areaSize || !seatingCapacity) {
        e.preventDefault();
        showError('אנא מלא את כל השדות הנדרשים');
        return;
    }
    
    // Show loading state
    const submitBtn = document.getElementById('submitBtn');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> יוצר דוח AI...';
    submitBtn.disabled = true;
    
    // Debug: log form data
    console.log('Form submission data:', {
        business_name: businessName,
        business_type: businessType,
        area_sqm: areaSize,
        seating_capacity: seatingCapacity
    });
});

// Keyboard navigation
document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowLeft') {
        changeStep(1);
    } else if (e.key === 'ArrowRight') {
        changeStep(-1);
    }
});

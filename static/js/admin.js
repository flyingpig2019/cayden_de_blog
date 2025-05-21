/**
 * Admin JavaScript file for Cayden's Growth Blog
 * This file is only loaded when an admin is logged in
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize inline editing for all content-editable elements
    initInlineEditing();
});

/**
 * Initialize inline editing functionality for elements with contenteditable attribute
 */
function initInlineEditing() {
    // Add visual cues to editable elements
    const editableElements = document.querySelectorAll('[contenteditable="true"]');
    
    editableElements.forEach(element => {
        // Add edit icon and tooltip
        element.setAttribute('data-tooltip', 'Click to edit');
        
        // Add focus and blur events for better UX
        element.addEventListener('focus', function() {
            this.classList.add('editing');
            this.style.backgroundColor = '#f0f8ff';
        });
        
        element.addEventListener('blur', function() {
            this.classList.remove('editing');
            this.style.backgroundColor = '';
        });
    });
}

/**
 * Handle file uploads with preview
 * @param {HTMLElement} inputElement - The file input element
 * @param {HTMLElement} previewElement - The element to show the preview in
 */
function handleFileUpload(inputElement, previewElement) {
    inputElement.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.style.maxWidth = '100%';
                img.style.maxHeight = '200px';
                
                previewElement.innerHTML = '';
                previewElement.appendChild(img);
            };
            
            reader.readAsDataURL(file);
        }
    });
}

/**
 * Show confirmation dialog before deleting items
 * @param {string} message - The confirmation message to display
 * @returns {boolean} True if confirmed, false otherwise
 */
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

/**
 * Display notification to the user
 * @param {string} message - The message to display
 * @param {string} type - The type of notification (success, error, info)
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.padding = '10px 15px';
    notification.style.borderRadius = '4px';
    notification.style.zIndex = '9999';
    notification.style.maxWidth = '300px';
    notification.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    
    if (type === 'success') {
        notification.style.backgroundColor = '#dff0d8';
        notification.style.color = '#3c763d';
        notification.style.border = '1px solid #d6e9c6';
    } else if (type === 'error') {
        notification.style.backgroundColor = '#f2dede';
        notification.style.color = '#a94442';
        notification.style.border = '1px solid #ebccd1';
    } else {
        notification.style.backgroundColor = '#d9edf7';
        notification.style.color = '#31708f';
        notification.style.border = '1px solid #bce8f1';
    }
    
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transition = 'opacity 0.5s';
        
        setTimeout(() => {
            notification.remove();
        }, 500);
    }, 3000);
}
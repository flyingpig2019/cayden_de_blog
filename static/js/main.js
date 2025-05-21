/**
 * Main JavaScript file for Cayden's Growth Blog
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize flash message dismissal
    initFlashMessages();
    
    // Initialize any tooltips
    initTooltips();
});

/**
 * Initialize flash message dismissal functionality
 */
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        // Add close button to each message
        const closeBtn = document.createElement('span');
        closeBtn.innerHTML = '&times;';
        closeBtn.className = 'flash-close';
        closeBtn.style.float = 'right';
        closeBtn.style.cursor = 'pointer';
        closeBtn.style.marginLeft = '10px';
        message.prepend(closeBtn);
        
        // Add click event to close button
        closeBtn.addEventListener('click', function() {
            message.style.display = 'none';
        });
        
        // Auto-hide messages after 5 seconds
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transition = 'opacity 0.5s';
            
            // Remove from DOM after fade out
            setTimeout(() => {
                message.style.display = 'none';
            }, 500);
        }, 5000);
    });
}

/**
 * Initialize tooltips for elements with data-tooltip attribute
 */
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.style.position = 'relative';
        
        element.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = tooltipText;
            tooltip.style.position = 'absolute';
            tooltip.style.bottom = '100%';
            tooltip.style.left = '50%';
            tooltip.style.transform = 'translateX(-50%)';
            tooltip.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
            tooltip.style.color = 'white';
            tooltip.style.padding = '5px 10px';
            tooltip.style.borderRadius = '4px';
            tooltip.style.fontSize = '14px';
            tooltip.style.zIndex = '1000';
            tooltip.style.whiteSpace = 'nowrap';
            tooltip.style.marginBottom = '5px';
            
            this.appendChild(tooltip);
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltip = this.querySelector('.tooltip');
            if (tooltip) {
                tooltip.remove();
            }
        });
    });
}

/**
 * Format date to a readable string
 * @param {Date} date - The date to format
 * @returns {string} Formatted date string
 */
function formatDate(date) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString(document.documentElement.lang || 'en', options);
}

/**
 * Format time to a readable string
 * @param {Date} date - The date to format
 * @returns {string} Formatted time string
 */
function formatTime(date) {
    const options = { hour: '2-digit', minute: '2-digit' };
    return date.toLocaleTimeString(document.documentElement.lang || 'en', options);
}

/**
 * Format datetime to a readable string
 * @param {Date} date - The date to format
 * @returns {string} Formatted datetime string
 */
function formatDateTime(date) {
    return `${formatDate(date)} ${formatTime(date)}`;
}
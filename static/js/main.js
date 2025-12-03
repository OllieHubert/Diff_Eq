// Main JavaScript file for ODE Methods website

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    // Add any global JavaScript functionality here
    console.log('ODE Methods website loaded');
    
    // Highlight current page in navigation
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-menu a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.opacity = '1';
            link.style.fontWeight = 'bold';
        }
    });
});

// Utility function to format equations for display
function formatEquation(eq) {
    return eq.replace(/\*\*/g, '^').replace(/\*/g, '\\cdot ');
}


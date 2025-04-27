/**
 * Main JavaScript for Smart Fill-in-the-Blanks with AI
 */

// Add smooth scrolling to all links
document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    for (const link of links) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 70,
                    behavior: 'smooth'
                });
            }
        });
    }
});

// Format AI response text with markdown-like syntax
function formatAIResponse(text) {
    if (!text) return '';
    
    // Replace line breaks with <br>
    text = text.replace(/\n/g, '<br>');
    
    // Bold text between ** **
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Italic text between * *
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Headers
    text = text.replace(/^# (.*?)$/gm, '<h2>$1</h2>');
    text = text.replace(/^## (.*?)$/gm, '<h3>$1</h3>');
    text = text.replace(/^### (.*?)$/gm, '<h4>$1</h4>');
    
    // Lists
    text = text.replace(/^- (.*?)$/gm, '• $1<br>');
    
    return text;
}

// Add a global error handler
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.message);
    
    // You could add more sophisticated error handling here
    // such as sending errors to a logging service
});

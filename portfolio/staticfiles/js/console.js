// Console interaction for 90s retro portfolio

document.addEventListener('DOMContentLoaded', function() {
    const consoleOutput = document.getElementById('console-output');
    const navItems = document.querySelectorAll('.nav-item[data-category]');
    let currentCategory = null;
    
    // Get current category from URL or active nav item
    function getCurrentCategory() {
        const urlParams = new URLSearchParams(window.location.search);
        const category = urlParams.get('category') || 'about-me';
        return category;
    }
    
    // Update console output based on category
    function updateConsole(category) {
        // Special categories that don't have skills
        const specialCategories = ['about-me', 'open-source', 'education', 'skills'];
        
        // Check if category has skills by looking at nav item data attribute
        const navItem = document.querySelector(`.nav-item[data-category="${category}"]`);
        const hasSkills = navItem ? navItem.getAttribute('data-has-skills') === 'true' : false;
        
        if (!category || specialCategories.includes(category) || !hasSkills) {
            // For non-skill categories, show welcome message
            showWelcomeMessage();
            return;
        }
        
        // Get current language from URL
        const urlParams = new URLSearchParams(window.location.search);
        const lang = urlParams.get('lang') || 'en';
        
        // Show cd command first, then fetch skills
        displayCDCommand(category);
        
        // Fetch console output from API
        setTimeout(() => {
            fetch(`/api/console/${category}/?lang=${lang}`)
                .then(response => {
                    if (!response.ok) {
                        // If 404, check if it's a special category
                        return response.json().then(data => {
                            if (data && data.is_special) {
                                showWelcomeMessage();
                            } else {
                                displayConsoleError(data ? data.error : 'Category not found');
                            }
                        }).catch(() => {
                            // If JSON parsing fails, just show welcome message
                            showWelcomeMessage();
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    if (data && data.output) {
                        displayConsoleOutput(data.output, category);
                    } else if (data && data.error) {
                        displayConsoleError(data.error);
                    }
                })
                .catch(error => {
                    console.error('Error fetching console output:', error);
                    // On error, show welcome message instead of error
                    showWelcomeMessage();
                });
        }, 500); // Delay after cd command
    }
    
    // Display cd command
    function displayCDCommand(category) {
        consoleOutput.innerHTML = '';
        const cdLine = document.createElement('div');
        cdLine.className = 'console-line';
        cdLine.textContent = `C:\\>cd ${category}`;
        consoleOutput.appendChild(cdLine);
        
        const promptLine = document.createElement('div');
        promptLine.className = 'console-line';
        promptLine.textContent = `C:\\${category}>`;
        consoleOutput.appendChild(promptLine);
    }
    
    // Display console output with typewriter effect
    function displayConsoleOutput(output, category) {
        // Add cat command
        const catLine = document.createElement('div');
        catLine.className = 'console-line';
        catLine.textContent = `C:\\${category}>cat skills.txt`;
        consoleOutput.appendChild(catLine);
        
        const lines = output.split('\n');
        
        lines.forEach((line, index) => {
            setTimeout(() => {
                const lineElement = document.createElement('div');
                lineElement.className = 'console-line';
                lineElement.textContent = line;
                consoleOutput.appendChild(lineElement);
                
                // Auto-scroll to bottom
                consoleOutput.scrollTop = consoleOutput.scrollHeight;
            }, (index + 1) * 50); // 50ms delay between lines for typewriter effect
        });
    }
    
    // Display error message
    function displayConsoleError(error) {
        consoleOutput.innerHTML = '';
        const errorLine = document.createElement('div');
        errorLine.className = 'console-line';
        errorLine.textContent = `C:\\>Error: ${error}`;
        errorLine.style.color = '#ff4444';
        consoleOutput.appendChild(errorLine);
    }
    
    // Show welcome message
    function showWelcomeMessage() {
        consoleOutput.innerHTML = '';
        const messages = [
            'C:\\>Welcome to Portfolio Terminal',
            'C:\\>Select a category to view skills',
            'C:\\>_'
        ];
        
        messages.forEach((msg, index) => {
            setTimeout(() => {
                const lineElement = document.createElement('div');
                lineElement.className = 'console-line';
                lineElement.textContent = msg;
                consoleOutput.appendChild(lineElement);
            }, index * 100);
        });
    }
    
    // Handle nav item clicks
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            const category = this.getAttribute('data-category');
            currentCategory = category;
            
            // Update console after a short delay to allow page navigation
            setTimeout(() => {
                updateConsole(category);
            }, 100);
        });
    });
    
    // Initialize console on page load
    currentCategory = getCurrentCategory();
    updateConsole(currentCategory);
    
    // Update console when category changes via URL (back/forward buttons)
    window.addEventListener('popstate', function() {
        currentCategory = getCurrentCategory();
        updateConsole(currentCategory);
    });
});


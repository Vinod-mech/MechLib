// Main JavaScript for ANITS Digital Library

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        if (!alert.classList.contains('alert-danger')) {
            setTimeout(function() {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });

    // File upload progress
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Show file size
                const fileSize = (file.size / (1024 * 1024)).toFixed(2);
                const fileName = file.name;
                
                // Create or update file info display
                let fileInfo = document.querySelector('.file-info');
                if (!fileInfo) {
                    fileInfo = document.createElement('div');
                    fileInfo.className = 'file-info mt-2';
                    input.parentNode.appendChild(fileInfo);
                }
                
                fileInfo.innerHTML = `
                    <small class="text-muted">
                        <i class="fas fa-file me-1"></i>
                        Selected: ${fileName} (${fileSize} MB)
                    </small>
                `;
            }
        });
    });

    // Search form enhancements
    const searchForm = document.querySelector('form[action*="search"]');
    if (searchForm) {
        const yearSelect = searchForm.querySelector('select[name="year"]');
        const subjectSelect = searchForm.querySelector('select[name="subject"]');
        
        if (yearSelect && subjectSelect) {
            yearSelect.addEventListener('change', function() {
                if (this.value) {
                    // Filter subjects based on selected year
                    const yearId = parseInt(this.value);
                    const allOptions = subjectSelect.querySelectorAll('option');
                    
                    allOptions.forEach(function(option) {
                        if (option.value === '') {
                            option.style.display = 'block';
                            return;
                        }
                        
                        const optionText = option.textContent;
                        const yearMatch = optionText.includes(yearSelect.options[yearSelect.selectedIndex].text);
                        
                        option.style.display = yearMatch ? 'block' : 'none';
                    });
                    
                    // Reset subject selection
                    subjectSelect.value = '';
                } else {
                    // Show all subjects
                    subjectSelect.querySelectorAll('option').forEach(function(option) {
                        option.style.display = 'block';
                    });
                }
            });
        }
    }

    // Confirmation dialogs for delete actions
    const deleteButtons = document.querySelectorAll('button[onclick*="confirm"]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
                return false;
            }
        });
    });

    // Table sorting (simple client-side sorting)
    const sortableHeaders = document.querySelectorAll('th[data-sort]');
    sortableHeaders.forEach(function(header) {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            const table = this.closest('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const index = Array.from(this.parentNode.children).indexOf(this);
            const isAsc = !this.classList.contains('sort-asc');
            
            // Remove existing sort classes
            sortableHeaders.forEach(h => h.classList.remove('sort-asc', 'sort-desc'));
            
            // Add current sort class
            this.classList.add(isAsc ? 'sort-asc' : 'sort-desc');
            
            // Sort rows
            rows.sort(function(a, b) {
                const aText = a.children[index].textContent.trim();
                const bText = b.children[index].textContent.trim();
                
                if (isAsc) {
                    return aText.localeCompare(bText, undefined, {numeric: true});
                } else {
                    return bText.localeCompare(aText, undefined, {numeric: true});
                }
            });
            
            // Reorder rows in DOM
            rows.forEach(row => tbody.appendChild(row));
        });
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Form validation improvements
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Processing...';
                
                // Re-enable button after 5 seconds (in case of errors)
                setTimeout(function() {
                    submitButton.disabled = false;
                    submitButton.innerHTML = submitButton.innerHTML.replace(
                        '<i class="fas fa-spinner fa-spin me-1"></i>Processing...',
                        submitButton.textContent
                    );
                }, 5000);
            }
        });
    });

    // Statistics counter animation (if elements exist)
    const counters = document.querySelectorAll('[data-counter]');
    if (counters.length > 0) {
        const animateCounter = function(counter) {
            const target = parseInt(counter.getAttribute('data-counter'));
            const count = parseInt(counter.textContent) || 0;
            const increment = target / 100;
            
            if (count < target) {
                counter.textContent = Math.ceil(count + increment);
                setTimeout(() => animateCounter(counter), 20);
            } else {
                counter.textContent = target;
            }
        };
        
        // Trigger animation when counters come into view
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        });
        
        counters.forEach(counter => observer.observe(counter));
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('.flaskmotion-nav-link');
    const content = document.querySelector('.flaskmotion-content');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const page = this.getAttribute('data-flaskmotion-page');
            loadPage(page);
        });
    });

    function loadPage(page) {
        // Fade out current content
        content.classList.add('flaskmotion-fade-out');
        
        // Fetch new content using AJAX
        fetch(`/load/${page}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Page not found');
                }
                return response.text();
            })
            .then(data => {
                // Update content
                content.innerHTML = data;
                content.classList.remove('flaskmotion-fade-out');
                content.classList.add('flaskmotion-fade-in');
                
                // Remove the fade-in class after the animation completes
                setTimeout(() => content.classList.remove('flaskmotion-fade-in'), 500);
            })
            .catch(error => console.error(error));
    }
});

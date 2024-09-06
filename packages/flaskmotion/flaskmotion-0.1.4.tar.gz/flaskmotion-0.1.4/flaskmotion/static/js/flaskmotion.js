document.addEventListener("DOMContentLoaded", () => {
    const contentContainer = document.getElementById('fm-container');

    function fetchAndTransition(targetUrl) {
        // Add fade-out class to initiate the fade-out effect
        contentContainer.classList.add('fade-out');

        setTimeout(() => {
            fetch(targetUrl)
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newContent = doc.querySelector('#fm-container').innerHTML;

                    // Update content and apply fade-in effect
                    contentContainer.innerHTML = newContent;
                    contentContainer.classList.remove('fade-out');
                    contentContainer.classList.add('fade-in');

                    setTimeout(() => {
                        contentContainer.classList.remove('fade-in');
                    }, 500);

                    // Update the browser history
                    history.pushState(null, '', targetUrl);
                })
                .catch(error => console.error('Error fetching page:', error));
        }, 500); // Delay for fade-out effect
    }

    function attachLinkListeners() {
        const links = document.querySelectorAll('a');
        links.forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                const targetUrl = link.getAttribute('href');
                fetchAndTransition(targetUrl);
            });
        });
    }

    attachLinkListeners();

    window.addEventListener('popstate', () => {
        fetchAndTransition(window.location.pathname);
    });
});

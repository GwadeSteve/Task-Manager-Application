// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('#navbar');
    const links = navbar.querySelectorAll('a');
    const sections = document.querySelectorAll('.section');
    const menuBtn = document.querySelector('#menu-btn');
    const mobileBg = document.querySelector('.magic i');
    const task_detail = document.querySelector('#task-detail');
    const category_detail = document.querySelector('#category-detail');
    let isActive = false;

    // Function to update the active link based on the current URL
    function updateActiveLink() {
        const currentPath = window.location.pathname;

        links.forEach(link => {
            const linkPath = link.getAttribute('href');
            if (currentPath === linkPath) {
                link.classList.add('active');
                const sectionId = link.dataset.section;
                const section = document.querySelector(`#${sectionId}`);
                section.classList.add('active');
            } else {
                link.classList.remove('active');
                const sectionId = link.dataset.section;
                const section = document.querySelector(`#${sectionId}`);
                section.classList.remove('active');
            }
        });
    }

    // Call the updateActiveLink function to initialize the active link
    updateActiveLink();

    // Add event listener to update the active link when a link is clicked
    links.forEach(link => {
        link.addEventListener('click', () => {
            updateActiveLink();
        });
    });

    menuBtn.addEventListener('click', () => {
        navbar.classList.toggle('active');
        isActive = !isActive;

        if (isActive) {
            menuBtn.classList.replace('bx-menu', 'bx-x');
        } else {
            menuBtn.classList.replace('bx-x', 'bx-menu');
        }
    });

    mobileBg.addEventListener('click', () => {
        navbar.classList.toggle('active');
        isActive = !isActive;
        if (isActive) {
            menuBtn.classList.replace('bx-menu', 'bx-x');
        } else {
            menuBtn.classList.replace('bx-menu', 'bx-x');
        }
    });
});
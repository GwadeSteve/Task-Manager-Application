const navbar = document.querySelector('#navbar');
const links = navbar.querySelectorAll('a');
const sections = document.querySelectorAll('.section');
const menuBtn = document.querySelector('#menu-btn');
const mobileBg = document.querySelector('.magic i')
let isActive = false;

links.forEach(link => {
    link.addEventListener('click', () => {
        links.forEach(otherLink => otherLink.classList.remove('active'));
        link.classList.add('active');
        sections.forEach(section => section.classList.remove('active'));
        const sectionId = link.dataset.section;
        const section = document.querySelector(`#${sectionId}`);
        section.classList.add('active');
    });
});

menuBtn.addEventListener('click', () => {
    navbar.classList.toggle('active');
    isActive = !isActive;

    if (isActive) {
        menuBtn.classList.replace('bx-menu', 'bx-x');
        //document.querySelector('.main-content').style.transform = 'translateX(140px)';
    } else {
        menuBtn.classList.replace('bx-x', 'bx-menu');
        //document.querySelector('.main-content').style.transform = 'translateX(0)';
    }
});

mobileBg.addEventListener('click', () => {
    navbar.classList.toggle('active');
    isActive = !isActive;
    if (isActive) {
        menuBtn.classList.replace('bx-menu', 'bx-x');
        //document.querySelector('.main-content').style.transform = 'translateX(140px)';
    } else {
        menuBtn.classList.replace('bx-menu', 'bx-x');
        //document.querySelector('.main-content').style.transform = 'translateX(0)';
    }
})
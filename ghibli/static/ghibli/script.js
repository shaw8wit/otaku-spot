// * removes the notification
(document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
    var $notification = $delete.parentNode;
    $delete.addEventListener('click', () => {
        $notification.classList.add('is-hidden');
    })
});


// * manupulates the hamburger menu
let menu = document.querySelector('.navbar-burger');
menu.addEventListener('click', () => {
    const target = menu.dataset.target;
    const $target = document.getElementById(target);
    menu.classList.toggle('is-active');
    $target.classList.toggle('is-active');
});
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

// * changes the notification 
function editNotification(notification, class_val, text) {
    let class_list = ['is-warning', 'is-error', 'is-success', 'is-info'];
    class_list.forEach(e => notification.classList.remove(e));
    notification.querySelector('span').innerText = text;
    notification.classList.add(class_val);
    notification.classList.remove('is-hidden');
}

// * changes the icon
function changeIcon(icon, class_val) {
    icon.classList.remove('fa-plus', 'fa-trash-o');
    icon.classList.add(class_val);
}

/**
 ** gets the quote data to be worked on.
 * @param {element} e The card element where the data resides.
 * @param {boolean} status The saving-deleting or sharing status. 
 */
function getData(e, status) {

    let quote = e.querySelector('.quote').innerText;
    let anime = e.querySelector('.anime').innerText;
    let character = e.querySelector('.character').innerText;

    if (status) {
        window.prompt("Copy to clipboard: Ctrl+C, Enter", `${character} from ${anime} said: ${quote}`);
    } else {
        let icon = e.querySelector('.fa');
        let plus = icon.classList.contains('fa-plus');
        let notification = e.querySelector('.notification');

        fetch('/quotes/addData', {
            method: 'POST',
            body: JSON.stringify({
                anime: anime,
                character: character,
                quote: quote,
                addDel: plus,
            })
        }).then(response => {
            if (![200, 201].includes(response.status)) return response.json();
            else if (response.status == 200) {
                changeIcon(icon, 'fa-plus');
                editNotification(notification, "is-info", "Quote deleted from profile successfully!");
            } else {
                changeIcon(icon, 'fa-trash-o');
                editNotification(notification, "is-success", "Quote saved to profile successfully!");
            }
        }).then(err => {
            if (err) editNotification(notification, "is-danger", err.error);
            if (icon.classList.contains('profile')) e.parentNode.removeChild(e);
        });
    }
}

// * for saving or removing any quotes
let saveQuote = document.querySelectorAll('.saveQuote');
saveQuote.forEach(e => e.addEventListener('click', () => getData(e.closest('.card'), false)));

// * for sharing or copying any quotes
let shareQuote = document.querySelectorAll('.shareQuote');
shareQuote.forEach(e => e.addEventListener('click', () => getData(e.closest('.card'), true)))

/**
 ** gets the profile data to be worked on.
 ** makes edits according to the changes made by user.
 */
function editProfile() {
    username = document.querySelector('.username');
    email = document.querySelector('.email');
    notification = document.querySelector('.profnotif');
    if (edit.innerText === 'Edit') {
        edit.innerText = 'Save';
        username.readOnly = false;
        email.readOnly = false;
    } else {
        edit.innerText = 'Edit';
        username.readOnly = true;
        email.readOnly = true;
        fetch('/quotes/profile', {
            method: 'PUT',
            body: JSON.stringify({
                username: username.value,
                email: email.value,
            })
        }).then(response => {
            if (![200, 202, 204].includes(response.status)) return response.json();
            else if (response.status === 200) editNotification(notification, "is-info", "Profile data unchanged.");
            else if (response.status === 204) editNotification(notification, "is-warning", "Username and/or Email already exists!");
            else editNotification(notification, "is-success", "Profile data changed successfully.");
        }).then(err => {
            if (err) editNotification(notification, "is-error", err.error);;
        });
    }
}

// * for editing profile
let edit = document.querySelector('.edit');
if (edit !== null) edit.addEventListener('click', editProfile);
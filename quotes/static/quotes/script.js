(document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
    var $notification = $delete.parentNode;

    $delete.addEventListener('click', () => {
        $notification.classList.add('is-hidden');
    })
});


let menu = document.querySelector('.navbar-burger');
menu.addEventListener('click', () => {
    const target = menu.dataset.target;
    const $target = document.getElementById(target);
    menu.classList.toggle('is-active');
    $target.classList.toggle('is-active');
});

function getData(e) {
    let anime = e.querySelector('.anime').innerText;
    let character = e.querySelector('.character').innerText;
    let quote = e.querySelector('.quote').innerText;
    let notification = e.querySelector('.notification');
    let icon = e.querySelector('.fa');
    let text;

    fetch('/quotes/addData', {
        method: 'POST',
        body: JSON.stringify({
            anime: anime,
            character: character,
            quote: quote,
        })
    }).then(response => {
        // * can use 200 fulfilled, 201 created, 202 Accepted
        if (response.status !== 204) return response.json();
    }).then(err => {
        if (icon.classList.contains('fa-plus')) {
            icon.classList.replace('fa-plus', 'fa-trash-o');
            text = "Quote saved to profile successfully!";
        } else {
            icon.classList.replace('fa-trash-o', 'fa-plus');
            text = "Quote deleted from profile successfully!";
        }
        if (err) text = err.error;
    }).then(e => {
        notification.querySelector('span').innerText = text;
        notification.classList.toggle('is-hidden');
        if (icon.classList.contains('profile')) window.location.reload();
    });
}

let saveQuote = document.querySelectorAll('.saveQuote');
saveQuote.forEach(e => e.addEventListener('click', () => getData(e.closest('.card'))));

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
            // * can use 200 fulfilled, 201 created, 202 Accepted
            if (response.status !== 204) return response.json();
        }).then(err => {
            if (err) text = err.error;
            else text = 'Successful!'
        }).then(e => {
            notification.querySelector('span').innerText = text;
            notification.classList.toggle('is-hidden');
        });
    }
}

let edit = document.querySelector('.edit');
edit.addEventListener('click', editProfile);
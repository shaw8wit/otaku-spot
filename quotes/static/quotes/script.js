(document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
    var $notification = $delete.parentNode;

    $delete.addEventListener('click', () => {
        $notification.parentNode.removeChild($notification);
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
    let text;

    fetch('/quotes/addData', {
        method: 'POST',
        body: JSON.stringify({
            anime: anime,
            character: character,
            quote: quote,
        })
    }).then(response => {
        if (response.status !== 204) return response.json();
        text = "Quote saved successfully!";
    }).then(err => {
        if (err) {
            text = err.error;
        }
    }).then(e => {
        notification.querySelector('span').innerText = text;
        notification.classList.toggle('is-hidden');
    });
}

let saveQuote = document.querySelectorAll('.saveQuote');
saveQuote.forEach(e => e.addEventListener('click', () => getData(e.closest('.card'))));
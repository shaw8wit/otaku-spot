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
    while (true) {
        if (e.classList.contains('card')) break;
        e = e.parentNode;
    }
    let anime = e.querySelector('.anime').innerText;
    let character = e.querySelector('.character').innerText;
    let quote = e.querySelector('.quote').innerText;
    console.log(anime, character, quote);
    // ! data parsed now create and save to user model

    fetch('/quotes/addData', {
        method: 'POST',
        body: JSON.stringify({
            anime: anime,
            character: character,
            quote: quote,
        })
    }).then(response => {
        if (response.status !== 204) return response.json();
    }).then(err => err && alert(err.error));
}

let saveQuote = document.querySelectorAll('.saveQuote');
saveQuote.forEach(e => e.addEventListener('click', () => getData(e)));
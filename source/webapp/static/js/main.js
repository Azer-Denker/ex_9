function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

async function makeRequest(url, method='GET', data=undefined) {
    let opts = {method, headers: {}};

    if (!csrfSafeMethod(method))
        opts.headers['X-CSRFToken'] = getCookie('csrftoken');

    if (data) {
        opts.headers['Content-Type'] = 'application/json';
        opts.body = JSON.stringify(data);
    }

    let response = await fetch(url, opts);

    if (response.ok) {  // нормальный ответ
        return await response.json();
    } else {            // ошибка
        let error = new Error(response.statusText);
        error.response = response;
        throw error;
    }
}


async function Add(event) {
    event.preventDefault();
    let to_fav_button = event.target;
    let url = to_fav_button.href;
    try {
        let response = await makeRequest(url, 'GET');
        console.log(response);

    }
    catch (error) {
        console.log(error);
    }

    to_fav_button.classList.add('hide');
    const deleteBtn = to_fav_button.parentElement.getElementsByClassName('remove')[0];
    deleteBtn.classList.remove('hide');
}

async function Remove(event) {
    event.preventDefault();
    let delete_from_fav = event.target;
    let url = delete_from_fav.href;

    try {
        let response = await makeRequest(url , "GET");
        console.log(response);

    }
    catch (error) {
        console.log(error);
    }

    delete_from_fav.classList.add('hide');
    const to_fav_button = delete_from_fav.parentElement.getElementsByClassName('add')[0];
   to_fav_button.classList.remove('hide');
}

window.addEventListener('load', function() {
    const fav_buttons = document.getElementsByClassName('add');
    const delete_from_fav_buttons = document.getElementsByClassName('remove');

    for (let button of fav_buttons) {button.onclick = Add}
    for (let button of delete_from_fav_buttons) {button.onclick = Remove}
});


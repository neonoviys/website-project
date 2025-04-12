const textInput = document.querySelector('input[name=city]');
const dataList = document.querySelector('datalist[id=Cities]');
const cityError = document.getElementById('cityError');

let timeout;

// Запрос на сервер для получения JSON с первыми пяти похожими городами
async function DataBaseRequest() {
    const query = textInput.value;
    if (query != '') {
        const url = 'http://' + location.host + '/api/search_city?city=' + query
        const response = await fetch(url)
        const data = await response.json()
        dataList.innerHTML = '' // Удаляем все предыдущие опции
        // Добавляем новые опции
        data.results.forEach(item => {
            console.log(item.city)
            const option = document.createElement('option');
            option.value = item.city;
            dataList.appendChild(option)
        })
    }
}


function validateCity() {
    const options = Array.from(dataList.querySelectorAll('option')); // Получаем все варианты городов
    const inputValue = textInput.value.trim(); // Получаем введённое значение

    // Проверяем, есть ли введённый город в списке
    let isValid = options.some(option => option.value === inputValue);
    if (inputValue == '') {
        isValid = true;
        // cityError.style.display = 'none'; // Скрываем ошибку
        // console.log("WAK");
    }

    if (!isValid && inputValue !== '') {
        cityError.style.display = 'block'; // Показываем ошибку
    } else {
        cityError.style.display = 'none'; // Скрываем ошибку
    }

    return isValid; // Возвращаем результат проверки
}

// Функция для задержки запроса
function callback(evt) {
    clearTimeout(timeout);
    timeout = setTimeout(function () {
        DataBaseRequest();
    }, 200);
}

// Событие ввода
textInput.addEventListener('input', callback);

// Событие потери фокуса (когда пользователь уходит с поля ввода)
textInput.addEventListener('blur', function () {
    validateCity();
});

// Событие отправки формы (если форма есть)
const ass = document.querySelector('.FormContainer'); // Убедитесь, что у вас есть форма
console.log(ass);
ass.addEventListener('submit', function (event) {
    console.log("cool")
    if (!validateCity()) {
        event.preventDefault(); // Отменяем отправку формы, если город невалиден
        cityError.style.display = 'block'; // Показываем ошибку
    }
});
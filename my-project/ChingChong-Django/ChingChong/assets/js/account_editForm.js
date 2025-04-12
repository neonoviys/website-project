
const settingsButton = document.querySelector('.Settings');
const editModal = document.getElementById('editProfileModal');
const cancelEdit = document.getElementById('cancelEdit');
const saveEdit = document.getElementById('saveEdit');

// Открыть модалку
settingsButton.addEventListener('click', () => {
    editModal.style.display = 'flex';
});

// Закрыть модалку
cancelEdit.addEventListener('click', () => {
    editModal.style.display = 'none';
});

// Сохранение данных (отправка на сервер)
// saveEdit.addEventListener('click', (e) => {
//     // e.preventDefault();
//     // const form = document.getElementById('editProfileForm');
//     // const formData = new FormData(form);

//     // // Пример отправки данных на сервер (заменить URL на свой)
//     // fetch('/api/update_profile', {
//     //     method: 'POST',
//     //     body: JSON.stringify(Object.fromEntries(formData)),
//     //     headers: {
//     //         'Content-Type': 'application/json'
//     //     }
//     // })
//     // .then(response => response.json())
//     // .then(data => {
//     //     if (data.success) {
//     //         alert('Профиль обновлён');
//     //         location.reload(); // Обновить страницу
//     //     } else {
//     //         alert('Ошибка при обновлении профиля');
//     //     }
//     // })
//     // .catch(error => console.error('Ошибка:', error));
// });


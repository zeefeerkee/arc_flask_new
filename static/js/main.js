function sendPostRequest(action) {
    fetch('/update_values', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'move': action,
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        const speed = data.speed; // Получаем скорость из ответа сервера
        const progressBar = document.getElementById('progress-bar');
        progressBar.style.width = speed + '%';
        progressBar.setAttribute('aria-valuenow', speed);

        if (action === '3' || action === '4') {
            document.getElementById('3').classList.toggle('active-btn', action === '3');
            document.getElementById('4').classList.toggle('active-btn', action === '4');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Обработчики событий для кнопок
document.querySelectorAll('.round-btn').forEach(button => {
    button.addEventListener('click', function() {
        const action = this.id;
        sendPostRequest(action);
    });
});
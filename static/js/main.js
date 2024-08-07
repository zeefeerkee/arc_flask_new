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
    .then(response => response.text())
    .then(data => console.log('Success:', data))
    .catch(error => console.error('Error:', error));
}

// Обработчики событий для кнопок
document.querySelectorAll('.round-btn').forEach(button => {
    button.addEventListener('click', function() {
        const action = this.id;
        sendPostRequest(action);
    });
});
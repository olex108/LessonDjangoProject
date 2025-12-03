<script>
  // Получение CSRF токена из cookies
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i=0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrftoken = getCookie('csrftoken');
  const btn = document.getElementById('publish-toggle-btn');

  btn.addEventListener('click', function() {
    if (confirm('Подтвердить изменение публикации?')) {
      fetch('', {  // Текущий URL, можно оставить пустым
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          alert(data.message);

          // Обновляем кнопку и её текст в зависимости от нового статуса
          if (data.new_state === true) {
            btn.className = 'btn btn-danger';
            btn.textContent = 'Отменить публикацию';
          } else {
            btn.className = 'btn btn-primary';
            btn.textContent = 'Опубликовать';
          }
        } else {
          alert('Ошибка: ' + data.message);
        }
      })
      .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка. Попробуйте позже.');
      });
    }
  });
</script>
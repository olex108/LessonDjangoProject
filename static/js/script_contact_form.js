// JavaScript/AJAX код
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('myForm');
    const modalEl = document.getElementById('successModal');
    const modal = new bootstrap.Modal(modalEl);

    form.addEventListener('submit', function(e) {
      e.preventDefault(); // предотвращаем стандартную отправку формы

      const url = form.getAttribute('data-url');
      const formData = new FormData(form);

      fetch(url, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: formData
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Ошибка сети');
        }
        return response.json();
      })
      .then(data => {
        // предполагается, что сервер возвращает JSON с успехом
        if (data.success) {
          // показываем модальное окно
          modal.show();
          // Можно очистить форму, например
          form.reset();
        } else {
          // Обработка ошибок
          alert('Ошибка при отправке формы: ' + data.error);
        }
      })
      .catch(error => {
        alert('Произошла ошибка: ' + error.message);
      });
    });
  });
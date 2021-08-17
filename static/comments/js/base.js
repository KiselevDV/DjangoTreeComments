// Если HTML открыта (jQuery)
$(document).ready(function () {

    // Логика на открытие/закрытие формы ответа к комментарию
    // Тег-ссылка, при нажатии (click) отображает форму-ответ
    // <a href="#" class="reply" data-id="{id}" data-parent={parent_id}>Ответить</a>
    $(".reply").on('click', function () {
        // У данной кнопки (this), получаем атрибут (attr) с именем (data-id)
        var parentId = $(this).attr('data-id');
        // $("#form-" + parentId) = id данной формы, fadeToggle - показать/скрыть содержимое по клику
        $("#form-" + parentId).fadeToggle();
    })

    // Логика на отправку формы ответа к комментарию
    $(".submit-reply").on('click', function (e) {
        e.preventDefault()  // отменить стандартное поведение
        // attr - получить тот или иной атрибут для данной кнопки (this = '.submit-reply')
        var parentId = $(this).attr('data-submit-reply');
        var id = $(this).attr('data-id');
        // Получить текст/данные из тега textarea, по name="comment-text"
        var text = $("#form-" + id).find('textarea[name="comment-text"]').val();

        // csrf token из https://docs.djangoproject.com/en/3.2/ref/csrf/, для отправки ответа post
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        const csrftoken = getCookie('csrftoken');

        // Данные для создания самого комментария (дочернего)
        data = {
            user: '{{ request.user.username }}',
            parentId: parentId,
            text: text,
            id: id,
            csrfmiddlewaretoken: csrftoken
        }

        // AJAX запрос на сервер
        $.ajax({
            method: 'POST',
            data: data,
            url: "{% url 'comment_child_create' %}",
            success: function (data) {
                // При успешной отправке перенаправляем на страницу с постамий
                window.location.replace('/post-comments');
            }
        })
    })
})
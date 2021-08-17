from pprint import pprint

from django.template import Library
from django.utils.html import mark_safe

register = Library()


@register.filter
def comments_filter(comments_list):
    """
    Выстраивание древа всех комментариев в
    виде HTML их рекурсивным вызовом
    """
    # pprint(comments_list)
    res = """
            <ul style="list-style-type:none;>
              <div class="col-md-12 mt-2">
                {}
              </div>
            </ul>    
          """
    i = ''  # пустая строка для формирования ответа виде HTML

    for comment in comments_list:
        i += """
<li>
  <div class="col-md-12 mb-2 mt-2 p-0">
    <small>{author}</small> | опубликовано: {timestamp}
    <hr>
    <p>{text} | id={id}</p>
    <a href="#" class="reply" data-id="{id}" data-parent={parent_id}>Ответить</a>
    <form action="" method="POST" class="comment-form form-group" id="form-{id}" style="display:none;">
      <textarea type="text" class="form-control" name="comment-text"></textarea><br>
      <input type="submit" class="btn btn-primary submit-reply" data-id="{id}" data-submit-reply="{parent_id}" value="Отправить"/>
    </form>  
  </div>
</li>       
""".format(id=comment['id'], author=comment['author'], timestamp=comment['timestamp'],
           text=comment['text'], parent_id=comment['parent_id'])

        # Рекурсивно расширить HTML ответ детьми
        if comment.get('children'):
            i += comments_filter(comment['children'])

    return mark_safe(res.format(i))

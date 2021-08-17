"""
Создание/сбор всех комментариев, в общий список диктов, рекурсивным способом
"""


def get_children(qs_child):
    """Для обработки 'детей' у комментариев"""
    res = []
    for comment in qs_child:
        c = {
            'id': comment.id,
            'text': comment.text,
            'timestamp': comment.timestamp.strftime('%Y-%m-%d %H:%m'),
            'author': comment.user,
            'is_child': comment.is_child,
            'parent_id': comment.get_parent,
        }

        # Заново проверяем на наличие детей и если они есть, сново
        # вызываем данную ф-ию (рекурсивно). exists() - проверяет
        # наличие значений для данного поля
        if comment.comment_children.exists():
            c['children'] = get_children(comment.comment_children.all())
        res.append(c)
    return res


def create_comments_tree(qs):
    """Принимает queryset отдаёт список диктов"""
    res = []
    for comment in qs:
        # Пройтись по всем комментариям в кверисете и переписать их на дикты
        с = {
            'id': comment.id,
            'text': comment.text,
            # timestamp - инстанс DateTime объекта со своими атрибутами
            # strftime - формат вывода значения
            'timestamp': comment.timestamp.strftime('%Y-%m-%d %H:%m'),
            'author': comment.user,
            'is_child': comment.is_child,
            # Используем ф-ию get_parent, для получения пустой строки у
            # комментариев без родителя вместо объекта none
            'parent_id': comment.get_parent,
        }

        # Для комментариев с детьми другая логика - рекурсивный вызов
        # related_name='comment_children', список всех детей комментария
        if comment.comment_children:
            с['children'] = get_children(comment.comment_children.all())

        if not comment.is_child:
            res.append(с)
    return res

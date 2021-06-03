import os
from datetime import datetime, timedelta
from time import sleep

from data import constants


def get_index_comment(last_index: int, comment_list: list) -> int:
    """
    Возвращает индекс для размещения следующего поста.
    :param last_index: последний используемый индекс
    :param comment_list: лист с комментариями, которые нужно отправлять на Реддит
    :return:
    """
    if last_index + 1 > len(comment_list):
        return 0
    return last_index


def get_my_comments() -> list:
    """
    Возвращает мои комментарии.
    :return:
    """
    if not os.path.isfile("data/comment.txt"):
        return []
    with open("data/comment.txt", "r") as f:
        comments_reply = f.read()
        comments_reply = comments_reply.split("\n")
        return list(filter(None, comments_reply))


def get_my_subreddits() -> list:
    """
    Возвращает наблюдаемые ботом сабреддиты.
    :return:
    """
    if not os.path.isfile("data/subreddits.txt"):
        return []
    with open("data/subreddits.txt", "r") as f:
        my_subreddits = f.read()
        my_subreddits = my_subreddits.split("\n")
        return list(filter(None, my_subreddits))


def get_posts_replied_id() -> list:
    """
    Возвращает idшники комментов и постов в которые уже писали.
    :return:
    """
    if not os.path.isfile("data/posts_replied_to.txt"):
        return []
    with open("data/posts_replied_to.txt", "r") as f:
        my_subreddits = f.read()
        my_subreddits = my_subreddits.split("\n")
        return list(filter(None, my_subreddits))


def add_comment_id_in_list(post_id: str):
    """
    Добавляет idшник поста в список.
    :param post_id:
    :return:
    """
    with open("data/posts_replied_to.txt", "a") as f:
        f.write(post_id + "\n")


def wait_time_between_comments():
    """
    Останавливает выполнение функции на время между комментариями, если оно еще не пришло. Обновляет время.
    :return:
    """

    if datetime.now() > constants.LAST_COMMENT_TIME + timedelta(seconds=constants.TIME_RANGE):
        constants.LAST_COMMENT_TIME = datetime.now()
        sleep(constants.TIME_RANGE)
    else:
        sleep_time = constants.LAST_COMMENT_TIME + timedelta(seconds=constants.TIME_RANGE) - datetime.now()
        transform_sleep_time = round(sleep_time.seconds + sleep_time.microseconds * 0.000001, 2)
        sleep(transform_sleep_time)
        constants.LAST_COMMENT_TIME = datetime.now()


def comment_for_post(comments_list: list) -> str:
    """
    Возвращает следующий комментария для публикации.
    :param comments_list: спискок со всеми комментариями.
    :return:
    """
    comment_index = get_index_comment(constants.LAST_COMMENT_INDEX, comments_list)
    constants.LAST_COMMENT_INDEX = comment_index + 1  # Обновляю индекс комментариев
    return comments_list[comment_index]


def write_comment_to_reddit(comments_list: list, current_post):
    """
    Отправляет определенный комментарий под посты и обновляет Idшники постов в списке
    :param comments_list: список с комментариями
    :param current_post: текущий пост
    :return:
    """
    current_post.reply(comment_for_post(comments_list))  # Отправляю сообщение
    add_comment_id_in_list(current_post.id)  # Добавляю idшник в список обработанных постов
    wait_time_between_comments()


def clean_post_replied(count_post: int):
    post_id_list = get_posts_replied_id()
    if len(post_id_list) > count_post:
        with open("data/posts_replied_to.txt", "w") as f:
            for post_id in post_id_list[int(len(post_id_list) / 1.3):]:
                f.write(post_id + "\n")

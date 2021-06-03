import praw
import prawcore
from datetime import datetime, timedelta
from time import sleep

from data import constants
from utils import get_my_subreddits, get_posts_replied_id, get_my_comments, write_comment_to_reddit, clean_post_replied

if __name__ == '__main__':
    start = input('Включить режим "Ответ под комментариями"? Y / N: ')
    if start in ['Y', 'y', 'у', 'У']:
        constants.STRATEGY = "COMM"
        print('---- Запущен режим "Ответ под комментариями" ----')
    else:
        constants.STRATEGY = "POST"
        print('---- Запущен режим "Ответ под постами" ----')

    reddit = praw.Reddit(
        client_id=constants.client_id,
        client_secret=constants.client_secret,
        password=constants.password,
        user_agent=constants.user_agent,
        username=constants.username,
    )

    clean_post_replied(10000)  # Чистит список, если количество больше заданного числа, чтобы не переполнялась память
    MAIN_TIME = datetime.now() + timedelta(minutes=constants.DOWNTIME)
    constants.LAST_COMMENT_TIME = datetime.now() - timedelta(seconds=constants.TIME_RANGE)

    print("---- Бот работает ----")
    while True:
        while MAIN_TIME > datetime.now():
            subreddits = [reddit.subreddit(subreddit_name) for subreddit_name in get_my_subreddits()]
            for subreddit in subreddits:

                try:
                    for post in subreddit.new(limit=constants.COUNT_NEW_POST):

                        # Данный блок отправляет сообщения только под постами
                        if constants.STRATEGY == 'POST':
                            if get_posts_replied_id().count(post.id) + 1 > constants.COUNT_REPLIED_COMMENTS:
                                continue
                            write_comment_to_reddit(get_my_comments(), post)

                        # Данный блок отправляет сообщения под комментарии под постами
                        elif constants.STRATEGY == 'COMM':
                            for comment in post.comments[constants.COUNT_NEW_COMMENTS::-1]:
                                if get_posts_replied_id().count(comment.id) + 1 > constants.COUNT_REPLIED_COMMENTS:
                                    continue
                                try:
                                    write_comment_to_reddit(get_my_comments(), comment)
                                except praw.exceptions.RedditAPIException:
                                    continue

                except prawcore.exceptions.NotFound:
                    continue

            # Выжидаю время простоя проверки ботом новых сообщений
            sleep(constants.CHECK_TIMEOUT)
        else:
            print(f"---- Бот уходит в сон на {constants.DOWNTIME * 60} sec. ----")
            sleep(constants.DOWNTIME * 60)
            MAIN_TIME = datetime.now() + timedelta(minutes=constants.DOWNTIME)

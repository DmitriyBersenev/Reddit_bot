oauth_url = 'https://oauth.reddit.com'
reddit_url = 'https://www.reddit.com'
short_url = 'https://redd.it'

client_id = 'your_client_id'
client_secret = 'your_client_secret'

password = 'your_password'
username = 'your_username'
user_agent = 'PyEng Bot 0.1'

DOWNTIME = 30                           # Время простоя в минутах (min)
STRATEGY = 'COMM'                       # Выбираем стратегию POST - отвечать под постами, COMM - под комментариями
COUNT_REPLIED_COMMENTS = 2              # Максимально количество ответов под одним комментом, постом
TIME_RANGE = 7                          # Разница между отправляемыми сообщениями в секундах (sec)
CHECK_TIMEOUT = 1                       # Как часто проверять Реддит на появление новых постов (sec)
COUNT_NEW_POST = 5                      # Количество новых постов, которые бот будет постоянно просматривать
COUNT_NEW_COMMENTS = 10                 # Количество новых комментов, которые бот будет постоянно просматривать

LAST_COMMENT_INDEX = 0                  # Индекс последнего коммента. Нужен для рулетки комментариев
LAST_COMMENT_TIME = None                # Время последнего комментария

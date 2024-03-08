from typing import Any
from config_data.config import DATABASE_URL_NOT_ASYNC
import psycopg2


def get_all_number_chat_id_and_time_traking_habit():
    result_all:  list[tuple[Any, ...]] = []
    try:
        # пытаемся подключиться к базе данных
        conn = psycopg2.connect(f'{DATABASE_URL_NOT_ASYNC}')
    except Exception as exp:
        # в случае сбоя подключения будет выведено сообщение  в STDOUT
        print(f'Can`t establish connection to database, error {exp}')
    else:
        cursor = conn.cursor()
        cursor.execute("""SELECT
            h.id,
            u.telegram_id AS telegram_id,
            h.name_habit AS name,
            hi.count AS count_tracking,
            hi.alert_time AS data,
            u.is_active AS is_active
        FROM
            users u
        JOIN
            habits h ON u.id = h.user_id
        JOIN
            habittrackings hi ON h.id = hi.habit_id
        ORDER BY
            u.telegram_id, hi.alert_time""")
        result_all = cursor.fetchall()
        cursor.close()
        conn.close()
    return result_all

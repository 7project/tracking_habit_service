from typing import Any
from config_data.config import DATABASE_URL_NOT_ASYNC
import psycopg2


def get_all_number_chat_id_and_time_tracking_habit():
    result_all:  list[tuple[Any, ...]] = []
    try:
        conn = psycopg2.connect(f'{DATABASE_URL_NOT_ASYNC}')
    except Exception as exp:
        print(f'Can`t establish connection to database, error {exp}')
    else:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT
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
            u.telegram_id, hi.alert_time
            """)
        result_all = cursor.fetchall()
        cursor.close()
        conn.close()
    return result_all


def update_tracking_habit_count_add_one(habit_id):
    try:
        conn = psycopg2.connect(f'{DATABASE_URL_NOT_ASYNC}')
        cursor = conn.cursor()
        cursor.execute("""
                    UPDATE
                        habittrackings
                    SET
                        count = count + 1 
                    WHERE
                        habit_id = {habit_id}
                    """.format(habit_id=habit_id))
        conn.commit()
    except Exception as exp:
        conn.rollback()
        print(f'update_tracking_habit_count_add_one Can`t establish connection to database, error {exp}')
    finally:
        cursor.close()
        conn.close()



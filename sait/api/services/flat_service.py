from api.database import get_connection

def get_flats(id_complex):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = f"""
            SELECT * FROM main_flats
            WHERE id_complex = {id_complex}
            """
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

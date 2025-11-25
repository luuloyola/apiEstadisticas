import os
import psycopg2
from Crypto.Cipher import AES
from dotenv import load_dotenv
from classes.message import Message
from classes.statistics import Statistics

load_dotenv()

conn_string = os.getenv("DATABASE_URL")
encryption_key_hex = os.getenv("ENCRYPTION_KEY")

if not conn_string or not encryption_key_hex:
    raise ValueError("DATABASE_URL y ENCRYPTION_KEY deben estar definidos en .env")

try:
    ENCRYPTION_KEY = bytes.fromhex(encryption_key_hex)
    if len(ENCRYPTION_KEY) != 32:
        raise ValueError("ENCRYPTION_KEY debe tener 32 bytes (64 caracteres hex)")
except ValueError as e:
    raise ValueError(f"ENCRYPTION_KEY inválida: {e}")


def decrypt_message(content: str) -> str:
    try:
        parts = content.split(":")
        if len(parts) != 3:
            raise ValueError("Formato de mensaje encriptado inválido. Esperado: iv:ciphertext:auth_tag")

        iv = bytes.fromhex(parts[0])
        ciphertext = bytes.fromhex(parts[1])
        auth_tag = bytes.fromhex(parts[2])

        cipher = AES.new(ENCRYPTION_KEY, AES.MODE_GCM, nonce=iv)
        plaintext = cipher.decrypt_and_verify(ciphertext, auth_tag)

        return plaintext.decode("utf-8")
    except ValueError as e:
        print(f"Error de formato en mensaje encriptado: {e}")
        raise
    except Exception as e:
        print(f"Error desencriptando mensaje: {e}")
        raise


def get_chat_session():
    try:
        with psycopg2.connect(conn_string) as conn:
            print("Conexión a BD establecida")
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT m."id", m."chatSessionId", cs."chatGroupId", m."content", m."createdAt", m."sender"
                    FROM "Message" AS m
                    JOIN "ChatSession" AS cs ON m."chatSessionId" = cs."id"
                    WHERE (cs."sessionEndedAt" IS NOT NULL OR cs."updatedAt" + INTERVAL '4 hours' < NOW()) AND cs."analyzed" = false
                    ORDER BY m."createdAt";
                """)
                rows = cur.fetchall()

                if not rows:
                    print("No hay sesiones pendientes de análisis")
                    return None

                print(len(rows))
                list_session = {}
                for row in rows:
                    chat_session_id = row[1]
                    if chat_session_id not in list_session:
                        list_session[chat_session_id] = []

                    decrypted_content = decrypt_message(row[3])
                    row_list = list(row)
                    row_list[3] = decrypted_content

                    new_message = Message(row_list)
                    print(new_message)
                    list_session[chat_session_id].append(new_message)

                return list_session
    except psycopg2.Error as e:
        print(f"Error de base de datos: {e}")
        raise
    except Exception as e:
        print(f"Error inesperado: {e}")
        raise


def transaction_stats(stat: Statistics, chat: list[Message]) -> None:
    conn = None
    try:
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()

        insert_values = (
            stat.get_summary(),
            stat.get_chat_id(),
            stat.get_amount_messages(),
            stat.get_min_words_per_message(),
            stat.get_max_words_per_message(),
            stat.get_hate_speech(),
            stat.get_ironic(),
            stat.get_change_theme(),
            stat.get_bet_type(),
            stat.get_positive_percentage(),
            stat.get_negative_percentage(),
            stat.get_neutral_percentage(),
            stat.get_chat_group_id(),
            stat.get_most_frequent_sentiment()
        )

        cur.execute("""
            INSERT INTO "statistics" (
                summary,
                chat_id,
                amount_messages,
                min_words_per_message,
                max_words_per_message,
                hate_speech,
                ironic,
                change_theme,
                bet_type,
                positive_percentage,
                negative_percentage,
                neutral_percentage,
                chat_group_id,
                most_frequent_sentiment
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, insert_values)

        for message in chat:
            cur.execute("""
                UPDATE "Message"
                SET "sentimentLabel" = %s
                WHERE id = %s
            """, (message.get_sentiment(), message.get_id()))

        cur.execute("""
            UPDATE "ChatSession"
            SET analyzed = TRUE
            WHERE id = %s
        """, (stat.get_chat_id(),))

        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
            print(f"Error en transacción - ROLLBACK ejecutado: {e}")
        raise
    except Exception as e:
        if conn:
            conn.rollback()
            print(f"Error inesperado - ROLLBACK ejecutado: {e}")
        raise
    finally:
        if conn:
            conn.close()
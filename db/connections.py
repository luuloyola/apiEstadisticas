import os
import psycopg2
from Crypto.Cipher import AES
from dotenv import load_dotenv
from classes.message import Message
from classes.statistics import Statistics

load_dotenv()
conn_string = os.getenv("DATABASE_URL")
encription = os.getenv("ENCRYPTION_KEY")

def decrypt_message(content):
    try:
        # Separar iv, encryptedData, authTag
        parts = content.split(":")
        if len(parts) != 3:
            raise ValueError("Formato de mensaje encriptado inválido")

        iv = bytes.fromhex(parts[0])
        ciphertext = bytes.fromhex(parts[1])
        auth_tag = bytes.fromhex(parts[2])

        # Crear el decipher AES-256-GCM
        cipher = AES.new(encription, AES.MODE_GCM, nonce=iv)
        plaintext = cipher.decrypt_and_verify(ciphertext, auth_tag)

        return plaintext.decode("utf-8")
    except Exception as e:
        print(e)
        return e


def get_chat_session():
    try:
        with psycopg2.connect(conn_string) as conn:
            print("Connection established")
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT m.id, m.chatSessionId, m.content, m.createdAt
                    FROM Message AS m
                    JOIN ChatSession AS cs ON m.chatSessionId = cs.id
                    WHERE cs.finished IS NOT NULL AND cs.analyzed = false
                    ORDER BY m.createdAt;
                """)
                rows = cur.fetchall()
                if len(rows) == 0:
                    return None

                list_session = dict()
                for row in rows:
                    if row[1] not in list_session:
                        list_session[row[1]] = []
                    row[2] = decrypt_message(row[2])
                    new_message = Message(row)
                    list_session[row[1]].append(new_message)
                return list_session
    except Exception as e:
        print("Connection failed.")
        print(e)
        return e


def transaction_stats(stat: Statistics, chat: [Message]):
    try:
        with psycopg2.connect() as conn:
            with conn.cursor() as cur:
                insert_values = (
                    stat.get_summary(),
                    stat.get_chat_id(),
                    stat.get_amount_messages(),
                    stat.get_min_words_per_message(),
                    stat.get_max_words_per_message(),
                    stat.get_hate_speech_percentage(),
                    stat.get_ironic_percentage(),
                    stat.get_change_theme(),
                    stat.get_bet_type()
                )

                cur.execute("""
                    INSERT INTO Statistic (
                        summary,
                        chat_id,
                        amount_messages,
                        min_words_per_message,
                        max_words_per_message,
                        hate_speech_percentage,
                        ironic_percentage,
                        change_theme,
                        bet_type
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, insert_values)

                for message in chat:
                    cur.execute("""
                    UPDATE Message
                    SET sentiment = %s
                    WHERE id = %s""", (message.get_sentiment(), message.get_id()))

                cur.execute("""
                    UPDATE ChatSession
                    SET analyzed = TRUE
                    WHERE id = %s
                """, stat[1])
    except Exception as e:
        print("Connection failed.")
        print(e)
        return e
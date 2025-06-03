import sqlite3
import datetime

# Caminho do banco
DB_PATH = './banco/projeto_bradesco.db'

def conectar_banco():
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON")
    return con

def verificar_email(remetente: str):
    con = conectar_banco()
    cursor = con.cursor()

    # Verifica se o e-mail está na tabela
    cursor.execute("SELECT * FROM email WHERE EmaCom = ?", (remetente,))
    resultado = cursor.fetchone()

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if resultado:
        print(f"[OK] Email autorizado: {remetente}")
        cursor.execute("""
            INSERT INTO LogHis (DatLog, CodStatus, Response, ObsLog)
            VALUES (?, ?, ?, ?)
        """, (now, 200, "Autorizado", f"E-mail {remetente} reconhecido."))
    else:
        print(f"[ALERTA] Email suspeito: {remetente}")
        cursor.execute("""
            INSERT INTO LogHis (DatLog, CodStatus, Response, ObsLog)
            VALUES (?, ?, ?, ?)
        """, (now, 403, None, f"E-mail {remetente} não reconhecido."))

    con.commit()
    cursor.close()
    con.close()

# Simulando recebimento de e-mails
emails_recebidos = [
    "contato@empresa1.com",
    "fraude@naoexiste.com"
]

for email in emails_recebidos:
    verificar_email(email)

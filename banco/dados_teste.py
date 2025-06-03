import sqlite3
import datetime

# Abre conexão com o banco existente
con = sqlite3.connect("./banco/projeto_bradesco.db")
con.execute("PRAGMA foreign_keys = ON")
cursor = con.cursor()

# Inserir países
cursor.execute("INSERT INTO Pais (NomPais) VALUES (?)", ("Brasil",))
cursor.execute("INSERT INTO Pais (NomPais) VALUES (?)", ("Argentina",))
cursor.execute("INSERT INTO Pais (NomPais) VALUES (?)", ("Coreia do Sul",))


# Buscar CodPais
cursor.execute("SELECT CodPais FROM Pais WHERE NomPais = ?", ("Brasil",))
codpais_brasil = cursor.fetchone()[0]

cursor.execute("SELECT CodPais FROM Pais WHERE NomPais = ?", ("Argentina",))
codpais_argentina = cursor.fetchone()[0]

# Inserir cidades
cursor.execute("INSERT INTO Cidade (NomCid, CodPais) VALUES (?, ?)", ("São Paulo", codpais_brasil))
cursor.execute("INSERT INTO Cidade (NomCid, CodPais) VALUES (?, ?)", ("Buenos Aires", codpais_argentina))

# Buscar CodCid
cursor.execute("SELECT CodCid FROM Cidade WHERE NomCid = ?", ("São Paulo",))
codcid_sp = cursor.fetchone()[0]

cursor.execute("SELECT CodCid FROM Cidade WHERE NomCid = ?", ("Buenos Aires",))
codcid_ba = cursor.fetchone()[0]

# Inserir empresas
cursor.execute("""
    INSERT INTO Empresa (NumCnpj, EndRua, EndNum, EndCpl, NomContato, TelContato, CodCid) 
    VALUES (?, ?, ?, ?, ?, ?, ?)""", 
    ("12.345.678/0001-90", "Rua A", "123", "Sala 1", "Carlos Silva", "(11) 91234-5678", codcid_sp))

cursor.execute("""
    INSERT INTO Empresa (NumCnpj, EndRua, EndNum, EndCpl, NomContato, TelContato, CodCid) 
    VALUES (?, ?, ?, ?, ?, ?, ?)""", 
    ("98.765.432/0001-10", "Avenida B", "456", None, "Ana Souza", "(21) 99876-5432", codcid_ba))

# Buscar CodEmp
cursor.execute("SELECT CodEmp FROM Empresa WHERE NumCnpj = ?", ("12.345.678/0001-90",))
codemp_1 = cursor.fetchone()[0]

cursor.execute("SELECT CodEmp FROM Empresa WHERE NumCnpj = ?", ("98.765.432/0001-10",))
codemp_2 = cursor.fetchone()[0]

# Inserir emails
cursor.execute("INSERT INTO Email (EmaCom, CodEmp) VALUES (?, ?)", ("contato@empresa1.com", codemp_1))
cursor.execute("INSERT INTO Email (EmaCom, CodEmp) VALUES (?, ?)", ("suporte@empresa2.com", codemp_2))

# Inserir logs
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cursor.execute("""
    INSERT INTO LogHis (DatLog, CodStatus, Response, ObsLog)
    VALUES (?, ?, ?, ?)""", 
    (now, 200, "Resposta OK", "Teste de log OK"))

cursor.execute("""
    INSERT INTO LogHis (DatLog, CodStatus, Response, ObsLog)
    VALUES (?, ?, ?, ?)""", 
    (now, 400, "Erro na requisição", "Teste de log erro"))

# Salvar as alterações
con.commit()

cursor.close()
con.close()

print("Dados inseridos com sucesso!")

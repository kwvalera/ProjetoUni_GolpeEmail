import sqlite3

# Cria ou abre o banco de dados SQLite
con = sqlite3.connect("./banco/projeto_bradesco.db")

# Ativa suporte a chaves estrangeiras (muito importante no SQLite!)
con.execute("PRAGMA foreign_keys = ON")

# Cria o cursor para executar comandos SQL
cursor = con.cursor()


# Criar tabelas países
cursor.execute("""
CREATE TABLE IF NOT EXISTS pais (
    CodPais INTEGER PRIMARY KEY AUTOINCREMENT,
    NomPais VARCHAR(100) UNIQUE NOT NULL
)
""")

# Criar tabelas cidades
cursor.execute("""
CREATE TABLE IF NOT EXISTS cidade (
    CodCid INTEGER PRIMARY KEY AUTOINCREMENT,
    NomCid VARCHAR(100) UNIQUE NOT NULL,
    CodPais INTEGER NOT NULL,
    FOREIGN KEY (CodPais) REFERENCES pais(CodPais)
)
""")

#Criar tabela empresas
cursor.execute("""
CREATE TABLE IF NOT EXISTS empresa (
    CodEmp INTEGER PRIMARY KEY AUTOINCREMENT,
    NumCnpj VARCHAR(18) UNIQUE NOT NULL,
    EndRua TEXT NOT NULL,
    EndNum TEXT NOT NULL,
    EndCpl TEXT,
    NomContato VARCHAR(100),
    TelContato VARCHAR(20),
    CodCid INTEGER NOT NULL,
    FOREIGN KEY (CodCid) REFERENCES cidade(CodCid)
)
""")

# Criar tabelas emails
cursor.execute("""
CREATE TABLE IF NOT EXISTS email (
    CodEmail INTEGER PRIMARY KEY AUTOINCREMENT,
    EmaCom VARCHAR(254) NOT NULL,
    CodEmp INTEGER NOT NULL,
    FOREIGN KEY (CodEmp) REFERENCES empresa(CodEmp)    
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS log_his (
    CodLog INTEGER PRIMARY KEY AUTOINCREMENT,
    DatLog DATETIME NOT NULL,
    CodStatus INTEGER NOT NULL,
    Response TEXT,
    ObsLog TEXT
)
""")


print("Banco e tabela criados com sucesso!")

con.commit()
cursor.close()
con.close()


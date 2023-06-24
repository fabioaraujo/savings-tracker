import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv

load_dotenv()

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host=os.getenv("HOST"), user=os.getenv("USER_DB"), password=os.getenv("PWD_DB")
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Existe algo errado no nome de usuário ou senha")
    print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `savings_tracker`;")

cursor.execute("CREATE DATABASE `savings_tracker`;")

cursor.execute("USE `savings_tracker`;")

# criando tabelas
TABLES = {}
TABLES[
    "sonho"
] = """
      CREATE TABLE `sonho` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `valor_inicial` double NOT NULL,
      `valor_final` double NOT NULL,
      `data_inicial` datetime NOT NULL,
      `data_final` datetime NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;"""

TABLES[
    "sonho_acompanhamento"
] = """
      CREATE TABLE `sonho_acompanhamento` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `sonho_id` int(11) NOT NULL,
      `data`datetime NOT NULL,
      `valor` double NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;"""

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print("Criando tabela {}:".format(tabela_nome), end=" ")
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Já existe")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
conn.close()

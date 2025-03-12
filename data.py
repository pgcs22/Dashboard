import datetime as dt
import pymysql
import pandas as pd

# Conectar ao MySQL
def conectar_mysql():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Lir@30112024',
        database='Investimentos'
    )


# Função para executar consultas SQL e retornar um DataFrame
def query_to_df(query, conexao):
    with conexao.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return pd.DataFrame(result, columns=columns)

def carregar_dados_filtrados(investimento):
    conexao = conectar_mysql()
    try:
        query_filtrada = f"""
        SELECT Data, Rendimento, Retirada, Depósito, Saldo
        FROM dados_de_investimentos
        WHERE Investimento = '{investimento}'
        ORDER BY Data;
        """
        dataframe = query_to_df(query_filtrada, conexao)
        dataframe['Movimentação'] = dataframe['Depósito'] - dataframe['Retirada']
        return dataframe
    finally:
        conexao.close()

conexao = conectar_mysql()

try:
    # Consultas SQL para carregar os dados
    df_1 = query_to_df("SELECT * FROM dados_de_investimentos", conexao)  # Substitua pelo nome da tabela
    df_2 = query_to_df("SELECT * FROM Historico", conexao)  # Substitua pelo nome da tabela

    # Manipulação dos dados (se necessário)
    df_1['Movimentação'] = df_1['Depósito'] - df_1['Retirada']

    # Consulta para obter a última data da tabela de investimentos
    query = "SELECT MAX(Data) AS ultima_data FROM dados_de_investimentos;"
    with conexao.cursor() as cursor:
        cursor.execute(query)
        resultado = cursor.fetchone()  # fetchone() retorna uma tupla com o resultado
        if resultado:
            ultima_data = resultado[0]  # Acessar o primeiro (e único) elemento da tupla
            print(f"A última data na coluna é: {ultima_data}")
        else:
            raise ValueError("Nenhum dado encontrado na tabela.")

    # Calcular a data de um ano atrás
    ano_anterior = ultima_data - dt.timedelta(days=365)

    # Consulta para obter os dados dos últimos 12 meses
    query = f"""
    SELECT *
    FROM dados_de_investimentos
    WHERE Data >= '{ano_anterior.strftime('%Y-%m-%d')}'
    ORDER BY Investimento, Data
    """
    query_2 = f"""
    SELECT Saldo
    FROM Historico
    ORDER BY id DESC
    LIMIT 1;
    """

    df_3 = query_to_df(query, conexao)

    Saldo = query_to_df(query_2, conexao)

    # Calcular o Acumulado 12 Meses
    df_3['Acumulado 12 Meses'] = df_3.groupby('Investimento')['Rendimento']\
        .rolling(window=12, min_periods=1).apply(lambda x: (1 + x).prod() - 1, raw=True)\
        .reset_index(level=0, drop=True)

    # Aplicar o deslocamento (shift)
    df_3['Acumulado 12 Meses'] = df_3.groupby('Investimento')['Acumulado 12 Meses'].shift(1)

    # Exibir o DataFrame resultante
    print(df_3.head())

finally:
    # Fechar a conexão com o banco de dados
    conexao.close()


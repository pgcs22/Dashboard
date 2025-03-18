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
        SELECT Data, Rendimento, Retirada, Depósito, Saldo,
        (Depósito - Retirada) as Movimentação
        FROM dados_de_investimentos
        WHERE Investimento = '{investimento}'
        ORDER BY Data;
        """
        dataframe = query_to_df(query_filtrada, conexao)

        return dataframe
    finally:
        conexao.close()

conexao = conectar_mysql()

try:
    # Consultas SQL para carregar os dados
    df_Dados = query_to_df("SELECT * FROM dados_de_investimentos", conexao)  # Substitua pelo nome da tabela
    df_Historico = query_to_df("SELECT * FROM Historico", conexao)  # Substitua pelo nome da tabela

    # Manipulação dos dados (se necessário)
    df_Dados['Movimentação'] = df_Dados['Depósito'] - df_Dados['Retirada']


    # Consulta para obter a última data da tabela de investimentos
    query_ultima_data = "SELECT MAX(Data) AS ultima_data FROM dados_de_investimentos;"
    with conexao.cursor() as cursor:
        cursor.execute(query_ultima_data)
        resultado = cursor.fetchone()  # fetchone() retorna uma tupla com o resultado
        if resultado:
            ultima_data = resultado[0]  # Acessar o primeiro (e único) elemento da tupla
        else:
            raise ValueError("Nenhum dado encontrado na tabela.")

    # Calcular a data de um ano atrás
    ano_anterior = ultima_data - dt.timedelta(days=365)
    ano_atual = ultima_data.year
    ultimo_aporte = df_Dados[df_Dados['Data']==ultima_data]
    ultimo_aporte = ultimo_aporte['Movimentação'].sum()

    # Consulta para obter os dados dos últimos 12 meses
    query_1 = f"""
    SELECT *
    FROM dados_de_investimentos
    WHERE Data >= '{ano_anterior.strftime('%Y-%m-%d')}'
    ORDER BY Investimento, Data
    """
    query_2 = f"""
    SELECT *
    FROM Historico
    ORDER BY id DESC
    LIMIT 1;
    """

    query_3 = f"""
    SELECT EXP(SUM(LOG(Rendimento + 1))) AS multiplicacao
    FROM Historico
    WHERE YEAR(Data) = {ano_atual};
    """

    query_4 = f"""
    SELECT EXP(SUM(LOG(Rendimento + 1))) AS multiplicacao
    FROM (
        SELECT Rendimento
        FROM Historico
        ORDER BY Data DESC
        LIMIT 12
    ) AS ultimos_12;
    """

    query_5 = f"""
        SELECT EXP(SUM(LOG(Inflação + 1))) AS multiplicacao
        FROM (
            SELECT Inflação
            FROM Historico
            ORDER BY Data DESC
            LIMIT 12
        ) AS ultimos_12;
        """

    query_6 = f"""
        SELECT EXP(SUM(LOG(Inflação + 1))) AS multiplicacao
        FROM Historico
        WHERE YEAR(Data) = {ano_atual};
        """

    query_7 = f"""
        SELECT
        YEAR(Data) AS Ano,
        MONTH(Data) AS Mes,
        SUM(Depósito - Retirada) AS Movimentacao_Total
        FROM dados_de_investimentos
        WHERE YEAR(Data) = {ano_atual}
        GROUP BY YEAR(Data), MONTH(Data)
        ORDER BY Ano, Mes; 
        """
    query_8 = f"""
        SELECT SUM(Ganhos) AS Ganho_total
        FROM dados_de_investimentos
        WHERE YEAR(Data) = {ano_atual}
        """

    query_9 = f"""
        SELECT
        risco as Risco,
        SUM(saldo) AS Saldo,
        SUM(Depósito - Retirada) AS Investido,
        SUM(Ganhos) AS Ganhos,
        SUM(Ganhos) / SUM(saldo) AS Rendimento -- Cálculo do rendimento
        FROM dados_de_investimentos
        WHERE Data = '{ultima_data}'
        GROUP BY risco;
            """

    query_10 = f"""
            WITH SaldoUltimoMes AS (
            SELECT
            risco,
            SUM(saldo) AS SaldoUltimoMes
            FROM dados_de_investimentos
            WHERE Data = '{ultima_data}'
            GROUP BY risco
            )
            SELECT
            d.risco AS Risco,
            s.SaldoUltimoMes AS Saldo,
            SUM(d.Depósito - d.Retirada) AS Investido,
            SUM(d.Ganhos) AS Ganhos,
            SUM(d.Ganhos) / s.SaldoUltimoMes AS Rendimento -- Cálculo do rendimento usando o saldo do último mês
            FROM dados_de_investimentos d
            JOIN SaldoUltimoMes s ON d.risco = s.risco
            WHERE YEAR(d.Data) = '{ano_atual}'
            GROUP BY d.risco, s.SaldoUltimoMes;
                """

    df_3 = query_to_df(query_1, conexao)
    Saldo = query_to_df(query_2, conexao)
    rendimento_ano = query_to_df(query_3, conexao)
    rendimento_12_meses = query_to_df(query_4, conexao)
    inflacao_12_meses= query_to_df(query_5, conexao)
    inflacao_ano = query_to_df(query_6, conexao)
    media_aporte = query_to_df(query_7, conexao)
    ganho_ano = query_to_df(query_8, conexao)
    tabela_de_riscos = query_to_df(query_9, conexao)
    tabela_de_riscos_ano = query_to_df(query_10, conexao)

    # Calcular o Acumulado 12 Meses
    df_3['Acumulado 12 Meses'] = df_3.groupby('Investimento')['Rendimento']\
        .rolling(window=12, min_periods=1).apply(lambda x: (1 + x).prod() - 1, raw=True)\
        .reset_index(level=0, drop=True)

    # Aplicar o deslocamento (shift)
    df_3['Acumulado 12 Meses'] = df_3.groupby('Investimento')['Acumulado 12 Meses'].shift(1)




finally:
    # Fechar a conexão com o banco de dados
    conexao.close()


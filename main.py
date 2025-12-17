import streamlit as st
import pandas as pd

def calc_general_status(df:pd.DataFrame):
    ## Dados Gerais
    df_data = df.groupby(by="Data")[['Valor']].sum()
    
    ## Shift desloca a linha
    df_data['lag_1'] = df_data['Valor'].shift(1)

    ##Calculo da diferença mensal
    df_data['Diferença Mensal Abs.'] = df_data['Valor'] - df_data['lag_1']
    
    ## Calculo média de meses
    df_data['Média 6M Diferença Mensal Abs.'] = df_data['Diferença Mensal Abs.'].rolling(6).mean() 
    df_data['Média 12M Diferença Mensal Abs.'] = df_data['Diferença Mensal Abs.'].rolling(12).mean() 
    df_data['Média 24M Diferença Mensal Abs.'] = df_data['Diferença Mensal Abs.'].rolling(24).mean() 
    df_data['Diferença Mensal Rel.'] = df_data['Valor'] / df_data['lag_1'] - 1
    df_data['Evolução 6M Total'] = df_data['Valor'].rolling(6).apply(lambda x: x[-1] - x[0])
    df_data['Evolução 12M Total'] = df_data['Valor'].rolling(12).apply(lambda x: x[-1] - x[0]) 
    df_data['Evolução 24M Total'] = df_data['Valor'].rolling(24).apply(lambda x: x[-1] - x[0]) 
    df_data['Evolução 6M Relativa'] = df_data['Valor'].rolling(6).apply(lambda x: x[-1] / x[0] - 1)
    df_data['Evolução 12M Relativa'] = df_data['Valor'].rolling(12).apply(lambda x: x[-1] / x[0] - 1) 
    df_data['Evolução 24M Relativa'] = df_data['Valor'].rolling(24).apply(lambda x: x[-1] / x[0] - 1) 
    
    df_data = df_data.drop('lag_1', axis=1)

    return df_data

st.set_page_config(page_title="Finanças", page_icon=":moneybag:")


st.markdown('''
            # Boas Vindas!
            
            ## Nosso APP Financeiro!

            Espero que você curta a expericiência da nossa solução para organização financeira.
''')
# Widget de upload de dados
file_upload = st.file_uploader(label="Faça upload dos dados aqui", type=['csv'])

# Verifica se foi feito o upload do arquivo
if file_upload:

    # Leitura dos dados
    df = pd.read_csv(file_upload)
    #formatando a data
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y').dt.date


    # Exibição dos dados do App
    exp1 = st.expander('Dados Brutos')
     
    columns_fmt = {'Valor' : st.column_config.NumberColumn(label="valor", format="R$ %f")}
    exp1.dataframe(df, hide_index=True, column_config=columns_fmt)
    
    # Visão Instituição
    exp2 = st.expander('Instituições')
    df_instituicao = df.pivot_table(index='Data', columns='Instituição', values='Valor')
    # Criando abas
    tab_data, tab_history, tab_share = exp2.tabs(['Dados', 'Histórico', 'Distribuição'])
    with tab_data:
        st.dataframe(df_instituicao)
    with tab_history:
        st.line_chart(df_instituicao)

    with tab_share:

        ## exibindo somente datas existentes
        date = st.selectbox('Filtro data', options=df_instituicao.index)
        
        # Grafico de distruibuição
        st.bar_chart(df_instituicao.loc[date])



    exp3 = st.expander('Estatísticas Gerais')
    df_status = calc_general_status(df)

    columns_config = {
        'Valor':st.column_config.NumberColumn('Valor', format='R$ %.2f'),
        'Diferença Mensal Abs.':st.column_config.NumberColumn('Diferença Mensal Abs.', format='R$ %.2f'),
        'Média 6M Diferença Mensal Abs.':st.column_config.NumberColumn('Média 6M Diferença Mensal Abs.', format='R$ %.2f'),
        'Média 12M Diferença Mensal Abs.':st.column_config.NumberColumn('Média 12M Diferença Mensal Abs.', format='R$ %.2f'),
        'Média 24M Diferença Mensal Abs.':st.column_config.NumberColumn('Média 24M Diferença Mensal Abs.', format='R$ %.2f'),
        'Evolução 6M Total':st.column_config.NumberColumn('Evolução 6M Total', format='R$ %.2f'),
        'Evolução 12M Total':st.column_config.NumberColumn('Evolução 12M Total', format='R$ %.2f'),
        'Evolução 24M Total':st.column_config.NumberColumn('Evolução 24M Total', format='R$ %.2f'),
        'Diferença Mensal Rel.': st.column_config.NumberColumn('Diferença Mensal Rel.', format='percent'),
        'Evolução 6M Relativa': st.column_config.NumberColumn('Evolução 6M Relativa', format='percent'),
        'Evolução 12M Relativa': st.column_config.NumberColumn('Evolução 12M Relativa', format='percent'),
        'Evolução 24M Relativa': st.column_config.NumberColumn('Evolução 24M Relativa', format='percent'),
    }

    exp3.dataframe(df_status, column_config=columns_config)
    abs_cols = [
        'Diferença Mensal Abs.',
        'Média 6M Diferença Mensal Abs.',
        'Média 12M Diferença Mensal Abs.',
        'Média 24M Diferença Mensal Abs.'
    ]
    exp3.line_chart(df_status[abs_cols])
        
        
        ## Entrada com calendario
        # date = st.date_input(label='Data para Distribuição', 
        #               min_value=df_instituicao.index.min(), 
        #               max_value=df_instituicao.index.max())
        # # Ultima data de dados

        # if date not in df_instituicao.index:
        #     st.warning('Entre com uma data valida')
        # else:
        #     st.bar_chart(df_instituicao.loc[date])
        # last_dt = df_instituicao.sort_index().iloc[date]
        # st.bar_chart(last_dt)


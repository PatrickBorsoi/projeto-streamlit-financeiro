import streamlit as st
import pandas as pd
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
        st.bar_chart(df_instituicao.loc[date])
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


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
    exp2.dataframe(df_instituicao)
    exp2.line_chart(df_instituicao)
    
    # Ultima data de dados
    last_dt = df_instituicao.sort_index().iloc[-1]
    exp2.bar_chart(last_dt)
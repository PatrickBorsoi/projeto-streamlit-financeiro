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

    # Exibição dos dados do App
    columns_fmt = {'Valor' : st.column_config.NumberColumn(label="valor", format="R$ %f")}
    st.dataframe(df, hide_index=True, column_config=columns_fmt)
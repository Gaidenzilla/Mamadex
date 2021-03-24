import pandas    as pd
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import plotly.graph_objects as go

df=pd.read_csv('Mamada.csv',index_col=False)
df=pd.DataFrame(df)

df.reset_index(inplace=True)


df.Nome=df.Nome.astype('string')

df.columns=['idx','Nome','Mamadas','Dano Total', 'Dano Médio','Recorde de Dano','KDA','Vitórias','Partidas','Eliminações','Recorde de Eliminações','Derrubadas','Assistências','Mortes',
            'Dano Total', 'Dano Médio','Recorde de Dano','KDA','Vitórias','Partidas','Eliminações','Recorde de Eliminações','Derrubadas','Assistências','Mortes']

st.set_page_config(page_title='Mamadex Team', page_icon=None, layout='wide', initial_sidebar_state='auto')

st.sidebar.title('Filtros')
st.sidebar.header('Comparar Jogadores')
st.sidebar.header('Mamador')
f_name=st.sidebar.multiselect('Selecione os mamadores',df['Nome'].unique(),[])
st.sidebar.header('Ver dados de jogadores com dano médio maior que:')
f_dmg=st.sidebar.slider('Selecione um valor de Dano Médio',min_value=0,max_value=610, value=0,step=50)
st.sidebar.header('Ver dados de jogadores com número de partidas totais acima de:')
f_part=st.sidebar.slider('Selecione um número de partidas',min_value=110,max_value=1570, value=0,step=50)



f_season=st.sidebar.checkbox('Apenas Temporada 8', False)




if f_season:
    df = df.iloc[:,[1,2,14, 15, 16, 17, 18, 19, 20, 21, 22, 23]]
    df['Win Rate'] = (df['Vitórias'] / df['Partidas']) * 100
    st.sidebar.header('Ver dados de jogadores com número de partidas na temporada acima de:')
    f_s8=st.sidebar.slider('Selecione um número de partidas',min_value=0,max_value=400, value=0,step=10)
    df = df.loc[df['Partidas'] > f_s8]
else:
    df=df.iloc[:,1:13]
    df['Win Rate'] = (df['Vitórias'] / df['Partidas']) * 100
    df=df.loc[df['Partidas']>f_part]

if (f_name)!= []:
    df=df.loc[df['Nome'].isin(f_name)]

if (f_dmg)!=0:
    df=df.loc[df['Dano Médio']>f_dmg]

st.title('Visão Geral dos Jogadores')


st.write(df.style.format({'KDA':'{:.2f}','Win Rate':'{:.2f}%'}))

st.title('Maior Mamador até agora')

c1,c2 = st.beta_columns(2)
mamador=df.loc[df['Mamadas']==df['Mamadas'].max()]
mamador=mamador.round({'Win Rate':2})


name=str(mamador['Nome'])
name=name.split()[1]

with c1:
    st.write(mamador.T, height=800)

with c2:
    im = Image.open('{}.jpg'.format(name))
    st.image(im,caption='Chupeteiro Dourado')

c1,c2 = st.beta_columns(2)

with c1:
    st.title('Estatísticas Gerais da Galera')
    dmg_mean=df.iloc[:,3].mean()
    dmg_std=df.iloc[:,3].std()
    dmg_median=df.iloc[:,3].median()
    q75=df.iloc[:,3].quantile(0.75)

    dm=pd.DataFrame({'Média':[dmg_mean],'Desvio Padrão':[dmg_std],'Mediana':[dmg_median],'Top 25%':[q75]},index=['Dano Médio'])


    m_mean=df.iloc[:,1].mean()
    m_std=df.iloc[:,1].std()
    m_median=df.iloc[:,1].median()
    q75 = df.iloc[:, 1].quantile(0.75)

    mmd=pd.DataFrame({'Média':[m_mean],'Desvio Padrão':[m_std],'Mediana':[m_mean],'Top 25%':[q75]},index=['Mamadas'])


    kda_mean=df.iloc[:,5].mean()
    kda_std=df.iloc[:,5].std()
    kda_median=df.iloc[:,5].median()
    q75 = df.iloc[:, 5].quantile(0.75)

    kda=pd.DataFrame({'Média':[kda_mean],'Desvio Padrão':[kda_std],'Mediana':[kda_mean],'Top 25%':[q75]},index=['KDA'])

    wr_mean=df.iloc[:,12].mean()
    wr_std=df.iloc[:,12].std()
    wr_median=df.iloc[:,12].median()
    q75 = df.iloc[:, 12].quantile(0.75)

    wr=pd.DataFrame({'Média':[wr_mean],'Desvio Padrão':[wr_std],'Mediana':[wr_mean],'Top 25%':[q75]},index=['Win Rate'])

    data=pd.concat([dm,mmd,kda,wr])
    st.dataframe(data.style.format('{:.2f}'),width=1800)

with c2:
    med_dmg=df[['Nome','Dano Médio']].loc[df['Dano Médio']==df['Dano Médio'].max()]
    mined_dmg=df[['Nome','Dano Médio']].loc[df['Dano Médio']==df['Dano Médio'].min()]
    m_KDA=df[['Nome','KDA']].loc[df['KDA']==df['KDA'].max()]
    min_KDA=df[['Nome','KDA']].loc[df['KDA']==df['KDA'].min()]
    dmg_record=df[['Nome','Recorde de Dano']].loc[df['Recorde de Dano']==df['Recorde de Dano'].max()]
    kill_record=df[['Nome','Recorde de Eliminações']].loc[df['Recorde de Eliminações']==df['Recorde de Eliminações'].max()]
    max_wr=df[['Nome','Win Rate']].loc[df['Win Rate']==df['Win Rate'].max()]
    min_wr = df[['Nome', 'Win Rate']].loc[df['Win Rate'] == df['Win Rate'].min()]
    assist=df[['Nome','Assistências']].loc[df['Assistências']==df['Assistências'].max()]
    st.title('Recordes da Galera')
    rec=pd.DataFrame({'Recorde':['Maior Dano Médio','Menor Dano Médio','Maior KDA','Menor KDA','Dano em uma partida','Kills em uma partida','Maior Win Rate','Menor Win Rate','Sazon'],
                      'Valor':[df['Dano Médio'].max(),df['Dano Médio'].min(),df['KDA'].max(),df['KDA'].min(),df['Recorde de Dano'].max(),df['Recorde de Eliminações'].max(),df['Win Rate'].max(),df['Win Rate'].min(),df['Assistências'].max()],
                      'Quem Fez':[med_dmg['Nome'].to_string(index=False),mined_dmg['Nome'].to_string(index=False),m_KDA['Nome'].to_string(index=False),min_KDA['Nome'].to_string(index=False)
                                  ,dmg_record['Nome'].to_string(index=False),kill_record['Nome'].to_string(index=False),max_wr['Nome'].to_string(index=False),min_wr['Nome'].to_string(index=False),assist['Nome'].to_string(index=False)]})
    st.write(rec.style.format({'Valor':'{:.2f}'}),width=1800)

idx=['Mamadas','KDA','WR']
nome=df['Nome'].to_list()
listammd=df['Mamadas'].to_list()
listakda=df['KDA'].to_list()
listawr=df['Win Rate'].to_list()


# Quero comparar Mamadas, Dano médio,KDA, WR
bars=[]
for i in range(len(nome)):
    bars.append(go.Bar(name=nome[i], x=idx, y=[listammd[i], listakda[i], listawr[i]]))

fig = go.Figure(data=bars)

# Change the bar mode
fig.update_layout(barmode='group')
fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor="LightSteelBlue",)
#fig.show()
st.title('Gráfico Comparativo de Estatísticas')
st.plotly_chart(fig)

st.title('Gráfico Comparativo de Estatísticas Gerais')
idx=['Dano Médio','Recorde de Dano','Eliminações','Partidas']
listadmg=df['Dano Médio'].to_list()
listarec=df['Recorde de Dano'].to_list()
listael=df['Eliminações'].to_list()
listapart=df['Partidas'].to_list()
bars=[]
for i in range(len(nome)):
    bars.append(go.Bar(name=nome[i], x=idx, y=[listadmg[i], listarec[i], listael[i],listapart[i]]))
fig = go.Figure(data=bars)
fig.update_layout(barmode='group')
fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor="LightSteelBlue",)
st.plotly_chart(fig)

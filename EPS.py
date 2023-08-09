import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config (page_title = 'EPS Movies EDA' , layout = "wide" , page_icon = '📊')
with st.sidebar:
    st.header('EPS Movies Analysis')
    About = st.sidebar.checkbox(":blue[EPS Movies EDA]")
    Planning = st.sidebar.checkbox(":orange[Show About Application]")
    About_me = st.sidebar.checkbox(":green[Show About me]")
    if About:
        st.sidebar.header(":blue[About EDA & Application Info]")
        st.sidebar.write(""" 
        * :blue[*movie_name:*].
        * :blue[*year:*].
        * :blue[*runtime:*].
        * :blue[*genre:*].
        * :blue[*rating:*].
        * :blue[*director:*].
        * :blue[*actor_1:*] .
        * :blue[*actor_2:*] .
        * :blue[*votes:*] .
        * :blue[*metascore:*] .
        * :blue[*gross_collection:*] .
        * :red[So let us see the insights 👀]
        """)
    # ______________________________________________________________________________________________________________________________________________________________________________________________________
    if Planning :
        st.sidebar.header(":orange[Application Planning]")
        st.sidebar.write("""
        * 1) Data Information :
            * Describe : All Info , Categorical , Numerical , Custom Field
            * Data Information (df.info()) : All Info , Categorical , Numerical , Custom Field
            * Corrolation (heatmap)
        * 2) Univariate analysis :
    
        * 3) Bivariate analysiss :
    
        * 4) Multivatiate analysiss
        """)
    # ______________________________________________________________________________________________________________________________________________________________________________________________________
    if About_me :
        st.sidebar.header(":green[About me]")
        st.sidebar.write("""
        - Osama SAAD
        - Student Data Scaience & Machine Learning @ Epsilon AI
        - Infor ERP Consaltant @ Ibnsina Pharma
        - LinkedIn: 
            https://www.linkedin.com/in/ossama-ahmed-saad-525785b2
        - Github : 
            https://github.com/OsamaSamnudi
        """)
# "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
# Data_Info ,Bivariate , Univariate , Multivariate
Data_Info , Univariate ,Bivariate, Multivariate = st.tabs (['Data Information 💾' , 'Univariate Analysis 🔴'  , 'Bivariate Analysis 🟠' , 'Multivariate Analysis🟢'])

pd.options.display.float_format = '{:.,2f}'.format
df = pd.read_csv('imdb_movies_ v2.csv',index_col= 0)

with Data_Info:
    with st.container():
        st.header("Data Describe  💾")
        DI_select = st.selectbox('Please select:',['Please select','All Columns' , 'Categorical' , 'Numerical' , 'custom'])
        if DI_select == 'Please select':
            st.write(":red[Please Choise a column from the list:]")
        elif DI_select == 'All Columns':
            st.write(":violet[Describe Table (All Columns):]")
            st.dataframe(data=df.describe().T , use_container_width=True)
        elif DI_select == 'Numerical':
            st.write(":orange[*Describe Table (All Numerical):*]")
            st.dataframe(data=df.describe(exclude = ['object']).T , use_container_width=True)
        elif DI_select == 'Categorical':
            st.write(":orange[*Describe Table (All Categorical):*]")
            st.dataframe(data=df.describe(include = ['object']).T , use_container_width=True)
        else:
            columns = st.selectbox('Please select:',df.columns.tolist())
            st.write(":orange[*Describe Table for :*]",columns)
            st.dataframe(data=df[columns].describe())

    with st.container():
        pd.options.display.float_format = '{:,.0f}'.format
        st.header("Data Information")
        DataInfo = st.checkbox("Show Data Info")
        if DataInfo :
            st.dataframe(data=df.dtypes.reset_index(name='Type'), hide_index=True, use_container_width=True)  

    with st.container():
        st.subheader('Heatmap Corrolation')
        corrolation = st.checkbox('Show Corrolations')
        if corrolation :
            cor = df.select_dtypes(exclude='object').corr()
            fig_corr = px.imshow(cor , text_auto=True , width= 800 , height= 800  , color_continuous_scale='tropic')
            st.plotly_chart(fig_corr,use_container_width=True,theme="streamlit")
# "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
with Univariate:
    with st.container():
        st.header('Univariate Analysis 🔴')
        st.subheader('Analysis for custom columns')
        lst = ['Please select','year','runtime','genre','rating','director','actor_1','actor_2','votes','metascore','gross_collection']
        lst_select = st.selectbox("Select" , lst)
        st.subheader(f'Histogram of {lst_select}')
        if lst_select == 'Please select':
            st.write(":red[Please Choise a column from the list:]")
        else:
            fig = px.histogram(df, x =lst_select , color_discrete_sequence=['lightskyblue'], text_auto=True)
            st.plotly_chart(fig,use_container_width=True)
    
    with st.container():
        st.subheader('Top / Les 10')
        lst_1 = ['Please select','genre', 'rating', 'director','actor_1', 'actor_2']
        lst_select_1 = st.selectbox("Select" , lst_1)
        col1, col2, col3 = st.columns([7,1,7])
        with col1 :
            if lst_select_1 == 'Please select':
                st.write(":red[Please Choise a column from the list:]")
            else:
                msk = df.groupby(lst_select_1)[['movie_name']].count().reset_index().nlargest(10 , columns = 'movie_name' )
                fig_1 = px.bar(msk , x =lst_select_1 ,y = 'movie_name' ,color_discrete_sequence=['lightskyblue'] ,text_auto=True , title =f"Top 10 {lst_select_1} has Movies")
                st.plotly_chart(fig_1,use_container_width=True)

        with col3 :
            if lst_select_1 == 'Please select':
                st.write(":red[Please Choise a column from the list:]")
            else:
                msk_2 = df.groupby(lst_select_1)[['movie_name']].count().reset_index().nsmallest(10 , columns = 'movie_name' )
                fig_2 = px.bar(msk_2 , x =lst_select_1 ,y = 'movie_name' ,color_discrete_sequence=['darkorange'] ,text_auto=True , title =f"Less 10 {lst_select_1} has Movies")
                st.plotly_chart(fig_2,use_container_width=True)
# "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
with Bivariate:
    with st.container():
        st.header('Bivariate Analysis 🟠')
        st.subheader('Custom selection x (Categorical) vs y (Numerical)')
        x = st.selectbox('Select x :' , ['Please select','genre', 'director', 'actor_1', 'actor_2'])
        y = st.selectbox('Select y :' , ['Please select','runtime', 'rating', 'votes', 'metascore', 'gross_collection'])
        if x == 'Please select' or y == 'Please select' :
            st.write(":red[Please Choise a column from x & y:]")
        else:
            st.write(f'Sum of {x} vs {y}')
            msk_3 = df.groupby(x)[[y]].mean().sort_values(by = y , ascending = False).nlargest(10 , y).reset_index()
            fig_3 = px.bar(msk_3 , x = x , y = y , text_auto=True , color_discrete_sequence=px.colors.qualitative.Plotly)
            st.plotly_chart(fig_3,use_container_width=True)

    with st.container():
        st.subheader('Univariate Analysis YoY by custom Numerical selection')
        NumList = ['Please select','runtime', 'rating', 'votes', 'metascore', 'gross_collection']
        Numerical = st.selectbox('Numerical List' , NumList)
        if Numerical == 'Please select':
            st.write(":red[Please Choise a column from x & y:]")
        else:
            st.write(f'YoY Line Chart for {y}')
            msk_4 = df.groupby('year')[Numerical].mean().sort_values(ascending = False).reset_index().nlargest(10 , 'year')
            fig_4 = px.line(msk_4 , x = 'year' , y = Numerical , color_discrete_sequence=px.colors.qualitative.Plotly , markers= True)
            st.plotly_chart(fig_4,use_container_width=True)
# "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
with Multivariate:
    with st.container():
        st.header('Multivariate Analysis🟢')
        st.subheader('Custom selection x (Categorical) vs y (Numerical) - Scatter Plot')
        Sc_x = st.selectbox('Select X:' , ['Please select','movie_name', 'year', 'runtime', 'genre', 'rating', 'director','actor_1', 'actor_2', 'votes', 'metascore', 'gross_collection'])
        Sc_y = st.selectbox('Select Y :' , ['Please select','movie_name', 'year', 'runtime', 'genre', 'rating', 'director','actor_1', 'actor_2', 'votes', 'metascore', 'gross_collection'])
        if Sc_x == 'Please select' or Sc_y == 'Please select' :
            st.write(":red[Please Choise a column from x & y:]")
        else:
            if Sc_x == Sc_y:
                st.write(":red[Please Choise a column from x & y:]")
            else:
                st.write(f'Scatter Plot of {Sc_x} vs {Sc_y}')
                fig_5 = px.scatter(df , x=Sc_x , y=Sc_y , marginal_x='box' ,color = 'year' , title = f"{Sc_x} VS  {Sc_y}")
                st.plotly_chart(fig_5,use_container_width=True)

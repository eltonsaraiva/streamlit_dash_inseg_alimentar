import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    layout='wide',
    page_icon=':bar_chart:'
)

def load_data():
    data = pd.read_csv('UN_food_security.csv')
    item_filter = "Prevalence of severe food insecurity in the total population (percent) (3-year average)"
    filtered_data = data[data['Item'] == item_filter]
    filtered_data['Year_Middle'] = filtered_data['Year'].apply(lambda x: int(x.split('-')[0]) + 1)
    filtered_data['Value_Clean'] = pd.to_numeric(filtered_data['Value'].str.replace('<', '').replace('>', ''), errors='coerce')
    filtered_data.dropna(subset=['Value_Clean'], inplace=True)

    return filtered_data

data = load_data()

st.title('Dashboard - Segurança Alimentar Mundial')
st.markdown('Fonte: UN Food and Agriculture Organization')

years = data['Year_Middle'].unique()
selected_year = st.selectbox(
    label='Selecione: ',
    options=years
)

filtered_data_year = data[data['Year_Middle'] == selected_year]


fig_map = px.choropleth(
    data_frame=filtered_data_year,
    locations='Area',
    locationmode="country names",
    color='Value_Clean',
    hover_name='Area',
    hover_data={'Year_Middle':False, 'Value_Clean':True},
    color_continuous_scale='ylorrd',
    title=f'Insegurança Alimentar Global - {selected_year}'
)

st.plotly_chart(
    figure_or_data=fig_map,
    use_container_width=True
)

top_countries = filtered_data_year.nlargest(10, 'Value_Clean')


fig_bar = px.bar(
    data_frame=top_countries,
    x='Value_Clean',
    y='Area',
    orientation='h',
    color='Value_Clean',
    color_continuous_scale='YlOrRd',
    title='TOP 10 Países com maiores Insegurança Alimentar'
)

fig_bar.update_layout(
    yaxis={'categoryorder':'total ascending'}
)
st.plotly_chart(
    figure_or_data=fig_bar,
    use_container_width=True
)

st.text(f'Dataframe - {selected_year}')
st.dataframe(filtered_data_year)
st.text(f'Dataframe - TOP 10 - {selected_year}')
st.dataframe(top_countries)

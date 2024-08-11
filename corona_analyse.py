import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# Veriyi yükleme
data = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")

# Veri temizleme
data = data.drop(columns=["Province/State", "Lat", "Long"])
data = data.groupby("Country/Region").aggregate(np.sum).T
data.index.name = "Date"
data = data.reset_index()

# Veriyi eritme
melt_data = data.melt(id_vars=["Date"], var_name="Country", value_name="Confirmed")
melt_data["Date"] = pd.to_datetime(melt_data["Date"])
melt_data["Date"] = melt_data["Date"].dt.strftime("%Y/%m/%d")

# Son gün verisi
max_date = melt_data["Date"].max()
lastday = melt_data[melt_data["Date"] == max_date]
Total = lastday["Confirmed"].sum()

# Türkiye için çizgi grafiği
figure = px.line(melt_data[melt_data["Country"] == "Turkey"], x="Date", y="Confirmed", title="Confirmed Cases in Turkey Over Time")
pio.write_html(figure, 'turkey_cases_over_time.html')  # HTML dosyasına kaydetme

# Total vakalar için gösterge grafiği
fig = go.Figure()
fig.add_trace(go.Indicator(
    mode="number",
    value=int(Total),
    number={"valueformat": "0.f"},
    title={"text": "Total Confirmed Cases"},
    domain={"row": 0, "column": 0}
))
pio.write_html(fig, 'total_confirmed_cases.html')  # HTML dosyasına kaydetme

# Choropleth haritası (normal)
fig = px.choropleth(lastday, 
                    locations='Country',
                    locationmode='country names',
                    color='Confirmed',
                    color_continuous_scale='dense',
                    range_color=(0, max(lastday["Confirmed"])),
                    title="Confirmed Cases by Country on {}".format(max_date))
pio.write_html(fig, 'choropleth_normal.html')  # HTML dosyasına kaydetme

# Choropleth haritası (logaritmik ölçek)
fig = px.choropleth(lastday, 
                    locations='Country',
                    locationmode='country names',
                    color=np.log10(lastday["Confirmed"] + 1),  # +1 to avoid log(0)
                    color_continuous_scale='dense',
                    range_color=(0, np.log10(max(lastday["Confirmed"]) + 1)),
                    title="Log-Scaled Confirmed Cases by Country on {}".format(max_date))
pio.write_html(fig, 'choropleth_log_scaled.html')  # HTML dosyasına kaydetme

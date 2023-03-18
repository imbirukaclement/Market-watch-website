from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import numpy as np
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from IPython.display import HTML
import requests
from datetime import datetime
import geemap.foliumap as geemap
import ee

app = Flask(__name__)


@app.route("/")
def home():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("kif/kisumu.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Kisumu").sheet1
    data = sheet.get_all_records()
    kf = pd.DataFrame(data)
    df1 = kf.dropna(how="all")
    df2 = df1.replace({

        "Wholesale": "[A-Za-z/]",
        "Retail": "[A-Za-z/]"
    }, "", regex=True)
    df3 = df2.replace({

        "Market": "-",
        "Commodity": "-",
        'Classification': "-",
        "Wholesale": "-",
        "Retail": "-",
        "Supply Volume": "-",
        "County": "-"
    }, np.NaN, regex=True)
    df3['date'] = df3['Date']
    df3['Wholesale(KGs)'] = pd.to_numeric(df3["Wholesale"])
    df3['Retail(KGs)'] = pd.to_numeric(df3["Retail"])
    df4 = df3.drop(["Wholesale", "Retail"], axis=1).sort_values(by=['Date'], ascending=True).set_index("date")
    Kat = df4[df4["Market"] == "Katito"]
    kat = Kat[Kat["Commodity"] == "Red Irish potato"]
    Kat = df4[df4["Market"] == "Katito"]
    On = Kat[Kat["Commodity"] == "Dry Onions"]
    On["Change"] = ((On['Retail(KGs)'] / On['Retail(KGs)'].shift(1)) - 1)
    change_2 = round(float(On.loc[On["Date"] == f"{On.Date[len(On.Date) - 1]}", 'Change']), 2)
    kb = df4[df4["Market"] == "Kibuye"]
    kat["Change"] = ((kat['Retail(KGs)'] / kat['Retail(KGs)'].shift(1)) - 1)
    hass = kb[kb["Classification"] == "Hass"]
    hass["Change"] = ((hass['Retail(KGs)'] / hass['Retail(KGs)'].shift(1)) - 1)
    change_1 = round(float(hass.loc[hass["Date"] == f"{hass.Date[len(hass.Date) - 1]}", 'Change']), 2)
    change_8 = round(float(kat['Change'][-1]), 2)
    today = datetime.now().year
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("kif/Nairobi.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Nairobi").sheet1
    data = sheet.get_all_records()
    nb = pd.DataFrame(data)
    df1 = nb.dropna(how="all")
    df2 = df1.replace({
        "Wholesale": "[A-Za-z/]",
        "Retail": "[A-Za-z/]"
    }, "", regex=True)
    df3 = df2.replace({
        "Market": "-",
        "Commodity": "-",
        'Classification': "-",
        "Wholesale": "-",
        "Retail": "-",
        "Supply Volume": "-",
        "County": "-"
    }, np.NaN, regex=True)
    df3['Wholesale(KGs)'] = pd.to_numeric(df3["Wholesale"])
    df3['Retail(KGs)'] = pd.to_numeric(df3["Retail"])
    df3['date'] = df3['Date']
    df4 = df3.drop(["Wholesale", "Retail"], axis=1).sort_values(by=['Date'], ascending=True).set_index("date")
    onions = df4[df4["Commodity"] == 'Dry Onions']
    onions_k = onions[onions['Market'] == 'Kangemi Market']
    onions_k_clean = onions_k.fillna(method="bfill")
    onions_k_clean["Change"] = ((onions_k_clean['Retail(KGs)'] / onions_k_clean['Retail(KGs)'].shift(1)) - 1)
    avocado = df4[df4["Commodity"] == 'Avocado']
    avocado_local = avocado[avocado["Classification"] == "Local"]
    avocado_local_k = avocado_local[avocado_local["Market"] == "Kangemi Market"]
    avocado_local_k_clean = avocado_local_k.fillna(method="bfill")
    avocado_local_k_clean["Change"] = (
            (avocado_local_k_clean['Retail(KGs)'] / avocado_local_k_clean['Retail(KGs)'].shift(1)) - 1)
    avocado_local_k_clean
    rice = df4[df4["Commodity"] == 'Rice']
    rice_p = rice[rice['Classification'] == "Pishori"]
    rice_p_k = rice_p[rice_p["Market"] == "Kangemi Market"]
    rice_p_k_clean = rice_p_k.fillna(method="ffill")
    rice_p_k_clean["Change"] = ((rice_p_k_clean['Retail(KGs)'] / rice_p_k_clean['Retail(KGs)'].shift(1)) - 1)
    change_5 = round(float(
        rice_p_k_clean.loc[rice_p_k_clean["Date"] == f"{rice_p_k_clean.Date[len(rice_p_k_clean.Date) - 1]}", 'Change']),
        2)

    change_4 = round(float(avocado_local_k_clean.loc[avocado_local_k_clean[
                                                         "Date"] == f"{avocado_local_k_clean.Date[len(avocado_local_k_clean.Date) - 1]}", 'Change']),
                     2)
    change_3 = round(float(
        onions_k_clean.loc[onions_k_clean["Date"] == f"{onions_k_clean.Date[len(onions_k_clean.Date) - 1]}", 'Change']),
        2)

    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("kif//naks.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Nakuru").sheet1
    data = sheet.get_all_records()
    nf = pd.DataFrame(data)
    df1 = nf.dropna(how="all")
    df2 = df1.replace({
        "Wholesale": "[A-Za-z/]",
        "Retail": "[A-Za-z/]"
    }, "", regex=True)
    df3 = df2.replace({
        "Market": "-",
        "Commodity": "-",
        'Classification': "-",
        "Wholesale": "-",
        "Retail": "-",
        "Supply Volume": "-",
        "County": "-"
    }, np.NaN, regex=True)
    df3['Wholesale(KGs)'] = pd.to_numeric(df3["Wholesale"])
    df3['Retail(KGs)'] = pd.to_numeric(df3["Retail"])
    df3['date'] = df3['Date']
    df4 = df3.drop(["Wholesale", "Retail"], axis=1).sort_values(by=['Date'], ascending=True).set_index("date")
    Onions = df4[df4['Commodity'] == 'Dry Onions']
    on1 = Onions.drop(["Classification"], axis=1)
    on1[["Wholesale(KGs)", "Retail(KGs)"]] = on1[["Wholesale(KGs)", "Retail(KGs)"]].fillna(method="ffill")
    on1['Wholesale(KGs)'] = pd.to_numeric(on1["Wholesale(KGs)"])
    on1['Retail(KGs)'] = pd.to_numeric(on1["Retail(KGs)"])
    on1['Date'] = pd.to_datetime(on1["Date"])
    Naivasha_Market = on1[on1['Market'] == "Naivasha Market"]
    Naivasha_Market["Change"] = ((Naivasha_Market['Retail(KGs)'] / Naivasha_Market['Retail(KGs)'].shift(1)) - 1)
    White_maize = df4[df4["Classification"] == 'White Maize']
    w = White_maize[White_maize['Market'] == "Nakuru Wakulima"].fillna(method="bfill")
    w["Change"] = ((w['Retail(KGs)'] / w['Retail(KGs)'].shift(1)) - 1)

    change_6 = round(float(Naivasha_Market.loc[Naivasha_Market[
                                                   "Date"] == f"{Naivasha_Market.Date[len(Naivasha_Market.Date) - 1]}", 'Change']),
                     2)
    change_7 = round(float(w.loc[w["Date"] == f"{w.Date[len(w.Date) - 1]}", 'Change']), 2)

    fig_k = px.line(kat, x="Date", y=["Wholesale(KGs)", "Retail(KGs)"], title="Katito Market Red Irish potato Price",
                    template="plotly_white", width=600)
    fig_k1 = px.line(onions_k_clean, x="Date", y=["Retail(KGs)", "Wholesale(KGs)"],
                     title="Kangemi Market Dry Onions Price", template="plotly_white", width=600)
    fig_k2 = px.line(Naivasha_Market, y=["Retail(KGs)", "Wholesale(KGs)"], x="Date",
                     title=" Naivasha Onion Price Per Kg", template="plotly_white", width=600)

    graphJSON_k = json.dumps(fig_k, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_1 = json.dumps(fig_k1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_2 = json.dumps(fig_k2, cls=plotly.utils.PlotlyJSONEncoder)

    new_change = [change_1, change_2, change_3, change_4, change_5, change_6, change_7, change_8]

    return render_template("index.html", change=new_change, date=today,
                           graphJSON_y=graphJSON_k, graphJSON_z=graphJSON_1, graphJSON_x=graphJSON_2)


@app.route("/kisumu_graph")
def kisumu_graph():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("kif//kisumu.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Kisumu").sheet1
    data = sheet.get_all_records()
    kf = pd.DataFrame(data)
    df1 = kf.dropna(how="all")
    df2 = df1.replace({

        "Wholesale": "[A-Za-z/]",
        "Retail": "[A-Za-z/]"
    }, "", regex=True)
    df3 = df2.replace({

        "Market": "-",
        "Commodity": "-",
        'Classification': "-",
        "Wholesale": "-",
        "Retail": "-",
        "Supply Volume": "-",
        "County": "-"
    }, np.NaN, regex=True)
    df3['Wholesale(KGs)'] = pd.to_numeric(df3["Wholesale"])
    df3['Retail(KGs)'] = pd.to_numeric(df3["Retail"])
    df4 = df3.drop(["Wholesale", "Retail"], axis=1)
    Ah = df4[df4["Market"] == "Ahero"]
    kat_s = df4[df4["Market"] == "Katito"]
    kat_S = kat_s[kat_s["Classification"] == "Sindano"]

    Kat = df4[df4["Market"] == "Katito"]
    On = Kat[Kat["Commodity"] == "Dry Onions"]
    aher = df4[df4["Market"] == "Ahero"]
    ah = aher[aher["Commodity"] == "Dry Onions"]
    kib = df4[df4["Market"] == "Kibuye"]
    kibs = kib[kib["Commodity"] == "Dry Onions"]
    up_kibs = kibs.fillna(method="backfill")
    up_kibs["Retail(KGs)"] = up_kibs["Wholesale(KGs)"]
    up_kibs["Wholesale(KGs)"] = kibs["Retail(KGs)"]
    up_K_data = up_kibs.replace({
        "Wholesale(KGs)": 120
    }, 80)
    Holo = df4[df4["Market"] == "Holo"]
    Hol = Holo[Holo["Commodity"] == "Dry Onions"]
    kat_p = df4[df4["Market"] == "Katito"]
    up_kat = kat_p[kat_p["Classification"] == "Pishori"]
    ah_p = df4[df4["Market"] == "Ahero"]
    ahh_p = ah_p[ah_p["Classification"] == "Pishori"]
    fig_k7 = px.line(ahh_p, x="Date", y=["Wholesale(KGs)", "Retail(KGs)"], title="Ahero Market Pishori Price",
                     template="plotly_white", width=600)
    fig_k6 = px.line(up_kat, x="Date", y=["Wholesale(KGs)", "Retail(KGs)"], title="Katito Market Pishori Price",
                     template="plotly_white", width=600)
    fig_k5 = px.line(Hol, x="Date", y=["Wholesale(KGs)", "Retail(KGs)"], title="Holo Market Dry Onions Price",
                     template="plotly_white", width=600)
    fig_k4 = px.line(up_K_data, x="Date", y=["Wholesale(KGs)", "Retail(KGs)"], title="Kibuye Market Dry Onions Price",
                     template="plotly_white", width=600)
    fig_k3 = px.line(ah, x="Date", y=["Wholesale(KGs)", "Retail(KGs)"], title="Ahero Market Dry Onions Price",
                     template="plotly_white", width=600)
    fig_k2 = px.line(On, x="Date", y=["Wholesale(KGs)", "Retail(KGs)"], title="Katito Market Dry Onions Price",
                     template="plotly_white", width=600)
    fig_k1 = px.line(kat_S, x="Date", y=["Wholesale(KGs)", "Retail(KGs)"], title="Katito Market Sindano Price",
                     template="plotly_white", width=600)
    graphJSON_1 = json.dumps(fig_k7, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_2 = json.dumps(fig_k6, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_3 = json.dumps(fig_k5, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_4 = json.dumps(fig_k4, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_5 = json.dumps(fig_k3, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_6 = json.dumps(fig_k2, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_7 = json.dumps(fig_k1, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("graph.html", graphJSON_a=graphJSON_1, graphJSON_b=graphJSON_2,
                           graphJSON_c=graphJSON_3,
                           graphJSON_d=graphJSON_4, graphJSON_e=graphJSON_5, graphJSON_f=graphJSON_6,
                           graphJSON_g=graphJSON_7)


@app.route('/Nairobi')
def nairobi_graph():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("kif//Nairobi.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Nairobi").sheet1
    data = sheet.get_all_records()
    nb = pd.DataFrame(data)
    df1 = nb.dropna(how="all")
    df2 = df1.replace({
        "Wholesale": "[A-Za-z/]",
        "Retail": "[A-Za-z/]"
    }, "", regex=True)
    df3 = df2.replace({
        "Market": "-",
        "Commodity": "-",
        'Classification': "-",
        "Wholesale": "-",
        "Retail": "-",
        "Supply Volume": "-",
        "County": "-"
    }, np.NaN, regex=True)
    df3['Wholesale(KGs)'] = pd.to_numeric(df3["Wholesale"])
    df3['Retail(KGs)'] = pd.to_numeric(df3["Retail"])
    df4 = df3.drop(["Wholesale", "Retail"], axis=1)
    onions = df4[df4["Commodity"] == 'Dry Onions']
    onions_g = onions[onions['Market'] == 'Gikomba']
    onions = df4[df4["Commodity"] == 'Dry Onions']
    onions_k = onions[onions['Market'] == 'Kangemi Market']
    onions_k_clean = onions_k.fillna(method="bfill")
    onions_w = onions[onions['Market'] == 'Nairobi Wakulima']
    onions_w_clean = onions_w.fillna(method="bfill")
    avocado = df4[df4["Commodity"] == 'Avocado']
    avocado_local = avocado[avocado["Classification"] == "Local"]
    avocado_local_k = avocado_local[avocado_local["Market"] == "Kangemi Market"]
    avocado_local_k_clean = avocado_local_k.fillna(method="bfill")
    avocado = df4[df4["Commodity"] == 'Avocado']
    avocado_fuerte = avocado[avocado["Classification"] == "Fuerte"]
    avocado_fuerte_k = avocado_fuerte[avocado_fuerte["Market"] == "Kangemi Market"]
    avocado_fuerte_k_clean = avocado_fuerte_k.fillna(method="bfill")
    avocado = df4[df4["Commodity"] == 'Avocado']
    avocado_fuerte = avocado[avocado["Classification"] == "Fuerte"]
    avocado_fuerte_w = avocado_fuerte[avocado_fuerte["Market"] == "Nairobi Wakulima"]
    avocado_fuerte_w_clean = avocado_fuerte_w.fillna(method="bfill")
    wheat = df4[df4["Commodity"] == 'Wheat']
    wheat_k = wheat[wheat["Market"] == "Kangemi Market"]
    wheat_k_clean = wheat_k.fillna(method="bfill")
    rice = df4[df4["Commodity"] == 'Rice']
    rice_p = rice[rice['Classification'] == "Pishori"]
    rice_p_k = rice_p[rice_p["Market"] == "Kangemi Market"]
    rice = df4[df4["Commodity"] == 'Rice']
    rice_p = rice[rice['Classification'] == "Pishori"]
    rice_p_k = rice_p[rice_p["Market"] == "Nyamakima"]
    rice_p_k_clean = rice_p_k.fillna(method="ffill")

    fig_k2 = px.line(onions_k_clean, x="Date", y=["Retail(KGs)", "Wholesale(KGs)"],
                     title="Kangemi Market Dry Onions Price", template="plotly_white", width=600)
    fig_k3 = px.line(onions_w_clean, x="Date", y=["Retail(KGs)", "Wholesale(KGs)"],
                     title="Kangemi Market Dry Onions Price", template="plotly_white", width=600)
    fig_k4 = px.line(avocado_local_k_clean, x="Date", y=["Retail(KGs)", "Wholesale(KGs)"],
                     title="Kangemi Market Local Avocado Price", template="plotly_white", width=600)
    fig_k5 = px.line(avocado_fuerte_k_clean, x="Date", y=["Retail(KGs)", "Wholesale(KGs)"],
                     title="Kangemi Market Fuerte Avocado Price", template="plotly_white", width=600)
    fig_k6 = px.line(avocado_fuerte_w_clean, x="Date", y=["Retail(KGs)", "Wholesale(KGs)"],
                     title="Nairobi Wakulima Market Fuerte Avocado Price", template="plotly_white", width=600)
    fig_k7 = px.line(wheat_k_clean, x="Date", y=["Retail(KGs)", "Wholesale(KGs)"], title="Kangemi Market Wheat Price",
                     template="plotly_white", width=600)
    fig_k8 = px.line(rice_p_k_clean, x="Date", y=["Retail(KGs)", "Wholesale(KGs)"],
                     title="Kangemi Market Pishori Rice Price", template="plotly_white", width=600)

    graphJSON_2 = json.dumps(fig_k2, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_3 = json.dumps(fig_k3, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_4 = json.dumps(fig_k4, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_5 = json.dumps(fig_k5, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_6 = json.dumps(fig_k6, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_7 = json.dumps(fig_k7, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_8 = json.dumps(fig_k8, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("graph2.html", graphJSON_b=graphJSON_2,
                           graphJSON_c=graphJSON_3,
                           graphJSON_d=graphJSON_4, graphJSON_e=graphJSON_5, graphJSON_f=graphJSON_6,
                           graphJSON_g=graphJSON_7, graphJSON_h=graphJSON_8)


@app.route('/Nakuru')
def nakuru_graph():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("kif//naks.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Nakuru").sheet1
    data = sheet.get_all_records()
    nf = pd.DataFrame(data)
    df1 = nf.dropna(how="all")
    df2 = df1.replace({
        "Wholesale": "[A-Za-z/]",
        "Retail": "[A-Za-z/]"
    }, "", regex=True)
    df3 = df2.replace({
        "Market": "-",
        "Commodity": "-",
        'Classification': "-",
        "Wholesale": "-",
        "Retail": "-",
        "Supply Volume": "-",
        "County": "-"
    }, np.NaN, regex=True)
    df3['Wholesale(KGs)'] = pd.to_numeric(df3["Wholesale"])
    df3['Retail(KGs)'] = pd.to_numeric(df3["Retail"])
    df4 = df3
    sindano = df4[df4["Classification"] == 'Sindano']
    d = sindano[sindano["Market"] == "Nakuru Wakulima"].fillna(method="bfill")
    pishori = df4[df4["Classification"] == 'Pishori']
    p = pishori[pishori['Market'] == "Nakuru Wakulima"].fillna(method="bfill")
    White_maize = df4[df4["Classification"] == 'White Maize']
    w = White_maize[White_maize['Market'] == "Nakuru Wakulima"].fillna(method="bfill")
    Onions = df4[df4['Commodity'] == 'Dry Onions']
    on1 = Onions.drop(["Classification"], axis=1)
    on1[["Wholesale(KGs)", "Retail(KGs)"]] = on1[["Wholesale(KGs)", "Retail(KGs)"]].fillna(method="ffill")
    on1['Wholesale(KGs)'] = pd.to_numeric(on1["Wholesale(KGs)"])
    on1['Retail(KGs)'] = pd.to_numeric(on1["Retail(KGs)"])
    Nakuru_top_market = on1[on1['Market'] == "Nakuru Top Market"]
    Naivasha_Market = on1[on1['Market'] == "Naivasha Market"]
    fig_k1 = px.line(d, y=["Retail(KGs)", "Wholesale(KGs)"], x="Date",
                     title=" Nakuru Wakulima Market Sindano Price Per Kg ",
                     template="plotly_white", width=600)
    fig_k2 = px.line(p, y=["Retail(KGs)", "Wholesale(KGs)"], x="Date", title=" Nakuru Wakulima Pishori Price Per Kg",
                     template="plotly_white", width=600)
    fig_k3 = px.line(w, y=["Retail(KGs)", "Wholesale(KGs)"], x="Date",
                     title=" Nakuru Wakulima White Maize Price Per Kg", template="plotly_white", width=600)
    fig_k4 = px.line(Naivasha_Market, y=["Retail(KGs)", "Wholesale(KGs)"], x="Date",
                     title=" Naivasha Onion Price Per Kg", template="plotly_white", width=600)
    fig_k5 = px.line(Nakuru_top_market, y=["Retail(KGs)", "Wholesale(KGs)"], x="Date",
                     title=" Nakuru Top Market Onion Price Per Kg", template="plotly_white", width=600)

    graphJSON_1 = json.dumps(fig_k1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_2 = json.dumps(fig_k2, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_3 = json.dumps(fig_k3, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_4 = json.dumps(fig_k4, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_5 = json.dumps(fig_k5, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("graph3.html", graphJSON_a=graphJSON_1, graphJSON_b=graphJSON_2,
                           graphJSON_c=graphJSON_3,
                           graphJSON_d=graphJSON_4, graphJSON_e=graphJSON_5)


@app.route("/data")
def data():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("kif//Nairobi.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Nairobi").sheet1
    data = sheet.get_all_records()
    nb = pd.DataFrame(data)
    df1 = nb.dropna(how="all")
    df2 = df1.replace({
        "Wholesale": "[A-Za-z/]",
        "Retail": "[A-Za-z/]"
    }, "", regex=True)
    df3 = df2.replace({
        "Market": "-",
        "Commodity": "-",
        'Classification': "-",
        "Wholesale": "-",
        "Retail": "-",
        "Supply Volume": "-",
        "County": "-"
    }, np.NaN, regex=True)
    df3['Wholesale(KGs)'] = pd.to_numeric(df3["Wholesale"])
    df3['Retail(KGs)'] = pd.to_numeric(df3["Retail"])
    df4 = df3.drop(["Wholesale", "Retail"], axis=1)
    onions = df4[df4["Commodity"] == 'Dry Onions']
    onions_g = onions[onions['Market'] == 'Gikomba']
    onions = df4[df4["Commodity"] == 'Dry Onions']
    onions_k = onions[onions['Market'] == 'Kangemi Market']
    onions_k_clean = onions_k.fillna(method="bfill")
    onions_w = onions[onions['Market'] == 'Nairobi Wakulima']
    onions_w_clean = onions_w.fillna(method="bfill")
    avocado = df4[df4["Commodity"] == 'Avocado']
    avocado_local = avocado[avocado["Classification"] == "Local"]
    avocado_local_k = avocado_local[avocado_local["Market"] == "Kangemi Market"]
    avocado_local_k_clean = avocado_local_k.fillna(method="bfill")
    avocado = df4[df4["Commodity"] == 'Avocado']
    avocado_fuerte = avocado[avocado["Classification"] == "Fuerte"]
    avocado_fuerte_k = avocado_fuerte[avocado_fuerte["Market"] == "Kangemi Market"]
    avocado_fuerte_k_clean = avocado_fuerte_k.fillna(method="bfill")
    avocado = df4[df4["Commodity"] == 'Avocado']
    avocado_fuerte = avocado[avocado["Classification"] == "Fuerte"]
    avocado_fuerte_w = avocado_fuerte[avocado_fuerte["Market"] == "Nairobi Wakulima"]
    avocado_fuerte_w_clean = avocado_fuerte_w.fillna(method="bfill")
    wheat = df4[df4["Commodity"] == 'Wheat']
    wheat_k = wheat[wheat["Market"] == "Kangemi Market"]
    wheat_k_clean = wheat_k.fillna(method="bfill")
    rice = df4[df4["Commodity"] == 'Rice']
    rice_p = rice[rice['Classification'] == "Pishori"]
    rice = df4[df4["Commodity"] == 'Rice']
    rice_p = rice[rice['Classification'] == "Pishori"]
    rice_p_k = rice_p[rice_p["Market"] == "Nyamakima"]
    rice_p_k_clean = rice_p_k.fillna(method="ffill")
    rice_p_k_cleaned = rice_p_k_clean.replace({
        "Wholesale(KGs)": 356

    }, 156)
    market_1 = HTML(onions_k_clean.to_html())
    market_2 = HTML(onions_w_clean.to_html())
    market_3 = HTML(avocado_local_k_clean.to_html())
    market_4 = HTML(avocado_fuerte_k_clean.to_html())
    market_5 = HTML(avocado_fuerte_w_clean.to_html())
    market_6 = HTML(wheat_k_clean.to_html())
    market_7 = HTML(rice_p_k_clean.to_html())
    nairobi_market = [market_1, market_2, market_3, market_4, market_5, market_6, market_7]
    return render_template("data.html", nairobi_market=nairobi_market)


@app.route('/nakuru_data')
def nakuru_data():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("kif//naks.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Nakuru").sheet1
    data = sheet.get_all_records()
    nf = pd.DataFrame(data)
    df1 = nf.dropna(how="all")
    df2 = df1.replace({
        "Wholesale": "[A-Za-z/]",
        "Retail": "[A-Za-z/]"
    }, "", regex=True)
    df3 = df2.replace({
        "Market": "-",
        "Commodity": "-",
        'Classification': "-",
        "Wholesale": "-",
        "Retail": "-",
        "Supply Volume": "-",
        "County": "-"
    }, np.NaN, regex=True)
    df3['Wholesale(KGs)'] = pd.to_numeric(df3["Wholesale"])
    df3['Retail(KGs)'] = pd.to_numeric(df3["Retail"])
    df4 = df3
    sindano = df4[df4["Classification"] == 'Sindano']
    d = sindano[sindano["Market"] == "Nakuru Wakulima"].fillna(method="bfill")
    pishori = df4[df4["Classification"] == 'Pishori']
    p = pishori[pishori['Market'] == "Nakuru Wakulima"].fillna(method="bfill")
    White_maize = df4[df4["Classification"] == 'White Maize']
    w = White_maize[White_maize['Market'] == "Nakuru Wakulima"].fillna(method="bfill")
    Onions = df4[df4['Commodity'] == 'Dry Onions']
    on1 = Onions.drop(["Classification"], axis=1)
    on1[["Wholesale(KGs)", "Retail(KGs)"]] = on1[["Wholesale(KGs)", "Retail(KGs)"]].fillna(method="ffill")
    on1['Wholesale(KGs)'] = pd.to_numeric(on1["Wholesale(KGs)"])
    on1['Retail(KGs)'] = pd.to_numeric(on1["Retail(KGs)"])
    Nakuru_top_market = on1[on1['Market'] == "Nakuru Top Market"]
    Naivasha_Market = on1[on1['Market'] == "Naivasha Market"]
    market_1 = HTML(d.to_html())
    market_2 = HTML(p.to_html())
    market_3 = HTML(w.to_html())
    market_4 = HTML(Naivasha_Market.to_html())
    market_5 = HTML(Nakuru_top_market.to_html())
    nakuru_market = [market_1, market_2, market_3, market_4, market_5]
    return render_template("data_2.html", nakuru_market=nakuru_market)


@app.route('/kisumu_data')
def kisumu_data():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("kif//kisumu.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Kisumu").sheet1
    data = sheet.get_all_records()
    kf = pd.DataFrame(data)
    df1 = kf.dropna(how="all")
    df2 = df1.replace({

        "Wholesale": "[A-Za-z/]",
        "Retail": "[A-Za-z/]"
    }, "", regex=True)
    df3 = df2.replace({

        "Market": "-",
        "Commodity": "-",
        'Classification': "-",
        "Wholesale": "-",
        "Retail": "-",
        "Supply Volume": "-",
        "County": "-"
    }, np.NaN, regex=True)
    df3['Wholesale(KGs)'] = pd.to_numeric(df3["Wholesale"])
    df3['Retail(KGs)'] = pd.to_numeric(df3["Retail"])
    df4 = df3.drop(["Wholesale", "Retail"], axis=1)
    Ah = df4[df4["Market"] == "Ahero"]
    ah_p = Ah[Ah["Commodity"] == "Red Irish potato"]
    kat_s = df4[df4["Market"] == "Katito"]
    kat_S = kat_s[kat_s["Classification"] == "Sindano"]

    Kat = df4[df4["Market"] == "Katito"]
    On = Kat[Kat["Commodity"] == "Dry Onions"]
    aher = df4[df4["Market"] == "Ahero"]
    ah = aher[aher["Commodity"] == "Dry Onions"]
    kib = df4[df4["Market"] == "Kibuye"]
    kibs = kib[kib["Commodity"] == "Dry Onions"]
    up_kibs = kibs.fillna(method="backfill")
    up_kibs["Retail(KGs)"] = up_kibs["Wholesale(KGs)"]
    up_kibs["Wholesale(KGs)"] = kibs["Retail(KGs)"]
    up_K_data = up_kibs.replace({
        "Wholesale(KGs)": 120
    }, 80)
    Holo = df4[df4["Market"] == "Holo"]
    Hol = Holo[Holo["Commodity"] == "Dry Onions"]
    kat_p = df4[df4["Market"] == "Katito"]
    up_kat = kat_p[kat_p["Classification"] == "Pishori"]
    ah_p = df4[df4["Market"] == "Ahero"]
    ahh_p = ah_p[ah_p["Classification"] == "Pishori"]
    market_1 = HTML(ahh_p.to_html())
    market_2 = HTML(up_kat.to_html())
    market_3 = HTML(Hol.to_html())
    market_4 = HTML(up_K_data.to_html())
    market_5 = HTML(ah.to_html())
    market_6 = HTML(On.to_html())
    market_7 = HTML(kat_S.to_html())
    kisumu_dat = [market_1, market_2, market_3, market_4, market_5, market_6, market_7]
    return render_template('data_3.html', kisumu_dat=kisumu_dat)


@app.route('/weather', methods=['POST', 'GET'])
def weather_data():
    location_i = request.form.get('location')
    api_key = "4856d05830439e769a7291914a8c2206"
    api_link = "https://api.openweathermap.org/data/2.5/weather?q=" + f"{location_i}" + "&appid=" + api_key
    response = requests.get(api_link)
    response.raise_for_status()
    data = response.json()
    temp = int((data['main']['temp']) - 273.15)
    weather_description = data['weather'][0]['description']
    humidity = int(data['main']['humidity'])
    wind_speed = int(data['wind']['speed'])
    condition_code = int(data["weather"][0]['id'])

    def rain():
        if condition_code < 700:
            return "it will rain today"
        else:
            return "It will not rain today"

    date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
    loc = str(location_i).upper()
    weather_elements = [date_time, temp, humidity, wind_speed, weather_description, rain(), loc]
    return render_template("weather.html", weather_elements=weather_elements)


@app.route('/geo')
def geo_data():
    try:
        ee.Initialize()
    except Exception as e:
        ee.Authenticate()
        ee.Initialize()
    Map = geemap.Map(center=[1.9577, 37.2972], zoom=4)
    dataset = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2') \
        .filterDate('2022-01-01', '2022-02-01')

    # Applies scaling factors.
    def applyScaleFactors(image):
        opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
        thermalBands = image.select('ST_B.*').multiply(0.00341802).add(149.0)
        return image.addBands(opticalBands, None, True).addBands(thermalBands, None, True)

    dataset = dataset.map(applyScaleFactors)

    visualization = {
        'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
        'min': 0.0,
        'max': 0.3,
    }

    Map.addLayer(dataset, visualization, 'True Color (432)')
    map_1 = HTML(Map.to_html())
    return render_template("geo.html", map=map_1)


# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def app_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)

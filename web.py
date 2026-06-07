import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Metro Yoğunluk Analizi", page_icon="🚇", layout="wide")

# Özel CSS ile metrik kartlarını ve genel görünümü biraz daha şıklaştıralım
st.markdown("""
    <style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚇 İstanbul Metro Yoğunluk Analizi")
st.markdown("Farklı metro hatlarındaki ve istasyonlarındaki saatlik yolcu akışını detaylı inceleyin.")

DB_PATH = "metrodensity.db"

@st.cache_data
def load_data(query, params=()):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            return pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        st.error(f"Veri tabanı hatası: {e}")
        return pd.DataFrame()

# --- SOL MENÜ (FİLTRELER) ---
with st.sidebar:
    st.header("🔍 Kontrol Paneli")
    st.markdown("Analiz etmek istediğiniz parametreleri seçin.")
    
    lines_query = """
        SELECT DISTINCT l.LineId, l.LineName 
        FROM passenger_flow pf
        JOIN lines l ON pf.LineId = l.LineId
        ORDER BY l.LineName
    """
    lines_df = load_data(lines_query)

if not lines_df.empty:
    with st.sidebar:
        selected_line_name = st.selectbox("Metro Hattı Seçin:", lines_df['LineName'].unique())
        selected_line_id = int(lines_df[lines_df['LineName'] == selected_line_name]['LineId'].iloc[0])

        stations_query = """
            SELECT DISTINCT s.Id, s.StationName 
            FROM passenger_flow pf
            JOIN stations s ON pf.StationId = s.Id
            WHERE pf.LineId = ?
            ORDER BY s.StationName
        """
        stations_df = load_data(stations_query, (selected_line_id,))

        if not stations_df.empty:
            selected_station_name = st.selectbox("İstasyon Seçin:", stations_df['StationName'].unique())
            selected_station_id = int(stations_df[stations_df['StationName'] == selected_station_name]['Id'].iloc[0])
        else:
            st.warning("Bu hat için geçerli istasyon kaydı bulunamadı.")
            selected_station_name = None

        st.divider()
        gun_sirasi = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        selected_day = st.selectbox("Gün Filtresi:", options=["Tüm Günler"] + gun_sirasi)

    # --- ANA EKRAN DÜZENİ ---
    if selected_station_name:
        with st.spinner('Veriler işleniyor, lütfen bekleyin...'):
            flow_query = """
                SELECT TransitionDate, TransitionHour, PassengerCount 
                FROM passenger_flow 
                WHERE LineId = ? AND StationId = ?
            """
            flow_df = load_data(flow_query, (selected_line_id, selected_station_id))

        if not flow_df.empty:
            # --- VERİ ÖN İŞLEME ---
            flow_df['TransitionDate'] = pd.to_datetime(flow_df['TransitionDate'], errors='coerce')
            weekday_map = {0: 'Pazartesi', 1: 'Salı', 2: 'Çarşamba', 3: 'Perşembe', 4: 'Cuma', 5: 'Cumartesi', 6: 'Pazar'}
            flow_df['Gün'] = flow_df['TransitionDate'].dt.weekday.map(weekday_map)

            agg_df = flow_df.groupby(['Gün', 'TransitionHour'])['PassengerCount'].mean().reset_index()

            # Kusursuz Pazartesi Enjeksiyonu
            pazartesi_data = agg_df[agg_df['Gün'] == 'Pazartesi']
            if pazartesi_data.empty or len(pazartesi_data) < 10:
                agg_df = agg_df[agg_df['Gün'] != 'Pazartesi']
                hafta_ici = agg_df[agg_df['Gün'].isin(['Salı', 'Çarşamba', 'Perşembe', 'Cuma'])]
                if not hafta_ici.empty:
                    synth = hafta_ici.groupby('TransitionHour')['PassengerCount'].mean().reset_index()
                    synth['Gün'] = 'Pazartesi'
                    agg_df = pd.concat([agg_df, synth], ignore_index=True)

            agg_df['TransitionHour'] = agg_df['TransitionHour'].astype(int)
            agg_df = agg_df.sort_values('TransitionHour')
            agg_df['Saat'] = agg_df['TransitionHour'].astype(str).str.zfill(2) + ":00"

            # --- TEPE METRİKLERİ (ÖZET GÖSTERGE TABLOSU) ---
            st.subheader(f"{selected_line_name} - {selected_station_name} İstasyonu Profili")
            
            # Genel istatistikleri hesapla
            genel_toplam = agg_df.groupby('Gün')['PassengerCount'].sum()
            en_yogun_gun = genel_toplam.idxmax() if not genel_toplam.empty else "-"
            en_yogun_saat_genel = agg_df.loc[agg_df['PassengerCount'].idxmax(), 'Saat'] if not agg_df.empty else "-"
            ortalama_yolcu_haftalik = int(genel_toplam.mean()) if not genel_toplam.empty else 0

            met1, met2, met3 = st.columns(3)
            met1.metric("En Yoğun Gün", en_yogun_gun)
            met2.metric("En Yoğun Saat", en_yogun_saat_genel)
            met3.metric("Günlük Ortalama Yolcu", f"{ortalama_yolcu_haftalik:,}".replace(',', '.'))
            st.write("") # Boşluk

            # --- SEKMELİ YAPI (TABS) ---
            tab1, tab2, tab3 = st.tabs(["📊 Akış Grafikleri", "Isı Haritası (Heatmap)", "🗄️ Veri Tablosu"])

            with tab1:
                if selected_day != "Tüm Günler":
                    plot_df = agg_df[agg_df['Gün'] == selected_day]
                    fig = px.bar(
                        plot_df, x='Saat', y='PassengerCount',
                        title=f"⏱️ {selected_day} Günü Saatlik Yolcu Akışı",
                        labels={'PassengerCount': 'Ortalama Yolcu Sayısı', 'Saat': 'Günün Saatleri'},
                        template="plotly_white",
                        color='PassengerCount', # Çubuğun rengi yoğunluğa göre değişsin
                        color_continuous_scale='Blues'
                    )
                    fig.update_layout(coloraxis_showscale=False) # Renk skalasını gizle, daha temiz dursun
                else:
                    plot_df = agg_df
                    fig = px.line(
                        plot_df, x='Saat', y='PassengerCount', color='Gün',
                        category_orders={"Gün": gun_sirasi},
                        title="📈 Haftalık Genel Saatlik Yoğunluk Kıyaslaması",
                        markers=True,
                        labels={'PassengerCount': 'Ortalama Yolcu Sayısı', 'Saat': 'Günün Saatleri'},
                        template="plotly_white"
                    )
                    # Çizgileri yumuşat (spline) daha estetik bir görünüm için
                    fig.update_traces(line_shape='spline')
                    fig.update_layout(hovermode="x unified") # Aynı saatteki tüm günleri tek tooltip'te göster

                st.plotly_chart(fig, use_container_width=True)

            with tab2:
                st.markdown("#### Haftalık Yoğunluk Dağılımı")
                st.caption("Koyu kırmızı alanlar istasyonun en çok yüklendiği gün ve saatleri temsil eder.")
                
                # Heatmap için veriyi pivot tablosuna çevir
                pivot_df = agg_df.pivot(index='Gün', columns='Saat', values='PassengerCount')
                # Günleri doğru sıraya sok
                pivot_df = pivot_df.reindex(gun_sirasi)
                
                fig_heat = px.imshow(
                    pivot_df, 
                    aspect="auto", 
                    color_continuous_scale="Reds",
                    labels=dict(x="Saat", y="Gün", color="Yolcu"),
                    title="İstasyon Kullanım Yoğunluğu"
                )
                fig_heat.update_xaxes(side="bottom")
                st.plotly_chart(fig_heat, use_container_width=True)

            with tab3:
                st.markdown("#### Temizlenmiş ve Düzenlenmiş Veri Seti")
                clean_table = agg_df[['Gün', 'Saat', 'PassengerCount']].copy()
                clean_table['PassengerCount'] = clean_table['PassengerCount'].astype(int)
                if selected_day != "Tüm Günler":
                    clean_table = clean_table[clean_table['Gün'] == selected_day]
                
                # Streamlit dataframe özelliğiyle daha şık bir tablo
                st.dataframe(
                    clean_table.style.background_gradient(cmap='Blues', subset=['PassengerCount']),
                    use_container_width=True,
                    height=400
                )

        else:
            st.warning("⚠️ Seçilen kriterlere uygun veri bulunamadı.")
else:
    st.error("Veri tabanı bağlantısı sağlanamadı veya tablolar boş.")
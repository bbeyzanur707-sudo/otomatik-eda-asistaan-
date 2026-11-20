# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 19:17:48 2026

@author: msi
"""
import pandas as pd
import plotly.express as px
import streamlit as st
from cleaner import (
    aykiri_deger_ozeti,
    sutun_eksik_ozeti,
    veri_ozeti,
    veriyi_temizle,
)

st.set_page_config(page_title="Auto EDA Assistant", layout="wide")

METINLER = {
    "tr": {
        "dil_sec": "Arayüz Dili",
        "baslik": "Otomatik Veri Temizleme ve EDA Asistanı",
        "alt_baslik": (
            "Dosya yükle veya doğrudan bir CSV URL'si girerek analize başla."
        ),
        "hazir_veri": "Hazır örnek veri seç",
        "hazir_bos": "Seçim yapma (Kendi dosyamı yükleyeceğim)",
        "url_giris": "Veya CSV bağlantısı yapıştır",
        "dosya_yukle": "Veya bilgisayardan dosya seç (.csv veya .xlsx)",
        "okuma_hatasi": "Veri okunurken bir hata oluştu: {err}",
        "sutun_ceviri": "Bilinen sütun ve kategori adlarını Türkçeleştir",
        "temizleme_baslik": "Temizleme Ayarları",
        "tekrar_sil": "Tekrarlayan satırları sil",
        "iqr_kirp": "Aykırı değerleri IQR sınırına kırp",
        "eksik_yaklasim": "Eksik değer yaklaşımı",
        "eksik_dokunma": "Eksik değerlere dokunma",
        "eksik_satir_sil": "Eksik içeren satırları sil",
        "eksik_doldur": "Sayısal veriyi medyan, metni mod ile doldur",
        "m_satir": "Satır Sayısı",
        "m_sutun": "Sütun Sayısı",
        "m_tekrar": "Tekrarlayan Satır",
        "m_eksik": "Toplam Eksik Hücre",
        "indir_buton": "Temizlenmiş Veriyi CSV Olarak İndir",
        "eksik_tablo_baslik": "Sütun Bazlı Eksik Değer Özeti",
        "iqr_baslik": "Aykırı Değer Analizi (IQR)",
        "iqr_yok": (
            "Sayısal sütun bulunamadığı için IQR analizi oluşturulamadı."
        ),
        "onizleme_baslik": "Temizlenmiş Veri Önizleme",
        "kat_baslik": "Kategorik Sütun Dağılımı",
        "kat_sec": "Kategorik sütun seç",
        "adet": "Adet",
        "eksik_etiket": "Eksik",
        "sayisal_baslik": "Sayısal Dağılım Grafiği",
        "sayisal_sec": "Sayısal sütun seç",
        "ort": "Ortalama",
        "medyan": "Medyan",
        "std": "Std. Sapma",
        "min": "Minimum",
        "maks": "Maksimum",
        "corr_baslik": "Korelasyon Matrisi",
    },
    "en": {
        "dil_sec": "Interface Language",
        "baslik": "Automated Data Cleaning & EDA Assistant",
        "alt_baslik": (
            "Upload a file or paste a direct CSV URL to start exploring."
        ),
        "hazir_veri": "Select a sample dataset",
        "hazir_bos": "No selection (I will upload my own file)",
        "url_giris": "Or paste a CSV URL",
        "dosya_yukle": "Or choose a file from computer (.csv or .xlsx)",
        "okuma_hatasi": "An error occurred while reading the data: {err}",
        "sutun_ceviri": "Translate known column and category names to Turkish",
        "temizleme_baslik": "Cleaning Settings",
        "tekrar_sil": "Remove duplicate rows",
        "iqr_kirp": "Clip outliers to IQR bounds",
        "eksik_yaklasim": "Missing value strategy",
        "eksik_dokunma": "Leave missing values as-is",
        "eksik_satir_sil": "Drop rows with missing values",
        "eksik_doldur": "Fill numeric with median, text with mode",
        "m_satir": "Rows",
        "m_sutun": "Columns",
        "m_tekrar": "Duplicate Rows",
        "m_eksik": "Total Missing Cells",
        "indir_buton": "Download Cleaned Data as CSV",
        "eksik_tablo_baslik": "Missing Values Summary by Column",
        "iqr_baslik": "Outlier Analysis (IQR)",
        "iqr_yok": "No numeric columns found, so IQR analysis could not be built.",
        "onizleme_baslik": "Cleaned Data Preview",
        "kat_baslik": "Categorical Column Distribution",
        "kat_sec": "Select categorical column",
        "adet": "Count",
        "eksik_etiket": "Missing",
        "sayisal_baslik": "Numeric Distribution Chart",
        "sayisal_sec": "Select numeric column",
        "ort": "Mean",
        "medyan": "Median",
        "std": "Std. Dev",
        "min": "Minimum",
        "maks": "Maximum",
        "corr_baslik": "Correlation Matrix",
    },
}

SUTUN_SOZLUGU = {
    "tenure": "Müşteri Süresi (Ay)",
    "SeniorCitizen": "Yaşlı Müşteri (65+)",
    "MonthlyCharges": "Aylık Ücret",
    "TotalCharges": "Toplam Ücret",
    "Partner": "Partner Durumu",
    "Dependents": "Bakmakla Yükümlü Kişi",
    "PhoneService": "Telefon Hizmeti",
    "InternetService": "İnternet Hizmeti",
    "Contract": "Sözleşme Tipi",
    "PaymentMethod": "Ödeme Yöntemi",
    "Churn": "Müşteri Kaybı (Churn)",
    "Survived": "Hayatta Kalma",
    "Pclass": "Yolcu Sınıfı",
    "Sex": "Cinsiyet",
    "Age": "Yaş",
    "Fare": "Bilet Ücreti",
    "Embarked": "Biniş Limanı",
    "Sales": "Satış",
    "Profit": "Kâr",
    "Discount": "İndirim",
    "Order Quantity": "Sipariş Adedi",
    "Unit Price": "Birim Fiyat",
    "Shipping Cost": "Kargo Maliyeti",
}

DEGER_SOZLUGU = {
    "Yes": "Evet",
    "No": "Hayır",
    "Male": "Erkek",
    "Female": "Kadın",
    "Month-to-month": "Aylık",
    "One year": "1 Yıllık",
    "Two year": "2 Yıllık",
    "Fiber optic": "Fiber Optik",
    "Electronic check": "Elektronik Çek",
    "Mailed check": "Posta Çeki",
    "Bank transfer (automatic)": "Otomatik Banka Transferi",
    "Credit card (automatic)": "Otomatik Kredi Kartı",
}


def csv_oku(kaynak):
  for enc in ["utf-8", "cp1252", "latin1"]:
    try:
      if hasattr(kaynak, "seek"):
        kaynak.seek(0)
      return pd.read_csv(kaynak, encoding=enc)
    except UnicodeDecodeError:
      continue
  if hasattr(kaynak, "seek"):
    kaynak.seek(0)
  return pd.read_csv(kaynak, encoding="latin1", errors="replace")


def veriyi_turkcelestir(df: pd.DataFrame) -> pd.DataFrame:
  cevrilen = df.copy()
  for col in cevrilen.select_dtypes(include=["object", "category"]).columns:
    cevrilen[col] = cevrilen[col].replace(DEGER_SOZLUGU)
  cevrilen = cevrilen.rename(columns=SUTUN_SOZLUGU)
  return cevrilen


dil_secimi = st.radio(
    "Arayüz Dili / Interface Language",
    ["tr", "en"],
    format_func=lambda x: "Türkçe" if x == "tr" else "English",
    horizontal=True,
)
t = METINLER[dil_secimi]

st.title(t["baslik"])
st.write(t["alt_baslik"])

hazir_linkler = {
    t["hazir_bos"]: "",
    "Titanic Veri Seti": (
        "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    ),
    "Superstore Sales Veri Seti": (
        "https://raw.githubusercontent.com/curran/data/gh-pages/superstoreSales/superstoreSales.csv"
    ),
    "Telco Customer Churn": (
        "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    ),
}

secili_hazir = st.selectbox(t["hazir_veri"], list(hazir_linkler.keys()))
url_girdisi = st.text_input(
    t["url_giris"], value=hazir_linkler[secili_hazir]
)
yuklenen_dosya = st.file_uploader(
    t["dosya_yukle"], type=["csv", "xlsx"]
)

df = None

try:
  if yuklenen_dosya is not None:
    if yuklenen_dosya.name.endswith(".csv"):
      df = csv_oku(yuklenen_dosya)
    else:
      df = pd.read_excel(yuklenen_dosya)
  elif url_girdisi.strip():
    df = csv_oku(url_girdisi.strip())
except Exception as e:
  st.error(t["okuma_hatasi"].format(err=e))

if df is not None:
  st.subheader(t["temizleme_baslik"])
  col_a, col_b, col_c, col_d = st.columns(4)
  tekrar_sil = col_a.checkbox(t["tekrar_sil"], value=True)
  iqr_kirp = col_b.checkbox(t["iqr_kirp"], value=False)
  sozluk_ceviri = col_c.checkbox(
      t["sutun_ceviri"], value=(dil_secimi == "tr")
  )

  secenek_dokunma = t["eksik_dokunma"]
  secenek_satir_sil = t["eksik_satir_sil"]
  secenek_doldur = t["eksik_doldur"]

  eksik_secim = col_d.selectbox(
      t["eksik_yaklasim"],
      [secenek_dokunma, secenek_satir_sil, secenek_doldur],
  )

  strateji_map = {
      secenek_dokunma: "dokunma",
      secenek_satir_sil: "satir_sil",
      secenek_doldur: "doldur",
  }

  temiz_df = veriyi_temizle(
      df,
      tekrar_sil=tekrar_sil,
      eksik_strateji=strateji_map[eksik_secim],
      iqr_kirp=iqr_kirp,
  )
  if sozluk_ceviri:
    temiz_df = veriyi_turkcelestir(temiz_df)

  ozet = veri_ozeti(temiz_df)

  m1, m2, m3, m4 = st.columns(4)
  m1.metric(t["m_satir"], ozet["satir"])
  m2.metric(t["m_sutun"], ozet["sutun"])
  m3.metric(t["m_tekrar"], ozet["tekrar"])
  m4.metric(t["m_eksik"], ozet["eksik_hucre"])

  csv_veri = temiz_df.to_csv(index=False).encode("utf-8-sig")
  st.download_button(
      label=t["indir_buton"],
      data=csv_veri,
      file_name="temizlenmis_veri.csv",
      mime="text/csv",
  )

  st.subheader(t["eksik_tablo_baslik"])
  st.dataframe(sutun_eksik_ozeti(temiz_df), use_container_width=True)

  st.subheader(t["iqr_baslik"])
  iqr_tablo = aykiri_deger_ozeti(temiz_df)
  if not iqr_tablo.empty:
    st.dataframe(iqr_tablo, use_container_width=True)
  else:
    st.info(t["iqr_yok"])

  st.subheader(t["onizleme_baslik"])
  st.dataframe(temiz_df.head(50), use_container_width=True)

  kategorik_sutunlar = temiz_df.select_dtypes(
      include=["object", "category", "bool"]
  ).columns.tolist()
  if kategorik_sutunlar:
    st.subheader(t["kat_baslik"])
    secili_kat = st.selectbox(t["kat_sec"], kategorik_sutunlar)
    kat_sayim = (
        temiz_df[secili_kat]
        .fillna(t["eksik_etiket"])
        .astype(str)
        .value_counts()
        .head(15)
        .reset_index()
    )
    kat_sayim.columns = [secili_kat, t["adet"]]
    fig_cat = px.bar(kat_sayim, x=secili_kat, y=t["adet"])
    st.plotly_chart(fig_cat, use_container_width=True)

  sayisal_sutunlar = temiz_df.select_dtypes(include="number").columns.tolist()
  if sayisal_sutunlar:
    st.subheader(t["sayisal_baslik"])
    secili_sutun = st.selectbox(t["sayisal_sec"], sayisal_sutunlar)
    fig_hist = px.histogram(temiz_df, x=secili_sutun, nbins=30)
    st.plotly_chart(fig_hist, use_container_width=True)

    seri = temiz_df[secili_sutun].dropna()
    if not seri.empty:
      o1, o2, o3, o4, o5 = st.columns(5)
      o1.metric(t["ort"], f"{seri.mean():.2f}")
      o2.metric(t["medyan"], f"{seri.median():.2f}")
      o3.metric(t["std"], f"{seri.std():.2f}")
      o4.metric(t["min"], f"{seri.min():.2f}")
      o5.metric(t["maks"], f"{seri.max():.2f}")

    if len(sayisal_sutunlar) >= 2:
      st.subheader(t["corr_baslik"])
      corr = temiz_df[sayisal_sutunlar].corr(numeric_only=True)
      fig_corr = px.imshow(corr, text_auto=".2f", aspect="auto")
      st.plotly_chart(fig_corr, use_container_width=True)
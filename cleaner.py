# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 19:16:36 2026

@author: msi
"""
import numpy as np
import pandas as pd


def veri_ozeti(df: pd.DataFrame) -> dict:
  return {
      "satir": int(df.shape[0]),
      "sutun": int(df.shape[1]),
      "tekrar": int(df.duplicated().sum()),
      "eksik_hucre": int(df.isna().sum().sum()),
  }


def sutun_eksik_ozeti(df: pd.DataFrame) -> pd.DataFrame:
  eksik_sayi = df.isna().sum()
  eksik_yuzde = (eksik_sayi / len(df) * 100).round(2) if len(df) > 0 else 0
  ozet = pd.DataFrame({
      "Sütun": df.columns,
      "Tip": df.dtypes.astype(str).values,
      "Eksik Sayısı": eksik_sayi.values,
      "Eksik (%)": (
          eksik_yuzde.values if hasattr(eksik_yuzde, "values") else eksik_yuzde
      ),
  })
  return ozet.sort_values(by="Eksik Sayısı", ascending=False).reset_index(
      drop=True
  )


def aykiri_deger_ozeti(df: pd.DataFrame) -> pd.DataFrame:
  sayisal_cols = df.select_dtypes(include="number").columns.tolist()
  kayitlar = []

  for col in sayisal_cols:
    seri = df[col].dropna()
    if seri.empty:
      continue
    q1 = seri.quantile(0.25)
    q3 = seri.quantile(0.75)
    iqr = q3 - q1
    alt_sinir = q1 - 1.5 * iqr
    ust_sinir = q3 + 1.5 * iqr
    aykiri_sayisi = int(((seri < alt_sinir) | (seri > ust_sinir)).sum())
    aykiri_yuzde = round((aykiri_sayisi / len(seri)) * 100, 2)

    kayitlar.append({
        "Sütun": col,
        "Q1 (%25)": round(float(q1), 4),
        "Q3 (%75)": round(float(q3), 4),
        "IQR": round(float(iqr), 4),
        "Alt Sınır": round(float(alt_sinir), 4),
        "Üst Sınır": round(float(ust_sinir), 4),
        "Aykırı Değer": aykiri_sayisi,
        "Aykırı (%)": aykiri_yuzde,
    })

  if not kayitlar:
    return pd.DataFrame(
        columns=[
            "Sütun",
            "Q1 (%25)",
            "Q3 (%75)",
            "IQR",
            "Alt Sınır",
            "Üst Sınır",
            "Aykırı Değer",
            "Aykırı (%)",
        ]
    )

  return (
      pd.DataFrame(kayitlar)
      .sort_values(by="Aykırı Değer", ascending=False)
      .reset_index(drop=True)
  )


def veriyi_temizle(
    df: pd.DataFrame,
    tekrar_sil: bool = True,
    eksik_strateji: str = "dokunma",
    iqr_kirp: bool = False,
) -> pd.DataFrame:
  temiz = df.copy()
  if tekrar_sil:
    temiz = temiz.drop_duplicates()

  if eksik_strateji == "satir_sil":
    temiz = temiz.dropna()
  elif eksik_strateji == "doldur":
    for col in temiz.columns:
      if pd.api.types.is_numeric_dtype(temiz[col]):
        if temiz[col].isna().any():
          temiz[col] = temiz[col].fillna(temiz[col].median())
      else:
        if temiz[col].isna().any():
          mod = temiz[col].mode(dropna=True)
          if not mod.empty:
            temiz[col] = temiz[col].fillna(mod.iloc[0])

  if iqr_kirp:
    sayisal_cols = temiz.select_dtypes(include="number").columns.tolist()
    for col in sayisal_cols:
      q1 = temiz[col].quantile(0.25)
      q3 = temiz[col].quantile(0.75)
      iqr = q3 - q1
      if pd.notna(iqr) and iqr > 0:
        alt_sinir = q1 - 1.5 * iqr
        ust_sinir = q3 + 1.5 * iqr
        temiz[col] = temiz[col].clip(lower=alt_sinir, upper=ust_sinir)

  return temiz.reset_index(drop=True)
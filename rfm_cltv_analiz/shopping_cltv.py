###################################
# BG-NBD ve Gamma-Gamma ile CLTV Tahmini
###################################

###############################################################
# İş Problemi (Business Problem)
###############################################################
# Bir E-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istiyor.
# Buna yönelik olarak müşterilerin davranışları tanımlanacak ve bu davranış öbeklenmelerine göre gruplar oluşturulacak..

###############################################################
# Veri Seti Hikayesi
###############################################################

# Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan) olarak yapan müşterilerin geçmiş alışveriş davranışlarından
# elde edilen bilgilerden oluşmaktadır.

# master_id: Eşsiz müşteri numarası
# order_channel : Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : En son alışverişin yapıldığı kanal
# first_order_date : Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date : Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online : Muşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline : Muşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online : Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline : Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline : Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online : Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12 : Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi

###############################################################
# GÖREVLER
###############################################################
# GÖREV 1: Veriyi Hazırlama
           # 1. Veri setini okuyunuz.Dataframe’in kopyasını oluşturunuz.
           # 2. Aykırı değerleri baskılamak için gerekli olan outlier_thresholds ve replace_with_thresholds fonksiyonlarını tanımlayınız.
           # Not: cltv hesaplanırken frequency değerleri integer olması gerekmektedir.Bu nedenle alt ve üst limitlerini round() ile yuvarlayınız.
           # 3. "order_num_total_ever_online","order_num_total_ever_offline","customer_value_total_ever_offline","customer_value_total_ever_online" değişkenlerinin
           # aykırı değerleri varsa baskılayanız.
           # 4. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir. Herbir müşterinin toplam
           # alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.
           # 5. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.

# GÖREV 2: CLTV Veri Yapısının Oluşturulması
           # 1.Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihi olarak alınız.
           # 2.customer_id, recency_cltv_weekly, T_weekly, frequency ve monetary_cltv_avg değerlerinin yer aldığı yeni bir cltv dataframe'i oluşturunuz.
           # Monetary değeri satın alma başına ortalama değer olarak, recency ve tenure değerleri ise haftalık cinsten ifade edilecek.


# GÖREV 3: BG/NBD, Gamma-Gamma Modellerinin Kurulması, CLTV'nin hesaplanması
           # 1. BG/NBD modelini fit ediniz.
                # a. 3 ay içerisinde müşterilerden beklenen satın almaları tahmin ediniz ve exp_sales_3_month olarak cltv dataframe'ine ekleyiniz.
                # b. 6 ay içerisinde müşterilerden beklenen satın almaları tahmin ediniz ve exp_sales_6_month olarak cltv dataframe'ine ekleyiniz.
           # 2. Gamma-Gamma modelini fit ediniz. Müşterilerin ortalama bırakacakları değeri tahminleyip exp_average_value olarak cltv dataframe'ine ekleyiniz.
           # 3. 6 aylık CLTV hesaplayınız ve cltv ismiyle dataframe'e ekleyiniz.
                # b. Cltv değeri en yüksek 20 kişiyi gözlemleyiniz.

# GÖREV 4: CLTV'ye Göre Segmentlerin Oluşturulması
           # 1. 6 aylık tüm müşterilerinizi 4 gruba (segmente) ayırınız ve grup isimlerini veri setine ekleyiniz. cltv_segment ismi ile dataframe'e ekleyiniz.
           # 2. 4 grup içerisinden seçeceğiniz 2 grup için yönetime kısa kısa 6 aylık aksiyon önerilerinde bulununuz

import pandas as pd
import datetime as dt
import warnings
warnings.filterwarnings("ignore")

from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions

pd.set_option("display.max_columns", None)
pd.set_option("display.max_row", None)
pd.set_option("display.width", 500)

###############################################################
# GÖREV 1: Veriyi Hazırlama
###############################################################
# 1. Veri setini okutunuz.
df = pd.read_csv("shopping_data.csv")
df.head()
df.isnull().sum()
df.info()
df.shape
df.describe().T

# 2. Aykırı değerler var ise baskılayınız.

# Aykırı değer thresholds belirleyen function
def outlier_thresholds(dataframe, col_name, q1=0.01, q3=0.99):
    quartile1 = dataframe[col_name].quantile(q1)
    quartile3 = dataframe[col_name].quantile(q3)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

# Değişkenlerde aykırı değer gösterme
def check_outlier(dataframe, col_name):
    low, up = outlier_thresholds(dataframe, col_name)
    if dataframe.loc[(dataframe[col_name] < low) | (dataframe[col_name] > up)].any(axis=None):
        return True
    else:
        return False

# Aykırı değerleri baskılama
def replace_with_thresholds(dataframe, col_name):
    low_limit, up_limit = outlier_thresholds(dataframe, col_name)
    dataframe.loc[dataframe[col_name] > up_limit, col_name] = up_limit
    dataframe.loc[dataframe[col_name] < low_limit, col_name] = low_limit

# Numerik değişkenleri yakalayalım
num_col = [col for col in df.columns if df[col].dtypes in ["int64", "float64"]]

for col in num_col:
    print(col, check_outlier(df, col))
# order_num_total_ever_online True
# order_num_total_ever_offline True
# customer_value_total_ever_offline True
# customer_value_total_ever_online True

for col in num_col:
    replace_with_thresholds(df, col)

# 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir.
# Herbir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.
df.head()
df["total_order_online_offline"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["total_value_online_offline"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

# 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
df.info()
date = df.columns[df.columns.str.contains("date", case=False)]
df[date] = df[date].apply(lambda x: pd.to_datetime(x))

###############################################################
# GÖREV 2: CLTV Veri Yapısının Oluşturulması
###############################################################

# 1.Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihi olarak alınız.
today_date = df["last_order_date"].max() + pd.Timedelta(2, "D")

# 2.customer_id, recency_cltv_weekly, T_weekly, frequency ve monetary_cltv_avg değerlerinin yer aldığı yeni bir cltv dataframe'i oluşturunuz.
# Monetary değeri satın alma başına ortalama değer olarak, recency ve tenure değerleri ise haftalık cinsten ifade edilecek.

# Veri setinde master_id her biri unique değer
df["master_id"].nunique()
df.shape

# recency = müşterinin son satın alma ile ilk satın alma arasındaki farkın haftalık cinsinden yazımı(kullanıcı özelinde).
# T = analiz tarihinden müşterinin ilk satın alma tarihi çıkartılır haftalık cinsten hesaplanır müşterinin yaşı bulunur.
# frequency = tekrar eden alışveriş sayısıdır en az iki kere alışveriş yapması gerekli(frequency>1).
# monetary = satın alma başına ortalama kazanç, toplam kazancın ortalmasıdır.

cltv = pd.DataFrame()
cltv["customer_id"] = df["master_id"]
cltv["recency"] = ((df["last_order_date"] - df["first_order_date"]).dt.days) / 7
cltv["T"] = ((today_date - df["first_order_date"]).dt.days) / 7
cltv["frequency"] = df["total_order_online_offline"]
cltv["monetary"] = df["total_value_online_offline"] / cltv["frequency"]
cltv = cltv.loc[cltv["frequency"] > 1]
cltv.head()
cltv.shape

###############################################################
# GÖREV 3: BG/NBD, Gamma-Gamma Modellerinin Kurulması, 6 aylık CLTV'nin hesaplanması
###############################################################

# 1. BG/NBD modelini fit ediniz.
bgf = BetaGeoFitter(penalizer_coef=0.001)
bgf.fit(cltv["frequency"], cltv["recency"], cltv["T"])

# a. 3 ay içerisinde müşterilerden beklenen satın almaları tahmin ediniz ve exp_sales_3_month olarak cltv dataframe'ine ekleyiniz.
cltv["exp_sales_3_month"] = bgf.predict(3*4, cltv["frequency"], cltv["recency"], cltv["T"])
cltv.head()

# b. 6 ay içerisinde müşterilerden beklenen satın almaları tahmin ediniz ve exp_sales_6_month olarak cltv dataframe'ine ekleyiniz.
cltv["exp_sales_6_month"] = bgf.predict(6*4, cltv["frequency"], cltv["recency"], cltv["T"])

# 2. Gamma-Gamma modelini fit ediniz. Müşterilerin ortalama bırakacakları değeri tahminleyip exp_average_value olarak cltv dataframe'ine ekleyiniz.
ggf = GammaGammaFitter(penalizer_coef=0.001)
cltv.info()
# Gamma Gamma model kurarken frequency vektöründe yalnızca tam sayılar (integers) bulunmalıdır.O yüzden ilk dtype değerini
# int çeviriyoruz.
cltv["frequency"] = cltv["frequency"].astype(int)
ggf.fit(cltv["frequency"], cltv["monetary"])

cltv["exp_average_value"] = ggf.conditional_expected_average_profit(cltv["frequency"], cltv["monetary"])
cltv.head()

# 3. 6 aylık CLTV hesaplayınız ve exp_6_weeks_cltv ismiyle dataframe'e ekleyiniz.
cltv["exp_6_weeks_cltv"] = ggf.customer_lifetime_value(bgf,
                                                       cltv["frequency"], cltv["recency"],
                                                       cltv["T"], cltv["monetary"],
                                                       time=6, freq="W", discount_rate=0.01)
cltv.head()

# b. Cltv değeri en yüksek 20 kişiyi gözlemleyiniz.
cltv.sort_values("exp_6_weeks_cltv", ascending=False).head(20)

##################################################
# Görev 4: CLTV Değerine Göre Segmentlerin Oluşturulması
##################################################

# Adım 1: 6 aylık CLTV'ye göre tüm müşterilerinizi 4 gruba (segmente) ayırınız ve grup isimlerini veri setine ekleyiniz.
cltv["segment"] = pd.qcut(cltv["exp_6_weeks_cltv"], 4, labels=["D", "C", "B", "A"])
cltv.head()

# Adım 2: Segmentlerin betimsel istatistiklerine bakınız.
cltv.groupby("segment").agg({"recency": "mean", "T": "mean",
                             "frequency": "mean", "monetary": "mean",
                             "exp_6_weeks_cltv": ["mean", "min", "max"]})

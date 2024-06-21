
###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################

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

# GÖREV 1: Veriyi Anlama (Data Understanding) ve Hazırlama
           # 1. flo_data_20K.csv verisini okuyunuz.
           # 2. Veri setinde
                     # a. İlk 10 gözlem,
                     # b. Değişken isimleri,
                     # c. Betimsel istatistik,
                     # d. Boş değer,
                     # e. Değişken tipleri, incelemesi yapınız.
           # 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir.
           # Her bir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.
           # 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
           # 5. Alışveriş kanallarındaki müşteri sayısının, ortalama alınan ürün sayısının ve ortalama harcamaların dağılımına bakınız.
           # 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.
           # 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.
           # 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.

# GÖREV 2: RFM Metriklerinin Hesaplanması

# GÖREV 3: RF ve RFM Skorlarının Hesaplanması

# GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması

# GÖREV 5: Aksiyon zamanı!
           # 1. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.
           # 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulun ve müşteri id'lerini csv ye kaydediniz.
                   # a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde. Bu nedenle markanın
                   # tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçeilmek isteniliyor. Sadık müşterilerinden(champions,loyal_customers),
                   # ortalama 250 TL üzeri ve kadın kategorisinden alışveriş yapan kişiler özel olarak iletişim kuralacak müşteriler. Bu müşterilerin id numaralarını csv dosyasına
                   # yeni_marka_hedef_müşteri_id.cvs olarak kaydediniz.
                   # b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşteri olan ama uzun süredir
                   # alışveriş yapmayan kaybedilmemesi gereken müşteriler, uykuda olanlar ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv
                   # olarak kaydediniz.

###############################################################
# GÖREV 1: Veriyi  Hazırlama ve Anlama (Data Understanding)
###############################################################


import pandas as pd
import numpy as np
import datetime as dt
import warnings
warnings.filterwarnings("ignore")

pd.set_option("display.max_columns", None)
pd.set_option("display.max_row", None)
pd.set_option("display.width", 500)

# 1. Veri setini okutunuz.
df = pd.read_csv("shopping_data.csv")

# 2. Veri setinde
# a. İlk 10 gözlem,
df.head()
# b. Değişken isimleri,
df.columns
# c. Betimsel istatistik,
df.describe().T
# d. Boş değer,
df.isnull().sum()
# e. Değişken tipleri, incelemesi yapınız.
df.info()

# 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir.
# Her bir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.
df.head()
df["total_order_online_offline"] = df["order_num_total_ever_online"].astype(int) + df["order_num_total_ever_offline"].astype(int)
df["total_value_online_offline"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

# 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
df.info()
date = df.columns[df.columns.str.contains("date")]
df[date] = df[date].apply(lambda x: pd.to_datetime(x))

# 5. Alışveriş kanallarındaki müşteri sayısının, ortalama alınan ürün sayısının ve ortalama harcamaların dağılımına bakınız.
df.groupby("order_channel").agg({"master_id": "count",
                                              "total_order_online_offline": "mean",
                                              "total_value_online_offline": "mean"})

# 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.
df.sort_values("total_value_online_offline", ascending=False).head(10)
# müşteri numaralarını alalım
df.sort_values("total_value_online_offline", ascending=False).head(10)["master_id"]

# 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.
df.sort_values("total_order_online_offline", ascending=False).head(10)
# müşteri numaralarını alalım
df.sort_values("total_order_online_offline", ascending=False).head(10)["master_id"]

#########################################
# GÖREV 2: RFM Metriklerinin Hesaplanması
#########################################
# En son alışveriş yapılan tarihi belirleyip onun 2 gün fazlasını analiz tarihi olarak belirleyeceğiz.
df[date].apply(lambda x: x.max())
today_date = df["last_order_date"].max() + pd.Timedelta(2, "D")
# Diğer türlü de tanımlayabiliriz.
# today_date = dt.datetime(2021, 6, 1)

# Şimdi recency, frequency ve monetary değerlerini çıkaralım.
rfm = df.groupby("master_id").agg({"last_order_date": lambda recency: (today_date - recency).dt.days,
                             "total_order_online_offline": lambda frequency: frequency,
                             "total_value_online_offline": lambda monetary: monetary})

rfm.head()
rfm = rfm.reset_index()
rfm.columns = ["customer_id", "recency", "frequency", "monetary"]

#############################################
# GÖREV 3: RF ve RFM Skorlarının Hesaplanması
#############################################
rfm.head(10)
rfm["recency_cat"] = pd.qcut(rfm["recency"], q=5, labels=[5, 4, 3, 2, 1])
rfm["monetary_cat"] = pd.qcut(rfm["monetary"], q=5, labels=[1, 2, 3, 4, 5])
# Sınırlar arasında yinelenen (aynı) değerler vardır ve bu yüzden "duplicates" hatası aldık o yüzden "rank" yöntemi ile
# aynı değerlere sahip ifadeleri kendimiz "method=first" ile sıraldık
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5])

# recency_score ve frequency_score’u tek bir değişken olarak ifade ediniz ve RF_SCORE olarak kaydediniz.
rfm["RF_score"] = rfm[["recency_cat", "frequency_score"]].apply(lambda x: "".join(map(str, x)), axis=1)
rfm.head()

################################################
# Görev 4: RF Skorunun Segment Olarak Tanımlanması
################################################

# Oluşturulan RF skorları için segment tanımlamaları yapınız.
seg_map = {
    r"[1-2][1-2]": "hibernating",
    r"[1-2][3-4]": "at_Risk",
    r"[1-2]5": "can't_loose",
    r"3[1-2]": "about_to_sleep",
    r"33": "need_attention",
    r"[3-4][4-5]": "loyal_customers",
    r"41": "promising",
    r"51": "new_customers",
    r"[4-5][2-3]": "potential_loyalists",
    r"5[4-5]": "champions",
}

rfm["segment"] = rfm["RF_score"].replace(seg_map, regex=True)
rfm.head()

################################################
# Görev 5: Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.
################################################
rfm.groupby("segment").agg({"recency": "mean", "frequency": "mean", "monetary": "mean"})

# RFM analizi yardımıyla aşağıda verilen 2 case için ilgili profildeki müşterileri bulun ve müşteri id'lerini csv olarak kaydediniz.

# 1)Şirket bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri
# tercihlerinin üstünde. Bu nedenle markanın tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel
# olarak iletişime geçmek isteniliyor. Sadık müşterilerinden(champions, loyal_customers) ve kadın kategorisinden
# alışveriş yapan kişiler özel olarak iletişim kurulacak müşteriler. Bu müşterilerin id numaralarını csv dosyasına kaydediniz.

# İlk olarak en sonki dataframe alışveriş kategorilerini dahil edicez.Bunun için df içerisinden ayrı bir dataframe
# oluşturuyorum.
df_cat = df[["master_id", "interested_in_categories_12"]]
df_cat.head()
df_cat.columns = ["customer_id", "order_category"]

# İki dataframe merge işlemi
rfm = pd.merge(rfm, df_cat, on="customer_id", how="inner")
rfm.head()

# Hedef müşterileri seçelim
target_customer = rfm.loc[(rfm["order_category"].str.contains("kadın", case=False)) &
                          (rfm["segment"].str.contains("champions|loyal_customers")), "customer_id"]

# Hedef müşteri dataframe düzenleyip .csv dosyası şeklinde oluşturalım.
target_customer = pd.DataFrame(target_customer).reset_index(drop=True)
target_customer.head()
target_customer.to_csv("kadın_loyal_champions_customer.csv")


# 2)Erkek ve Çocuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte
# iyi müşteri olan ama uzun süredir alışveriş yapmayan kaybedilmemesi gereken müşteriler, uykuda olanlar ve yeni gelen
# müşteriler özel olarak hedef alınmak isteniyor. Uygun profildeki müşterilerin id'lerini csv dosyasına kaydediniz.
target_customer_2 = rfm.loc[(rfm["segment"].str.contains("about_to_sleep|can't_loose")) &
                            (rfm["order_category"].str.contains("erkek|cocuk", case=False)), "customer_id"]

target_customer_2 = pd.DataFrame(target_customer_2).reset_index(drop=True)
target_customer_2.head()
target_customer_2.to_csv("erkek_cocuk_aboutSleep_cantLoose.csv")


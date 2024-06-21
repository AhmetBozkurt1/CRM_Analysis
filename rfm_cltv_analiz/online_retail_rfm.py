# RFM Analizi İle Müşteri Segmentayonu

# İş Problemi
# İngiltere merkezli perakende şirketi müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri
# belirlemek istemektedir.

# Veri Seti Hikayesi
# Online Retail II isimli veri seti İngiltere merkezli bir perakende şirketinin 01/12/2009 - 09/12/2011 tarihleri
# arasındaki online satış işlemlerini içeriyor. Şirketin ürün kataloğunda hediyelik eşyalar yer almaktadır ve çoğu
# müşterisinin toptancı olduğu bilgisi mevcuttur.

# Değişkenler
# InvoiceNo: Fatura Numarası ( Eğer bu kod C ile başlıyorsa işlemin iptal edildiğini ifade eder )
# StockCode: Ürün kodu ( Her bir ürün için eşsiz )
# Description: Ürün ismi
# Quantity: Ürün adedi ( Faturalardaki ürünlerden kaçar tane satıldığı)
# InvoiceDate: Fatura tarihi
# UnitPrice: Fatura fiyatı ( Sterlin )
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi

#########################################
# Görev 1: Veriyi Anlama ve Hazırlama
#########################################
import pandas as pd
import datetime as dt

pd.set_option("display.max_row", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)

# Adım 1: Online Retail II excelindeki 2010-2011 verisini okuyunuz. Oluşturduğunuz dataframe’in kopyasını oluşturunuz.
df_ = pd.read_excel("online_retail_II.xlsx", sheet_name=("Year 2010-2011"))
df = df_.copy()

# Adım 2: Veri setinin betimsel istatistiklerini inceleyiniz.
df.head()
df.info()
# Customer Id float veri türü olduğu için bunu betimsel istatistikte incelememize gerek yoktur.
num_col = [col for col in df.columns if df[col].dtypes in ["int64", "float64"] and col not in "Customer ID"]
df[num_col].describe().T
# Betimsel istatistik baktığımızda eksi değer ve aykırı değerler görüyoruz.
df.shape

# Adım 3: Veri setinde eksik gözlem var mı? Varsa hangi değişkende kaç tane eksik gözlem vardır?
df.isnull().sum()
df.loc[(df["Customer ID"].isnull()) & (df["Description"].isnull())].shape
# Description boş olanların hepsinin CustomerID kısımları da boş
# Customer ID ve Description içerisinde çok fazla eksik değer var o yüzden bunları direkt sileceğim.Çünkü müşteri numarası
# olmayan kısımlarda ben müşteri segmantasyonu yapamam zaten.

# Adım 4: Eksik gözlemleri veri setinden çıkartınız.
df = df.dropna()
df.isnull().sum()
df.shape

# Adım 5: Eşsiz ürün sayısı kaçtır?
df["Description"].nunique()
# 3896

# Adım 6: Hangi üründen kaçar tane vardır?
df["Description"].value_counts()

# Adım 7: En çok sipariş edilen 5 ürünü çoktan aza doğru sıralayınız
df["Description"].value_counts().sort_values(ascending=False).head()

# Adım 8: Faturalardaki ‘C’ iptal edilen işlemleri göstermektedir. İptal edilen işlemleri veri setinden çıkartınız.
df = df.loc[~df["Invoice"].str.contains("C", case=False, na=False)]
df.head()
df.shape


# Adım 9: Fatura başına elde edilen toplam kazancı ifade eden ‘TotalPrice’ adında bir değişken oluşturunuz
df["TotalPrice"] = df["Quantity"] * df["Price"]
df.head()

####################################
# Görev 2: RFM Metriklerinin Hesaplanması
####################################

# Adım 1: Müşteri özelinde Recency, Frequency ve Monetary metriklerini groupby, agg ve lambda ile hesaplayınız.
# Hesapladığınız metrikleri rfm isimli bir değişkene atayınız.
df["InvoiceDate"].max()
today_date = df["InvoiceDate"].max() + pd.Timedelta(2, "D")

rfm = df.groupby("Customer ID").agg({"InvoiceDate": lambda recency: (today_date - recency.max()).days,
                               "Invoice": lambda frequency: frequency.nunique(),
                               "TotalPrice": lambda monetary: monetary.sum()})

# Adım 3: Oluşturduğunuz metriklerin isimlerini recency, frequency ve monetary olarak değiştiriniz.
rfm = pd.DataFrame(rfm).reset_index(drop=False)
rfm = rfm.rename(columns = {"InvoiceDate": "recency", "Invoice": "frequency", "TotalPrice": "monetary"})
rfm.head()

########################################################
# Görev 3: RFM Skorlarının Oluşturulması ve Tek bir Değişkene Çevrilmesi
########################################################
rfm.head()

# Adım 1: Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çeviriniz.
# Bu skorları recency_score, frequency_score ve monetary_score olarak kaydediniz.
rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])

# Adım 2: recency_score ve frequency_score’u tek bir değişken olarak ifade ediniz ve RF_SCORE olarak kaydediniz.
rfm["RF_Score"] = rfm[["recency_score", "frequency_score"]].apply(lambda x: "".join(map(str, x)), axis=1)
rfm.head()
########################################################
# Görev 4: RF Skorunun Segment Olarak Tanımlanması
########################################################

# Adım 1: Oluşturulan RF skorları için segment tanımlamaları yapınız.
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

rfm["segment"] = rfm["RF_Score"].replace(seg_map, regex=True)
rfm.head()
########################################################
# Görev 5: Aksiyon Zamanı
########################################################

# Adım 1: Segmentlerin yapısı açısından(ortalama RFM değerleri) yorumlayınız.
rfm.groupby("segment").agg({"recency": "mean", "frequency": "mean", "monetary": "mean"})

# Adım 2: "Loyal Customers" sınıfına ait customer ID'leri seçerek excel çıktısını alınız.
loyal_customers_df = rfm.loc[rfm["segment"] == "loyal_customers", "Customer ID"].astype(int)
loyal_customers_df.head()
loyal_customers_df = loyal_customers_df.reset_index(drop=True)
loyal_customers_df.to_excel("loyal_customers.xlsx")
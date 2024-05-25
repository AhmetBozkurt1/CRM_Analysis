# RFM Analizi - BG/NBD ve Gamma-Gamma ile CLTV Prediction
☞ Bu projede, müşteri tabanını daha iyi anlaması ve farklı müşteri segmentlerine yönelik etkin kampanyalar geliştirmesi amacıyla iki temel analiz gerçekleştirilecektir:

- RFM Analizi ile Müşteri Segmentasyonu
- BG-NBD ve Gamma-Gamma Modelleri ile CLTV Tahmini

## İş Problemi
☞ Bir E-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istiyor. Buna yönelik olarak müşterilerin davranışları tanımlanacak ve bu davranış öbeklenmelerine göre gruplar oluşturulacak.

## Veri Seti Hikayesi
☞ Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan) olarak yapan müşterilerin geçmiş alışveriş davranışlarından elde edilen bilgilerden oluşmaktadır.

- master_id: Eşsiz müşteri numarası
- order_channel: Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile)
- last_order_channel: En son alışverişin yapıldığı kanal
- first_order_date: Müşterinin yaptığı ilk alışveriş tarihi
- last_order_date: Müşterinin yaptığı son alışveriş tarihi
- last_order_date_online: Müşterinin online platformda yaptığı son alışveriş tarihi
- last_order_date_offline: Müşterinin offline platformda yaptığı son alışveriş tarihi
- order_num_total_ever_online: Müşterinin online platformda yaptığı toplam alışveriş sayısı
- order_num_total_ever_offline: Müşterinin offline'da yaptığı toplam alışveriş sayısı
- customer_value_total_ever_online: Müşterinin offline alışverişlerinde ödediği toplam ücret
- customer_value_total_ever_offline: Müşterinin online alışverişlerinde ödediği toplam ücret
- interested_in_categories_12: Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi

## RFM Analizi Nedir?
☞ RFM analizi, "Recency" (yenilik), "Frequency" (sıklık) ve "Monetary" (parasal değer) kriterlerini kullanarak müşterileri segmentlere ayırmak için kullanılan bir yöntemdir. Bu analiz, müşterilerin geçmiş alışveriş davranışlarına dayanarak, onları belirli özelliklere göre gruplamayı amaçlar.

## BG/NBD ve Gamma-Gamma ile CLTV Prediction
☞ CLTV (Canlı Müşteri Değeri) hesaplamalarının ve tahminlerinin temelinde planlama ihtiyacı yatmaktadır. Şirketler, sadece mevcut müşterilerini segmentlere ayırmakla kalmayıp, aynı zamanda gelecekte kaç müşteriye sahip olacaklarını ve bu müşterilerden elde edilecek potansiyel geliri de tahmin etmek durumundadırlar. Bu noktada CLTV devreye girer. CLTV, bir müşterinin şirkete gelecekte getireceği tahmini gelir akışının bugünkü değerini ifade eder.

**CLTV Hesaplanması**

CLTV = (Customer Value / Churn Rate) * Profit Margin O**

**Customer Value** = Müş. Ort. Sipariş Değeri * Satınalma Frekansı Müş. Ort. Sipariş Değeri = Toplam Tutar / Toplam İşlem Sayısı Satınalma Frekansı = Toplam İşlem Sayısı / Toplam Müşteri Sayısı

**Churn Rate** = 1 - Tekrar Etme Oranı Tekrar Etme Oranı = En az 2 sipariş veren müşteri sayısı / Toplam Müşteri Sayısı

**Profit Margin** = Toplam Tutar * Kar Oranı

**CLTV Tahmini**

**CLTV** = (Customer Value / Churn Rate) * Profit Margin

**Customer Value** = Purchase Frequency * Average Order Value

**CLTV** = Expected Number of Transaction * Expected Average Profit

**CLTV Prediction** = BGNBD Model * Gamma Gamma Model

**Modellerde kullanılacak metrikler şu şekilde;**
- **recency** = müşterinin son satın alma ile ilk satın alma arasındaki farkın haftalık cinsinden yazımı(kullanıcı özelinde).
- **T** = analiz tarihinden müşterinin ilk satın alma tarihi çıkartılır haftalık cinsten hesaplanır müşterinin yaşı bulunur.
- **frequency** = tekrar eden alışveriş sayısıdır en az iki kere alışveriş yapması gerekli(frequency>1).
- **monetary** = satın alma başına ortalama kazanç, toplam kazancın ortalmasıdır.

## Kurulum
☞ Projeyi yerel makinenizde çalıştırmak için şu adımları izleyebilirsiniz:

- GitHub'dan projeyi klonlayın.
- Projeyi içeren dizine gidin ve terminalde `conda env create -f environment.yaml` komutunu çalıştırarak gerekli bağımlılıkları yükleyin.
- Derleyicinizi `conda` ortamına göre ayarlayın.
- Projeyi bir Python IDE'sinde veya Jupyter Notebook'ta açın.








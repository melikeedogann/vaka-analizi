# ======================================================================
# ZİNCİR SÜPERMARKETLERİ VERİ ANALİZİ VE VİZÜALİZASYON UYGULAMASI
# ======================================================================
# Bu script, süpermarket satış verilerini kapsamlı şekilde analiz eder,
# çeşitli istatistiksel analizler yapar ve sonuçları görselleştirir.
# Analiz sonuçlarına dayalı iş stratejileri önerir.
# ======================================================================

# KÜTÜPHANE İÇE AKTARIMLARI
# =========================
# Veri manipülasyonu ve analizi için pandas
import pandas as pd
# Grafik oluşturma için matplotlib ve seaborn
import matplotlib.pyplot as plt
import seaborn as sns
# Matematiksel işlemler için numpy
import numpy as np
# Grafik düzeni oluşturmak için matplotlib araçları
from matplotlib.ticker import FuncFormatter
# Dosya sistem işlemleri için
import os
# Gelişmiş grafik düzeni kontrolü için
import matplotlib.gridspec as gridspec
# Yüzde formatı için matplotlib araçları
from matplotlib.ticker import PercentFormatter
# İstatistiksel testler için scipy
from scipy import stats

# MATPLOTLIB TÜRKÇE KARAKTER DESTEĞİ
# ==================================
# Türkçe karakterleri düzgün göstermek için font ayarı
plt.rcParams['font.family'] = 'DejaVu Sans'

# VERİ YÜKLEME VE İLK İNCELEME
# ============================
# CSV dosyasından veri setini yükle
df = pd.read_csv('2425 vaka02 - zincir supermarket_sales - Sheet1.csv')

# VERİ SETİ HAKKINDA GENEL BİLGİLER
# =================================
# Veri setinin boyutunu (satır ve sütun sayısı) yazdır
print("Veri Seti Boyutu:", df.shape)
print("\nVeri Seti Sütunları:")
# Tüm sütun isimlerini listele
print(df.columns.tolist())
print("\nVeri Seti Başlangıç:")
# İlk 5 satırı göster
print(df.head())

# VERİ SETİNİN İSTATİSTİKSEL ÖZETİ
# ================================
print("\nVeri Seti İstatistikleri:")
# Sayısal sütunlar için istatistiksel özet (ortalama, std, min, max, vs.)
print(df.describe())

# VERİ KALİTESİ KONTROLÜ
# ======================
print("\nEksik Veri Sayısı:")
# Her sütunda kaç tane eksik veri olduğunu kontrol et
print(df.isnull().sum())

print("\nVeri Tipleri:")
# Her sütunun veri tipini göster
print(df.dtypes)

# TARİH VE ZAMAN VERİLERİNİN İŞLENMESİ
# ====================================
# Tarih sütununu datetime formatına dönüştür (zaman analizleri için gerekli)
df['Date'] = pd.to_datetime(df['Date'])
# Tarihten ay bilgisini çıkar (1-12 arası değerler)
df['Month'] = df['Date'].dt.month
# Tarihten gün bilgisini çıkar (1-31 arası değerler)
df['Day'] = df['Date'].dt.day
# Haftanın hangi günü olduğunu çıkar (0=Pazartesi, 6=Pazar)
df['DayOfWeek'] = df['Date'].dt.dayofweek

# KATEGORİK VERİLERİN DAĞILIMI
# ============================
print("\nŞehir Sayıları:")
# Her şehirde kaç tane kayıt olduğunu say
print(df['City'].value_counts())

print("\nŞube Sayıları:")
# Her şubede kaç tane kayıt olduğunu say
print(df['Branch'].value_counts())

print("\nMüşteri Tipi Sayıları:")
# Üye ve Normal müşteri sayılarını say
print(df['Customer type'].value_counts())

print("\nÜrün Kategorileri Sayıları:")
# Her ürün kategorisinde kaç tane satış olduğunu say
print(df['Product line'].value_counts())

print("\nÖdeme Yöntemi Sayıları:")
# Her ödeme yönteminde kaç tane işlem olduğunu say
print(df['Payment'].value_counts())

# ZAMANSAL DAĞILIM ANALİZİ
# ========================
print("\nAy Bazında Kayıt Sayıları:")
# Aylara göre kayıt sayılarını sırala ve göster
month_counts = df['Month'].value_counts().sort_index()
print(month_counts)

# ======================================================================
# SORU 1: İŞLETME GELİRLERİNİN ÜRÜN VE MÜŞTERİ TİPLERİNE GÖRE ANALİZİ
# ======================================================================
print("\n\n====== SORU 1: GELİR ANALİZİ ======")

# ÜRÜN KATEGORİLERİNE GÖRE DETAYLI GELİR ANALİZİ
# ===============================================
# Ürün kategorilerine göre çoklu istatistiksel analiz yap
product_revenue = df.groupby('Product line').agg({
    'Total': 'sum',           # Toplam satış tutarı
    'gross income': 'sum',    # Toplam brüt gelir
    'Invoice ID': 'count',    # İşlem sayısı
    'Quantity': 'sum',        # Toplam satılan ürün adedi
    'Unit price': 'mean',     # Ortalama birim fiyat
    'Rating': 'mean'          # Ortalama müşteri memnuniyeti
}).sort_values('Total', ascending=False)  # Toplam satışa göre büyükten küçüğe sırala

# Gelir yüzdelerini hesapla (her kategorinin toplam içindeki payı)
product_revenue['Revenue_Percentage'] = product_revenue['Total'] / product_revenue['Total'].sum() * 100
# Ortalama işlem değerini hesapla (toplam satış / işlem sayısı)
product_revenue['Average_Transaction'] = product_revenue['Total'] / product_revenue['Invoice ID']

print("\nÜrün Kategorilerine Göre Gelir Analizi:")
print(product_revenue)

# MÜŞTERİ TİPLERİNE GÖRE DETAYLI GELİR ANALİZİ
# =============================================
# Müşteri tiplerine göre çoklu istatistiksel analiz yap
customer_revenue = df.groupby('Customer type').agg({
    'Total': 'sum',           # Toplam satış tutarı
    'gross income': 'sum',    # Toplam brüt gelir
    'Invoice ID': 'count',    # İşlem sayısı
    'Quantity': 'sum',        # Toplam satılan ürün adedi
    'Unit price': 'mean',     # Ortalama birim fiyat
    'Rating': 'mean'          # Ortalama müşteri memnuniyeti
}).sort_values('Total', ascending=False)

# Gelir yüzdelerini ve ortalama işlem değerini hesapla
customer_revenue['Revenue_Percentage'] = customer_revenue['Total'] / customer_revenue['Total'].sum() * 100
customer_revenue['Average_Transaction'] = customer_revenue['Total'] / customer_revenue['Invoice ID']

print("\nMüşteri Tiplerine Göre Gelir Analizi:")
print(customer_revenue)

# ÜRÜN VE MÜŞTERİ TİPİ KOMBİNASYON ANALİZİ
# ==========================================
# Her ürün kategorisi için müşteri tiplerinin karşılaştırmalı analizi
product_customer_revenue = df.groupby(['Product line', 'Customer type']).agg({
    'Total': 'sum',
    'gross income': 'sum',
    'Invoice ID': 'count',
    'Quantity': 'sum'
}).sort_values(['Product line', 'Total'], ascending=[True, False])

print("\nÜrün ve Müşteri Tipi Kombinasyonuna Göre Gelir:")
print(product_customer_revenue)

# ŞUBE BAZINDA PERFORMANS ANALİZİ
# ===============================
# Her şubenin performansını karşılaştır
branch_revenue = df.groupby('Branch').agg({
    'Total': 'sum',
    'gross income': 'sum',
    'Invoice ID': 'count',
    'Quantity': 'sum'
}).sort_values('Total', ascending=False)

# Şube bazında gelir yüzdelerini hesapla
branch_revenue['Revenue_Percentage'] = branch_revenue['Total'] / branch_revenue['Total'].sum() * 100

print("\nŞubelere Göre Gelir Analizi:")
print(branch_revenue)

# ŞEHİR BAZINDA GELİR ANALİZİ
# ============================
# Her şehirin toplam gelir katkısını analiz et
city_revenue = df.groupby('City').agg({
    'Total': 'sum',
    'gross income': 'sum',
    'Invoice ID': 'count',
    'Quantity': 'sum'
}).sort_values('Total', ascending=False)

city_revenue['Revenue_Percentage'] = city_revenue['Total'] / city_revenue['Total'].sum() * 100

print("\nŞehirlere Göre Gelir Analizi:")
print(city_revenue)

# CİNSİYET BAZINDA GELİR ANALİZİ
# ===============================
# Erkek ve kadın müşterilerin harcama davranışlarını karşılaştır
gender_revenue = df.groupby('Gender').agg({
    'Total': 'sum',
    'gross income': 'sum',
    'Invoice ID': 'count',
    'Quantity': 'sum'
}).sort_values('Total', ascending=False)

gender_revenue['Revenue_Percentage'] = gender_revenue['Total'] / gender_revenue['Total'].sum() * 100
gender_revenue['Average_Transaction'] = gender_revenue['Total'] / gender_revenue['Invoice ID']

print("\nCinsiyete Göre Gelir Analizi:")
print(gender_revenue)

# ÖDEME YÖNTEMİ ANALİZİ
# =====================
# Hangi ödeme yönteminin daha çok tercih edildiğini analiz et
payment_revenue = df.groupby('Payment').agg({
    'Total': 'sum',
    'gross income': 'sum',
    'Invoice ID': 'count',
    'Quantity': 'sum'
}).sort_values('Total', ascending=False)

payment_revenue['Revenue_Percentage'] = payment_revenue['Total'] / payment_revenue['Total'].sum() * 100

print("\nÖdeme Yöntemine Göre Gelir Analizi:")
print(payment_revenue)

# ZAMAN SERİSİ ANALİZİ
# ====================
# Günlük satış trendlerini analiz et
daily_revenue = df.groupby('Date').agg({
    'Total': 'sum',
    'Invoice ID': 'count'
})

print("\nGünlük Gelir Analizi (İlk 5 gün):")
print(daily_revenue.head())

# Aylık gelir trendlerini analiz et
monthly_revenue = df.groupby('Month').agg({
    'Total': 'sum',
    'Invoice ID': 'count',
    'gross income': 'sum'
})

print("\nAylık Gelir Analizi:")
print(monthly_revenue)

# Haftanın günlerine göre satış davranışını analiz et
weekday_revenue = df.groupby('DayOfWeek').agg({
    'Total': 'sum',
    'Invoice ID': 'count',
    'gross income': 'sum'
})

print("\nHaftanın Günlerine Göre Gelir Analizi:")
print(weekday_revenue)

# KORELASYON ANALİZİ
# ==================
# Sayısal değişkenler arasındaki ilişkileri analiz et
numeric_df = df.select_dtypes(include=[np.number])  # Sadece sayısal sütunları seç
correlation = numeric_df.corr()  # Korelasyon matrisini hesapla

print("\nNümerik Değişkenler Arasındaki Korelasyon:")
print(correlation[['Total', 'gross income', 'Quantity', 'Unit price', 'Rating']].sort_values('Total', ascending=False))

# ======================================================================
# SORU 2: ÇALIŞMA STRATEJİSİ ANALİZİ VE ÖNERİLER
# ======================================================================
print("\n\n====== SORU 2: ÇALIŞMA STRATEJİSİ ANALİZİ ======")

# MÜŞTERİ MEMNUNİYETİ ANALİZİ
# ============================
# Ürün kategorilerine göre müşteri memnuniyetini analiz et
rating_by_product = df.groupby('Product line')['Rating'].mean().sort_values(ascending=False)
print("\nÜrün Kategorilerine Göre Ortalama Değerlendirme Puanı:")
print(rating_by_product)

# Şubelere göre müşteri memnuniyetini karşılaştır
rating_by_branch = df.groupby('Branch')['Rating'].mean().sort_values(ascending=False)
print("\nŞubelere Göre Ortalama Değerlendirme Puanı:")
print(rating_by_branch)

# Müşteri tipine göre memnuniyet seviyesini analiz et
rating_by_customer = df.groupby('Customer type')['Rating'].mean().sort_values(ascending=False)
print("\nMüşteri Tipine Göre Ortalama Değerlendirme Puanı:")
print(rating_by_customer)

# SAATLİK SATIŞ ANALİZİ
# =====================
# En karlı saatleri belirlemek için saatlik analiz yap
hourly_analysis = df.copy()
# Zaman bilgisinden saat değerini çıkar
hourly_analysis['Hour'] = pd.to_datetime(df['Time']).dt.hour

# Saatlik gelir istatistiklerini hesapla
hourly_revenue = hourly_analysis.groupby('Hour').agg({
    'Total': 'sum',           # Toplam satış
    'Invoice ID': 'count',    # İşlem sayısı
    'gross income': 'sum'     # Brüt gelir
}).sort_values('Total', ascending=False)

print("\nSaat Bazında Gelir Analizi:")
print(hourly_revenue)

# ŞUBE-ÜRÜN KATEGORİSİ KOMBİNASYON ANALİZİ
# =========================================
# Her şubede hangi ürün kategorilerinin daha başarılı olduğunu analiz et
branch_product_analysis = df.groupby(['Branch', 'Product line']).agg({
    'Total': 'sum',
    'Invoice ID': 'count',
    'gross income': 'sum',
    'Rating': 'mean'
}).sort_values(['Branch', 'Total'], ascending=[True, False])

print("\nŞube-Ürün Kategorisi Kombinasyonuna Göre Gelir:")
print(branch_product_analysis)

# ŞEHİR-ÜRÜN KATEGORİSİ KOMBİNASYON ANALİZİ
# ==========================================
# Her şehirde hangi ürün kategorilerinin tercih edildiğini analiz et
city_product_analysis = df.groupby(['City', 'Product line']).agg({
    'Total': 'sum',
    'Invoice ID': 'count',
    'gross income': 'sum',
    'Rating': 'mean'
}).sort_values(['City', 'Total'], ascending=[True, False])

print("\nŞehir-Ürün Kategorisi Kombinasyonuna Göre Gelir:")
print(city_product_analysis)

# MÜŞTERİ SEGMENTASYON ANALİZİ
# ============================
# Müşteri tipi, cinsiyet ve ürün tercihi kombinasyonlarını analiz et
customer_segment_analysis = df.groupby(['Customer type', 'Gender', 'Product line']).agg({
    'Total': 'sum',
    'Invoice ID': 'count',
    'gross income': 'sum',
    'Rating': 'mean'
}).sort_values(['Customer type', 'Gender', 'Total'], ascending=[True, True, False])

print("\nMüşteri Segmentasyonu Analizi:")
print(customer_segment_analysis)

# ======================================================================
# VİZÜALİZASYON BÖLÜMÜ - ANA GRAFİKLER
# ======================================================================
# Ana analiz grafikleri için büyük figür oluştur
plt.figure(figsize=(20, 15))
plt.suptitle('ZİNCİR SÜPERMARKETLERİ VERİ ANALİZİ', fontsize=20, fontweight='bold')

# 1. ÜRÜN KATEGORİLERİNE GÖRE GELİR DAĞILIMI
plt.subplot(2, 2, 1)
# Çubuk grafiği oluştur ve renklendır
product_revenue['Total'].plot(kind='bar', color='skyblue')
plt.title('Ürün Kategorilerine Göre Toplam Gelir')
plt.xlabel('Ürün Kategorisi')
plt.ylabel('Toplam Gelir ($)')
plt.xticks(rotation=45, ha='right')  # X ekseni etiketlerini döndür
# Her çubuğun üstüne yüzde değerini ekle
for i, v in enumerate(product_revenue['Revenue_Percentage']):
    plt.text(i, product_revenue['Total'][i] + 1000, f'%{v:.1f}', ha='center')

# 2. MÜŞTERİ TİPLERİNE GÖRE GELİR DAĞILIMI
plt.subplot(2, 2, 2)
customer_revenue['Total'].plot(kind='bar', color='lightgreen')
plt.title('Müşteri Tiplerine Göre Toplam Gelir')
plt.xlabel('Müşteri Tipi')
plt.ylabel('Toplam Gelir ($)')
# Yüzde değerlerini ekle
for i, v in enumerate(customer_revenue['Revenue_Percentage']):
    plt.text(i, customer_revenue['Total'][i] + 1000, f'%{v:.1f}', ha='center')

# 3. ŞUBELERE GÖRE GELİR DAĞILIMI
plt.subplot(2, 2, 3)
branch_revenue['Total'].plot(kind='bar', color='salmon')
plt.title('Şubelere Göre Toplam Gelir')
plt.xlabel('Şube')
plt.ylabel('Toplam Gelir ($)')
# Yüzde değerlerini ekle
for i, v in enumerate(branch_revenue['Revenue_Percentage']):
    plt.text(i, branch_revenue['Total'][i] + 1000, f'%{v:.1f}', ha='center')

# 4. ÖDEME YÖNTEMLERİNE GÖRE GELİR DAĞILIMI
plt.subplot(2, 2, 4)
payment_revenue['Total'].plot(kind='bar', color='lightpink')
plt.title('Ödeme Yöntemlerine Göre Toplam Gelir')
plt.xlabel('Ödeme Yöntemi')
plt.ylabel('Toplam Gelir ($)')
# Yüzde değerlerini ekle
for i, v in enumerate(payment_revenue['Revenue_Percentage']):
    plt.text(i, payment_revenue['Total'][i] + 1000, f'%{v:.1f}', ha='center')

# Grafik düzenini optimize et ve kaydet
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('gelir_analizi.png', dpi=300, bbox_inches='tight')

# ======================================================================
# DETAYLI ANALİZ GRAFİKLERİ
# ======================================================================
# İkinci grafik seti - daha detaylı analizler
plt.figure(figsize=(20, 15))
plt.suptitle('ZİNCİR SÜPERMARKETLERİ DETAYLI ANALİZ', fontsize=20, fontweight='bold')

# 1. ÜRÜN KATEGORİLERİNE GÖRE ORTALAMA DEĞERLENDİRME
plt.subplot(2, 2, 1)
rating_by_product.plot(kind='bar', color='gold')
plt.title('Ürün Kategorilerine Göre Ortalama Değerlendirme Puanı')
plt.xlabel('Ürün Kategorisi')
plt.ylabel('Ortalama Puan (1-10)')
plt.xticks(rotation=45, ha='right')
plt.ylim(0, 10)  # Y ekseni limitini 0-10 arasında ayarla

# 2. SAAT BAZINDA GELİR ANALİZİ
plt.subplot(2, 2, 2)
hourly_revenue['Total'].plot(kind='bar', color='mediumturquoise')
plt.title('Saat Bazında Toplam Gelir')
plt.xlabel('Saat')
plt.ylabel('Toplam Gelir ($)')

# 3. AYLIK GELİR ANALİZİ
plt.subplot(2, 2, 3)
monthly_revenue['Total'].plot(kind='bar', color='mediumpurple')
plt.title('Aylık Toplam Gelir')
plt.xlabel('Ay')
plt.ylabel('Toplam Gelir ($)')
# X ekseni etiketlerini Türkçe ay isimleriyle değiştir
plt.xticks(ticks=[0, 1, 2], labels=['Ocak', 'Şubat', 'Mart'])

# 4. ŞEHİRLERE GÖRE GELİR DAĞILIMI
plt.subplot(2, 2, 4)
city_revenue['Total'].plot(kind='bar', color='lightcoral')
plt.title('Şehirlere Göre Toplam Gelir')
plt.xlabel('Şehir')
plt.ylabel('Toplam Gelir ($)')
# Yüzde değerlerini ekle
for i, v in enumerate(city_revenue['Revenue_Percentage']):
    plt.text(i, city_revenue['Total'][i] + 1000, f'%{v:.1f}', ha='center')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('detayli_analiz.png', dpi=300, bbox_inches='tight')

# ======================================================================
# MÜŞTERİ SEGMENTASYON VE İLİŞKİ GRAFİKLERİ
# ======================================================================
# Üçüncü grafik seti - müşteri segmentasyonu ve ilişkiler
plt.figure(figsize=(20, 15))
plt.suptitle('ZİNCİR SÜPERMARKETLERİ MÜŞTERİ SEGMENTASYONU', fontsize=20, fontweight='bold')

# 1. MÜŞTERİ TİPİ VE CİNSİYET BAZINDA GELİR
# Müşteri tipi ve cinsiyetin birlikte analizi için pivot tablo oluştur
customer_gender_revenue = df.groupby(['Customer type', 'Gender'])['Total'].sum().unstack()
plt.subplot(2, 2, 1)
customer_gender_revenue.plot(kind='bar', color=['skyblue', 'salmon'])
plt.title('Müşteri Tipi ve Cinsiyet Bazında Toplam Gelir')
plt.xlabel('Müşteri Tipi')
plt.ylabel('Toplam Gelir ($)')
plt.legend(title='Cinsiyet')

# 2. ÜRÜN KATEGORİLERİNE GÖRE MÜŞTERİ TİPİ DAĞILIMI
# Ürün kategorileri ve müşteri tiplerinin çapraz analizi
product_customer_pivot = pd.pivot_table(df, values='Total', 
                                       index='Product line', 
                                       columns='Customer type', 
                                       aggfunc='sum')
plt.subplot(2, 2, 2)
product_customer_pivot.plot(kind='bar', color=['lightgreen', 'lightcoral'])
plt.title('Ürün Kategorilerine Göre Müşteri Tipi Dağılımı')
plt.xlabel('Ürün Kategorisi')
plt.ylabel('Toplam Gelir ($)')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Müşteri Tipi')

# 3. KORELASYON ISI HARİTASI
plt.subplot(2, 2, 3)
# Önemli değişkenler arasındaki korelasyonu ısı haritası olarak göster
correlation_vars = ['Total', 'Quantity', 'Unit price', 'gross income', 'Rating']
sns.heatmap(correlation[correlation_vars].loc[correlation_vars], 
            annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Değişkenler Arası Korelasyon')

# 4. ÜRÜN KATEGORİLERİNE GÖRE ORTALAMA İŞLEM DEĞERİ
# Her ürün kategorisindeki ortalama harcama miktarını analiz et
avg_transaction_by_product = df.groupby(['Product line'])['Total'].mean().sort_values(ascending=False)
plt.subplot(2, 2, 4)
avg_transaction_by_product.plot(kind='bar', color='mediumorchid')
plt.title('Ürün Kategorilerine Göre Ortalama İşlem Değeri')
plt.xlabel('Ürün Kategorisi')
plt.ylabel('Ortalama İşlem Değeri ($)')
plt.xticks(rotation=45, ha='right')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('musteri_segmentasyonu.png', dpi=300, bbox_inches='tight')

# ======================================================================
# STRATEJİ ÖNERİLERİ İÇİN VERİ GÖRSELLEŞTİRME
# ======================================================================
# Dördüncü grafik seti - strateji önerileri için veri görselleştirme
plt.figure(figsize=(20, 15))
plt.suptitle('ZİNCİR SÜPERMARKETLERİ STRATEJİ ÖNERİLERİ İÇİN ANALİZ', fontsize=20, fontweight='bold')

# 1. ŞUBE-ÜRÜN KATEGORİSİ MATRİSİ
# Hangi şubede hangi ürün kategorisinin daha başarılı olduğunu göster
branch_product_pivot = pd.pivot_table(df, values='Total',
                                     index='Branch',
                                     columns='Product line',
                                     aggfunc='sum')
plt.subplot(2, 2, 1)
sns.heatmap(branch_product_pivot, annot=True, fmt='.0f', cmap='YlGnBu', linewidths=0.5)
plt.title('Şube-Ürün Kategorisi Gelir Matrisi')
plt.ylabel('Şube')
plt.xlabel('Ürün Kategorisi')

# 2. ŞUBE BAZINDA MÜŞTERİ MEMNUNİYETİ
# Her şubede ürün kategorilerine göre müşteri memnuniyeti
branch_rating_product = pd.pivot_table(df, values='Rating',
                                     index='Branch',
                                     columns='Product line',
                                     aggfunc='mean')
plt.subplot(2, 2, 2)
sns.heatmap(branch_rating_product, annot=True, fmt='.1f', cmap='RdYlGn', 
           linewidths=0.5, vmin=0, vmax=10)
plt.title('Şube-Ürün Kategorisi Değerlendirme Matrisi')
plt.ylabel('Şube')
plt.xlabel('Ürün Kategorisi')

# 3. GÜN İÇİ SAAT BAZINDA GELİR DAĞILIMI
plt.subplot(2, 2, 3)
# Saatlik gelir trendini çizgi grafik olarak göster
hourly_revenue['Total'].plot(kind='line', marker='o', color='teal')
plt.title('Saat Bazında Gelir Dağılımı')
plt.xlabel('Saat')
plt.ylabel('Toplam Gelir ($)')
plt.grid(True, linestyle='--', alpha=0.7)  # Grid çizgileri ekle

# 4. ŞUBE BAZINDA ÖDEME YÖNTEMİ DAĞILIMI
# Her şubede hangi ödeme yönteminin ne kadar kullanıldığını yüzde olarak göster
branch_payment = pd.crosstab(df['Branch'], df['Payment'], values=df['Total'], 
                           aggfunc='sum', normalize='index') * 100
plt.subplot(2, 2, 4)
branch_payment.plot(kind='bar', stacked=True, colormap='Set3')
plt.title('Şube Bazında Ödeme Yöntemi Dağılımı (%)')
plt.xlabel('Şube')
plt.ylabel('Yüzde (%)')
plt.legend(title='Ödeme Yöntemi')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('strateji_analiz.png', dpi=300, bbox_inches='tight')

# ======================================================================
# ÖZET BULGULAR VE SONUÇLAR
# ======================================================================
print("\n\n====== ÖZET BULGULAR ======")

# 1. EN YÜKSEK GELİR GETİREN ÜRÜN KATEGORİLERİ
print("\nEn Yüksek Gelir Getiren Ürün Kategorileri:")
for idx, (category, percentage) in enumerate(zip(product_revenue.index, product_revenue['Revenue_Percentage']), 1):
    print(f"{idx}. {category}: %{percentage:.2f}")

# 2. MÜŞTERİ TİPİ BAZINDA GELİR DAĞILIMI
print("\nMüşteri Tipi Bazında Gelir Dağılımı:")
for idx, (customer_type, percentage) in enumerate(zip(customer_revenue.index, customer_revenue['Revenue_Percentage']), 1):
    print(f"{idx}. {customer_type}: %{percentage:.2f}")

# 3. ŞUBE PERFORMANSLARI
print("\nŞube Performansları:")
for idx, (branch, percentage) in enumerate(zip(branch_revenue.index, branch_revenue['Revenue_Percentage']), 1):
    print(f"{idx}. Şube {branch}: %{percentage:.2f}")

# 4. MÜŞTERİ MEMNUNİYETİ EN YÜKSEK ÜRÜN KATEGORİLERİ
print("\nMüşteri Memnuniyeti En Yüksek Ürün Kategorileri:")
for idx, (category, rating) in enumerate(zip(rating_by_product.index, rating_by_product), 1):
    print(f"{idx}. {category}: {rating:.2f}/10")

# 5. EN AKTİF SATIŞ SAATLERİ
print("\nEn Aktif Satış Saatleri:")
top_hours = hourly_revenue.head(5).index.tolist()
for hour in top_hours:
    print(f"- {hour}:00")

# ======================================================================
# STRATEJİ ÖNERİLERİ RAPORU
# ======================================================================
print("\n====== STRATEJİ ÖNERİLERİ ======")

# Kapsamlı strateji önerileri raporu
print("""
1. Ürün Stratejileri:
   - Spor ve Seyahat kategorisinde ürün çeşitliliğini artırın (en yüksek gelir getiren kategori)
   - Yiyecek ve İçecekler kategorisini geliştirin (gelir artırma potansiyeli yüksek)
   - Elektronik Aksesuarlar kategorisinde müşteri memnuniyetini artıracak iyileştirmeler yapın

2. Müşteri Stratejileri:
   - Üyelik programını güçlendirin (üyeler daha yüksek ortalama alışveriş değerine sahip)
   - Erkek müşterilere yönelik kampanyalar geliştirin (kadın müşterilere göre daha düşük harcama yapıyorlar)
   - Yeni müşterileri üyeliğe dönüştürecek teşvikler sunun

3. Şube Stratejileri:
   - A şubesinin başarılı uygulamalarını diğer şubelere yayın
   - C şubesi için ürün gamını gözden geçirin ve iyileştirin
   - Şube B'de elektronik ve moda ürünlerine ağırlık verin

4. Operasyonel Stratejiler:
   - En yoğun satış saatlerinde (15:00-19:00) personel sayısını artırın
   - Sabah saatlerinde özel kampanyalar düzenleyerek müşteri trafiğini dengelendirin
   - E-cüzdan kullanımını teşvik edin (işletme maliyetlerini düşürmek için)

5. Zamansal Stratejiler:
   - Haftasonu satışlarını artıracak özel kampanyalar düzenleyin
   - Ay sonlarına doğru artan satış trendini destekleyin
   - Mart ayında görülen düşüşü önlemek için özel stratejiler geliştirin
""")

print("\nAnaliz tamamlandı. Grafikler ve detaylı sonuçlar kaydedildi.")

# ======================================================================
# EK GÖRSELLEŞTİRMELER
# ======================================================================
# Görselleştirme stil ayarları
plt.style.use('seaborn')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# 1. ÖDEME YÖNTEMLERİ PASTA GRAFİĞİ
plt.figure(figsize=(10, 6))
payment_counts = df['Payment'].value_counts()
plt.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%')
plt.title('Ödeme Yöntemleri Dağılımı')
plt.savefig('odeme_yontemleri.png')
plt.close()

# 2. SAATLİK ORTALAMA SATIŞ ANALİZİ
df['Hour'] = pd.to_datetime(df['Time']).dt.hour
hourly_sales = df.groupby('Hour')['Total'].mean()
plt.figure(figsize=(12, 6))
plt.plot(hourly_sales.index, hourly_sales.values, marker='o')
plt.title('Saatlik Ortalama Satış Tutarları')
plt.xlabel('Saat')
plt.ylabel('Ortalama Satış Tutarı ($)')
plt.grid(True)
plt.savefig('saatlik_satislar.png')
plt.close()

# 3. ÜRÜN KATEGORİLERİ DETAY ANALİZİ
category_stats = df.groupby('Product line').agg({
    'Total': ['mean', 'sum', 'count'],
    'Rating': 'mean'
}).round(2)

plt.figure(figsize=(12, 6))
sns.barplot(x=category_stats.index, y=category_stats[('Total', 'mean')])
plt.title('Ürün Kategorilerine Göre Ortalama Satış Tutarları')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('kategori_satislari.png')
plt.close()

# 4. MÜŞTERİ TİPİ VE CİNSİYET ÇAPRAZ ANALİZİ
customer_gender = pd.crosstab(df['Customer type'], df['Gender'])
plt.figure(figsize=(10, 6))
customer_gender.plot(kind='bar', stacked=True)
plt.title('Müşteri Tipi ve Cinsiyet Dağılımı')
plt.xlabel('Müşteri Tipi')
plt.ylabel('Müşteri Sayısı')
plt.legend(title='Cinsiyet')
plt.tight_layout()
plt.savefig('musteri_analizi.png')
plt.close()

# 5. KORELASYON MATRİSİ DETAYLI ANALİZİ
# Önemli sayısal değişkenler arasındaki ilişkileri analiz et
numeric_columns = ['Unit price', 'Quantity', 'Total', 'Rating', 'cogs', 'gross income']
correlation_matrix = df[numeric_columns].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Değişkenler Arası Korelasyon Matrisi')
plt.tight_layout()
plt.savefig('korelasyon.png')
plt.close()

# 6. ŞUBE PERFORMANS KARŞILAŞTIRMASI
branch_stats = df.groupby('Branch').agg({
    'Total': ['mean', 'sum', 'count'],
    'Rating': 'mean'
}).round(2)

plt.figure(figsize=(10, 6))
sns.barplot(x=branch_stats.index, y=branch_stats[('Total', 'mean')])
plt.title('Şubelere Göre Ortalama Satış Tutarları')
plt.xlabel('Şube')
plt.ylabel('Ortalama Satış Tutarı ($)')
plt.tight_layout()
plt.savefig('sube_performansi.png')
plt.close()

# 7. İSTATİSTİKSEL ÖZET VE VERİ KALİTESİ RAPORU
statistical_summary = df.describe().round(2)

# 8. ZAMAN SERİSİ TRENDİ ANALİZİ
df['Date'] = pd.to_datetime(df['Date'])
daily_sales = df.groupby('Date')['Total'].sum()

plt.figure(figsize=(15, 6))
plt.plot(daily_sales.index, daily_sales.values)
plt.title('Günlük Toplam Satışlar')
plt.xlabel('Tarih')
plt.ylabel('Toplam Satış ($)')
plt.grid(True)
plt.tight_layout()
plt.savefig('gunluk_satislar.png')
plt.close()

# ======================================================================
# İSTATİSTİKSEL HİPOTEZ TESTLERİ
# ======================================================================
# 1. MÜŞTERİ TİPLERİNE GÖRE ORTALAMA SATIŞ TUTARI FARKI
# Üye müşteriler ile normal müşteriler arasında anlamlı fark var mı?
member_sales = df[df['Customer type'] == 'Member']['Total']
normal_sales = df[df['Customer type'] == 'Normal']['Total']
t_stat, p_value = stats.ttest_ind(member_sales, normal_sales)

# 2. CİNSİYETLERE GÖRE ORTALAMA SATIŞ TUTARI FARKI
# Erkek ve kadın müşteriler arasında anlamlı harcama farkı var mı?
male_sales = df[df['Gender'] == 'Male']['Total']
female_sales = df[df['Gender'] == 'Female']['Total']
t_stat_gender, p_value_gender = stats.ttest_ind(male_sales, female_sales)

# SONUÇLARI YAZDIRMA
print("\nDetaylı İstatistiksel Özet:")
print(statistical_summary)
print("\nKategori Bazlı İstatistikler:")
print(category_stats)
print("\nŞube Performans İstatistikleri:")
print(branch_stats)
print("\nİstatistiksel Test Sonuçları:")
print(f"Müşteri Tipi Farkı Testi p-değeri: {p_value:.4f}")
print(f"Cinsiyet Farkı Testi p-değeri: {p_value_gender:.4f}") 
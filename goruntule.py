# ======================================================================
# ZİNCİR SÜPERMARKETLERİ VERİ ANALİZİ VE GÖRÜNTÜLEME UYGULAMASI
# ======================================================================
# Bu uygulama, süpermarket satış verilerini analiz etmek ve sekmeli bir
# arayüzde görselleştirmek için tasarlanmış Tkinter tabanlı bir GUI uygulamasıdır.
# Çok detaylı analizler, grafikler ve öneriler içerir.
# ======================================================================

# KÜTÜPHANE İÇE AKTARIMLARI
# =========================
# Veri analizi ve manipülasyonu için pandas
import pandas as pd
# Grafik oluşturma için matplotlib ve seaborn
import matplotlib.pyplot as plt
import seaborn as sns
# Matematiksel işlemler için numpy
import numpy as np
# GUI oluşturmak için tkinter modülleri
import tkinter as tk
from tkinter import ttk, scrolledtext
# Görsel işleme için PIL
from PIL import Image, ImageTk
# Sistem işlemleri için os
import os
# Matplotlib'i Tkinter ile entegre etmek için
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# VERİ YÜKLEME VE ÖN İŞLEME
# =========================
# CSV dosyasından süpermarket satış verilerini yükle
df = pd.read_csv('2425 vaka02 - zincir supermarket_sales - Sheet1.csv')

# Tarih sütununu datetime formatına çevir (zaman analizleri için gerekli)
df['Date'] = pd.to_datetime(df['Date'])
# Tarihten ay bilgisini çıkar (aylık trend analizleri için)
df['Month'] = df['Date'].dt.month
# Tarihten gün bilgisini çıkar (günlük analizler için)
df['Day'] = df['Date'].dt.day
# Haftanın hangi günü olduğunu çıkar (0=Pazartesi, 6=Pazar)
df['DayOfWeek'] = df['Date'].dt.dayofweek

# ANA UYGULAMA SINIFI
# ===================
class SupermarketAnalysisApp:
    """
    Süpermarket analiz uygulamasının ana sınıfı.
    Çok sekmeli bir arayüz ile kapsamlı veri analizi ve görselleştirme sağlar.
    """
    
    def __init__(self, root):
        """
        Uygulama başlatıcısı. Ana pencereyi ve tüm bileşenleri oluşturur.
        
        Args:
            root: Tkinter ana pencere nesnesi
        """
        self.root = root
        # Pencere başlığını ayarla
        self.root.title("ZİNCİR SÜPERMARKETLERİ VERİ ANALİZİ")
        # Pencere boyutunu ayarla
        self.root.geometry("1200x800")
        # Arka plan rengini ayarla
        self.root.configure(bg="#f0f0f0")
        
        # Ana çerçeveyi oluştur (tüm bileşenler buraya yerleştirilecek)
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Uygulama başlığını oluştur ve yerleştir
        title_label = ttk.Label(self.main_frame, text="ZİNCİR SÜPERMARKETLERİ VERİ ANALİZİ", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Sekmeli panel kontrolünü oluştur
        self.tab_control = ttk.Notebook(self.main_frame)
        
        # Tüm analiz sekmelerini oluştur
        self.create_overview_tab()         # Genel bakış ve veri seti bilgileri
        self.create_product_analysis_tab() # Ürün kategorileri analizi
        self.create_customer_analysis_tab() # Müşteri segmentasyonu analizi
        self.create_branch_analysis_tab()  # Şube performans analizi
        self.create_time_analysis_tab()    # Zaman bazlı analizler
        self.create_recommendations_tab()  # Strateji önerileri
        
        # Sekmeli paneli ekrana yerleştir
        self.tab_control.pack(expand=True, fill=tk.BOTH)
        
        # Alt bilgi (copyright) etiketi
        footer_label = ttk.Label(self.main_frame, text="© 2023 Zincir Süpermarketleri Analiz Raporu", 
                                font=("Arial", 8))
        footer_label.pack(pady=5)

    def create_overview_tab(self):
        """
        Genel bakış sekmesini oluşturur.
        Veri seti bilgileri, analiz yöntemi ve veri önizlemesi içerir.
        """
        # Genel bakış sekmesini oluştur
        overview_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(overview_tab, text="Genel Bakış")
        
        # Veri seti ve analiz hakkında bilgi metni
        info_text = """
        ZİNCİR SÜPERMARKETLERİ VERİ ANALİZİ
        
        Bu uygulama, ZİNCİR SÜPERMARKETLERİ'nin 3 farklı şubedeki 3 aylık satış verilerini (1000 kayıt) analiz etmektedir.
        
        Veri Seti Özellikleri:
        • 1000 adet satış kaydı
        • 3 farklı şubede 3 aylık satış verileri (Ocak-Mart 2019)
        • Şehirler: Yangon, Mandalay, Naypyitaw
        • Müşteri tipleri: Üye ve Normal
        • 6 ürün kategorisi
        • 3 ödeme yöntemi
        
        Aşağıdaki analizler yapılmıştır:
        1. Ürün Kategorilerine Göre Gelir Analizi
        2. Müşteri Tiplerine Göre Gelir Analizi
        3. Şube Bazında Gelir Analizi
        4. Zaman Bazlı Analizler
        5. Strateji Önerileri
        
        Bu analizler sonucunda işletme için stratejik öneriler oluşturulmuştur.
        """
        
        # Kaydırılabilir metin alanı oluştur ve bilgi metnini ekle
        info_scroll = scrolledtext.ScrolledText(overview_tab, wrap=tk.WORD, width=80, height=20, 
                                               font=("Arial", 11))
        info_scroll.insert(tk.END, info_text)
        info_scroll.configure(state='disabled')  # Sadece okunabilir yap
        info_scroll.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Veri seti önizleme bölümü
        preview_frame = ttk.LabelFrame(overview_tab, text="Veri Seti Önizleme")
        preview_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Veri önizleme tablosu - ilk 5 satırı göster
        preview_text = scrolledtext.ScrolledText(preview_frame, wrap=tk.WORD, width=80, height=10, 
                                                font=("Courier New", 10))
        preview_text.insert(tk.END, df.head().to_string())
        preview_text.configure(state='disabled')  # Sadece okunabilir yap
        preview_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def create_product_analysis_tab(self):
        """
        Ürün kategorileri analiz sekmesini oluşturur.
        Ürün kategorilerine göre gelir analizi ve önerileri içerir.
        """
        # Ürün analizi sekmesini oluştur
        product_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(product_tab, text="Ürün Analizi")
        
        # Ürün kategorileri analizi çerçevesi
        product_frame = ttk.LabelFrame(product_tab, text="Ürün Kategorilerine Göre Gelir Analizi")
        product_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # ÜRÜN KATEGORİLERİ GELİR ANALİZİ GRAFİĞİ
        # Matplotlib figürü oluştur
        fig, ax = plt.subplots(figsize=(10, 6))
        # Ürün kategorilerine göre toplam geliri hesapla ve sırala
        product_revenue = df.groupby('Product line')['Total'].sum().sort_values(ascending=False)
        # Yüzde oranlarını hesapla
        product_percent = product_revenue / product_revenue.sum() * 100
        
        # Çubuk grafiği oluştur
        bars = ax.bar(product_revenue.index, product_revenue.values, color='skyblue')
        ax.set_title('Ürün Kategorilerine Göre Toplam Gelir')
        ax.set_xlabel('Ürün Kategorisi')
        ax.set_ylabel('Toplam Gelir ($)')
        plt.xticks(rotation=45, ha='right')  # X ekseni etiketlerini döndür
        
        # Her çubuğun üstüne yüzde bilgisini ekle
        for i, (bar, percent) in enumerate(zip(bars, product_percent)):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500, 
                    f'%{percent:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()  # Düzeni optimize et
        
        # Grafiği Tkinter canvas'ına yerleştir
        canvas = FigureCanvasTkAgg(fig, product_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ÜRÜN ANALİZİ SONUÇLARI VE ÖNERİLERİ
        info_frame = ttk.Frame(product_tab)
        info_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Analiz sonuçları metni
        product_info = """
        Ürün Kategorileri Analizi Sonuçları:
        
        1. Yiyecek ve İçecekler kategorisi en yüksek gelir sağlayan kategoridir (%17.38).
        2. Spor ve Seyahat ikinci en yüksek gelir getiren kategoridir (%17.07).
        3. Elektronik Aksesuarlar, Moda Aksesuarları ve Ev ve Yaşam Tarzı kategorileri birbirine yakın gelir oranlarına sahiptir.
        4. Sağlık ve Güzellik kategorisi en düşük gelir sağlayan kategoridir (%15.23).
        
        Öneriler:
        - Yiyecek ve İçecekler kategorisinde ürün çeşitliliğini artırın
        - Spor ve Seyahat kategorisini özel promosyonlarla destekleyin
        - Sağlık ve Güzellik kategorisinde müşteri deneyimini iyileştirin
        """
        
        # Analiz sonuçları için kaydırılabilir metin alanı
        info_text = scrolledtext.ScrolledText(info_frame, wrap=tk.WORD, width=80, height=10, 
                                             font=("Arial", 10))
        info_text.insert(tk.END, product_info)
        info_text.configure(state='disabled')  # Sadece okunabilir yap
        info_text.pack(fill=tk.X, padx=10, pady=10)

    def create_customer_analysis_tab(self):
        """
        Müşteri analizi sekmesini oluşturur.
        Müşteri tipi, cinsiyet ve segmentasyon analizlerini içerir.
        """
        # Müşteri analizi sekmesini oluştur
        customer_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(customer_tab, text="Müşteri Analizi")
        
        # SOL PANEL - Müşteri tipi analizi
        left_frame = ttk.Frame(customer_tab)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Müşteri tipi analizi çerçevesi
        customer_frame = ttk.LabelFrame(left_frame, text="Müşteri Tiplerine Göre Gelir Analizi")
        customer_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # MÜŞTERİ TİPİ GELİR GRAFİĞİ
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        # Müşteri tiplerine göre toplam geliri hesapla
        customer_revenue = df.groupby('Customer type')['Total'].sum()
        # Yüzde oranlarını hesapla
        customer_percent = customer_revenue / customer_revenue.sum() * 100
        
        # Çubuk grafiği oluştur
        bars1 = ax1.bar(customer_revenue.index, customer_revenue.values, color='lightgreen')
        ax1.set_title('Müşteri Tiplerine Göre Gelir')
        ax1.set_xlabel('Müşteri Tipi')
        ax1.set_ylabel('Toplam Gelir ($)')
        
        # Yüzde bilgilerini çubukların üstüne ekle
        for i, (bar, percent) in enumerate(zip(bars1, customer_percent)):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000, 
                    f'%{percent:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Grafiği canvas'a yerleştir
        canvas1 = FigureCanvasTkAgg(fig1, customer_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # SAĞ PANEL - Cinsiyet analizi
        right_frame = ttk.Frame(customer_tab)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Cinsiyet analizi çerçevesi
        gender_frame = ttk.LabelFrame(right_frame, text="Cinsiyete Göre Gelir Analizi")
        gender_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # CİNSİYET GELİR GRAFİĞİ
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        # Cinsiyete göre toplam geliri hesapla
        gender_revenue = df.groupby('Gender')['Total'].sum()
        # Yüzde oranlarını hesapla
        gender_percent = gender_revenue / gender_revenue.sum() * 100
        
        # Renk kodlu çubuk grafiği oluştur (pembe=kadın, mavi=erkek)
        bars2 = ax2.bar(gender_revenue.index, gender_revenue.values, color=['lightpink', 'lightblue'])
        ax2.set_title('Cinsiyete Göre Gelir')
        ax2.set_xlabel('Cinsiyet')
        ax2.set_ylabel('Toplam Gelir ($)')
        
        # Yüzde bilgilerini ekle
        for i, (bar, percent) in enumerate(zip(bars2, gender_percent)):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000, 
                    f'%{percent:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Grafiği canvas'a yerleştir
        canvas2 = FigureCanvasTkAgg(fig2, gender_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # MÜŞTERİ SEGMENTASYON ANALİZİ SONUÇLARI
        segment_frame = ttk.LabelFrame(customer_tab, text="Müşteri Segmentasyonu Analizi")
        segment_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Segmentasyon analizi sonuçları metni
        segment_info = """
        Müşteri Segmentasyonu Analizi Sonuçları:
        
        1. Üye müşteriler, toplam gelirin %50.85'ini oluşturmaktadır.
        2. Kadın müşteriler, toplam gelirin %51.98'ini oluşturmaktadır.
        3. Üye kadın müşteriler en çok Yiyecek ve İçecekler kategorisinde harcama yapmaktadır.
        4. Üye erkek müşteriler en çok Sağlık ve Güzellik kategorisinde harcama yapmaktadır.
        5. Normal kadın müşteriler en çok Elektronik Aksesuarlar kategorisinde harcama yapmaktadır.
        6. Normal erkek müşteriler en çok Spor ve Seyahat kategorisinde harcama yapmaktadır.
        
        Öneriler:
        - Üyelik programını güçlendirin (üyeler daha yüksek ortalama alışveriş değerine sahip)
        - Erkek müşterilere yönelik kampanyalar geliştirin
        - Müşteri segmentlerine özel teklifler sunun
        """
        
        # Segmentasyon sonuçları için metin alanı
        segment_text = scrolledtext.ScrolledText(segment_frame, wrap=tk.WORD, width=80, height=12, 
                                                font=("Arial", 10))
        segment_text.insert(tk.END, segment_info)
        segment_text.configure(state='disabled')  # Sadece okunabilir yap
        segment_text.pack(fill=tk.X, padx=5, pady=5)

    def create_branch_analysis_tab(self):
        """
        Şube analizi sekmesini oluşturur.
        Şube performansı ve şube-ürün kategori matrisi analizlerini içerir.
        """
        # Şube analizi sekmesini oluştur
        branch_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(branch_tab, text="Şube Analizi")
        
        # ŞUBE GELİR ANALİZİ
        branch_frame = ttk.LabelFrame(branch_tab, text="Şubelere Göre Gelir Analizi")
        branch_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Şube gelir grafiği oluştur
        fig, ax = plt.subplots(figsize=(10, 5))
        # Şubelere göre toplam geliri hesapla ve sırala
        branch_revenue = df.groupby('Branch')['Total'].sum().sort_values(ascending=False)
        # Yüzde oranlarını hesapla
        branch_percent = branch_revenue / branch_revenue.sum() * 100
        
        # Çubuk grafiği oluştur
        bars = ax.bar(branch_revenue.index, branch_revenue.values, color='salmon')
        ax.set_title('Şubelere Göre Toplam Gelir')
        ax.set_xlabel('Şube')
        ax.set_ylabel('Toplam Gelir ($)')
        
        # Yüzde bilgilerini ekle
        for i, (bar, percent) in enumerate(zip(bars, branch_percent)):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500, 
                    f'%{percent:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Grafiği canvas'a yerleştir
        canvas = FigureCanvasTkAgg(fig, branch_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ŞUBE-ÜRÜN KATEGORİSİ MATRİSİ ANALİZİ
        matrix_frame = ttk.LabelFrame(branch_tab, text="Şube-Ürün Kategorisi Matrisi")
        matrix_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Şube-Ürün matrisi grafiği oluştur
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        # Pivot tablo oluştur (şube vs ürün kategorisi)
        branch_product_pivot = pd.pivot_table(df, values='Total',
                                              index='Branch',
                                              columns='Product line',
                                              aggfunc='sum')
        
        # Isı haritası (heatmap) oluştur
        sns.heatmap(branch_product_pivot, annot=True, fmt='.0f', cmap='YlGnBu', 
                   linewidths=0.5, ax=ax2)
        ax2.set_title('Şube-Ürün Kategorisi Gelir Matrisi')
        ax2.set_ylabel('Şube')
        ax2.set_xlabel('Ürün Kategorisi')
        
        plt.tight_layout()
        
        # Grafiği canvas'a yerleştir
        canvas2 = FigureCanvasTkAgg(fig2, matrix_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ŞUBE ANALİZİ SONUÇLARI
        branch_info_frame = ttk.Frame(branch_tab)
        branch_info_frame.pack(pady=5, padx=20, fill=tk.X)
        
        # Şube analizi sonuçları metni
        branch_info = """
        Şube Analizi Sonuçları:
        
        1. Şube C (Naypyitaw) en yüksek gelire sahiptir (%34.24).
        2. Şube A (Yangon) ve Şube B (Mandalay) neredeyse aynı gelir seviyesine sahiptir (%32.88).
        3. Şube C'de en çok Yiyecek ve İçecekler kategorisi satılmaktadır.
        4. Şube A'da en çok Ev ve Yaşam Tarzı kategorisi satılmaktadır.
        5. Şube B'de en çok Spor ve Seyahat kategorisi satılmaktadır.
        
        Öneriler:
        - Şube C'nin başarı faktörlerini analiz edip diğer şubelere uygulayın
        - Şube B'de özellikle elektronik ve moda ürünlerine ağırlık verin
        - Şubeler arası performans karşılaştırma sistemi kurun
        """
        
        # Şube analizi sonuçları için metin alanı
        branch_info_text = scrolledtext.ScrolledText(branch_info_frame, wrap=tk.WORD, width=80, height=10, 
                                                    font=("Arial", 10))
        branch_info_text.insert(tk.END, branch_info)
        branch_info_text.configure(state='disabled')  # Sadece okunabilir yap
        branch_info_text.pack(fill=tk.X, padx=5, pady=5)

    def create_time_analysis_tab(self):
        """
        Zaman analizi sekmesini oluşturur.
        Saatlik ve aylık satış trendlerini analiz eder.
        """
        # Zaman analizi sekmesini oluştur
        time_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(time_tab, text="Zaman Analizi")
        
        # SAAT BAZINDA GELİR ANALİZİ
        hour_frame = ttk.LabelFrame(time_tab, text="Saat Bazında Gelir Analizi")
        hour_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Saatlik gelir grafiği oluştur
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Saat bilgisini Time sütunundan çıkar
        hourly_analysis = df.copy()
        hourly_analysis['Hour'] = pd.to_datetime(df['Time']).dt.hour
        # Saate göre toplam geliri hesapla
        hourly_revenue = hourly_analysis.groupby('Hour').agg({
            'Total': 'sum'
        }).sort_index()
        
        # Çizgi grafiği oluştur (trend analizi için uygun)
        ax.plot(hourly_revenue.index, hourly_revenue['Total'], marker='o', color='teal', linewidth=2)
        ax.set_title('Saat Bazında Gelir Dağılımı')
        ax.set_xlabel('Saat')
        ax.set_ylabel('Toplam Gelir ($)')
        ax.grid(True, linestyle='--', alpha=0.7)  # Grid ekle
        
        plt.tight_layout()
        
        # Grafiği canvas'a yerleştir
        canvas = FigureCanvasTkAgg(fig, hour_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # AYLIK GELİR ANALİZİ
        month_frame = ttk.LabelFrame(time_tab, text="Ay Bazında Gelir Analizi")
        month_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Aylık gelir grafiği oluştur
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        
        # Ay bazında toplam geliri hesapla (Month sütunu zaten mevcut)
        monthly_revenue = df.groupby('Month').agg({
            'Total': 'sum'
        })
        
        # Çubuk grafiği oluştur
        bars = ax2.bar(monthly_revenue.index, monthly_revenue['Total'], color='mediumpurple')
        ax2.set_title('Aylık Toplam Gelir')
        ax2.set_xlabel('Ay')
        ax2.set_ylabel('Toplam Gelir ($)')
        # X ekseni etiketlerini Türkçe ay isimleriyle değiştir
        ax2.set_xticks([1, 2, 3])
        ax2.set_xticklabels(['Ocak', 'Şubat', 'Mart'])
        
        plt.tight_layout()
        
        # Grafiği canvas'a yerleştir
        canvas2 = FigureCanvasTkAgg(fig2, month_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ZAMAN ANALİZİ SONUÇLARI
        time_info_frame = ttk.Frame(time_tab)
        time_info_frame.pack(pady=5, padx=20, fill=tk.X)
        
        # Zaman analizi sonuçları metni
        time_info = """
        Zaman Analizi Sonuçları:
        
        1. En yoğun satış saatleri: 19:00, 13:00, 10:00, 15:00 ve 14:00
        2. En düşük satış saatleri: Sabah saatleri (10:00 öncesi)
        3. Ocak ayında satışlar en yüksek seviyededir
        4. Şubat ayında satışlarda düşüş görülmektedir
        5. Mart ayında satışlar tekrar yükselme eğilimindedir
        
        Öneriler:
        - En yoğun satış saatlerinde (15:00-19:00) personel sayısını artırın
        - Sabah saatlerinde özel kampanyalar düzenleyerek müşteri trafiğini dengeleyin
        - Şubat ayı satışlarını artırmak için özel promosyonlar planlayın
        """
        
        # Zaman analizi sonuçları için metin alanı
        time_info_text = scrolledtext.ScrolledText(time_info_frame, wrap=tk.WORD, width=80, height=10, 
                                                  font=("Arial", 10))
        time_info_text.insert(tk.END, time_info)
        time_info_text.configure(state='disabled')  # Sadece okunabilir yap
        time_info_text.pack(fill=tk.X, padx=5, pady=5)

    def create_recommendations_tab(self):
        """
        Öneriler sekmesini oluşturur.
        Tüm analizlere dayalı kapsamlı strateji önerilerini içerir.
        """
        # Öneriler sekmesini oluştur
        recommendations_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(recommendations_tab, text="Öneriler")
        
        # Öneriler ana çerçevesi
        recommend_frame = ttk.Frame(recommendations_tab)
        recommend_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Öneriler başlığı
        title_label = ttk.Label(recommend_frame, text="ZİNCİR SÜPERMARKETLERİ İÇİN STRATEJİ ÖNERİLERİ", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # KAPSAMLI STRATEJİ ÖNERİLERİ METNİ
        recommendations_text = """
        1. ÜRÜN STRATEJİLERİ
        
        • Yiyecek ve İçecekler Kategorisinin Güçlendirilmesi:
          - Bu kategori hem en yüksek gelir getiren hem de müşteri memnuniyeti en yüksek kategoridir.
          - Ürün çeşitliliğinin artırılması ve özel promosyonlarla desteklenmesi gerekmektedir.
        
        • Spor ve Seyahat Kategorisinde Ürün Çeşitliliği:
          - İkinci en yüksek gelir getiren bu kategoride ürün gamını genişletmek ve sezonluk kampanyalar
            düzenlemek satışları artırabilir.
        
        • Sağlık ve Güzellik Kategorisinin Geliştirilmesi:
          - En düşük gelir payına sahip bu kategoride ürün kalitesini artırmak ve müşteri deneyimini
            iyileştirmek önemlidir.
        
        2. MÜŞTERİ STRATEJİLERİ
        
        • Üyelik Programının Güçlendirilmesi:
          - Üye müşteriler daha yüksek gelir getirdiğinden, üyelik avantajlarını artırmak ve
            yeni müşterileri üyeliğe teşvik etmek önemlidir.
        
        • Erkek Müşterilere Yönelik Kampanyalar:
          - Erkek müşterilerin harcama oranını artırmak için özel kampanyalar düzenlenmelidir.
        
        • Müşteri Sadakat Programları:
          - Müşteri sadakatini artırmak için puan toplama, özel indirimler ve kişiselleştirilmiş
            teklifler sunulmalıdır.
        
        3. ŞUBE STRATEJİLERİ
        
        • Şube C'nin Başarı Faktörlerinin Analizi:
          - En yüksek gelir getiren şubenin başarı faktörleri analiz edilip diğer şubelere de uygulanmalıdır.
        
        • Şube B'de Ürün Gamı Optimizasyonu:
          - Şube B'de özellikle elektronik ve moda ürünlerine ağırlık verilmelidir.
        
        • Şubeler Arası Performans Karşılaştırma Sistemi:
          - Şubeler arası rekabeti artıracak ve başarılı uygulamaların paylaşılmasını sağlayacak
            bir sistem kurulmalıdır.
        
        4. OPERASYONEL STRATEJİLER
        
        • Personel Planlaması:
          - En yoğun satış saatleri olan 19:00, 13:00 ve 15:00 saatlerinde personel sayısının artırılması,
            müşteri deneyimini iyileştirecektir.
        
        • Daha Az Yoğun Saatlerde Promosyonlar:
          - Sabah saatlerinde özel kampanyalar düzenleyerek müşteri trafiğini dengelemek gerekmektedir.
        
        • E-cüzdan Kullanımını Teşvik:
          - İşlem maliyetlerini düşürmek için e-cüzdan kullanımını teşvik edecek avantajlar sunulmalıdır.
        
        5. ZAMANSAL STRATEJİLER
        
        • Haftasonu Özel Kampanyaları:
          - Satışların en yüksek olduğu cumartesi günleri için özel kampanyalar düzenlenmelidir.
        
        • Aylık Satış Dalgalanmalarına Göre Planlama:
          - Şubat ayında görülen satış düşüşünün önlenmesi için özel stratejiler geliştirilmelidir.
        
        • Gün İçi Satış Stratejileri:
          - Satışların düşük olduğu saatlerde müşteri trafiğini artıracak promosyonlar planlanmalıdır.
        """
        
        # Öneriler için geniş kaydırılabilir metin alanı
        recommend_scroll = scrolledtext.ScrolledText(recommend_frame, wrap=tk.WORD, width=90, height=30, 
                                                    font=("Arial", 11))
        recommend_scroll.insert(tk.END, recommendations_text)
        recommend_scroll.configure(state='disabled')  # Sadece okunabilir yap
        recommend_scroll.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)


# UYGULAMA BAŞLATMA BÖLÜMÜ
# ========================
if __name__ == "__main__":
    # Tkinter ana pencere oluştur
    root = tk.Tk()
    # Uygulama nesnesini oluştur ve ana pencereyi geç
    app = SupermarketAnalysisApp(root)
    # Tkinter ana döngüsünü başlat (uygulamayı çalıştır)
    root.mainloop() 
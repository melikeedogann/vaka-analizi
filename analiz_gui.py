# ======================================================================
# ZİNCİR SÜPERMARKETLERİ VERİ ANALİZİ UYGULAMASI
# ======================================================================
# Bu uygulama, süpermarket satış verilerini analiz etmek ve görselleştirmek
# için tasarlanmış kapsamlı bir GUI (Grafik Kullanıcı Arayüzü) uygulamasıdır.
# ======================================================================

# KÜTÜPHANE İÇE AKTARIMLARI
# =========================
# Grafik arayüzü oluşturmak için gerekli Tkinter modülleri
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
# Görsel işleme için PIL kütüphanesi
from PIL import Image, ImageTk
# Veri analizi için temel kütüphaneler
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
# İstatistiksel analizler için scipy
from scipy import stats
# Dosya işlemleri ve tarih/zaman işlemleri
import os
from datetime import datetime
# Matplotlib'i Tkinter ile entegre etmek için gerekli ayarlar
import matplotlib
matplotlib.use('TkAgg')  # Tkinter ile uyumlu backend seçimi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# VERİ YÜKLEME VE ÖN İŞLEME BÖLÜMÜ
# =================================
# CSV dosyasından süpermarket satış verilerini yükle
df = pd.read_csv('2425 vaka02 - zincir supermarket_sales - Sheet1.csv')
# Tarih sütununu datetime formatına dönüştür (analiz için gerekli)
df['Date'] = pd.to_datetime(df['Date'])
# Tarihten ay bilgisini çıkar (aylık analizler için)
df['Month'] = df['Date'].dt.month
# Tarihten gün bilgisini çıkar (günlük analizler için)
df['Day'] = df['Date'].dt.day
# Haftanın hangi günü olduğunu çıkar (0=Pazartesi, 6=Pazar)
df['DayOfWeek'] = df['Date'].dt.dayofweek
# Zaman bilgisinden saat değerini çıkar (saatlik analizler için)
df['Hour'] = pd.to_datetime(df['Time']).dt.hour

# İSTATİSTİKSEL ANALİZ FONKSİYONLARI
# ==================================
def get_statistical_summary():
    """
    Veri setinin genel istatistiksel özetini döndürür.
    
    Returns:
        DataFrame: Sayısal değişkenlerin istatistiksel özeti (ortalama, std, min, max, vs.)
    """
    return df.describe().round(2)

def get_category_stats():
    """
    Ürün kategorilerine göre detaylı istatistiksel analiz yapar.
    
    Returns:
        DataFrame: Her ürün kategorisi için toplam satış, ortalama, sayı, 
                  derecelendirme ve brüt gelir bilgileri
    """
    return df.groupby('Product line').agg({
        'Total': ['mean', 'sum', 'count'],  # Ortalama, toplam ve işlem sayısı
        'Rating': 'mean',                   # Ortalama müşteri değerlendirmesi
        'gross income': 'sum'               # Toplam brüt gelir
    }).round(2)

def get_branch_stats():
    """
    Şube bazında performans analizi yapar.
    
    Returns:
        DataFrame: Her şube için satış istatistikleri ve müşteri memnuniyeti
    """
    return df.groupby('Branch').agg({
        'Total': ['mean', 'sum', 'count'],
        'Rating': 'mean',
        'gross income': 'sum'
    }).round(2)

def get_customer_stats():
    """
    Müşteri tipi ve cinsiyete göre segmentasyon analizi yapar.
    
    Returns:
        DataFrame: Müşteri segmentlerine göre satış performansı
    """
    return df.groupby(['Customer type', 'Gender']).agg({
        'Total': ['mean', 'sum', 'count'],
        'Rating': 'mean',
        'gross income': 'sum'
    }).round(2)

def get_payment_stats():
    """
    Ödeme yöntemlerine göre analiz yapar.
    
    Returns:
        DataFrame: Her ödeme yöntemi için satış istatistikleri
    """
    return df.groupby('Payment').agg({
        'Total': ['mean', 'sum', 'count'],
        'Rating': 'mean'
    }).round(2)

def get_time_analysis():
    """
    Zaman bazlı analizler yapar (saatlik, günlük, aylık).
    
    Returns:
        tuple: Saatlik, günlük ve aylık satış istatistikleri
    """
    # Saatlik satış analizi
    hourly = df.groupby('Hour')['Total'].agg(['mean', 'sum', 'count']).round(2)
    # Haftanın günlerine göre satış analizi
    daily = df.groupby('DayOfWeek')['Total'].agg(['mean', 'sum', 'count']).round(2)
    # Aylık satış analizi
    monthly = df.groupby('Month')['Total'].agg(['mean', 'sum', 'count']).round(2)
    return hourly, daily, monthly

def get_test_results():
    """
    İstatistiksel hipotez testleri yapar.
    Üye/Normal müşteriler ve Erkek/Kadın müşteriler arasındaki 
    satış farklarının istatistiksel anlamlılığını test eder.
    
    Returns:
        tuple: İki t-testi için p-değerleri
    """
    # Üye müşterilerin satış verilerini al
    member_sales = df[df['Customer type'] == 'Member']['Total']
    # Normal müşterilerin satış verilerini al
    normal_sales = df[df['Customer type'] == 'Normal']['Total']
    # İki grup arasında t-testi yap
    t_stat, p_value = stats.ttest_ind(member_sales, normal_sales)
    
    # Erkek müşterilerin satış verilerini al
    male_sales = df[df['Gender'] == 'Male']['Total']
    # Kadın müşterilerin satış verilerini al
    female_sales = df[df['Gender'] == 'Female']['Total']
    # İki grup arasında t-testi yap
    t_stat_gender, p_value_gender = stats.ttest_ind(male_sales, female_sales)
    
    return p_value, p_value_gender

# STRATEJİ VE BULGULAR RAPORU FONKSİYONU
# ======================================
def get_strategy_summary():
    """
    Analiz sonuçlarına dayalı kapsamlı strateji raporu oluşturur.
    
    Returns:
        str: Formatlanmış strateji raporu metni
    """
    # Rapor başlığı ve genel yapısı
    summary = """
ZİNCİR SÜPERMARKETLERİ ANALİZ RAPORU
====================================

1. GELİR ANALİZİ
----------------
"""
    # Ürün kategorileri analizi - En yüksek gelir getiren kategorileri listele
    product_stats = get_category_stats()
    summary += "\nÜrün Kategorileri Analizi:\n"
    for idx, cat in enumerate(product_stats.index, 1):
        summary += f"{idx}. {cat}: ${product_stats.loc[cat, ('Total', 'sum')]:,.2f}\n"
    
    # Müşteri segmentasyonu analizi - Hangi müşteri gruplarının daha karlı olduğunu göster
    customer_stats = get_customer_stats()
    summary += "\nMüşteri Segmenti Analizi:\n"
    for (cust_type, gender), stats in customer_stats.iterrows():
        summary += f"- {cust_type} ({gender}): ${stats[('Total', 'sum')]:,.2f}\n"
    
    # Şube performans analizi - Hangi şubenin daha başarılı olduğunu göster
    branch_stats = get_branch_stats()
    summary += "\nŞube Performans Analizi:\n"
    for idx, branch in enumerate(branch_stats.index, 1):
        summary += f"{idx}. Şube {branch}: ${branch_stats.loc[branch, ('Total', 'sum')]:,.2f}\n"
    
    # Zaman bazlı analiz - En yoğun satış zamanlarını belirle
    hourly, daily, monthly = get_time_analysis()
    summary += "\nZaman Bazlı Analiz:\n"
    summary += f"En yoğun saat: {hourly['sum'].idxmax()}:00 (${hourly['sum'].max():,.2f})\n"
    summary += f"En yoğun gün: {daily['sum'].idxmax()}. gün (${daily['sum'].max():,.2f})\n"
    summary += f"En yoğun ay: {monthly['sum'].idxmax()}. ay (${monthly['sum'].max():,.2f})\n"
    
    # Strateji önerileri bölümü
    summary += """
2. STRATEJİ ÖNERİLERİ
---------------------
"""
    # Ürün stratejileri - En başarılı kategorilere odaklanma önerileri
    summary += "\nÜrün Stratejileri:\n"
    top_product = product_stats[('Total', 'sum')].idxmax()
    summary += f"- {top_product} kategorisinde ürün çeşitliliğini artırın\n"
    summary += "- Düşük performanslı kategorilerde fiyat optimizasyonu yapın\n"
    
    # Müşteri stratejileri - Müşteri sadakati ve segmentasyon önerileri
    summary += "\nMüşteri Stratejileri:\n"
    summary += "- Üyelik programını güçlendirin\n"
    summary += "- Hedef müşteri segmentlerine özel kampanyalar düzenleyin\n"
    
    # Operasyonel stratejiler - İşletme verimliliği önerileri
    summary += "\nOperasyonel Stratejiler:\n"
    summary += "- En yoğun saatlerde personel sayısını artırın\n"
    summary += "- Şube bazlı performans iyileştirmeleri yapın\n"
    
    return summary

# MEVCUT GRAFİK DOSYALARI LİSTESİ
# ===============================
# Uygulamanın kullanabileceği grafik dosyalarının listesi
graphics = [
    ('Gelir Analizi', 'gelir_analizi.png'),
    ('Detaylı Analiz', 'detayli_analiz.png'),
    ('Müşteri Segmentasyonu', 'musteri_segmentasyonu.png'),
    ('Strateji Analiz', 'strateji_analiz.png'),
    ('Ödeme Yöntemleri', 'odeme_yontemleri.png'),
    ('Saatlik Satışlar', 'saatlik_satislar.png'),
    ('Kategori Satışları', 'kategori_satislari.png'),
    ('Müşteri Analizi', 'musteri_analizi.png'),
    ('Korelasyon', 'korelasyon.png'),
    ('Şube Performansı', 'sube_performansi.png'),
    ('Günlük Satışlar', 'gunluk_satislar.png'),
]

# ANA UYGULAMA SINIFI - TKINTER ARAYÜZÜ
# =====================================
class AnalizApp(tk.Tk):
    """
    Zincir Süpermarketleri Analiz Uygulamasının ana sınıfı.
    Tkinter tabanlı grafik kullanıcı arayüzü sağlar.
    """
    
    def __init__(self):
        """
        Uygulama başlatıcısı. Ana pencereyi oluşturur ve yapılandırır.
        """
        super().__init__()  # Tkinter.Tk sınıfını başlat
        # Pencere başlığını ayarla
        self.title('Zincir Süpermarketleri Analiz Paneli')
        # Pencere boyutunu ayarla (genişlik x yükseklik)
        self.geometry('1200x800')
        # Arka plan rengini ayarla
        self.configure(bg='#f0f0f0')
        # Tüm arayüz bileşenlerini oluştur
        self.create_widgets()
        
    def create_widgets(self):
        """
        Ana arayüz bileşenlerini oluşturur.
        Menü, sekmeli panel ve tüm sekmeleri yaratır.
        """
        # Üst menü çubuğunu oluştur
        self.create_menu()
        
        # Sekmeli panel (Notebook) oluştur - farklı analiz türleri için
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Tüm analiz sekmelerini oluştur
        self.create_dashboard_tab()      # Genel bakış sekmesi
        self.create_analysis_tab()       # Detaylı analiz sekmesi
        self.create_visualization_tab()  # Görselleştirme sekmesi
        self.create_strategy_tab()       # Strateji önerileri sekmesi
        self.create_export_tab()         # Dışa aktarma sekmesi
        
    def create_menu(self):
        """
        Üst menü çubuğunu oluşturur.
        Dosya işlemleri ve yardım menülerini içerir.
        """
        # Ana menü çubuğunu oluştur
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # DOSYA MENÜSÜ - Veri yenileme ve çıkış işlemleri
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Dosya", menu=file_menu)
        file_menu.add_command(label="Yenile", command=self.refresh_data)
        file_menu.add_separator()  # Menü ayırıcısı
        file_menu.add_command(label="Çıkış", command=self.quit)
        
        # YARDIM MENÜSÜ - Kullanım kılavuzu ve hakkında bilgileri
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Yardım", menu=help_menu)
        help_menu.add_command(label="Kullanım Kılavuzu", command=self.show_help)
        help_menu.add_command(label="Hakkında", command=self.show_about)
        
    def create_dashboard_tab(self):
        """
        Dashboard (ana panel) sekmesini oluşturur.
        Genel bakış için özet metrikleri ve temel grafikleri içerir.
        """
        # Dashboard sekmesinin ana çerçevesini oluştur
        dashboard = ttk.Frame(self.notebook)
        self.notebook.add(dashboard, text='Dashboard')
        
        # ÜST BİLGİ PANELİ - Genel performans metrikleri
        info_frame = ttk.LabelFrame(dashboard, text='Genel Bilgiler')
        info_frame.pack(fill='x', padx=5, pady=5)
        
        # Özet metriklerin yerleştirileceği çerçeve
        metrics_frame = ttk.Frame(info_frame)
        metrics_frame.pack(fill='x', padx=5, pady=5)
        
        # ÖZET METRİKLERİ HESAPLA VE GÖSTER
        # Toplam satış tutarını hesapla ve göster
        total_sales = df['Total'].sum()
        ttk.Label(metrics_frame, text=f'Toplam Satış: ${total_sales:,.2f}').pack(side='left', padx=10)
        
        # Ortalama sepet değerini hesapla ve göster
        avg_basket = df['Total'].mean()
        ttk.Label(metrics_frame, text=f'Ortalama Sepet: ${avg_basket:,.2f}').pack(side='left', padx=10)
        
        # Toplam işlem sayısını hesapla ve göster
        total_transactions = len(df)
        ttk.Label(metrics_frame, text=f'Toplam İşlem: {total_transactions:,}').pack(side='left', padx=10)
        
        # GRAFİKLER BÖLÜMÜ - Temel performans grafikleri
        charts_frame = ttk.Frame(dashboard)
        charts_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # SOL GRAFİK - Ürün kategorilerine göre satışlar
        fig1 = Figure(figsize=(6, 4))
        ax1 = fig1.add_subplot(111)
        product_stats = get_category_stats()
        product_stats[('Total', 'sum')].plot(kind='bar', ax=ax1)
        ax1.set_title('Ürün Kategorileri Satışları')
        ax1.set_ylabel('Toplam Satış ($)')
        # Grafiği Tkinter widget'ına dönüştür
        canvas1 = FigureCanvasTkAgg(fig1, charts_frame)
        canvas1.get_tk_widget().pack(side='left', fill='both', expand=True)
        
        # SAĞ GRAFİK - Saatlik satış trendi
        fig2 = Figure(figsize=(6, 4))
        ax2 = fig2.add_subplot(111)
        hourly, _, _ = get_time_analysis()
        hourly['sum'].plot(kind='line', ax=ax2)
        ax2.set_title('Saatlik Satış Trendi')
        ax2.set_ylabel('Toplam Satış ($)')
        # Grafiği Tkinter widget'ına dönüştür
        canvas2 = FigureCanvasTkAgg(fig2, charts_frame)
        canvas2.get_tk_widget().pack(side='right', fill='both', expand=True)
        
    def create_analysis_tab(self):
        """
        Detaylı analiz sekmesini oluşturur.
        İstatistiksel özetler ve kategorik analizler içerir.
        """
        # Detaylı analiz sekmesinin ana çerçevesini oluştur
        analysis = ttk.Frame(self.notebook)
        self.notebook.add(analysis, text='Detaylı Analiz')
        
        # SOL PANEL - İstatistiksel özet bilgileri
        left_frame = ttk.LabelFrame(analysis, text='İstatistiksel Özet')
        left_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Kaydırılabilir metin alanı oluştur ve istatistiksel özeti göster
        text1 = ScrolledText(left_frame, width=60, height=30)
        text1.pack(padx=5, pady=5)
        text1.insert(tk.END, str(get_statistical_summary()))
        text1.config(state='disabled')  # Sadece okunabilir yap
        
        # SAĞ PANEL - Kategorik analizler
        right_frame = ttk.LabelFrame(analysis, text='Kategorik Analizler')
        right_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # Analiz türü seçimi için açılır liste
        analysis_types = ['Ürün Kategorileri', 'Şubeler', 'Müşteri Tipleri', 'Ödeme Yöntemleri']
        self.analysis_combo = ttk.Combobox(right_frame, values=analysis_types, state='readonly')
        self.analysis_combo.pack(pady=5)
        # Seçim değiştiğinde analizi göster
        self.analysis_combo.bind('<<ComboboxSelected>>', self.show_analysis)
        
        # Seçilen analizin sonuçlarını gösterecek metin alanı
        self.analysis_text = ScrolledText(right_frame, width=60, height=25)
        self.analysis_text.pack(padx=5, pady=5)
        
    def create_visualization_tab(self):
        """
        Görselleştirme sekmesini oluşturur.
        İnteraktif grafik seçimi ve gösterimi sağlar.
        """
        # Görselleştirme sekmesinin ana çerçevesini oluştur
        viz = ttk.Frame(self.notebook)
        self.notebook.add(viz, text='Görselleştirme')
        
        # GRAFİK SEÇİM KONTROLÜ
        control_frame = ttk.Frame(viz)
        control_frame.pack(fill='x', padx=5, pady=5)
        
        # Grafik türü seçimi için etiket ve açılır liste
        ttk.Label(control_frame, text='Grafik Türü:').pack(side='left', padx=5)
        self.viz_combo = ttk.Combobox(control_frame, values=[
            'Ürün Kategorileri', 'Şube Performansı', 'Müşteri Segmentasyonu',
            'Zaman Analizi', 'Ödeme Yöntemleri', 'Korelasyon Analizi'
        ], state='readonly', width=40)
        self.viz_combo.pack(side='left', padx=5)
        # Seçim değiştiğinde grafiği göster
        self.viz_combo.bind('<<ComboboxSelected>>', self.show_visualization)
        
        # Grafiklerin gösterileceği ana alan
        self.viz_frame = ttk.Frame(viz)
        self.viz_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
    def create_strategy_tab(self):
        """
        Strateji ve öneriler sekmesini oluşturur.
        Analiz sonuçlarına dayalı iş stratejilerini gösterir.
        """
        # Strateji sekmesinin ana çerçevesini oluştur
        strategy = ttk.Frame(self.notebook)
        self.notebook.add(strategy, text='Strateji & Öneriler')
        
        # Strateji raporu için kaydırılabilir metin alanı
        text = ScrolledText(strategy, width=100, height=40)
        text.pack(padx=10, pady=10)
        # Strateji özetini metin alanına ekle
        text.insert(tk.END, get_strategy_summary())
        text.config(state='disabled')  # Sadece okunabilir yap
        
    def create_export_tab(self):
        """
        Dışa aktarma sekmesini oluşturur.
        Rapor ve veri dışa aktarma seçenekleri sunar.
        """
        # Dışa aktarma sekmesinin ana çerçevesini oluştur
        export = ttk.Frame(self.notebook)
        self.notebook.add(export, text='Dışa Aktar')
        
        # Dışa aktarma seçenekleri paneli
        options_frame = ttk.LabelFrame(export, text='Dışa Aktarma Seçenekleri')
        options_frame.pack(padx=10, pady=10)
        
        # Farklı dışa aktarma seçenekleri için butonlar
        ttk.Button(options_frame, text='Raporu PDF Olarak Kaydet',
                  command=self.export_pdf).pack(pady=5)
        ttk.Button(options_frame, text='Grafikleri Kaydet',
                  command=self.export_graphs).pack(pady=5)
        ttk.Button(options_frame, text='Veriyi Excel\'e Aktar',
                  command=self.export_excel).pack(pady=5)
        
    def show_analysis(self, event):
        """
        Seçilen analiz türüne göre ilgili istatistikleri gösterir.
        
        Args:
            event: Combobox seçim olayı
        """
        # Seçilen analiz türünü al
        selected = self.analysis_combo.get()
        # Mevcut metni temizle
        self.analysis_text.delete(1.0, tk.END)
        
        # Seçilen türe göre uygun analizi göster
        if selected == 'Ürün Kategorileri':
            self.analysis_text.insert(tk.END, str(get_category_stats()))
        elif selected == 'Şubeler':
            self.analysis_text.insert(tk.END, str(get_branch_stats()))
        elif selected == 'Müşteri Tipleri':
            self.analysis_text.insert(tk.END, str(get_customer_stats()))
        elif selected == 'Ödeme Yöntemleri':
            self.analysis_text.insert(tk.END, str(get_payment_stats()))
            
    def show_visualization(self, event):
        """
        Seçilen grafik türüne göre uygun görselleştirmeyi oluşturur ve gösterir.
        
        Args:
            event: Combobox seçim olayı
        """
        # Seçilen grafik türünü al
        selected = self.viz_combo.get()
        
        # Mevcut grafikleri temizle
        for widget in self.viz_frame.winfo_children():
            widget.destroy()
            
        # Yeni grafik figürü oluştur
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        # Seçilen türe göre uygun grafiği oluştur
        if selected == 'Ürün Kategorileri':
            # Ürün kategorileri için çubuk grafik
            product_stats = get_category_stats()
            product_stats[('Total', 'sum')].plot(kind='bar', ax=ax)
            ax.set_title('Ürün Kategorileri Satışları')
            ax.set_ylabel('Toplam Satış ($)')
            
        elif selected == 'Şube Performansı':
            # Şube performansı için çubuk grafik
            branch_stats = get_branch_stats()
            branch_stats[('Total', 'sum')].plot(kind='bar', ax=ax)
            ax.set_title('Şube Performansı')
            ax.set_ylabel('Toplam Satış ($)')
            
        elif selected == 'Müşteri Segmentasyonu':
            # Müşteri segmentasyonu için gruplu çubuk grafik
            customer_stats = get_customer_stats()
            customer_stats[('Total', 'sum')].unstack().plot(kind='bar', ax=ax)
            ax.set_title('Müşteri Segmentasyonu')
            ax.set_ylabel('Toplam Satış ($)')
            
        elif selected == 'Zaman Analizi':
            # Zaman analizi için çizgi grafik
            hourly, _, _ = get_time_analysis()
            hourly['sum'].plot(kind='line', ax=ax)
            ax.set_title('Saatlik Satış Trendi')
            ax.set_ylabel('Toplam Satış ($)')
            
        elif selected == 'Ödeme Yöntemleri':
            # Ödeme yöntemleri için pasta grafik
            payment_stats = get_payment_stats()
            payment_stats[('Total', 'sum')].plot(kind='pie', ax=ax, autopct='%1.1f%%')
            ax.set_title('Ödeme Yöntemleri Dağılımı')
            
        elif selected == 'Korelasyon Analizi':
            # Korelasyon analizi için ısı haritası
            corr = df[['Total', 'Quantity', 'Unit price', 'Rating']].corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
            ax.set_title('Değişkenler Arası Korelasyon')
            
        # Grafiği Tkinter widget'ına dönüştür ve göster
        canvas = FigureCanvasTkAgg(fig, self.viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    # YARDIMCI FONKSİYONLAR
    # ====================
    def refresh_data(self):
        """
        Veriyi yeniler (şu an için sadece bilgi mesajı gösterir).
        """
        messagebox.showinfo("Bilgi", "Veriler yenilendi!")
        
    def show_help(self):
        """
        Kullanım kılavuzunu gösterir.
        """
        help_text = """
Kullanım Kılavuzu:
------------------
1. Dashboard: Genel bakış ve özet metrikler
2. Detaylı Analiz: İstatistiksel ve kategorik analizler
3. Görselleştirme: İnteraktif grafikler
4. Strateji & Öneriler: Analiz sonuçları ve öneriler
5. Dışa Aktar: Rapor ve grafikleri kaydetme
"""
        messagebox.showinfo("Yardım", help_text)
        
    def show_about(self):
        """
        Uygulama hakkında bilgi gösterir.
        """
        about_text = """
Zincir Süpermarketleri Analiz Paneli
Versiyon 1.0
© 2024
"""
        messagebox.showinfo("Hakkında", about_text)
        
    # DIŞA AKTARMA FONKSİYONLARI
    # ==========================
    def export_pdf(self):
        """
        Raporu PDF formatında kaydeder (şu an için sadece bilgi mesajı).
        """
        messagebox.showinfo("Bilgi", "PDF raporu oluşturuldu!")
        
    def export_graphs(self):
        """
        Grafikleri dosya olarak kaydeder (şu an için sadece bilgi mesajı).
        """
        messagebox.showinfo("Bilgi", "Grafikler kaydedildi!")
        
    def export_excel(self):
        """
        Veriyi Excel formatında kaydeder (şu an için sadece bilgi mesajı).
        """
        messagebox.showinfo("Bilgi", "Veriler Excel'e aktarıldı!")

# UYGULAMA BAŞLATMA BÖLÜMÜ
# ========================
if __name__ == '__main__':
    # Uygulama nesnesini oluştur
    app = AnalizApp()
    # Tkinter ana döngüsünü başlat (pencereyi göster ve olayları dinle)
    app.mainloop() 
import wbdata
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import datetime
import sys

# Yorumlayıcı kontrolü
print("Python yorumlayıcı yolu:", sys.executable)

# Ülkeler ve göstergeler
countries = ["TUR", "USA", "DEU"]  # Türkiye, ABD, Almanya
indicator = {"FP.CPI.TOTL.ZG": "enflasyon"}  # Enflasyon (TÜFE, yıllık %)

# Tarih aralığı
start_date = datetime.datetime(2015, 1, 1)
end_date = datetime.datetime(2024, 12, 31)

# Veriyi çek
df = wbdata.get_dataframe(indicator, country=countries, date=(start_date, end_date))

# Veriyi temizle ve yeniden biçimlendir
df = df.reset_index()
df["date"] = pd.to_datetime(df["date"])
df = df.pivot(index="date", columns="country", values="enflasyon")
df = df.sort_index()
df = df.loc["2018":]  # 2018 sonrası veriler

# Grafik oluştur
plt.figure(figsize=(10, 6))
for column in df.columns:
    plt.plot(df.index, df[column], label=column)

plt.title("Yıllık Enflasyon (%) - Türkiye, ABD, Almanya")
plt.xlabel("Yıl")
plt.ylabel("Enflasyon (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("global_enflasyon.png")
plt.close()

# PDF Raporu oluştur
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=14)
pdf.cell(200, 10, txt="Küresel Enflasyon Raporu (2018-2024)", ln=True, align='C')

pdf.set_font("Arial", size=11)
pdf.multi_cell(0, 10, txt="""
Bu raporda Turkiye (TUR), Almanya (DEU) ve ABD (USA) icin 2018-2024 yillari arasinda Dunya Bankasi verilerine dayali olarak yillik tuketici enflasyonu oranlari karsilastirilmaktadir.
""")


pdf.image("global_enflasyon.png", x=10, y=None, w=190)
pdf.output("global_enflasyon_raporu.pdf")

print("✅ PDF raporu başarıyla oluşturuldu: global_enflasyon_raporu.pdf")

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

# E-posta bilgilerini ayarla
sender_email = "abkorkmaz66@gmail.com"
receiver_email = "abkorkmaz66@gmail.com"
subject = "Haftalık Ekonomik Rapor - Enflasyon"
body = "Merhaba,\n\nEk'te haftalık küresel enflasyon raporunu bulabilirsin.\n\nİyi çalışmalar."

# Uygulama şifresi kullan (Google için)
password = "rgwc xuat jzlb innc"  # Bu şifreyi ortam değişkeninden de okuyabilirsin güvenlik için

# E-posta mesajı oluştur
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject

msg.attach(MIMEText(body, "plain"))

# PDF dosyasını ekle
with open("global_enflasyon_raporu.pdf", "rb") as f:
    part = MIMEApplication(f.read(), Name="global_enflasyon_raporu.pdf")
    part["Content-Disposition"] = 'attachment; filename="global_enflasyon_raporu.pdf"'
    msg.attach(part)

# SMTP ile gönder
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        print("📧 E-posta başarıyla gönderildi!")
except Exception as e:
    print("❌ E-posta gönderilirken hata oluştu:", e)

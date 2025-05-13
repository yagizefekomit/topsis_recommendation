from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# Aranacak telefon listesi
product_list = ['Samsung Galaxy S25 Ultra 512 GB', 'Samsung Galaxy S25 Ultra 256 GB', 'Samsung Galaxy S25 256 GB', 'Samsung Galaxy S24 Ultra 1 TB', 'Samsung Galaxy S24 Ultra 512 GB', 'Samsung Galaxy S24 FE 256 GB', 'Samsung Galaxy S24 FE 256 GB', 'Samsung Galaxy S24 FE 128 GB', 'Samsung Galaxy S23 Ultra 512 GB 12 GB', 'Samsung Galaxy S23 Plus 256 GB', 'Samsung Galaxy S23 FE 128 GB', 'Samsung Galaxy S23 256 GB', 'Samsung Galaxy Z Fold 6 512 GB', 'Samsung Galaxy Z Flip 6 256 GB', 'Samsung Galaxy Z Fold 5 256 GB', 'Samsung Galaxy Z Flip 5 256 GB', 'Samsung Galaxy A56 256 GB', 'Samsung Galaxy A56 128 GB', 'Samsung Galaxy A55 256 GB', 'Samsung Galaxy A55 128 GB', 'Samsung Galaxy A54 256 GB', 'Samsung Galaxy A54 128 GB', 'Samsung Galaxy A36 256 GB', 'Samsung Galaxy A36 128 GB', 'Samsung Galaxy A35 256 GB', 'Samsung Galaxy A35 128 GB', 'Samsung Galaxy A34 256 GB', 'Samsung Galaxy A26 256 GB 8 GB', 'Samsung Galaxy A25 128 GB 6 GB Siyah', 'Samsung Galaxy A24 128 GB', 'Samsung Galaxy A15 128 GB 4 GB', 'Samsung Galaxy A14 128 GB', 'Samsung Galaxy A06 128 GB', 'Samsung Galaxy A05 128 GB', 'Samsung Galaxy A05s 128 GB', 'Samsung Galaxy M34 128 GB', 'Samsung Galaxy M15 128 GB', 'Samsung Galaxy M12 64 GB', 'iPhone 16 Pro Max 1 TB', 'iPhone 16 Pro Max 512 GB', 'iPhone 16 Pro Max 256 GB', 'iPhone 16 Pro 128 GB', 'iPhone 16 Pro Max 256 GB', 'iPhone 16 Pro Max 512 GB', 'iPhone 16 Pro Max 1 TB', 'iPhone 16 Plus 512 GB', 'iPhone 16 Plus 256 GB', 'iPhone 16 Plus 128 GB', 'iPhone 16 Pro 128 GB', 'iPhone 16 Pro Max 256 GB', 'iPhone 16 Pro Max 512 GB', 'iPhone 16e 256 GB', 'iPhone 16e 128 GB', 'iPhone 15 Pro Max 1 TB', 'iPhone 15 Pro Max 512 GB', 'iPhone 15 Pro Max 256 GB', 'iPhone 15 Pro 128 GB', 'iPhone 15 Pro Max 256 GB', 'iPhone 15 Pro Max 512 GB', 'iPhone 15 Plus 512 GB', 'iPhone 15 Plus 256 GB', 'iPhone 15 Plus 128 GB', 'iPhone 15 128 GB', 'iPhone 15 Pro Max 256 GB', 'iPhone 15 Pro Max 512 GB', 'Xiaomi 15 512 GB', 'Xiaomi 15 256 GB', 'Xiaomi 15 UItra 512 GB', 'Xiaomi 14T Pro 512 GB', 'Xiaomi 14 Ultra 512 GB', 'Xiaomi 13 Ultra 256 GB 12 GB', 'Xiaomi 13T Pro 512 GB', 'Xiaomi 13 Lite 256 GB', 'Xiaomi MIX Flip 512 GB', 'Xiaomi Redmi Note 14 Pro Plus 512 GB', 'Xiaomi Redmi Note 14 256 GB', 'Xiaomi Redmi Note 13 Pro Plus 5G 512 GB', 'Xiaomi Redmi Note 13 Pro 256 GB 8 GB', 'Xiaomi Redmi 13C 256 GB 8 GB', 'Xiaomi Redmi 14C 256 GB 8 GB', 'Xiaomi Redmi Note 12 Pro 5G 256 GB', 'Xiaomi Redmi Note 12 Pro 5G 256 GB', 'Xiaomi Redmi Note 12R 128 GB', 'Xiaomi Redmi Note 12 128 GB 8 GB', 'Xiaomi Redmi A2 Plus 64 GB 4 GB', 'Realme GT 7 Pro 512 GB', 'Realme GT 6 512 GB 16 GB', 'Realme GT 6T 256 GB', 'Realme 12 Pro Plus 512 GB 12 GB', 'Realme 12 Pro Plus 256 GB 8 GB', 'Realme 12 Plus 256 GB', 'Realme 12 512 GB', 'Realme 11 Pro Plus 512 GB', 'Realme 11 Pro 256 GB', 'Realme 11 128 GB', 'Realme C75 512 GB', 'Realme C75 256 GB', 'Realme C65 128 GB 8 GB', 'Realme C53 256 GB 8 GB', 'Realme C55 256 GB', 'Realme C51 128 GB', 'Realme Note 60 128 GB 4 GB', 'Realme Note 50 128 GB', 'Tecno Camon 30 Pro 512 GB Gri', 'Tecno Camon 30S Pro 256 GB', 'Tecno Camon 30 256 GB 12 GB', 'Tecno Camon 30 5G 512 GB', 'Tecno Camon 20 Premier 512 GB', 'Tecno Pova 6 Pro 256 GB', 'Tecno Pova 6 Pro 256 GB', 'Tecno Pova 5 Pro 256 GB', 'Tecno Pova 5 256 GB', 'Tecno Spark 30 Pro 256 GB Siyah', 'Tecno Spark 30C 256 GB 8 GB', 'Tecno Spark 20 Pro Plus 256 GB', 'Tecno Spark 20 Pro 256 GB 8 GB', 'Tecno Spark 20 128 GB', 'Tecno Spark 20C 128 GB 8 GB', 'Tecno Spark 10 Pro 128 GB', 'Tecno Spark 10 128 GB 8 GB', 'Tecno Spark Go 1 128 GB', 'Tecno Spark Go 2024 128 GB']

# Chrome başlat
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.akakce.com/")
driver.maximize_window()
time.sleep(2)

# Veriyi yazacağımız CSV dosyası
csv_filename = "akakce_urun_gorselleri.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Telefon Adı", "Görsel URL"])

    for product_name in product_list:
        # Ana sayfaya dön
        driver.get("https://www.akakce.com/")
        time.sleep(2)

        # Arama kutusuna ürün ismini yaz ve enterla
        search_box = driver.find_element(By.NAME, "q")
        search_box.clear()
        search_box.send_keys(product_name)
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

        # İlk ürüne tıkla
        #try:
        #    first_product = driver.find_element(By.CSS_SELECTOR, "div#PL > ul > li > a")
        #    first_product.click()
        #    time.sleep(3)

            # Ürün görseli al
        try:
            image_element = driver.find_element(By.CSS_SELECTOR, "#APL > li:nth-child(1) > a > figure > img")
            image_url = image_element.get_attribute("src")
        except:
            image_url = "Görsel bulunamadı"
        #except:
        #    image_url = "Ürün bulunamadı"

        # CSV'ye yaz
        writer.writerow([product_name, image_url])
        print(f"{product_name} → {image_url}")

# Tarayıcıyı kapat
driver.quit()
print(f"Tüm veriler '{csv_filename}' dosyasına kaydedildi.")

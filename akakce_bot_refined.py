# -*- coding: utf-8 -*-
import csv
import time
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def login(driver, username, password):
    driver.get("https://www.akakce.com")
    # … mevcut login adımların aynen gelsin …

def scrape_phone_specs(driver, model_name, columns):
    # 1) Arama ve sayfaya gitme
    #search_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name*='Search']")))
    search_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='q'], input[id*='Search']")) # '//*[@id="ACList4[object HTMLInputElement]"]'
    )
    search_input.clear()
    search_input.send_keys(model_name)
    search_input.send_keys(Keys.ENTER)
    #first_result = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#APL li:first-child a")))
    first_result = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#APL > li:nth-child(1) > a > span > span.bt_v8")) # #APL > li:nth-child(1) > a > span > span.bt_v8
    )
    first_result.click()
    time.sleep(3)  # sayfa yüklenmesi için

    # 2) BeautifulSoup ile sayfa kaynağını oku
    soup = BeautifulSoup(driver.page_source, "html.parser")

    specs = {"Model": model_name}

    # 2.1) Aratılan modeli doğrulamak için ismini al
    desc = soup.select_one("#pd_v8 > div.pdt_v8 > h1") # #pd_v8 > div.pdt_v8 > h1
    specs["desc"] = desc.get_text(strip=True)

    # 3) İstenen tüm kolonlar için ayrı ayrı çek, eksikse 'x' ata
    for col in columns:
        if col == "Model" or col == "Fiyat" or col == "desc":
            continue
        cell = soup.find("td", string=lambda t: t and t.strip() == col)
        if cell:
            val = cell.find_next_sibling("td")
            specs[col] = val.get_text(strip=True) if val else "x"
        else:
            specs[col] = "x"

    # 4) Fiyatı en sonunda çek
    price_elem = soup.select_one("#pd_v8 > div.bb_w > span.pb_v8 > span")
    specs["Fiyat"] = price_elem.get_text(strip=True) if price_elem else "x"

    return specs

def main():
    username = input("Akakçe e-posta adresiniz: ")
    password = getpass("Şifreniz: ")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        login(driver, username, password)
        print("✅ Giriş başarılı!")

        # Sorgulanacak kolonlar
        columns = [
            "Model","desc","Seri","RAM Kapasitesi","Dahili Hafıza","Batarya Kapasitesi",
            "Ekran Boyutu","Ekran Çözünürlüğü","Ekran Yenileme Hızı","Ekran Teknolojisi",
            "Ekran Parlaklık Değeri","Çıkış Yılı","Piksel Yoğunluğu","Ekran Gövde Oranı",
            "Ekran Dayanıklılığı","Dokunmatik","HDR","Always on Display",
            "Arka Kamera Sayısı","Arka Kamera","İkinci Arka Kamera","Üçüncü Arka Kamera",
            "Dördüncü Arka Kamera","Video Kayıt Çözünürlüğü","Video FPS Değeri",
            "Ön Kamera","Ön Kamera Video Çözünürlüğü","Ön Kamera Video FPS Değeri",
            "Ekran İçinde Ön Kamera","Optik Görüntü Sabitleme","İşletim Sistemi",
            "İşlemci (CPU)","İşlemci Hızı","Çekirdek Sayısı","Grafik İşlemcisi (GPU)",
            "Chipset","Ağırlık","Boyut","Fiyat"
        ]

        # Sorgulanacak telefon modelleri
        phones = ['Samsung Galaxy S25 Ultra 512 GB', 'Samsung Galaxy S25 Ultra 256 GB', 'Samsung Galaxy S25+ 256 GB', 'Samsung Galaxy S24 Ultra 1 TB', 'Samsung Galaxy S24 Ultra 512 GB', 'Samsung Galaxy S24+', 'Samsung Galaxy S24 FE', 'Samsung Galaxy S24 FE 128 GB', 'Samsung Galaxy S23 Ultra', 'Samsung Galaxy S23 Plus', 'Samsung Galaxy S23 FE', 'Samsung Galaxy S23 256 GB', 'Samsung Galaxy Z Fold 6', 'Samsung Galaxy Z Flip 6', 'Samsung Galaxy Z Fold 5', 'Samsung Galaxy Z Flip 5', 'Samsung Galaxy A56 256 GB', 'Samsung Galaxy A56 128 GB', 'Samsung Galaxy A55 256 GB', 'Samsung Galaxy A55 128 GB', 'Samsung Galaxy A54 256 GB', 'Samsung Galaxy A54 128 GB', 'Samsung Galaxy A36 256 GB', 'Samsung Galaxy A36 128 GB', 'Samsung Galaxy A35 256 GB', 'Samsung Galaxy A35 128 GB', 'Samsung Galaxy A34 256 GB', 'Samsung Galaxy A26', 'Samsung Galaxy A25 128 GB', 'Samsung Galaxy A24 256 GB', 'Samsung galaxy A15', 'Samsung Galaxy A14 128 GB', 'Samsung Galaxy A06 128 GB', 'Samsung Galaxy A05 128 GB', 'Samsung Galaxy A05s 128 GB', 'Samsung Galaxy M34 128 GB', 'Samsung Galaxy M15 128 GB', 'Samsung Galaxy M12 64 GB', 'iPhone 16 Pro Max 1 TB', 'iPhone 16 Pro Max 512 GB', 'iPhone 16 Pro Max 256 GB', 'iPhone 16 Pro 128 GB', 'iPhone 16 Pro 256 GB', 'iPhone 16 Pro 512 GB', 'iPhone 16 Pro 1 TB', 'iPhone 16 Plus 512 GB', 'iPhone 16 Plus 256 GB', 'iPhone 16 Plus 128 GB', 'iPhone 16 128 GB', 'iPhone 16 256 GB', 'iPhone 16 512 GB', 'iPhone 16e 256 GB', 'iPhone 16e 128 GB', 'iPhone 15 Pro Max 1 TB', 'iPhone 15 Pro Max 512 GB', 'iPhone 15 Pro Max 256 GB', 'iPhone 15 Pro 128 GB', 'iPhone 15 Pro 256 GB', 'iPhone 15 Pro 512 GB', 'iPhone 15 Plus 512 GB', 'iPhone 15 Plus 256 GB', 'iPhone 15 Plus 128 GB', 'iPhone 15 128 GB', 'iPhone 15 256 GB', 'iPhone 15 512 GB', 'Xiaomi 15 512 GB', 'Xiaomi 15 Ultra 512 GB Siyah', 'Xiaomi 15 256 GB', 'Xiaomi 14 T Pro 512 GB', 'Xiaomi 14 Ultra 512 GB', 'Xiaomi 13 Ultra', 'Xiaomi 13 T Pro', 'Xiaomi 13 Lite 256 GB', 'Xiaomi MIX Flip 512 GB', 'Xiaomi Redmi Note 14 Pro Plus', 'Xiaomi Redmi Note 14 256 GB', 'Xiaomi Redmi Note 13 Pro Plus 512 GB', 'Xiaomi Redmi Note 13 Pro 256 GB', 'Xiaomi Redmi 13C 256 GB', 'Xiaomi Redmi 14C 256 GB', 'Xiaomi Redmi Note 12 Pro 256 GB', 'Xiaomi Redmi Note 12S 256 GB', 'Xiaomi Redmi Note 12R 128 GB', 'Xiaomi Redmi Note 12 128 GB', 'Xiaomi Redmi A2 Plus 64 GB', 'Realme GT 7 Pro 512 GB', 'Realme GT 6 512 GB', 'Realme GT 6T 256 GB', 'Realme 12 Pro Plus 512 GB', 'Realme 12 Pro Plus 256 GB', 'Realme 12 Plus 256 GB', 'Realme 12 Lite 256 GB', 'Realme 12 512 GB', 'Realme 11 Pro Plus 512 GB', 'Realme 11 Pro 256 GB', 'Realme 11 128 GB', 'Realme C75 512 GB', 'Realme C75 256 GB', 'Realme C65 128 GB', 'Realme C53 256 GB', 'Realme C63 256 GB', 'Realme C63 128 GB', 'Realme C61 256 GB', 'Realme C55 256 GB', 'Realme C51 128 GB', 'Realme Note 60 128 GB', 'Realme Note 50 128 GB', 'Tecno Phantom V Fold 2 512 GB', 'Tecno Phantom V Flip 2 256 GB', 'Tecno Phantom X2 256 GB', 'Tecno Camon 30 Pro 512 GB', 'Tecno Camon 30S Pro 256 GB', 'Tecno Camon 30 256 GB', 'Tecno Camon 30 512 GB', 'Tecno Camon 20 Premier 512 GB', 'Tecno Camon 20S Pro 256 GB', 'Tecno Pova 6 Pro 256 GB', 'Tecno Pova 6 256 GB', 'Tecno Pova 5 Pro 256 GB', 'Tecno Pova 5 256 GB', 'Tecno Spark 30 Pro 256 GB', 'Tecno Spark 30C 256 GB', 'Tecno Spark 20 Pro Plus 256 GB', 'Tecno Spark 20 Pro 256 GB', 'Tecno Spark 20 128 GB', 'Tecno Spark 20C 128 GB', 'Tecno Spark 10 Pro 128 GB', 'Tecno Spark 10 128 GB', 'Tecno Spark Go 1 128 GB', 'Tecno Spark Go 2024 128 GB']

        # CSV dosyasını başlat ve başlıkları yaz
        filename = "phone_specs_new_edition.csv"
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()

        # Her model için scrape et ve CSV'ye kaydet
        for model in phones:
            specs = scrape_phone_specs(driver, model, columns)
            with open(filename, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=columns)
                writer.writerow(specs)
            print(f"✅ {model} kaydedildi.")
            time.sleep(3)  # her sorgu arasında 3 saniye bekle

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

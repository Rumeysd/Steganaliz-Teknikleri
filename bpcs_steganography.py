import numpy as np
import cv2
import os

# Metni bitlere çevirme
def text_to_bits(text):
    return ''.join(format(ord(i), '08b') for i in text)

# Bitleri tekrar metne çevirme
def bits_to_text(bits):
    return ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))

# BPCS algoritması ile mesaj gömme
def embed_message_bpcs(image_path, message, output_path='bpcs.jpeg'):
    try:
        message += '###'  # Sonlandırıcı
        bits = text_to_bits(message)

        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            print(f"❌ Görsel bulunamadı: {image_path}")
            return

        img = img.astype(np.float32)
        h, w = img.shape

        if len(bits) > h * w // 2:
            print("⚠️ Mesaj görsele sığmıyor. Daha küçük bir mesaj girin.")
            return

        idx = 0
        for i in range(0, h, 2):
            for j in range(0, w, 2):
                if idx + 1 >= len(bits):
                    break
                # 2x2 piksel bloğunu seç
                block = img[i:i+2, j:j+2]
                # Bloğun ikili desenini oluştur
                pixel_values = [int(block[0, 0] % 2), int(block[0, 1] % 2), 
                               int(block[1, 0] % 2), int(block[1, 1] % 2)]

                # Bloğu mesaj bitleriyle değiştir
                pixel_values[0] = int(bits[idx])
                pixel_values[1] = int(bits[idx + 1])
                block[0, 0] = block[0, 0] - block[0, 0] % 2 + pixel_values[0]
                block[0, 1] = block[0, 1] - block[0, 1] % 2 + pixel_values[1]
                block[1, 0] = block[1, 0] - block[1, 0] % 2 + pixel_values[2]
                block[1, 1] = block[1, 1] - block[1, 1] % 2 + pixel_values[3]
                
                img[i:i+2, j:j+2] = block
                idx += 2

        cv2.imwrite(output_path, img.astype(np.uint8))
        print(f"✅ Mesaj başarıyla '{output_path}' dosyasına gizlendi.")

    except Exception as e:
        print("❌ Hata oluştu:", str(e))

# BPCS algoritması ile mesajı çözme
def extract_message_bpcs(image_path='bpcs.jpeg'):
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            print(f"❌ Görsel bulunamadı: {image_path}")
            return

        img = img.astype(np.float32)
        h, w = img.shape
        bits = ''

        for i in range(0, h, 2):
            for j in range(0, w, 2):
                block = img[i:i+2, j:j+2]
                # Bloğun ikili desenini çıkart
                bits += str(int(block[0, 0] % 2))
                bits += str(int(block[0, 1] % 2))
                bits += str(int(block[1, 0] % 2))
                bits += str(int(block[1, 1] % 2))

        message = bits_to_text(bits)

        if '###' in message:
            message = message.split('###')[0]
            print("🕵️ Gizli Mesaj:", message)
            with open("mesaj.txt", "w", encoding="utf-8") as f:
                f.write(message)
            print("💾 Mesaj 'mesaj.txt' dosyasına kaydedildi.")
        else:
            print("⚠️ Gizli mesaj bulunamadı.")

    except Exception as e:
        print("❌ Hata oluştu:", str(e))

# Ana uygulama
if __name__ == "__main__":
    default_image = "bpcs.jpeg"  # Görsel adı jpeg olarak güncellendi
    if not os.path.exists(default_image):
        print(f"⚠️ Lütfen aynı klasöre '{default_image}' adlı bir görsel yerleştirin.")
    else:
        while True:
            print("\n📌 Menü:\n1. Mesaj Gizle\n2. Mesaj Çıkar\n3. Çıkış")
            secim = input("> Seçiminiz: ")

            if secim == "1":
                msg = input("🔐 Mesaj (160 karaktere kadar): ")
                if len(msg) > 160:
                    print("⚠️ Mesaj çok uzun!")
                else:
                    embed_message_bpcs(default_image, msg)

            elif secim == "2":
                extract_message_bpcs('bpcs.jpeg')

            elif secim == "3":
                print("👋 Programdan çıkılıyor.")
                break

            else:
                print("⚠️ Geçersiz seçim! Lütfen 1, 2 ya da 3 girin.")

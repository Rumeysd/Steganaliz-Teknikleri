from PIL import Image
import numpy as np
import os

def text_to_bits(text):
    return ''.join(format(ord(char), '08b') for char in text)

def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def hide_message(image_path, message, output_path='output.jpg'):
    if len(message) > 160:
        raise ValueError("Mesaj 160 karakteri geçmemeli.")
    
    message += '###'  # Mesaj bitiş işareti
    message_bits = text_to_bits(message)
    
    image = Image.open(image_path)
    image_np = np.array(image)

    if len(message_bits) > image_np.size:
        raise ValueError("Görüntüde yeterli piksel yok.")
    
    data_index = 0
    for row in image_np:
        for pixel in row:
            for color in range(3):  # RGB
                if data_index < len(message_bits):
                    pixel[color] = (pixel[color] & 0xFE) | int(message_bits[data_index])
                    data_index += 1

    new_image = Image.fromarray(image_np)
    new_image.save(output_path)
    print(f"✅ Mesaj başarıyla '{output_path}' dosyasına gizlendi.")

def extract_message(image_path='output.jpg'):
    from pathlib import Path
    image = Image.open(image_path)
    image_np = np.array(image)

    bits = ""
    chars = ""

    for row in image_np:
        for pixel in row:
            for color in range(3):
                bits += str(pixel[color] & 1)
                if len(bits) % 8 == 0:
                    byte = bits[-8:]
                    char = chr(int(byte, 2))
                    chars += char
                    if chars.endswith("###"):
                        message = chars[:-3]
                        print("🕵️ Gizli Mesaj:", message)
                        
                        # Mesajı 'mesaj.txt' dosyasına yaz
                        with open("mesaj.txt", "w", encoding="utf-8") as f:
                            f.write(message)
                        print("💾 Mesaj 'mesaj.txt' dosyasına kaydedildi.")
                        return message

    print("⚠️ Gizli mesaj bulunamadı.")
    return ""



# Ana Döngü
if __name__ == "__main__":
    image_file = 'input.jpg'
    if not os.path.exists(image_file):
        print("⚠️ 'input.jpg' adlı bir görüntü dosyası bu dizinde bulunmalı.")
    else:
        while True:
            print("\n🛠️  Menü:")
            print("1 - Mesaj gizle")
            print("2 - Gizlenmiş mesajı bul")
            print("3 - Çıkış")
            secim = input("👉 Lütfen yapmak istediğiniz işlemi seçin (1/2/3): ")

            if secim == '1':
                mesaj = input("🔐 Lütfen gizlemek istediğiniz mesajı girin (en fazla 160 karakter):\n> ")
                try:
                    hide_message(image_file, mesaj)
                    print("💡 Mesaj başarıyla gizlendi.")
                except Exception as e:
                    print("❌ Hata:", str(e))

            elif secim == '2':
                try:
                    extract_message('output.jpg')
                except Exception as e:
                    print("❌ Hata:", str(e))

            elif secim == '3':
                print("👋 Programdan çıkılıyor...")
                break

            else:
                print("⚠️ Geçersiz seçim. Lütfen 1, 2 veya 3 girin.")
1
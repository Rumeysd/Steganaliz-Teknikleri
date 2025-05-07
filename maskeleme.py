import wave
import numpy as np

# Mesajı bitlere dönüştürme
def text_to_bits(text):
    return ''.join(format(ord(i), '08b') for i in text)

# Mesajı bitlerden metne dönüştürme
def bits_to_text(bits):
    return ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))

# Ses dosyasına mesaj ekleme (Maskeleme ve Filtreleme)
def embed_message(input_audio, message, output_audio='output.wav'):
    if len(message) > 160:
        raise ValueError("Mesaj 160 karakteri geçmemeli.")

    message += '###'  # Mesaj sonu işareti
    message_bits = text_to_bits(message)
    
    with wave.open(input_audio, 'rb') as audio:
        params = audio.getparams()
        frames = bytearray(audio.readframes(audio.getnframes()))

    if len(message_bits) > len(frames):
        raise ValueError("Ses dosyası mesajı saklamak için yeterli değil.")
    
    # Mesajı ses dosyasına gizleme
    for i, bit in enumerate(message_bits):
        frames[i] = (frames[i] & 254) | int(bit)  # Maskeleme işlemi

    with wave.open(output_audio, 'wb') as output:
        output.setparams(params)
        output.writeframes(frames)
    
    print(f"✅ Mesaj gizlendi: {output_audio}")

# Gizli mesajı çıkarma
def extract_message(audio_file='output.wav'):
    with wave.open(audio_file, 'rb') as audio:
        frames = bytearray(audio.readframes(audio.getnframes()))

    bits = ''
    for frame in frames:
        bits += str(frame & 1)

    # Bitleri metne dönüştürme
    message = bits_to_text(bits)
    
    # Mesaj sonu işaretine kadar al
    message = message.split('###')[0]
    
    print(f"🕵️ Gizli Mesaj: {message}")
    
    # Mesajı dosyaya kaydet
    with open("mesaj.txt", "w", encoding="utf-8") as f:
        f.write(message)
    
    print("💾 Mesaj 'mesaj.txt' dosyasına kaydedildi.")

# Ana uygulama
if __name__ == "__main__":
    while True:
        print("\n📌 Menü:\n1. Mesaj Gizle\n2. Mesaj Çıkar\n3. Çıkış")
        secim = input("> Seçiminiz: ")

        if secim == "1":
            audio_path = input("🔹 Ses dosyası adı (örnek: input.wav): ")
            message = input("🔐 Mesaj (160 karaktere kadar): ")
            if len(message) > 160:
                print("⚠️ Mesaj çok uzun!")
            else:
                embed_message(audio_path, message)

        elif secim == "2":
            audio_path = input("🔍 Gizli mesajı içeren ses dosyası adı (örnek: output.wav): ")
            extract_message(audio_path)

        elif secim == "3":
            print("👋 Programdan çıkılıyor.")
            break
        else:
            print("⚠️ Geçersiz seçim!")

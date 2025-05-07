import wave
import numpy as np

# Bit dizisinden metne dönüştürme
def bits_to_text(bits):
    message = ''
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            message += chr(int(byte, 2))
    return message

# LSB tekniği ile gizli mesajı çıkarma
def extract_message(audio_file):
    with wave.open(audio_file, 'rb') as audio:
        params = audio.getparams()
        frames = bytearray(audio.readframes(audio.getnframes()))

    # Ses verisini numpy array'e dönüştür
    audio_data = np.array(frames, dtype=np.int16)

    # Gizli mesaj bitlerini çıkar
    message_bits = []
    for i in range(len(audio_data)):
        message_bits.append(str(audio_data[i] & 1))

    # Bit dizisini metne dönüştür
    message_bits = ''.join(message_bits)
    message = bits_to_text(message_bits)

    # '###' işareti ile mesajın sonunu kontrol et
    if '###' in message:
        message = message.split('###')[0]
        print("🕵️ Gizli Mesaj:", message)
        
        # Mesajı dosyaya kaydet
        with open("mesaj.txt", "w", encoding="utf-8") as f:
            f.write(message)
        
        print("💾 Mesaj 'mesaj.txt' dosyasına kaydedildi.")
    else:
        print("❌ Mesaj bulunamadı.")

# Ana uygulama
if __name__ == "__main__":
    audio_path = input("🔍 Gizli mesajı içeren ses dosyası adı (örnek: output.wav): ")
    extract_message(audio_path)

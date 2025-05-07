import wave

def text_to_bits(text):
    return ''.join(format(ord(char), '08b') for char in text)

def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def hide_message(audio_path, message, output_path='output.wav'):
    if len(message) > 160:
        raise ValueError("Mesaj 160 karakteri geçmemeli.")

    message += '###'  # Mesaj sonu işareti
    message_bits = text_to_bits(message)

    with wave.open(audio_path, 'rb') as audio:
        params = audio.getparams()
        frames = bytearray(audio.readframes(audio.getnframes()))

    if len(message_bits) > len(frames):
        raise ValueError("Ses dosyası mesajı saklamak için yeterli değil.")

    for i, bit in enumerate(message_bits):
        frames[i] = (frames[i] & 254) | int(bit)

    with wave.open(output_path, 'wb') as output:
        output.setparams(params)
        output.writeframes(frames)

    print("✅ Mesaj başarıyla gizlendi:", output_path)

def extract_message(audio_path='output.wav'):
    with wave.open(audio_path, 'rb') as audio:
        frames = bytearray(audio.readframes(audio.getnframes()))

    bits = ''.join([str(frame & 1) for frame in frames])
    chars = bits_to_text(bits)

    message = chars.split('###')[0]
    print("🕵️ Gizli Mesaj:", message)
    return message

# Ana uygulama: Kullanıcıdan mesaj al
if __name__ == "__main__":
    import os

    audio_file = 'input.wav'
    if not os.path.exists(audio_file):
        print("⚠️ 'input.wav' adlı bir ses dosyası bu dizinde bulunmalı!")
    else:
        mesaj = input("🔐 Lütfen gizlemek istediğiniz mesajı girin (en fazla 160 karakter):\n> ")
        try:
            hide_message(audio_file, mesaj)
            print("💡 Mesaj gizlenmiştir. 'output.wav' dosyasından geri alabilirsiniz.")
        except Exception as e:
            print("❌ Hata:", str(e))
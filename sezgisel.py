import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

def heuristic_hide(input_image, secret_message, output_image):
    try:
        # Görüntüyü RGB formatında aç
        img = Image.open(input_image).convert('RGB')
        img_array = np.array(img)
        
        binary_msg = ''.join([format(ord(i), '08b') for i in secret_message])
        binary_msg += '00000000'  # Sonlandırma işareti
        
        # Pikselleri yeniden şekillendir
        pixels = img_array.reshape((-1, 3))
        
        # Kümeleme yap
        kmeans = KMeans(n_clusters=5, random_state=0, n_init=10).fit(pixels)
        labels = kmeans.labels_
        
        # En az kullanılan küme
        unique, counts = np.unique(labels, return_counts=True)
        min_cluster = unique[np.argmin(counts)]
        
        # Mesajı gizle
        msg_index = 0
        for i in range(pixels.shape[0]):
            if labels[i] == min_cluster and msg_index < len(binary_msg):
                for j in range(3):
                    if msg_index < len(binary_msg):
                        pixels[i,j] = (pixels[i,j] & 254) | int(binary_msg[msg_index])
                        msg_index += 1
        
        # Orijinal şekline döndür ve kaydet
        img_array = pixels.reshape(img_array.shape)
        Image.fromarray(img_array).save(output_image)
        print(f"Mesaj başarıyla gizlendi! {len(secret_message)} karakter")
        
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")

def heuristic_extract(input_image, msg_length):
    try:
        img = Image.open(input_image).convert('RGB')
        img_array = np.array(img)
        pixels = img_array.reshape((-1, 3))
        
        kmeans = KMeans(n_clusters=5, random_state=0, n_init=10).fit(pixels)
        labels = kmeans.labels_
        
        unique, counts = np.unique(labels, return_counts=True)
        min_cluster = unique[np.argmin(counts)]
        
        binary_msg = ""
        for i in range(pixels.shape[0]):
            if labels[i] == min_cluster and len(binary_msg) < msg_length*8:
                for j in range(3):
                    if len(binary_msg) < msg_length*8:
                        binary_msg += str(pixels[i,j] & 1)
        
        # Mesajı binary'den çevir
        message = ""
        for i in range(0, min(len(binary_msg), msg_length*8), 8):
            byte = binary_msg[i:i+8]
            if len(byte) == 8:
                message += chr(int(byte, 2))
        
        return message
    
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
        return ""

def test_heuristic_method(image_path, message):
    print("\n=== Test Başlıyor ===")
    print(f"Orijinal Resim: {image_path}")
    print(f"Mesaj Uzunluğu: {len(message)} karakter")
    
    try:
        # Mesajı gizle
        output_path = "test_output.jpg"
        heuristic_hide(image_path, message, output_path)
        
        # Çıkarılan mesajlar
        print("\nÇıkarılan Mesajlar:")
        extracted_full = heuristic_extract(output_path, len(message))
        print(f"Tam mesaj: {extracted_full}")
        print(f"Eşleşme: {'✅' if extracted_full == message else '❌'}")
        
        # Görsel karşılaştırma
        original = Image.open(image_path)
        stego = Image.open(output_path)
        print("\nGörsel Boyutları:")
        print(f"Orijinal: {original.size}, Çıktı: {stego.size}")
        
        return extracted_full == message
    
    except Exception as e:
        print(f"Test sırasında hata: {str(e)}")
        return False

# Test örneği
if __name__ == "__main__":
    test_message = "Test123!"
    test_image = "output.jpg"  # Kendi resminizin yolunu verin
    
    # Önce basit bir test
    print("Basit Test:")
    heuristic_hide(test_image, test_message, "test_cikti.jpg")
    extracted = heuristic_extract("test_cikti.jpg", len(test_message))
    print(f"Çıkarılan: {extracted}")
    
    # Detaylı test
    test_result = test_heuristic_method(test_image, test_message)
    print("\nTest Sonucu:", "Başarılı" if test_result else "Başarısız")
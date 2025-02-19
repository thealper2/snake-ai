# :snake: Snake AI

Bu proje, derin öğrenme ve pekiştirmeli öğrenme tekniklerini kullanarak yılan oyunu oynayan bir yapay zeka geliştirmeyi amaçlamaktadır. Proje, Python programlama dili ve Pygame kütüphanesi kullanılarak geliştirilmiştir. Yapay zeka, Q-Learning ile eğitilerek oyunu oynamayı öğrenir.

---

## :clipboard: İçindekiler

1. [Proje Hakkında](https://github.com/thealper2/snake-ai?tab=readme-ov-file#clipboard-i%CC%87%C3%A7indekiler)
2. [Kurulum](https://github.com/thealper2/snake-ai?tab=readme-ov-file#hammer_and_wrench-kurulum)
3. [Kullanım](https://github.com/thealper2/snake-ai?tab=readme-ov-file#joystick-kullan%C4%B1m)
4. [Kod Yapısı](https://github.com/thealper2/snake-ai?tab=readme-ov-file#jigsaw-kod-yap%C4%B1s%C4%B1)
5. [Eğitim Süreci](https://github.com/thealper2/snake-ai?tab=readme-ov-file#mortar_board-e%C4%9Fitim-s%C3%BCreci)
6. [Sonuçlar](https://github.com/thealper2/snake-ai?tab=readme-ov-file#bar_chart-sonu%C3%A7lar)
7. [Katkıda Bulunma](https://github.com/thealper2/snake-ai?tab=readme-ov-file#handshake-katk%C4%B1da-bulunma)
8. [Lisans](https://github.com/thealper2/snake-ai?tab=readme-ov-file#scroll-lisans)

---

## :dart: Proje Hakkında

Bu proje, klasik Yılan Oyunu'nu oynayan bir yapay zeka geliştirmeyi hedefler. Yapay zeka, çevresini algılayarak (engeller, yiyecek konumu vb.) hareket kararları alır ve zamanla daha iyi performans göstermek için eğitilir. Proje, pekiştirmeli öğrenme (Reinforcement Learning) ve derin öğrenme (Deep Learning) tekniklerini birleştirir.

#### Temel Özellikler:

- **Pygame** ile oyun arayüzü.
- **PyTorch** ile sinir ağı modeli.
- **Q-Learning** ile pekiştirmeli öğrenme.
- Eğitim sürecinde kaydedilen istatistikler ve model kaydetme.

## :hammer_and_wrench: Kurulum

Projeyi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

#### Gereksinimler

- Python 3.8 veya üzeri
- PyTorch
- Pygame
- Numpy

#### Kurulum Adımları

1. Depoyu klonlayın:

```bash
git clone https://github.com/thealper2/snake-ai.git
cd snake-ai
```

2. Gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```

3. Projeyi çalıştırın:

```bash
python3 run.py
```

## :joystick: Kullanım

Proje, `train.py` dosyası üzerinden eğitim sürecini başlatır. Eğitim sırasında yapay zeka, oyunu oynamayı öğrenir ve her oyunun sonunda istatistikler kaydedilir.

#### Eğitimi başlatma

Modeli eğitmek için:

```bash
python3 run.py
```

#### Eğitilmiş Modeli Kullanma

Eğitilmiş bir modeli yükleyip test etmek için:

```bash
model = QNet(11, 256, 3)
model.load_state_dict(torch.load('models/modelX.pth'))
model.eval()
```

## :jigsaw: Kod Yapısı

Proje, aşağıdaki ana bileşenlerden oluşur:

### 1. `game.py`

- Oyunun temel mantığını ve arayüzünü içerir.
- Yılanın hareketi, yiyecek yerleştirme, çarpışma kontrolü gibi işlevleri yönetir.

### 2. `agent.py`

- Yapay zeka ajanını tanımlar.
- Durum algılama, hafıza yönetimi, eğitim ve aksiyon seçimi gibi işlevleri içerir.

### 3. `model.py`

- Sinir ağı modelini (**QNet**) tanımlar.
- Giriş, gizli ve çıkış katmanlarından oluşur.

### 4. `trainer.py`

- Modelin eğitim sürecini yönetir.
- Kayıp fonksiyonu ve optimizasyon işlemlerini içerir.

### 5. `constants.py`

- Oyun ve eğitim süreci için sabitleri (örneğin blok boyutu, pencere boyutları, renkler) içerir.

## :mortar_board: Eğitim Süreci

Yapay zeka, aşağıdaki adımlarla eğitilir.

1. **Durum Algılama**: Yılanın başı etrafındaki engeller ve yiyecek konumu algılanır.
2. **Aksiyon Seçimi**: Epsilon-greedy stratejisi kullanılarak rastgele veya model tarafından tahmin edilen bir aksiyon seçilir.
3. **Ödül Seçimi**:
    - Yiyecek yendiğinde: +10 puan.
    - Çarpışma veya zaman aşımı: -10 puan.
4. **Hafıza Yönetimi**: Her adımın deneyimi (state, action, reward, next_state, done) hafızaya kaydedilir.
5. **Eğitim**: Kısa ve uzun hafıza üzerinden model eğitilir.

## :bar_chart: Sonuçlar

Eğitim sırasında aşağıdaki istatistikler kaydedilir ve CSV dosyasına yazılır:

- Oyun numarası
- Skor
- Adım sayısı
- Yılan uzunluğu
- Ölüm nedeni
- Toplam yiyecek sayısı
- Ortalama skor
- En yüksek skor

Eğitim tamamlandıktan sonra, en yüksek skora sahip model `models/` dizinine kaydedilir.

## :handshake: Katkıda Bulunma

Bu projeye katkıda bulunmak isterseniz:

1. Depoyu forklayın.
2. Yeni bir branch oluşturun:

```bash
git checkout -b yeni-ozellik
```

3. Değişikliklerinizi yapın ve commit edin:

```bash
git commit -m "Yeni özellik eklendi"
```

4. Değişikliklerinizi pushlayın:

```bash
git push origin yeni-ozellik
```

5. Bir pull request oluşturun.

## :scroll: Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasını inceleyin.

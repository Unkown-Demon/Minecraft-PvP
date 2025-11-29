# ⚔️ Zor PvP Arena (Minecraft 1v1 Critical PvP Simulator)

Bu loyiha Minecraft'ning 1.9+ PvP mexanikasi, ayniqsa **Critical PvP** va **Anarxiya** serverlaridagi o'ziga xos elementlarni (Mace, Elytra, Talismanlar, 100+ sehrlar) o'zida mujassam etgan, Python'da Ursina (Panda3D asosida) yordamida yaratilgan 3D multiplayer o'yin simulyatoridir.

## ✨ Asosiy Xususiyatlar

| Xususiyat | Tavsif |
| :--- | :--- |
| **Critical PvP Mexanikasi** | 1.9+ hujum tezligi (cooldown), kritik zarba ehtimoli (`critical_chance`) va koeffitsienti (`critical_damage_multiplier`) to'liq amalga oshirilgan. |
| **Anarxiya Elementlari** | **Mace PvP** (tushish balandligiga qarab bonus zarar), **Elytra** (tezlik bonusi) va **Talismanlar** (stat bonuslari) qo'shilgan. |
| **100+ Sehrlar Tizimi** | Qurol va Armorda ishlaydigan 100 dan ortiq noyob sehrlar (masalan, `Healer`, `Vigor`, `Smash`, `Protection`) uchun asos yaratilgan. |
| **Tana Kuchaytirish (Armor)** | Armor tizimi `max_health` va `defense` statlarini oshirish orqali o'yinchining himoyasini ta'minlaydi. |
| **Multiplayer (1v1 Arena)** | Server/Klient arxitekturasi orqali 100x100 maydonda boshqa o'yinchilar bilan jang qilish imkoniyati. |
| **Chat va Admin Buyruqlari** | O'yin ichida chat (`T` tugmasi) va asosiy admin buyruqlari (`/gamemode`, `/heal`, `/tp`) qo'shilgan. |

## 🕹️ Boshqaruv

| Harakat | Tugma |
| :--- | :--- |
| **Harakatlanish** | `W`, `A`, `S`, `D` |
| **Kamera/Nishon** | Sichqoncha |
| **Hujum** | Sichqonchaning chap tugmasi |
| **Inventar almashtirish** | `1` dan `9` gacha tugmalar |
| **Maxsus Qobiliyat (Dash)** | `Q` |
| **Chatni ochish** | `T` |
| **Chatni yopish/Menyuga chiqish** | `Esc` |

## ⚙️ O'rnatish va Ishga Tushirish

### 1. Talablarni o'rnatish

Loyihani ishga tushirish uchun Python va `requirements.txt` faylidagi kutubxonalar kerak bo'ladi:

```bash
pip install -r requirements.txt
```

### 2. Teksturalarni Joylashtirish

Loyihada standart kub teksturalari ishlatiladi, ammo siz o'zingizning Minecraft teksturalaringizni qo'shishingiz mumkin.

1.  Loyihaning asosiy papkasida **`assets/textures`** nomli papkalar yarating.
2.  `textures_list.txt` faylida ko'rsatilgan tekstura fayllarini (masalan, `grass.png`, `sword.png`) shu papkaga joylashtiring.

### 3. Serverni Ishga Tushirish

Avval serverni ishga tushiring:

```bash
python server.py
```

### 4. Klientni (O'yinni) Ishga Tushirish

Server ishga tushgandan so'ng, o'yinni ishga tushiring. Agar bir nechta o'yinchi ulanmoqchi bo'lsa, har bir o'yinchi o'z kompyuterida ushbu buyruqni ishga tushirishi kerak:

```bash
python client.py
```

## 📝 Loyiha Tuzilishi

| Fayl | Vazifasi |
| :--- | :--- |
| `client.py` | O'yinning asosiy logikasi, 3D muhit, PvP mexanikasi, inventar, sehrlar va boshqaruvni o'z ichiga oladi. |
| `server.py` | Multiplayer uchun markaziy server logikasi, o'yinchilarning holatini sinxronizatsiya qiladi. |
| `requirements.txt` | Loyiha uchun zarur bo'lgan Python kutubxonalari ro'yxati. |
| `textures_list.txt` | Foydalanuvchi tomonidan taqdim etilishi kerak bo'lgan teksturalar ro'yxati. |

---
**Muallif:** Manus AI
**Litsenziya:** MIT (Yoki siz tanlagan litsenziya)

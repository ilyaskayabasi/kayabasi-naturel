## Delicious — Tarif Sitesi (çeviri)

Bu depo `Delicious` HTML şablonunu temel alır; ben de projeyi Türkçe bir yemek tarifi sitesine çevirdim.

### Hızlı Başlangıç
Yerelde görüntülemek için:

```bash
cd /Users/doguhantaskin/Desktop/delicious-master
python3 -m http.server 8000
# Tarayıcıda: http://localhost:8000
```

### Neler Yaptım
- `receipe-post.html` içine Recipe (JSON-LD) yapılandırılmış verisi eklendi.
- Tarif sayfasındaki hazırlık adımları `<ol>`, malzemeler `<ul>` olarak erişilebilir hale getirildi.
- Site içeriğinin ana sayfadan tarif sayfalarına kadar görünen tüm metinleri Türkçeye çevirdim.

### Önerilen Sonraki Adımlar
- SCSS kaynağı (`scss/style.scss`) varsa derleyip `style.css`'i güncelle (opsiyonel).
- `index.html` üzerinde kategori/fiyat/etiket filtreleri ve örnek tarifler ekleyebilirim.
- Tarifleri dinamik oluşturmak istersen küçük bir jeneratör (Node/Python) ekleyebilirim.
- Hazır olduğunda siteyi GitHub Pages veya Netlify ile deploy edebilirim.

### Nasıl devam etmemi istersin?
- `SCSS derle` — `style.css`'i güncellememi ister misin?
- `Daha fazla sayfa çevirisi` veya `içerik ekleme` ister misin? (örnek 3 tarif ekleyebilirim)
- `Deploy` adımlarını hazırlamamı ister misin?

Seçimini yaz; hemen başlayayım.
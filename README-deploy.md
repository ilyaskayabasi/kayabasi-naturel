# Deploy instructions

Bu repo statik bir site içeriyor. Aşağıdaki adımlar ile sitenizi GitHub Pages'e otomatik olarak yayınlayabilirsiniz.

1) Değişiklikleri commit ve push edin:

```bash
git add .
git commit -m "Add GitHub Pages deploy workflow and CNAME"
git push origin main
```

2) GitHub Actions otomatik olarak çalışacak ve `gh-pages` dalına siteyi yayınlayacak. Yayınlandıktan sonra erişim şu URL'lerde olabilir:

- Varsayılan GitHub Pages URL: `https://nefisyemek.github.io/nefistarif.io`
- Eğer `CNAME` ve DNS doğruysa: `https://nefistarif.io`

3) DNS kontrolü (eğer `nefistarif.io` domaini kendi kontrolünüzdeyse):

 - Alan adınızın DNS paneline `A` veya `CNAME` kayıtlarını ekleyin. GitHub Pages için genelde `A` kayıtları kullanılır:

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

4) Yerel önizleme yapmak isterseniz (macOS/zsh):

```bash
# Basit static server
cd $(git rev-parse --show-toplevel)
python3 -m http.server 8000
# veya
npx http-server -p 8000

# Sonra tarayıcıda açın: http://localhost:8000
```

Notlar:
- Workflow tüm repository kökünü `gh-pages` dalına publish edecek; eğer istemediğiniz büyük dosyalar varsa (ör. `backend/.venv`), onları `.gitignore` veya ek temizleme adımları ile hariç bırakın. Workflow zaten `backend/.venv` dizinini deploy öncesi siliyor.
- Ben push yapmam için GitHub erişimi/kullanıcı yetkisine ihtiyaç var; isterseniz sizin adınıza push etmem için erişim verin veya kendiniz push edin.

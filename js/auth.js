// Minimal client-side auth for static site using localStorage
(function(){
  'use strict';

  function safeGet(key){
    try{ return localStorage.getItem(key); }catch(e){ return null; }
  }
  function safeSet(key, val){
    try{ localStorage.setItem(key, val); return true; }catch(e){ return false; }
  }

  async function hashPassword(password){
    if(window.crypto && crypto.subtle && typeof crypto.subtle.digest === 'function'){
      var enc = new TextEncoder();
      var buf = await crypto.subtle.digest('SHA-256', enc.encode(password));
      return Array.from(new Uint8Array(buf)).map(function(b){ return b.toString(16).padStart(2,'0'); }).join('');
    }
    // fallback deterministic hash (not secure, but keeps UX working offline)
    var h = 2166136261 >>> 0;
    for(var i=0;i<password.length;i++){
      h ^= password.charCodeAt(i);
      h = Math.imul(h, 16777619) >>> 0;
    }
    return 'fnv1a_' + h.toString(16);
  }

  function getUsers(){
    var raw = safeGet('lezzet_users');
    if(!raw) return [];
    try{ return JSON.parse(raw) || []; }catch(e){ return []; }
  }
  function saveUsers(list){
    try{ safeSet('lezzet_users', JSON.stringify(list)); return true; }catch(e){ return false; }
  }

  function currentUser(){
    try{ var s = safeGet('lezzet_session'); return s ? JSON.parse(s) : null; }catch(e){ return null; }
  }

  function setSession(user){
    try{ safeSet('lezzet_session', JSON.stringify(user)); return true; }catch(e){ return false; }
  }

  function clearSession(){
    try{ localStorage.removeItem('lezzet_session'); return true; }catch(e){ return false; }
  }

  async function register(opts){
    var username = (opts.username || '').trim();
    var email = (opts.email || '').trim().toLowerCase();
    var password = opts.password || '';
    if(!username || !email || !password) return { ok:false, message: 'Lütfen tüm alanları doldurun.' };
    var users = getUsers();
    if(users.some(function(u){ return u.email === email; })) return { ok:false, message: 'Bu e-posta zaten kayıtlı.' };
    if(users.some(function(u){ return u.username === username; })) return { ok:false, message: 'Bu kullanıcı adı zaten alınmış.' };
    var hashed = await hashPassword(password + '|' + email);
    var user = { id: Date.now(), username: username, email: email, password: hashed };
    users.push(user);
    if(!saveUsers(users)) return { ok:false, message: 'Tarayıcı depolama izin vermiyor.' };
    setSession({ id: user.id, username: user.username, email: user.email });
    renderAuthLinks();
    return { ok:true, message: 'Kayıt başarılı.' };
  }

  async function login(opts){
    var identifier = (opts.identifier || '').trim();
    var password = opts.password || '';
    if(!identifier || !password) return { ok:false, message: 'Lütfen tüm alanları doldurun.' };
    var users = getUsers();
    var user = users.find(function(u){ return u.email === identifier.toLowerCase() || u.username === identifier; });
    if(!user) return { ok:false, message: 'Kullanıcı bulunamadı.' };
    var hashed = await hashPassword(password + '|' + user.email);
    if(hashed !== user.password) return { ok:false, message: 'Şifre yanlış.' };
    setSession({ id: user.id, username: user.username, email: user.email });
    renderAuthLinks();
    return { ok:true, message: 'Giriş başarılı.' };
  }

  function logout(){
    clearSession();
    renderAuthLinks();
  }

  function renderAuthLinks(){
    var container = document.getElementById('auth-links');
    if(!container) return;
    container.innerHTML = '';
    var user = currentUser();
    if(user){
      var li = document.createElement('li');
      li.innerHTML = '<a href="profile.html">' + escapeHtml(user.username) + '</a>';
      container.appendChild(li);
      var li2 = document.createElement('li');
      var a = document.createElement('a'); a.href = '#'; a.textContent = 'Çıkış Yap';
      a.addEventListener('click', function(e){ e.preventDefault(); logout(); window.location.href = 'index.html'; });
      li2.appendChild(a);
      container.appendChild(li2);
    } else {
      var li1 = document.createElement('li'); li1.innerHTML = '<a href="login.html">Giriş Yap</a>'; container.appendChild(li1);
      var li2 = document.createElement('li'); li2.innerHTML = '<a href="register.html">Kayıt Ol</a>'; container.appendChild(li2);
    }
  }

  function escapeHtml(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

  // expose API
  window.LezzetAuth = { register: register, login: login, logout: logout, currentUser: currentUser, renderAuthLinks: renderAuthLinks };

  // auto render on DOM ready
  document.addEventListener('DOMContentLoaded', function(){
    renderAuthLinks();
  });

})();

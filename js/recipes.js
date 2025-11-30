// recipes.js — dynamic recipe renderer, search/filter, and client-side ratings (localStorage)
(function(){
  var RECIPES_JSON = '/data/recipes.json';
  var RECIPES_API = '/api/recipes';
  // helpful absolute backend URL (when frontend served on different port)
  var RECIPES_API_BACKEND = 'http://127.0.0.1:5000/api/recipes';

  function createStars(container, recipeId){
    container.innerHTML = '';
    var key = 'rating_' + recipeId;
    var saved = localStorage.getItem(key);
    var current = saved ? Number(saved) : 0;
    container.dataset.current = current;
    for(var i=1;i<=5;i++){
      var star = document.createElement('span');
      star.className = 'star';
      star.dataset.value = i;
      star.innerHTML = '★';
      star.style.cursor = 'pointer';
      star.style.fontSize = '20px';
      star.style.marginRight = '4px';
      star.style.color = (i <= current) ? '#f4c150' : '#ddd';
      (function(v){
        star.addEventListener('click', function(){
          localStorage.setItem(key, v);
          container.dataset.current = v;
          updateStars(container, v);
        });
        star.addEventListener('mouseover', function(){ updateStars(container, v); });
        star.addEventListener('mouseout', function(){ updateStars(container, Number(container.dataset.current) || 0); });
      })(i);
      container.appendChild(star);
    }
  }

  function updateStars(container, value){
    var spans = container.querySelectorAll('.star');
    spans.forEach(function(s){
      var v = Number(s.dataset.value);
      s.style.color = (v <= value) ? '#f4c150' : '#ddd';
    });
  }

  function renderCard(recipe){
    var col = document.createElement('div');
    col.className = 'col-12 col-sm-6 col-lg-4 recipe-card';
    col.dataset.category = recipe.category || '';
    col.dataset.title = (recipe.title || '').toLowerCase();
    col.dataset.tags = (recipe.tags || []).join(',').toLowerCase();

    var html = '';
    html += '<div class="single-best-receipe-area mb-30">';
    html += '<img src="' + recipe.image + '" alt="' + escapeHtml(recipe.title) + '">';
    html += '<div class="receipe-content">';
    html += '<a href="' + recipe.url + '"><h5>' + escapeHtml(recipe.title) + '</h5></a>';
    html += '<p class="excerpt">' + escapeHtml(recipe.excerpt || '') + '</p>';
    html += '<div class="meta">';
    if(recipe.prep || recipe.cook){
      html += '<small>' + (recipe.prep ? 'Hazırlık: ' + escapeHtml(recipe.prep) : '') + (recipe.cook ? ' • Pişirme: ' + escapeHtml(recipe.cook) : '') + '</small>';
    }
    html += '</div>';
    html += '<div class="rating" data-recipe-id="' + escapeHtml(recipe.id) + '"></div>';
    html += '</div></div>';

    col.innerHTML = html;
    return col;
  }

  // expose a helper to render an array of recipes into a container selector
  window.renderRecipes = function(recipes, containerSelector){
    var container = document.querySelector(containerSelector);
    if(!container) return;
    container.innerHTML = '';
    recipes.forEach(function(r){
      container.appendChild(renderCard(r));
    });
  };

  // expose a helper to render single recipe card (returns DOM node)
  window.renderRecipeCard = function(recipe){
    return renderCard(recipe);
  };

  function escapeHtml(s){
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  function loadRecipes(){
    // Try relative API first (works when frontend is served by the same backend).
    // If that fails (CORS or different port), try the common local backend address,
    // finally fall back to the local JSON file.
    return fetch(RECIPES_API).then(function(res){
      if(!res.ok) throw new Error('API yüklenemedi: ' + res.status);
      return res.json();
    }).catch(function(){
      return fetch(RECIPES_API_BACKEND).then(function(res){
        if(!res.ok) throw new Error('backend api yüklenemedi');
        return res.json();
      }).catch(function(){
        return fetch(RECIPES_JSON).then(function(res){
          if(!res.ok) throw new Error('recipes.json yüklenemedi');
          return res.json();
        });
      });
    });
  }

  function applyFilters(){
    var cat = (document.getElementById('recipe-category-filter') || {}).value || '';
    var q = (document.getElementById('recipe-search') || {}).value || '';
    q = q.trim().toLowerCase();
    var cards = document.querySelectorAll('#recipes-list .recipe-card');
    cards.forEach(function(card){
      var cardCat = card.dataset.category || '';
      var title = card.dataset.title || '';
      var tags = card.dataset.tags || '';
      var matchesCat = (cat === '' || cat === cardCat);
      var matchesQuery = (q === '' || title.indexOf(q) !== -1 || tags.indexOf(q) !== -1);
      card.style.display = (matchesCat && matchesQuery) ? '' : 'none';
    });
  }

  function initUI(recipes){
    var container = document.getElementById('recipes-list');
    if(!container) return;
    container.innerHTML = '';
    recipes.forEach(function(r){
      var card = renderCard(r);
      container.appendChild(card);
    });
    // init ratings for any new rating widgets
    initRatings();

    // hook filter & search
    var select = document.getElementById('recipe-category-filter');
    if(select) select.addEventListener('change', applyFilters);
    var search = document.getElementById('recipe-search');
    if(search) search.addEventListener('input', function(){ applyFilters(); });
  }

  function initRatings(){
    var ratingEls = document.querySelectorAll('.rating');
    ratingEls.forEach(function(el){
      var id = el.dataset.recipeId;
      if(!id) return;
      // If already initialized (has children), skip
      if(el.querySelectorAll('.star').length) return createStars(el, id);
      createStars(el, id);
    });
  }

  document.addEventListener('DOMContentLoaded', function(){
    loadRecipes().then(function(list){
      initUI(list || []);
    }).catch(function(err){
      console.error('Tarifler yüklenirken hata:', err);
    });

    // Intercept header search form submit to avoid real POST (static server returns 501)
    var headerForm = document.getElementById('header-search-form');
    if(headerForm){
      headerForm.addEventListener('submit', function(e){
        e.preventDefault();
        var q = (document.getElementById('header-search') || {}).value || '';
        var searchInput = document.getElementById('recipe-search');
        if(searchInput){
          searchInput.value = q;
          // trigger input event to apply filters
          var ev = new Event('input', { bubbles: true });
          searchInput.dispatchEvent(ev);
        }
      });
    }
  });

})();

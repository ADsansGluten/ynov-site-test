/* Concept de refonte — interactions (aucune dépendance) */
(function(){
  'use strict';
  var doc=document, root=doc.documentElement;
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  root.classList.remove('no-js');
  var $=function(s,c){return (c||doc).querySelector(s)}, $$=function(s,c){return Array.prototype.slice.call((c||doc).querySelectorAll(s))};
  var BASE=(doc.body.getAttribute('data-base')||'');

  /* bandeau concept */
  var bar=$('.concept-bar');
  if(bar){
    try{ if(sessionStorage.getItem('cb')==='1'){bar.remove();} }catch(e){}
    var bx=$('.concept-bar button'); if(bx) bx.addEventListener('click',function(){bar.remove();try{sessionStorage.setItem('cb','1')}catch(e){}});
  }

  /* header : ombre au scroll + tiroir mobile */
  var head=$('.site-head');
  function onScroll(){ if(head) head.classList.toggle('scrolled',window.scrollY>8); }
  onScroll(); window.addEventListener('scroll',onScroll,{passive:true});
  var burger=$('.burger');
  if(burger) burger.addEventListener('click',function(){
    var o=doc.body.classList.toggle('drawer-open'); burger.setAttribute('aria-expanded',o);
  });

  /* révélations au scroll */
  var rv=$$('.reveal');
  if('IntersectionObserver' in window && !reduce){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});
    rv.forEach(function(el){io.observe(el)});
  } else rv.forEach(function(el){el.classList.add('in')});

  /* compteurs */
  function fmt(n){return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g,' ')}
  $$('[data-count]').forEach(function(el){
    var to=parseInt(el.getAttribute('data-count'),10), suf=el.getAttribute('data-suffix')||'';
    if(reduce||!('IntersectionObserver' in window)){el.textContent=fmt(to)+suf;return}
    var o=new IntersectionObserver(function(es){es.forEach(function(e){
      if(!e.isIntersecting) return; o.disconnect();
      var t0=performance.now(), d=1400;
      (function step(t){var p=Math.min(1,(t-t0)/d), v=1-Math.pow(1-p,4); el.textContent=fmt(Math.round(to*v))+suf; if(p<1) requestAnimationFrame(step)})(t0);
    })},{threshold:.6}); o.observe(el);
  });

  /* hero : halo qui suit doucement le pointeur + parallaxe des cartes */
  var hero=$('.hero');
  if(hero && !reduce && window.matchMedia('(pointer:fine)').matches){
    var b1=$('.blob',hero), cards=$$('.hv-card',hero), tx=0,ty=0,cx=0,cy=0,raf;
    hero.addEventListener('pointermove',function(e){
      var r=hero.getBoundingClientRect(); tx=(e.clientX-r.left)/r.width-.5; ty=(e.clientY-r.top)/r.height-.5; if(!raf) raf=requestAnimationFrame(tick);
    });
    function tick(){
      cx+=(tx-cx)*.07; cy+=(ty-cy)*.07;
      if(b1) b1.style.transform='translate('+(cx*-50)+'px,'+(cy*-40)+'px)';
      cards.forEach(function(c,i){var k=(i+1)*6; c.style.translate=(cx*k)+'px '+(cy*k)+'px';});
      raf=(Math.abs(tx-cx)>.001||Math.abs(ty-cy)>.001)?requestAnimationFrame(tick):null;
    }
  }

  /* onglets génériques */
  $$('[data-tabs]').forEach(function(box){
    var tabs=$$('.tab',box), panes=$$('[data-pane]',box.parentNode);
    function show(k){tabs.forEach(function(t){t.classList.toggle('on',t.dataset.tab===k)});panes.forEach(function(p){p.hidden=p.dataset.pane!==k})}
    tabs.forEach(function(t){t.addEventListener('click',function(){show(t.dataset.tab)})});
  });

  /* carte : survol liste <-> pin */
  $$('.campus-list a[data-c]').forEach(function(a){
    var pin=$('.pin[data-c="'+a.dataset.c+'"]');
    if(!pin) return;
    a.addEventListener('mouseenter',function(){pin.classList.add('on')});
    a.addEventListener('mouseleave',function(){pin.classList.remove('on')});
    pin.addEventListener('mouseenter',function(){a.classList.add('on')});
    pin.addEventListener('mouseleave',function(){a.classList.remove('on')});
  });

  /* formulaires de démonstration : rien n'est envoyé */
  $$('form.demo').forEach(function(f){
    f.addEventListener('submit',function(e){e.preventDefault();f.classList.add('sent');var ok=$('.ok',f);if(ok)ok.scrollIntoView({block:'nearest',behavior:'smooth'})});
  });

  /* finder (accueil) */
  var finder=$('#finder');
  if(finder) finder.addEventListener('submit',function(e){
    e.preventDefault(); var q=new URLSearchParams();
    ['niveau','fam','campus'].forEach(function(k){var v=finder.elements[k].value;if(v)q.set(k,v)});
    location.href=BASE+'formations/index.html'+(q.toString()?'?'+q.toString():'');
  });

  /* catalogue */
  var cat=$('#catalogue');
  if(cat && window.PROGS){
    var items=$$('.prog',cat), count=$('#count'), qI=$('#q'), nv=$$('input[name=niveau]'), fm=$$('input[name=fam]'), cp=$('#campus'), onl=$('#online'), empty=$('#empty');
    function norm(s){return (s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
    function apply(){
      var q=norm(qI.value), nvs=nv.filter(function(x){return x.checked}).map(function(x){return x.value}),
          fms=fm.filter(function(x){return x.checked}).map(function(x){return x.value}), c=cp.value, o=onl.checked, n=0;
      items.forEach(function(el,i){
        var p=window.PROGS[i];
        var ok=(!q||norm(p.t+' '+p.fn+' '+p.typ+' '+p.s).indexOf(q)>-1)&&(!nvs.length||nvs.indexOf(p.typ)>-1)&&(!fms.length||fms.indexOf(p.f)>-1)
          &&(!c||p.c.indexOf(c)>-1)&&(!o||p.on);
        el.hidden=!ok; if(ok) n++;
      });
      count.textContent=n+' formation'+(n>1?'s':''); empty.hidden=n>0;
    }
    var P=new URLSearchParams(location.search);
    if(P.get('q')) qI.value=P.get('q');
    if(P.get('niveau')) nv.forEach(function(x){x.checked=x.value===P.get('niveau')});
    if(P.get('fam')) fm.forEach(function(x){x.checked=x.value===P.get('fam')});
    if(P.get('campus')) cp.value=P.get('campus');
    if(P.get('online')==='1') onl.checked=true;
    [qI,cp,onl].concat(nv,fm).forEach(function(el){el.addEventListener('input',apply);el.addEventListener('change',apply)});
    var reset=$('#reset'); if(reset) reset.addEventListener('click',function(){qI.value='';cp.value='';onl.checked=false;nv.concat(fm).forEach(function(x){x.checked=false});apply()});
    apply();
  }

  /* palette de recherche (Ctrl/Cmd + K, ou "/") */
  var box=$('.cmdk');
  if(box && window.INDEX){
    var input=$('input',box), list=$('ul',box), sel=0, shown=[];
    function norm2(s){return (s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
    function render(){
      var q=norm2(input.value.trim()), r=window.INDEX.filter(function(x){return !q||norm2(x.t+' '+x.k).indexOf(q)>-1}).slice(0,40);
      shown=r; sel=0;
      list.innerHTML=r.length?r.map(function(x,i){return '<li class="'+(i===0?'sel':'')+'"><a href="'+BASE+x.u+'"><span>'+x.t+'</span><small>'+x.g+'</small></a></li>'}).join(''):'<div class="empty">Aucun résultat — essaie « IA », « Sophia » ou « alternance ».</div>';
    }
    function open(){box.classList.add('open');input.value='';render();setTimeout(function(){input.focus()},30);doc.body.style.overflow='hidden'}
    function close(){box.classList.remove('open');doc.body.style.overflow=''}
    $$('[data-cmdk]').forEach(function(b){b.addEventListener('click',open)});
    box.addEventListener('click',function(e){if(e.target===box)close()});
    input.addEventListener('input',render);
    doc.addEventListener('keydown',function(e){
      var tag=(e.target.tagName||'').toLowerCase();
      if((e.key==='k'&&(e.metaKey||e.ctrlKey))||(e.key==='/'&&tag!=='input'&&tag!=='textarea'&&tag!=='select')){e.preventDefault();box.classList.contains('open')?close():open();return}
      if(!box.classList.contains('open')) return;
      if(e.key==='Escape') close();
      if(e.key==='ArrowDown'||e.key==='ArrowUp'){
        e.preventDefault(); var lis=$$('li',list); if(!lis.length) return;
        lis[sel].classList.remove('sel'); sel=(sel+(e.key==='ArrowDown'?1:-1)+lis.length)%lis.length; lis[sel].classList.add('sel'); lis[sel].scrollIntoView({block:'nearest'});
      }
      if(e.key==='Enter'&&shown[sel]) location.href=BASE+shown[sel].u;
    });
  }
})();

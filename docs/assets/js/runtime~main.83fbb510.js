(()=>{"use strict";var e,t,r,o,a,n={},f={};function d(e){var t=f[e];if(void 0!==t)return t.exports;var r=f[e]={id:e,loaded:!1,exports:{}};return n[e].call(r.exports,r,r.exports,d),r.loaded=!0,r.exports}d.m=n,d.c=f,e=[],d.O=(t,r,o,a)=>{if(!r){var n=1/0;for(u=0;u<e.length;u++){r=e[u][0],o=e[u][1],a=e[u][2];for(var f=!0,i=0;i<r.length;i++)(!1&a||n>=a)&&Object.keys(d.O).every((e=>d.O[e](r[i])))?r.splice(i--,1):(f=!1,a<n&&(n=a));if(f){e.splice(u--,1);var c=o();void 0!==c&&(t=c)}}return t}a=a||0;for(var u=e.length;u>0&&e[u-1][2]>a;u--)e[u]=e[u-1];e[u]=[r,o,a]},d.n=e=>{var t=e&&e.__esModule?()=>e.default:()=>e;return d.d(t,{a:t}),t},r=Object.getPrototypeOf?e=>Object.getPrototypeOf(e):e=>e.__proto__,d.t=function(e,o){if(1&o&&(e=this(e)),8&o)return e;if("object"==typeof e&&e){if(4&o&&e.__esModule)return e;if(16&o&&"function"==typeof e.then)return e}var a=Object.create(null);d.r(a);var n={};t=t||[null,r({}),r([]),r(r)];for(var f=2&o&&e;"object"==typeof f&&!~t.indexOf(f);f=r(f))Object.getOwnPropertyNames(f).forEach((t=>n[t]=()=>e[t]));return n.default=()=>e,d.d(a,n),a},d.d=(e,t)=>{for(var r in t)d.o(t,r)&&!d.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})},d.f={},d.e=e=>Promise.all(Object.keys(d.f).reduce(((t,r)=>(d.f[r](e,t),t)),[])),d.u=e=>"assets/js/"+({53:"935f2afb",85:"1f391b9e",155:"5a71d88c",185:"6656866e",214:"a243a9e0",237:"1df93b7f",298:"f42c9a6a",349:"c076bf19",383:"be8181ad",414:"393be207",514:"1be78505",671:"0e384e19",801:"0ac489e7",817:"14eb3368",885:"5ede6613",918:"17896441"}[e]||e)+"."+{53:"2a93656a",85:"0226b9d2",155:"80f607c4",185:"15cbeda7",210:"f637648c",214:"4ec5cce4",237:"d7e430ed",298:"b867f16c",349:"29e8c5dd",383:"2446018e",414:"30535165",514:"e4d1af46",671:"ad48d587",801:"b3c2fb91",817:"a6446dee",885:"9604eb9c",918:"e8eb07a5",972:"d5cc17b1"}[e]+".js",d.miniCssF=e=>{},d.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),d.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),o={},a="docs:",d.l=(e,t,r,n)=>{if(o[e])o[e].push(t);else{var f,i;if(void 0!==r)for(var c=document.getElementsByTagName("script"),u=0;u<c.length;u++){var l=c[u];if(l.getAttribute("src")==e||l.getAttribute("data-webpack")==a+r){f=l;break}}f||(i=!0,(f=document.createElement("script")).charset="utf-8",f.timeout=120,d.nc&&f.setAttribute("nonce",d.nc),f.setAttribute("data-webpack",a+r),f.src=e),o[e]=[t];var b=(t,r)=>{f.onerror=f.onload=null,clearTimeout(s);var a=o[e];if(delete o[e],f.parentNode&&f.parentNode.removeChild(f),a&&a.forEach((e=>e(r))),t)return t(r)},s=setTimeout(b.bind(null,void 0,{type:"timeout",target:f}),12e4);f.onerror=b.bind(null,f.onerror),f.onload=b.bind(null,f.onload),i&&document.head.appendChild(f)}},d.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},d.p="/aurora-origin-python-sdk/",d.gca=function(e){return e={17896441:"918","935f2afb":"53","1f391b9e":"85","5a71d88c":"155","6656866e":"185",a243a9e0:"214","1df93b7f":"237",f42c9a6a:"298",c076bf19:"349",be8181ad:"383","393be207":"414","1be78505":"514","0e384e19":"671","0ac489e7":"801","14eb3368":"817","5ede6613":"885"}[e]||e,d.p+d.u(e)},(()=>{var e={303:0,532:0};d.f.j=(t,r)=>{var o=d.o(e,t)?e[t]:void 0;if(0!==o)if(o)r.push(o[2]);else if(/^(303|532)$/.test(t))e[t]=0;else{var a=new Promise(((r,a)=>o=e[t]=[r,a]));r.push(o[2]=a);var n=d.p+d.u(t),f=new Error;d.l(n,(r=>{if(d.o(e,t)&&(0!==(o=e[t])&&(e[t]=void 0),o)){var a=r&&("load"===r.type?"missing":r.type),n=r&&r.target&&r.target.src;f.message="Loading chunk "+t+" failed.\n("+a+": "+n+")",f.name="ChunkLoadError",f.type=a,f.request=n,o[1](f)}}),"chunk-"+t,t)}},d.O.j=t=>0===e[t];var t=(t,r)=>{var o,a,n=r[0],f=r[1],i=r[2],c=0;if(n.some((t=>0!==e[t]))){for(o in f)d.o(f,o)&&(d.m[o]=f[o]);if(i)var u=i(d)}for(t&&t(r);c<n.length;c++)a=n[c],d.o(e,a)&&e[a]&&e[a][0](),e[a]=0;return d.O(u)},r=self.webpackChunkdocs=self.webpackChunkdocs||[];r.forEach(t.bind(null,0)),r.push=t.bind(null,r.push.bind(r))})()})();
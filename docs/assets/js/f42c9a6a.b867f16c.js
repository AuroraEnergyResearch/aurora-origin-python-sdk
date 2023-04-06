"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[298],{3905:(e,n,t)=>{t.d(n,{Zo:()=>m,kt:()=>g});var r=t(7294);function a(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function o(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function i(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?o(Object(t),!0).forEach((function(n){a(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):o(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function s(e,n){if(null==e)return{};var t,r,a=function(e,n){if(null==e)return{};var t,r,a={},o=Object.keys(e);for(r=0;r<o.length;r++)t=o[r],n.indexOf(t)>=0||(a[t]=e[t]);return a}(e,n);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)t=o[r],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(a[t]=e[t])}return a}var l=r.createContext({}),c=function(e){var n=r.useContext(l),t=n;return e&&(t="function"==typeof e?e(n):i(i({},n),e)),t},m=function(e){var n=c(e.components);return r.createElement(l.Provider,{value:n},e.children)},u="mdxType",d={inlineCode:"code",wrapper:function(e){var n=e.children;return r.createElement(r.Fragment,{},n)}},f=r.forwardRef((function(e,n){var t=e.components,a=e.mdxType,o=e.originalType,l=e.parentName,m=s(e,["components","mdxType","originalType","parentName"]),u=c(t),f=a,g=u["".concat(l,".").concat(f)]||u[f]||d[f]||o;return t?r.createElement(g,i(i({ref:n},m),{},{components:t})):r.createElement(g,i({ref:n},m))}));function g(e,n){var t=arguments,a=n&&n.mdxType;if("string"==typeof e||a){var o=t.length,i=new Array(o);i[0]=f;var s={};for(var l in n)hasOwnProperty.call(n,l)&&(s[l]=n[l]);s.originalType=e,s[u]="string"==typeof e?e:a,i[1]=s;for(var c=2;c<o;c++)i[c]=t[c];return r.createElement.apply(null,i)}return r.createElement.apply(null,t)}f.displayName="MDXCreateElement"},3743:(e,n,t)=>{t.d(n,{Z:()=>g});var r=t(7462),a=t(7294),o=t(6668);function i(e){const n=e.map((e=>({...e,parentIndex:-1,children:[]}))),t=Array(7).fill(-1);n.forEach(((e,n)=>{const r=t.slice(2,e.level);e.parentIndex=Math.max(...r),t[e.level]=n}));const r=[];return n.forEach((e=>{const{parentIndex:t,...a}=e;t>=0?n[t].children.push(a):r.push(a)})),r}function s(e){let{toc:n,minHeadingLevel:t,maxHeadingLevel:r}=e;return n.flatMap((e=>{const n=s({toc:e.children,minHeadingLevel:t,maxHeadingLevel:r});return function(e){return e.level>=t&&e.level<=r}(e)?[{...e,children:n}]:n}))}function l(e){const n=e.getBoundingClientRect();return n.top===n.bottom?l(e.parentNode):n}function c(e,n){let{anchorTopOffset:t}=n;const r=e.find((e=>l(e).top>=t));if(r){return function(e){return e.top>0&&e.bottom<window.innerHeight/2}(l(r))?r:e[e.indexOf(r)-1]??null}return e[e.length-1]??null}function m(){const e=(0,a.useRef)(0),{navbar:{hideOnScroll:n}}=(0,o.L)();return(0,a.useEffect)((()=>{e.current=n?0:document.querySelector(".navbar").clientHeight}),[n]),e}function u(e){const n=(0,a.useRef)(void 0),t=m();(0,a.useEffect)((()=>{if(!e)return()=>{};const{linkClassName:r,linkActiveClassName:a,minHeadingLevel:o,maxHeadingLevel:i}=e;function s(){const e=function(e){return Array.from(document.getElementsByClassName(e))}(r),s=function(e){let{minHeadingLevel:n,maxHeadingLevel:t}=e;const r=[];for(let a=n;a<=t;a+=1)r.push(`h${a}.anchor`);return Array.from(document.querySelectorAll(r.join()))}({minHeadingLevel:o,maxHeadingLevel:i}),l=c(s,{anchorTopOffset:t.current}),m=e.find((e=>l&&l.id===function(e){return decodeURIComponent(e.href.substring(e.href.indexOf("#")+1))}(e)));e.forEach((e=>{!function(e,t){t?(n.current&&n.current!==e&&n.current.classList.remove(a),e.classList.add(a),n.current=e):e.classList.remove(a)}(e,e===m)}))}return document.addEventListener("scroll",s),document.addEventListener("resize",s),s(),()=>{document.removeEventListener("scroll",s),document.removeEventListener("resize",s)}}),[e,t])}function d(e){let{toc:n,className:t,linkClassName:r,isChild:o}=e;return n.length?a.createElement("ul",{className:o?void 0:t},n.map((e=>a.createElement("li",{key:e.id},a.createElement("a",{href:`#${e.id}`,className:r??void 0,dangerouslySetInnerHTML:{__html:e.value}}),a.createElement(d,{isChild:!0,toc:e.children,className:t,linkClassName:r}))))):null}const f=a.memo(d);function g(e){let{toc:n,className:t="table-of-contents table-of-contents__left-border",linkClassName:l="table-of-contents__link",linkActiveClassName:c,minHeadingLevel:m,maxHeadingLevel:d,...g}=e;const p=(0,o.L)(),v=m??p.tableOfContents.minHeadingLevel,h=d??p.tableOfContents.maxHeadingLevel,b=function(e){let{toc:n,minHeadingLevel:t,maxHeadingLevel:r}=e;return(0,a.useMemo)((()=>s({toc:i(n),minHeadingLevel:t,maxHeadingLevel:r})),[n,t,r])}({toc:n,minHeadingLevel:v,maxHeadingLevel:h});return u((0,a.useMemo)((()=>{if(l&&c)return{linkClassName:l,linkActiveClassName:c,minHeadingLevel:v,maxHeadingLevel:h}}),[l,c,v,h])),a.createElement(f,(0,r.Z)({toc:b,className:t,linkClassName:l},g))}},9093:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>d,contentTitle:()=>m,default:()=>v,frontMatter:()=>c,metadata:()=>u,toc:()=>f});var r=t(7462),a=t(7294),o=t(3905),i=t(3743);const s={tableOfContentsInline:"tableOfContentsInline_prmo"};function l(e){let{toc:n,minHeadingLevel:t,maxHeadingLevel:r}=e;return a.createElement("div",{className:s.tableOfContentsInline},a.createElement(i.Z,{toc:n,minHeadingLevel:t,maxHeadingLevel:r,className:"table-of-contents",linkClassName:null}))}const c={sidebar_position:2,sidebar_label:"Common Patterns",title:"Common Patterns",description:"Some example usage for getting started using the API",toc_min_heading_level:2,toc_max_heading_level:2},m=void 0,u={unversionedId:"common-patterns",id:"common-patterns",title:"Common Patterns",description:"Some example usage for getting started using the API",source:"@site/docs/common-patterns.mdx",sourceDirName:".",slug:"/common-patterns",permalink:"/aurora-origin-python-sdk/docs/common-patterns",draft:!1,tags:[],version:"current",sidebarPosition:2,frontMatter:{sidebar_position:2,sidebar_label:"Common Patterns",title:"Common Patterns",description:"Some example usage for getting started using the API",toc_min_heading_level:2,toc_max_heading_level:2},sidebar:"docSidebar",previous:{title:"Installation",permalink:"/aurora-origin-python-sdk/docs/intro"},next:{title:"SDK Reference",permalink:"/aurora-origin-python-sdk/docs/category/sdk-reference"}},d={},f=[{value:"Contents",id:"contents",level:3},{value:"Get projects",id:"get-projects",level:2},{value:"Get scenarios for a region",id:"get-scenarios-for-a-region",level:2},{value:"Get latest Central case",id:"get-latest-central-case",level:2}],g={toc:f},p="wrapper";function v(e){let{components:n,...t}=e;return(0,o.kt)(p,(0,r.Z)({},g,t,{components:n,mdxType:"MDXLayout"}),(0,o.kt)("h3",{id:"contents"},"Contents"),(0,o.kt)(l,{toc:f,mdxType:"TOCInline"}),(0,o.kt)("h2",{id:"get-projects"},"Get projects"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"session = OriginSession()\n\n# Get Projects\nsession.get_projects()\n")),(0,o.kt)("h2",{id:"get-scenarios-for-a-region"},"Get scenarios for a region"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},'session = OriginSession()\n\n# Get published scenarios for a region\nsession.get_aurora_scenarios(region="gbr")\n')),(0,o.kt)("h2",{id:"get-latest-central-case"},"Get latest Central case"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},'from datetime import datetime\n\ndef get_latest_central_for(region: str):\n  # First, get regional scenarios\n  scenarios_for_region = (\n      session.get_aurora_scenarios(region=region)\n        .get("data")\n        .get("getScenarios")\n  )\n\n  # Filter to central cases only\n  central_cases = [\n      scenario\n          for scenario\n          in scenarios_for_region\n          if "central" in scenario.get("name").lower()\n  ]\n\n  # Sort using publication date\n  central_cases.sort(\n      key=lambda scenario: datetime.fromisoformat(\n        scenario["publicationDate"]\n      ).timestamp(),\n      reverse=True\n  )\n\n  return central_cases[0]\n\n# Call function, getting latest case for AUS\nget_latest_central_for("aus")\n')))}v.isMDXComponent=!0}}]);
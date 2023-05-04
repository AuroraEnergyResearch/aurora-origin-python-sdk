"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[885],{3905:(e,n,r)=>{r.d(n,{Zo:()=>l,kt:()=>m});var t=r(7294);function o(e,n,r){return n in e?Object.defineProperty(e,n,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[n]=r,e}function i(e,n){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var t=Object.getOwnPropertySymbols(e);n&&(t=t.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),r.push.apply(r,t)}return r}function s(e){for(var n=1;n<arguments.length;n++){var r=null!=arguments[n]?arguments[n]:{};n%2?i(Object(r),!0).forEach((function(n){o(e,n,r[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):i(Object(r)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(r,n))}))}return e}function a(e,n){if(null==e)return{};var r,t,o=function(e,n){if(null==e)return{};var r,t,o={},i=Object.keys(e);for(t=0;t<i.length;t++)r=i[t],n.indexOf(r)>=0||(o[r]=e[r]);return o}(e,n);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(t=0;t<i.length;t++)r=i[t],n.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(o[r]=e[r])}return o}var c=t.createContext({}),p=function(e){var n=t.useContext(c),r=n;return e&&(r="function"==typeof e?e(n):s(s({},n),e)),r},l=function(e){var n=p(e.components);return t.createElement(c.Provider,{value:n},e.children)},u="mdxType",d={inlineCode:"code",wrapper:function(e){var n=e.children;return t.createElement(t.Fragment,{},n)}},y=t.forwardRef((function(e,n){var r=e.components,o=e.mdxType,i=e.originalType,c=e.parentName,l=a(e,["components","mdxType","originalType","parentName"]),u=p(r),y=o,m=u["".concat(c,".").concat(y)]||u[y]||d[y]||i;return r?t.createElement(m,s(s({ref:n},l),{},{components:r})):t.createElement(m,s({ref:n},l))}));function m(e,n){var r=arguments,o=n&&n.mdxType;if("string"==typeof e||o){var i=r.length,s=new Array(i);s[0]=y;var a={};for(var c in n)hasOwnProperty.call(n,c)&&(a[c]=n[c]);a.originalType=e,a[u]="string"==typeof e?e:o,s[1]=a;for(var p=2;p<i;p++)s[p]=r[p];return t.createElement.apply(null,s)}return t.createElement.apply(null,r)}y.displayName="MDXCreateElement"},9084:(e,n,r)=>{r.r(n),r.d(n,{assets:()=>c,contentTitle:()=>s,default:()=>d,frontMatter:()=>i,metadata:()=>a,toc:()=>p});var t=r(7462),o=(r(7294),r(3905));const i={sidebar_label:"scenario_enums",title:"origin_sdk.types.scenario_enums"},s=void 0,a={unversionedId:"origin_sdk/types/scenario_enums",id:"origin_sdk/types/scenario_enums",title:"origin_sdk.types.scenario_enums",description:"ScenarioRunType Objects",source:"@site/docs/origin_sdk/types/scenario_enums.md",sourceDirName:"origin_sdk/types",slug:"/origin_sdk/types/scenario_enums",permalink:"/aurora-origin-python-sdk/docs/origin_sdk/types/scenario_enums",draft:!1,tags:[],version:"current",frontMatter:{sidebar_label:"scenario_enums",title:"origin_sdk.types.scenario_enums"},sidebar:"docSidebar",previous:{title:"Scenario",permalink:"/aurora-origin-python-sdk/docs/origin_sdk/service/Scenario"},next:{title:"scenario_types",permalink:"/aurora-origin-python-sdk/docs/origin_sdk/types/scenario_types"}},c={},p=[{value:"ScenarioRunType Objects",id:"scenarioruntype-objects",level:2},{value:"ModelPriceSpikiness Objects",id:"modelpricespikiness-objects",level:2}],l={toc:p},u="wrapper";function d(e){let{components:n,...r}=e;return(0,o.kt)(u,(0,t.Z)({},l,r,{components:n,mdxType:"MDXLayout"}),(0,o.kt)("h2",{id:"scenarioruntype-objects"},"ScenarioRunType Objects"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"class ScenarioRunType(Enum)\n")),(0,o.kt)("p",null,"Internal only. Used to set a ",(0,o.kt)("inlineCode",{parentName:"p"},"scenarioRunType"),"."),(0,o.kt)("h2",{id:"modelpricespikiness-objects"},"ModelPriceSpikiness Objects"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"class ModelPriceSpikiness(Enum)\n")),(0,o.kt)("p",null,"Used to set a Model Price Spikiness on a scenario that implements this\nfeature, typically from the AUS region."))}d.isMDXComponent=!0}}]);
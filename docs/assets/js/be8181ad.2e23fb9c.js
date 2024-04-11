"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[383],{3905:(e,t,n)=>{n.d(t,{Zo:()=>c,kt:()=>y});var i=n(7294);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function a(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);t&&(i=i.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,i)}return n}function o(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?a(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):a(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,i,r=function(e,t){if(null==e)return{};var n,i,r={},a=Object.keys(e);for(i=0;i<a.length;i++)n=a[i],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(i=0;i<a.length;i++)n=a[i],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var s=i.createContext({}),p=function(e){var t=i.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):o(o({},t),e)),n},c=function(e){var t=p(e.components);return i.createElement(s.Provider,{value:t},e.children)},u="mdxType",d={inlineCode:"code",wrapper:function(e){var t=e.children;return i.createElement(i.Fragment,{},t)}},m=i.forwardRef((function(e,t){var n=e.components,r=e.mdxType,a=e.originalType,s=e.parentName,c=l(e,["components","mdxType","originalType","parentName"]),u=p(n),m=r,y=u["".concat(s,".").concat(m)]||u[m]||d[m]||a;return n?i.createElement(y,o(o({ref:t},c),{},{components:n})):i.createElement(y,o({ref:t},c))}));function y(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var a=n.length,o=new Array(a);o[0]=m;var l={};for(var s in t)hasOwnProperty.call(t,s)&&(l[s]=t[s]);l.originalType=e,l[u]="string"==typeof e?e:r,o[1]=l;for(var p=2;p<a;p++)o[p]=n[p];return i.createElement.apply(null,o)}return i.createElement.apply(null,n)}m.displayName="MDXCreateElement"},2652:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>s,contentTitle:()=>o,default:()=>d,frontMatter:()=>a,metadata:()=>l,toc:()=>p});var i=n(7462),r=(n(7294),n(3905));const a={sidebar_label:"scenario_types",title:"origin_sdk.types.scenario_types"},o=void 0,l={unversionedId:"origin_sdk/types/scenario_types",id:"origin_sdk/types/scenario_types",title:"origin_sdk.types.scenario_types",description:"The scenario_types module contains type hinting and can be useful when trying to",source:"@site/docs/origin_sdk/types/scenario_types.md",sourceDirName:"origin_sdk/types",slug:"/origin_sdk/types/scenario_types",permalink:"/aurora-origin-python-sdk/docs/origin_sdk/types/scenario_types",draft:!1,tags:[],version:"current",frontMatter:{sidebar_label:"scenario_types",title:"origin_sdk.types.scenario_types"},sidebar:"docSidebar",previous:{title:"scenario_enums",permalink:"/aurora-origin-python-sdk/docs/origin_sdk/types/scenario_enums"}},s={},p=[{value:"InputScenario Objects",id:"inputscenario-objects",level:2},{value:"ScenarioSummaryType Objects",id:"scenariosummarytype-objects",level:2},{value:"RegionDict Objects",id:"regiondict-objects",level:2},{value:"ScenarioType Objects",id:"scenariotype-objects",level:2}],c={toc:p},u="wrapper";function d(e){let{components:t,...n}=e;return(0,r.kt)(u,(0,i.Z)({},c,n,{components:t,mdxType:"MDXLayout"}),(0,r.kt)("p",null,"The scenario_types module contains type hinting and can be useful when trying to\nunderstand what options you have when interacting with functions, or what\noutputs to expect from queries. Enums are available in\n",(0,r.kt)("a",{parentName:"p",href:"/docs/origin_sdk/types/scenario_enums"},"scenario_enums")," for import and usage."),(0,r.kt)("h2",{id:"inputscenario-objects"},"InputScenario Objects"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class InputScenario(TypedDict)\n")),(0,r.kt)("p",null,"Interface for creating or updating scenarios. Note that while you may be\nable to create a scenario partially, the values required to put it into a\nlaunchable state varies based on configuration. If you are missing\nparameters, the service ought to tell you what is missing."),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Attributes"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"projectGlobalId")," ",(0,r.kt)("em",{parentName:"li"},"string")," - The ID of the project to create the scenario\nin"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"name")," ",(0,r.kt)("em",{parentName:"li"},"string")," - The name of the scenario"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"baseScenarioGlobalId")," ",(0,r.kt)("em",{parentName:"li"},"string")," - ",(0,r.kt)("strong",{parentName:"li"},"Required only for non-Aurorean use.")," The\n",'"',"base",'"'," scenario you wish to use. This is equivalent to your own\nscenario, or a published AER scenario that you wish to ",'"',"copy",'"',"."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"description")," ",(0,r.kt)("em",{parentName:"li"},"optional, string")," - A description for the scenario. Purely for user\npurposes, not used by the system."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"regionGroupCode")," ",(0,r.kt)("em",{parentName:"li"},"optional, string")," - A region group for the scenario. Be aware\nthat a ",'"',"regionGroup",'"'," would be AUS, whereas a ",'"',"region",'"'," would then be\n",'"',"VIC",'"'," or ",'"',"NSW",'"',". For most regions, the ",'"',"regionGroup",'"'," and it","'","s three\nletter region code are identical."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"useExogifiedInputs")," ",(0,r.kt)("em",{parentName:"li"},"optional, boolean")," - A true value here is equivalent to the\n",'"',"Model Determined Capacity",'"'," toggled off in the interface. When this\nis set to false, the model automatically builds capacity to support\ndemand. If you unselect this, you are choosing to take control of\ndefining the capacity build assumptions (this runs much more\nquickly). Whether these options are available, depends on the\nscenario this is based on."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"defaultCurrency")," ",(0,r.kt)("em",{parentName:"li"},"optional, string")," - Should be set automatically once a\n",(0,r.kt)("inlineCode",{parentName:"li"},"regionGroupCode")," is chosen, but can be overridden"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"retentionPolicy")," ",(0,r.kt)("em",{parentName:"li"},"optional, string")," - Internal only."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"scenarioRunType")," ",(0,r.kt)("em",{parentName:"li"},"optional, ScenarioRunType")," - Internal only. Can be values ",(0,r.kt)("inlineCode",{parentName:"li"},"MYR"),", ",(0,r.kt)("inlineCode",{parentName:"li"},"FYR")," or\n",(0,r.kt)("inlineCode",{parentName:"li"},"MYR_AND_FYR"),". Non-Auroreans should look to using the\n",(0,r.kt)("inlineCode",{parentName:"li"},"useExogifiedInputs")," flag over the scenarioRunType. The behaviour\nbetween the two differs slightly for a better Origin experience."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"modelPriceSpikiness")," ",(0,r.kt)("em",{parentName:"li"},"optional, ModelPriceSpikiness")," - Used for AUS, set\nthis to one of the ModelPriceSpikiness enum values if you wish to\nuse the feature."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"years")," ",(0,r.kt)("em",{parentName:"li"},"optional, List","[int]")," - Internal only."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"weatherYear")," ",(0,r.kt)("em",{parentName:"li"},"optional, int")," - The Weather Year for which to simulate (half)hourly profiles - if supported.\nShould only be used for scenarios with ",'"',"fixed capacities",'"'," and without further edits; i.e.\n",(0,r.kt)("inlineCode",{parentName:"li"},"useExogifiedInputs")," = ",(0,r.kt)("inlineCode",{parentName:"li"},"true"),", or ",(0,r.kt)("inlineCode",{parentName:"li"},"scenarioRunType")," = ",(0,r.kt)("inlineCode",{parentName:"li"},"FYR")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"advancedSettings")," ",(0,r.kt)("em",{parentName:"li"},"optional, AdvancedScenarioSettings")," - Internal only.")),(0,r.kt)("h2",{id:"scenariosummarytype-objects"},"ScenarioSummaryType Objects"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class ScenarioSummaryType(TypedDict)\n")),(0,r.kt)("p",null,"Dictionary received when requesting a list of scenarios"),(0,r.kt)("h2",{id:"regiondict-objects"},"RegionDict Objects"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class RegionDict(TypedDict)\n")),(0,r.kt)("p",null,"Regional information object."),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Attributes"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"regionCode")," ",(0,r.kt)("em",{parentName:"li"},"String")," - ISO code or similar from the service"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metaUrl")," ",(0,r.kt)("em",{parentName:"li"},"String")," - URL used to get the meta json file for this region","'","s downloads"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"dataUrlBase")," ",(0,r.kt)("em",{parentName:"li"},"String")," - URL used as the base to construct a download URL\nfor output data"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"__meta_json")," ",(0,r.kt)("em",{parentName:"li"},"Optional")," - Not provided by the service. This field is\npopulated as required by internal implementation of the Scenario class.\nObserve this at your own risk.")),(0,r.kt)("h2",{id:"scenariotype-objects"},"ScenarioType Objects"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class ScenarioType(ScenarioSummaryType)\n")),(0,r.kt)("p",null,"Extended scenario details received when requesting a single scenario"))}d.isMDXComponent=!0}}]);
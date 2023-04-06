"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[801],{3905:(e,t,r)=>{r.d(t,{Zo:()=>c,kt:()=>_});var n=r(7294);function a(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function o(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function i(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?o(Object(r),!0).forEach((function(t){a(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):o(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function s(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},o=Object.keys(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}var l=n.createContext({}),p=function(e){var t=n.useContext(l),r=t;return e&&(r="function"==typeof e?e(t):i(i({},t),e)),r},c=function(e){var t=p(e.components);return n.createElement(l.Provider,{value:t},e.children)},u="mdxType",d={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},g=n.forwardRef((function(e,t){var r=e.components,a=e.mdxType,o=e.originalType,l=e.parentName,c=s(e,["components","mdxType","originalType","parentName"]),u=p(r),g=a,_=u["".concat(l,".").concat(g)]||u[g]||d[g]||o;return r?n.createElement(_,i(i({ref:t},c),{},{components:r})):n.createElement(_,i({ref:t},c))}));function _(e,t){var r=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=r.length,i=new Array(o);i[0]=g;var s={};for(var l in t)hasOwnProperty.call(t,l)&&(s[l]=t[l]);s.originalType=e,s[u]="string"==typeof e?e:a,i[1]=s;for(var p=2;p<o;p++)i[p]=r[p];return n.createElement.apply(null,i)}return n.createElement.apply(null,r)}g.displayName="MDXCreateElement"},8137:(e,t,r)=>{r.r(t),r.d(t,{assets:()=>l,contentTitle:()=>i,default:()=>d,frontMatter:()=>o,metadata:()=>s,toc:()=>p});var n=r(7462),a=(r(7294),r(3905));const o={sidebar_label:"OriginSession",title:"origin_sdk.OriginSession"},i=void 0,s={unversionedId:"origin_sdk/OriginSession",id:"origin_sdk/OriginSession",title:"origin_sdk.OriginSession",description:"OriginSession Objects",source:"@site/docs/origin_sdk/OriginSession.md",sourceDirName:"origin_sdk",slug:"/origin_sdk/OriginSession",permalink:"/aurora-origin-python-sdk/docs/origin_sdk/OriginSession",draft:!1,tags:[],version:"current",frontMatter:{sidebar_label:"OriginSession",title:"origin_sdk.OriginSession"},sidebar:"docSidebar",previous:{title:"SDK Reference",permalink:"/aurora-origin-python-sdk/docs/category/sdk-reference"},next:{title:"Scenario",permalink:"/aurora-origin-python-sdk/docs/origin_sdk/service/Scenario"}},l={},p=[{value:"OriginSession Objects",id:"originsession-objects",level:2},{value:"get_aurora_scenarios",id:"get_aurora_scenarios",level:4},{value:"get_scenario_by_id",id:"get_scenario_by_id",level:4},{value:"create_scenario",id:"create_scenario",level:4},{value:"update_scenario",id:"update_scenario",level:4},{value:"delete_scenario",id:"delete_scenario",level:4},{value:"launch_scenario",id:"launch_scenario",level:4},{value:"get_projects",id:"get_projects",level:4},{value:"get_project",id:"get_project",level:4},{value:"create_project",id:"create_project",level:4},{value:"update_project",id:"update_project",level:4},{value:"delete_project",id:"delete_project",level:4},{value:"pin_project",id:"pin_project",level:4},{value:"unpin_project",id:"unpin_project",level:4},{value:"get_meta_json",id:"get_meta_json",level:4}],c={toc:p},u="wrapper";function d(e){let{components:t,...r}=e;return(0,a.kt)(u,(0,n.Z)({},c,r,{components:t,mdxType:"MDXLayout"}),(0,a.kt)("h2",{id:"originsession-objects"},"OriginSession Objects"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"class OriginSession(APISession)\n")),(0,a.kt)("p",null,"Manage access to the Origin API."),(0,a.kt)("p",null,"By default the session will connect to the production Origin API endpoint.\nThis can be overridden by passing the base_url into the constructor or by\nsetting the above environment variables for BASE_URLs. This feature is for\ninternal use only."),(0,a.kt)("p",null,"The authentication token is read from the user","'","s home directory\n",(0,a.kt)("em",{parentName:"p"},"$home/.aurora-api-key")," e.g. ",(0,a.kt)("em",{parentName:"p"},"C:/Users/Joe Bloggs/.aurora-api-key"),". This can\nbe overridden by passing the token into the constructor or by setting the\nenvironment variable ",(0,a.kt)("em",{parentName:"p"},"AURORA_API_KEY"),"."),(0,a.kt)("p",null,(0,a.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},(0,a.kt)("inlineCode",{parentName:"li"},"token")," ",(0,a.kt)("em",{parentName:"li"},"string, optional")," - Override the api authentication token used for\nAPI access. Defaults to None."),(0,a.kt)("li",{parentName:"ul"},(0,a.kt)("inlineCode",{parentName:"li"},"scenario_base_url")," ",(0,a.kt)("em",{parentName:"li"},"string, optional")," - Override the scenario service base url"),(0,a.kt)("li",{parentName:"ul"},(0,a.kt)("inlineCode",{parentName:"li"},"inputs_base_url")," ",(0,a.kt)("em",{parentName:"li"},"string, optional")," - Override the model inputs service base url")),(0,a.kt)("h4",{id:"get_aurora_scenarios"},"get","_","aurora","_","scenarios"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def get_aurora_scenarios(\n        region: Optional[str] = None) -> List[ScenarioSummaryType]\n")),(0,a.kt)("p",null,"Gets a list of all published Aurora scenarios."),(0,a.kt)("p",null,(0,a.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,a.kt)("p",null,"  region (string, optional) - A regional filter. We accept three\nletter ISO codes where appropriate. If in doubt as to which code to\nuse for a region (e.g. Iberia), you can check the Origin URL while\nbrowsing the platform. You will see something like\n",'"',".../launcher/aer/","<","REGION",">",'"'),(0,a.kt)("p",null,(0,a.kt)("strong",{parentName:"p"},"Returns"),":"),(0,a.kt)("p",null,"  List","[ScenarioSummaryType]"),(0,a.kt)("h4",{id:"get_scenario_by_id"},"get","_","scenario","_","by","_","id"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def get_scenario_by_id(scenario_id: str) -> ScenarioType\n")),(0,a.kt)("p",null,"Get a single scenario by it","'","s ID."),(0,a.kt)("p",null,(0,a.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,a.kt)("p",null,"  scenario_id (string) - The ID of the scenario"),(0,a.kt)("p",null,(0,a.kt)("strong",{parentName:"p"},"Returns"),":"),(0,a.kt)("p",null,"  ScenarioType"),(0,a.kt)("h4",{id:"create_scenario"},"create","_","scenario"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def create_scenario(scenario) -> ScenarioType\n")),(0,a.kt)("p",null,"Creates a new scenario"),(0,a.kt)("p",null,(0,a.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,a.kt)("p",null,"  scenario (InputScenario) -"),(0,a.kt)("h4",{id:"update_scenario"},"update","_","scenario"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def update_scenario(scenario_update) -> ScenarioType\n")),(0,a.kt)("h4",{id:"delete_scenario"},"delete","_","scenario"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def delete_scenario(scenario_id: str)\n")),(0,a.kt)("h4",{id:"launch_scenario"},"launch","_","scenario"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def launch_scenario(scenario_id: str) -> ScenarioType\n")),(0,a.kt)("h4",{id:"get_projects"},"get","_","projects"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def get_projects() -> List[ProjectSummaryType]\n")),(0,a.kt)("h4",{id:"get_project"},"get","_","project"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def get_project(project_id: str) -> ProjectType\n")),(0,a.kt)("h4",{id:"create_project"},"create","_","project"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def create_project(project) -> ProjectSummaryType\n")),(0,a.kt)("h4",{id:"update_project"},"update","_","project"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def update_project(project_update) -> ProjectSummaryType\n")),(0,a.kt)("h4",{id:"delete_project"},"delete","_","project"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def delete_project(project_id)\n")),(0,a.kt)("h4",{id:"pin_project"},"pin","_","project"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def pin_project(project_id)\n")),(0,a.kt)("h4",{id:"unpin_project"},"unpin","_","project"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def unpin_project(project_id)\n")),(0,a.kt)("h4",{id:"get_meta_json"},"get","_","meta","_","json"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def get_meta_json(meta_url: str)\n")))}d.isMDXComponent=!0}}]);
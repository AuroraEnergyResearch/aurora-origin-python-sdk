"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[574],{3905:(e,t,r)=>{r.d(t,{Zo:()=>p,kt:()=>_});var n=r(7294);function a(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function o(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function i(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?o(Object(r),!0).forEach((function(t){a(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):o(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function s(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},o=Object.keys(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}var c=n.createContext({}),l=function(e){var t=n.useContext(c),r=t;return e&&(r="function"==typeof e?e(t):i(i({},t),e)),r},p=function(e){var t=l(e.components);return n.createElement(c.Provider,{value:t},e.children)},u="mdxType",d={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},m=n.forwardRef((function(e,t){var r=e.components,a=e.mdxType,o=e.originalType,c=e.parentName,p=s(e,["components","mdxType","originalType","parentName"]),u=l(r),m=a,_=u["".concat(c,".").concat(m)]||u[m]||d[m]||o;return r?n.createElement(_,i(i({ref:t},p),{},{components:r})):n.createElement(_,i({ref:t},p))}));function _(e,t){var r=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=r.length,i=new Array(o);i[0]=m;var s={};for(var c in t)hasOwnProperty.call(t,c)&&(s[c]=t[c]);s.originalType=e,s[u]="string"==typeof e?e:a,i[1]=s;for(var l=2;l<o;l++)i[l]=r[l];return n.createElement.apply(null,i)}return n.createElement.apply(null,r)}m.displayName="MDXCreateElement"},5362:(e,t,r)=>{r.r(t),r.d(t,{assets:()=>c,contentTitle:()=>i,default:()=>d,frontMatter:()=>o,metadata:()=>s,toc:()=>l});var n=r(7462),a=(r(7294),r(3905));const o={sidebar_label:"Project",title:"origin_sdk.service.Project"},i=void 0,s={unversionedId:"origin_sdk/service/Project",id:"origin_sdk/service/Project",title:"origin_sdk.service.Project",description:"Project Objects",source:"@site/docs/origin_sdk/service/Project.md",sourceDirName:"origin_sdk/service",slug:"/origin_sdk/service/Project",permalink:"/aurora-origin-python-sdk/docs/origin_sdk/service/Project",draft:!1,tags:[],version:"current",frontMatter:{sidebar_label:"Project",title:"origin_sdk.service.Project"},sidebar:"docSidebar",previous:{title:"InputsEditor",permalink:"/aurora-origin-python-sdk/docs/origin_sdk/service/InputsEditor"},next:{title:"Scenario",permalink:"/aurora-origin-python-sdk/docs/origin_sdk/service/Scenario"}},c={},l=[{value:"Project Objects",id:"project-objects",level:2},{value:"get",id:"get",level:4},{value:"refresh",id:"refresh",level:4},{value:"pin",id:"pin",level:4},{value:"unpin",id:"unpin",level:4},{value:"create_scenario",id:"create_scenario",level:4},{value:"get_scenario_by_name",id:"get_scenario_by_name",level:4},{value:"get_or_create_scenario_by_name",id:"get_or_create_scenario_by_name",level:4},{value:"get_project_by_name",id:"get_project_by_name",level:4},{value:"get_or_create_project_by_name",id:"get_or_create_project_by_name",level:4}],p={toc:l},u="wrapper";function d(e){let{components:t,...r}=e;return(0,a.kt)(u,(0,n.Z)({},p,r,{components:t,mdxType:"MDXLayout"}),(0,a.kt)("h2",{id:"project-objects"},"Project Objects"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"class Project()\n")),(0,a.kt)("p",null,"The Project class is a more user-friendly set of mappings around the\nlower level OriginSession calls."),(0,a.kt)("h4",{id:"get"},"get"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def get(key: str)\n")),(0,a.kt)("p",null,"Shortcut for Project.project.get()"),(0,a.kt)("h4",{id:"refresh"},"refresh"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def refresh()\n")),(0,a.kt)("p",null,"Refreshes the project data."),(0,a.kt)("h4",{id:"pin"},"pin"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def pin()\n")),(0,a.kt)("p",null,"Pins the project, if it isn","'","t already"),(0,a.kt)("h4",{id:"unpin"},"unpin"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def unpin()\n")),(0,a.kt)("p",null,"Unpins the project, if it isn","'","t already"),(0,a.kt)("h4",{id:"create_scenario"},"create","_","scenario"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def create_scenario(scenario_opts: InputScenario) -> Scenario\n")),(0,a.kt)("p",null,"Shortcut to create a scenario in this project. See\nOriginSession.createScenario for info on argument ",(0,a.kt)("inlineCode",{parentName:"p"},"scenario_opts")),(0,a.kt)("h4",{id:"get_scenario_by_name"},"get","_","scenario","_","by","_","name"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def get_scenario_by_name(scenario_name: str) -> Scenario\n")),(0,a.kt)("p",null,"Gets a scenario from the current project using the name instead of an\nID."),(0,a.kt)("p",null,"NOTE: In the case of more than one scenario with the same name, the\nfirst one will be returned as ordered by the service."),(0,a.kt)("h4",{id:"get_or_create_scenario_by_name"},"get","_","or","_","create","_","scenario","_","by","_","name"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def get_or_create_scenario_by_name(scenario_name: str,\n                                   base_scenario_id: str) -> Scenario\n")),(0,a.kt)("p",null,"Either gets a scenario from this project or creates a scenario in\nthis project with the name specified. In the case of create, requires a\nbase_id."),(0,a.kt)("p",null,"NOTE: In the case of more than one scenario with the same name, the\nfirst one will be returned as ordered by the service."),(0,a.kt)("p",null,(0,a.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},(0,a.kt)("inlineCode",{parentName:"li"},"scenario_name")," - str - The name of the scenario to look for"),(0,a.kt)("li",{parentName:"ul"},(0,a.kt)("inlineCode",{parentName:"li"},"base_id")," - str - The ID of the scenario to use as a base in the case\nthat the scenario doesn","'","t exist")),(0,a.kt)("h4",{id:"get_project_by_name"},"get","_","project","_","by","_","name"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},'@staticmethod\ndef get_project_by_name(session: OriginSession, name: str) -> "Project"\n')),(0,a.kt)("p",null,"Gets a project using the name instead of an ID."),(0,a.kt)("p",null,"NOTE: In the case of more than one project with the same name, the\nfirst one will be returned as ordered by the service."),(0,a.kt)("h4",{id:"get_or_create_project_by_name"},"get","_","or","_","create","_","project","_","by","_","name"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},'@staticmethod\ndef get_or_create_project_by_name(session: OriginSession,\n                                  name: str,\n                                  pin_project: bool = False) -> "Project"\n')),(0,a.kt)("p",null,"Either creates a project with this name, or returns the project that\nalready exists with the same name."),(0,a.kt)("p",null,"NOTE: In the case of more than one project with the same name, the\nfirst one will be returned as ordered by the service."),(0,a.kt)("p",null,(0,a.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},(0,a.kt)("inlineCode",{parentName:"li"},"session")," - OriginSession - The session to make API calls with"),(0,a.kt)("li",{parentName:"ul"},(0,a.kt)("inlineCode",{parentName:"li"},"name")," - str - The name of the project to find/create"),(0,a.kt)("li",{parentName:"ul"},(0,a.kt)("inlineCode",{parentName:"li"},"pin_project")," - Optional, bool - Whether to pin the project if it","'","s not\nalready, defaults to False")))}d.isMDXComponent=!0}}]);
var UFO={req:["movie","width","height","majorversion","build"],opt:["play","loop","menu","quality","scale","salign","wmode","bgcolor","base","flashvars","devicefont","allowscriptaccess","seamlesstabbing","allowfullscreen","allownetworking"],optAtt:["id","name","align"],optExc:["swliveconnect"],ximovie:"ufo.swf",xiwidth:"215",xiheight:"138",ua:navigator.userAgent.toLowerCase(),pluginType:"",fv:[0,0],foList:[],create:function(a,b){if(!UFO.uaHas("w3cdom")||UFO.uaHas("ieMac")){return}UFO.getFlashVersion();UFO.foList[b]=UFO.updateFO(a);UFO.createCSS("#"+b,"visibility:hidden;");UFO.domLoad(b)},updateFO:function(a){if(typeof a.xi!="undefined"&&a.xi=="true"){if(typeof a.ximovie=="undefined"){a.ximovie=UFO.ximovie}if(typeof a.xiwidth=="undefined"){a.xiwidth=UFO.xiwidth}if(typeof a.xiheight=="undefined"){a.xiheight=UFO.xiheight}}a.mainCalled=false;return a},domLoad:function(b){var a=setInterval(function(){if((document.getElementsByTagName("body")[0]!=null||document.body!=null)&&document.getElementById(b)!=null){UFO.main(b);clearInterval(a)}},250);if(typeof document.addEventListener!="undefined"){document.addEventListener("DOMContentLoaded",function(){UFO.main(b);clearInterval(a)},null)}},main:function(b){var a=UFO.foList[b];if(a.mainCalled){return}UFO.foList[b].mainCalled=true;document.getElementById(b).style.visibility="hidden";if(UFO.hasRequired(b)){if(UFO.hasFlashVersion(parseInt(a.majorversion,10),parseInt(a.build,10))){if(typeof a.setcontainercss!="undefined"&&a.setcontainercss=="true"){UFO.setContainerCSS(b)}UFO.writeSWF(b)}else{if(a.xi=="true"&&UFO.hasFlashVersion(6,65)){UFO.createDialog(b)}}}document.getElementById(b).style.visibility="visible"},createCSS:function(a,e){var d=document.getElementsByTagName("head")[0];var c=UFO.createElement("style");if(!UFO.uaHas("ieWin")){c.appendChild(document.createTextNode(a+" {"+e+"}"))}c.setAttribute("type","text/css");c.setAttribute("media","screen");d.appendChild(c);if(UFO.uaHas("ieWin")&&document.styleSheets&&document.styleSheets.length>0){var b=document.styleSheets[document.styleSheets.length-1];if(typeof b.addRule=="object"){b.addRule(a,e)}}},setContainerCSS:function(d){var c=UFO.foList[d];var a=/%/.test(c.width)?"":"px";var b=/%/.test(c.height)?"":"px";UFO.createCSS("#"+d,"width:"+c.width+a+"; height:"+c.height+b+";");if(c.width=="100%"){UFO.createCSS("body","margin-left:0; margin-right:0; padding-left:0; padding-right:0;")}if(c.height=="100%"){UFO.createCSS("html","height:100%; overflow:hidden;");UFO.createCSS("body","margin-top:0; margin-bottom:0; padding-top:0; padding-bottom:0; height:100%;")}},createElement:function(a){return(UFO.uaHas("xml")&&typeof document.createElementNS!="undefined")?document.createElementNS("http://www.w3.org/1999/xhtml",a):document.createElement(a)},createObjParam:function(b,d,c){var a=UFO.createElement("param");a.setAttribute("name",d);a.setAttribute("value",c);b.appendChild(a)},uaHas:function(e){var d=UFO.ua;switch(e){case"w3cdom":return(typeof document.getElementById!="undefined"&&typeof document.getElementsByTagName!="undefined"&&(typeof document.createElement!="undefined"||typeof document.createElementNS!="undefined"));case"xml":var a=document.getElementsByTagName("meta");var c=a.length;for(var b=0;b<c;b++){if(/content-type/i.test(a[b].getAttribute("http-equiv"))&&/xml/i.test(a[b].getAttribute("content"))){return true}}return false;case"ieMac":return/msie/.test(d)&&!/opera/.test(d)&&/mac/.test(d);case"ieWin":return/msie/.test(d)&&!/opera/.test(d)&&/win/.test(d);case"gecko":return/gecko/.test(d)&&!/applewebkit/.test(d);case"opera":return/opera/.test(d);case"safari":return/applewebkit/.test(d);default:return false}},getFlashVersion:function(){if(UFO.fv[0]!=0){return}if(navigator.plugins&&typeof navigator.plugins["Shockwave Flash"]=="object"){UFO.pluginType="npapi";var a=navigator.plugins["Shockwave Flash"].description;if(typeof a!="undefined"){a=a.replace(/^.*\s+(\S+\s+\S+$)/,"$1");var b=parseInt(a.replace(/^(.*)\..*$/,"$1"),10);var f=/r/.test(a)?parseInt(a.replace(/^.*r(.*)$/,"$1"),10):0;UFO.fv=[b,f]}}else{if(window.ActiveXObject){UFO.pluginType="ax";try{var c=new ActiveXObject("ShockwaveFlash.ShockwaveFlash.7")}catch(d){try{var c=new ActiveXObject("ShockwaveFlash.ShockwaveFlash.6");UFO.fv=[6,0];c.AllowScriptAccess="always"}catch(d){if(UFO.fv[0]==6){return}}try{var c=new ActiveXObject("ShockwaveFlash.ShockwaveFlash")}catch(d){}}if(typeof c=="object"){var a=c.GetVariable("$version");if(typeof a!="undefined"){a=a.replace(/^\S+\s+(.*)$/,"$1").split(",");UFO.fv=[parseInt(a[0],10),parseInt(a[2],10)]}}}}},hasRequired:function(c){var b=UFO.req.length;for(var a=0;a<b;a++){if(typeof UFO.foList[c][UFO.req[a]]=="undefined"){return false}}return true},hasFlashVersion:function(b,a){return(UFO.fv[0]>b||(UFO.fv[0]==b&&UFO.fv[1]>=a))?true:false},writeSWF:function(d){var g=UFO.foList[d];var j=document.getElementById(d);if(UFO.pluginType=="npapi"){if(UFO.uaHas("gecko")||UFO.uaHas("xml")){while(j.hasChildNodes()){j.removeChild(j.firstChild)}var k=UFO.createElement("object");k.setAttribute("type","application/x-shockwave-flash");k.setAttribute("data",g.movie);k.setAttribute("width",g.width);k.setAttribute("height",g.height);var f=UFO.optAtt.length;for(var h=0;h<f;h++){if(typeof g[UFO.optAtt[h]]!="undefined"){k.setAttribute(UFO.optAtt[h],g[UFO.optAtt[h]])}}var e=UFO.opt.concat(UFO.optExc);var f=e.length;for(var h=0;h<f;h++){if(typeof g[e[h]]!="undefined"){UFO.createObjParam(k,e[h],g[e[h]])}}j.appendChild(k)}else{var l="";var e=UFO.opt.concat(UFO.optAtt).concat(UFO.optExc);var f=e.length;for(var h=0;h<f;h++){if(typeof g[e[h]]!="undefined"){l+=" "+e[h]+'="'+g[e[h]]+'"'}}j.innerHTML='<embed type="application/x-shockwave-flash" src="'+g.movie+'" width="'+g.width+'" height="'+g.height+'" pluginspage="http://www.macromedia.com/go/getflashplayer"'+l+"></embed>"}}else{if(UFO.pluginType=="ax"){var c="";var f=UFO.optAtt.length;for(var h=0;h<f;h++){if(typeof g[UFO.optAtt[h]]!="undefined"){c+=" "+UFO.optAtt[h]+'="'+g[UFO.optAtt[h]]+'"'}}var a="";var f=UFO.opt.length;for(var h=0;h<f;h++){if(typeof g[UFO.opt[h]]!="undefined"){a+='<param name="'+UFO.opt[h]+'" value="'+g[UFO.opt[h]]+'" />'}}var b=window.location.protocol=="https:"?"https:":"http:";j.innerHTML='<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"'+c+' width="'+g.width+'" height="'+g.height+'" codebase="'+b+"//download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version="+g.majorversion+",0,"+g.build+',0"><param name="movie" value="'+g.movie+'" />'+a+"</object>"}}},createDialog:function(a){var c=UFO.foList[a];UFO.createCSS("html","height:100%; overflow:hidden;");UFO.createCSS("body","height:100%; overflow:hidden;");UFO.createCSS("#xi-con","position:absolute; left:0; top:0; z-index:1000; width:100%; height:100%; background-color:#fff; filter:alpha(opacity:75); opacity:0.75;");UFO.createCSS("#xi-dia","position:absolute; left:50%; top:50%; margin-left: -"+Math.round(parseInt(c.xiwidth,10)/2)+"px; margin-top: -"+Math.round(parseInt(c.xiheight,10)/2)+"px; width:"+c.xiwidth+"px; height:"+c.xiheight+"px;");var i=document.getElementsByTagName("body")[0];var g=UFO.createElement("div");g.setAttribute("id","xi-con");var e=UFO.createElement("div");e.setAttribute("id","xi-dia");g.appendChild(e);i.appendChild(g);var j=window.location;if(UFO.uaHas("xml")&&UFO.uaHas("safari")){var h=document.getElementsByTagName("title")[0].firstChild.nodeValue=document.getElementsByTagName("title")[0].firstChild.nodeValue.slice(0,47)+" - Flash Player Installation"}else{var h=document.title=document.title.slice(0,47)+" - Flash Player Installation"}var b=UFO.pluginType=="ax"?"ActiveX":"PlugIn";var f=typeof c.xiurlcancel!="undefined"?"&xiUrlCancel="+c.xiurlcancel:"";var d=typeof c.xiurlfailed!="undefined"?"&xiUrlFailed="+c.xiurlfailed:"";UFO.foList["xi-dia"]={movie:c.ximovie,width:c.xiwidth,height:c.xiheight,majorversion:"6",build:"65",flashvars:"MMredirectURL="+j+"&MMplayerType="+b+"&MMdoctitle="+h+f+d};UFO.writeSWF("xi-dia")},expressInstallCallback:function(){var b=document.getElementsByTagName("body")[0];var a=document.getElementById("xi-con");b.removeChild(a);UFO.createCSS("body","height:auto; overflow:auto;");UFO.createCSS("html","height:auto; overflow:auto;")},cleanupIELeaks:function(){var b=document.getElementsByTagName("object");var d=b.length;for(var c=0;c<d;c++){b[c].style.display="none";for(var a in b[c]){if(typeof b[c][a]=="function"){b[c][a]=null}}}}};if(typeof window.attachEvent!="undefined"&&UFO.uaHas("ieWin")){window.attachEvent("onunload",UFO.cleanupIELeaks)};
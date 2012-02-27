var cssdropdown={disappeardelay:250,disablemenuclick:true,enableswipe:1,enableiframeshim:1,dropmenuobj:null,ie:document.all,firefox:document.getElementById&&!document.all,swipetimer:undefined,bottomclip:0,getposOffset:function(d,c){var b=(c=="left")?d.offsetLeft:d.offsetTop;var a=d.offsetParent;while(a!=null){b=(c=="left")?b+a.offsetLeft:b+a.offsetTop;a=a.offsetParent}return b},swipeeffect:function(){if(this.bottomclip<parseInt(this.dropmenuobj.offsetHeight)){this.bottomclip+=10+(this.bottomclip/10);this.dropmenuobj.style.clip="rect(0 auto "+this.bottomclip+"px 0)"}else{return}this.swipetimer=setTimeout("cssdropdown.swipeeffect()",10)},showhide:function(b,a){
	if(this.ie||this.firefox){
		
		this.dropmenuobj.style.left=this.dropmenuobj.style.top="-500px";
		
		}
	
	if(a.type=="click"&&b.visibility==hidden||a.type=="mouseover"){if(this.enableswipe==1){if(typeof this.swipetimer!="undefined"){clearTimeout(this.swipetimer)}b.clip="rect(0 auto 0 0)";this.bottomclip=0;this.swipeeffect()}b.visibility="visible"}else{if(a.type=="click"){b.visibility="hidden"}}},iecompattest:function(){return(document.compatMode&&document.compatMode!="BackCompat")?document.documentElement:document.body},clearbrowseredge:function(e,c){var b=0;if(c=="rightedge"){var d=this.ie&&!window.opera?this.iecompattest().scrollLeft+this.iecompattest().clientWidth-15:window.pageXOffset+window.innerWidth-15;this.dropmenuobj.contentmeasure=this.dropmenuobj.offsetWidth;if(d-this.dropmenuobj.x<this.dropmenuobj.contentmeasure){b=this.dropmenuobj.contentmeasure-e.offsetWidth}}else{var a=this.ie&&!window.opera?this.iecompattest().scrollTop:window.pageYOffset;var d=this.ie&&!window.opera?this.iecompattest().scrollTop+this.iecompattest().clientHeight-15:window.pageYOffset+window.innerHeight-18;this.dropmenuobj.contentmeasure=this.dropmenuobj.offsetHeight;if(d-this.dropmenuobj.y<this.dropmenuobj.contentmeasure){b=this.dropmenuobj.contentmeasure+e.offsetHeight;if((this.dropmenuobj.y-a)<this.dropmenuobj.contentmeasure){b=this.dropmenuobj.y+e.offsetHeight-a}}}return b},dropit:function(c,b,a){if(this.dropmenuobj!=null){this.dropmenuobj.style.visibility="hidden"}this.clearhidemenu();if(this.ie||this.firefox){c.onmouseout=function(){cssdropdown.delayhidemenu()};c.onclick=function(){return !cssdropdown.disablemenuclick};this.dropmenuobj=document.getElementById(a);this.dropmenuobj.onmouseover=function(){cssdropdown.clearhidemenu()};this.dropmenuobj.onmouseout=function(d){cssdropdown.dynamichide(d)};this.dropmenuobj.onclick=function(){cssdropdown.delayhidemenu()};this.showhide(this.dropmenuobj.style,b);this.dropmenuobj.x=this.getposOffset(c,"left");this.dropmenuobj.y=this.getposOffset(c,"top");

var browser=navigator.userAgent;
if(a=='video_archives' || a=='video_posted' || a=='video_view')
{
	

	this.dropmenuobj.style.left=this.dropmenuobj.x-this.clearbrowseredge(c,"rightedge")-170+"px";
	this.dropmenuobj.style.top=this.dropmenuobj.y-this.clearbrowseredge(c,"bottomedge")-245+c.offsetHeight+1+"px";	
}
else
{
	
	if(browser.indexOf('Firefox/3.6.19')!=-1)
	{
	
		if(a=='CommitmentPosted' || a=='TypePosted' || a=='SalaryPosted')
		{
			
			
		this.dropmenuobj.style.left=this.dropmenuobj.x-this.clearbrowseredge(c,"rightedge")-170+"px";
		this.dropmenuobj.style.top=this.dropmenuobj.y-this.clearbrowseredge(c,"bottomedge")-170+c.offsetHeight+1+"px";	
	
		}
		else
		{
		this.dropmenuobj.style.left=this.dropmenuobj.x-this.clearbrowseredge(c,"rightedge")-170+"px";
		this.dropmenuobj.style.top=this.dropmenuobj.y-this.clearbrowseredge(c,"bottomedge")-175+c.offsetHeight+1+"px";		
		}
	}
	else
	{

		this.dropmenuobj.style.left=this.dropmenuobj.x-this.clearbrowseredge(c,"rightedge")-170+"px";
	this.dropmenuobj.style.top=this.dropmenuobj.y-this.clearbrowseredge(c,"bottomedge")-175+c.offsetHeight+1+"px";	
	}
}



this.positionshim()}},positionshim:function(){if(this.enableiframeshim&&typeof this.shimobject!="undefined"){
	if(this.dropmenuobj.style.visibility=="visible")
	{
		this.shimobject.style.width=this.dropmenuobj.offsetWidth+"px";
		this.shimobject.style.height=this.dropmenuobj.offsetHeight+"px";
		this.shimobject.style.left=this.dropmenuobj.style.left;
		this.shimobject.style.top=this.dropmenuobj.style.top

		}
this.shimobject.style.display=(this.dropmenuobj.style.visibility=="visible")?"block":"none"}},hideshim:function(){if(this.enableiframeshim&&typeof this.shimobject!="undefined"){this.shimobject.style.display="none"}},contains_firefox:function(d,c){while(c.parentNode){if((c=c.parentNode)==d){return true}}return false},dynamichide:function(b){var a=window.event?window.event:b;if(this.ie&&!this.dropmenuobj.contains(a.toElement)){this.delayhidemenu()}else{if(this.firefox&&b.currentTarget!=a.relatedTarget&&!this.contains_firefox(a.currentTarget,a.relatedTarget)){this.delayhidemenu()}}},delayhidemenu:function(){this.delayhide=setTimeout("cssdropdown.dropmenuobj.style.visibility='hidden'; cssdropdown.hideshim()",this.disappeardelay)},clearhidemenu:function(){if(this.delayhide!="undefined"){clearTimeout(this.delayhide)}},startchrome:function(){for(var c=0;c<arguments.length;c++){var d=document.getElementById(arguments[c]).getElementsByTagName("a");for(var b=0;b<d.length;b++){if(d[b].getAttribute("rel")){var a=d[b].getAttribute("rel");d[b].onmouseover=function(g){var f=typeof g!="undefined"?g:window.event;cssdropdown.dropit(this,f,this.getAttribute("rel"))}}}}if(window.createPopup&&!window.XmlHttpRequest){document.write('<IFRAME id="iframeshim"  src="" style="display: none; left: 0; top: 0; z-index: 90; position: absolute; filter: progid:DXImageTransform.Microsoft.Alpha(style=0,opacity=0)" frameBorder="0" scrolling="no"></IFRAME>');this.shimobject=document.getElementById("iframeshim")}}};
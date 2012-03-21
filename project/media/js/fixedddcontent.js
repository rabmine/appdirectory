
$(document).ready(function(){
	
	
	dropdowncontent.show=function(anchorobj, subobj, e){
		if (!this.isContained(anchorobj, e) || (e && e.type=="click")){
			var e=window.event || e
			if (e.type=="click" && subobj.style.visibility=="visible"){
				subobj.style.visibility="hidden"
				return
			}
			var horizontaloffset=(subobj.dropposition[0]=="left")? -(subobj.offsetWidth-anchorobj.offsetWidth) : 0 //calculate user added horizontal offset
			var verticaloffset=(subobj.dropposition[1]=="top")? -subobj.offsetHeight : anchorobj.offsetHeight //calculate user added vertical offset
			subobj.style.left=this.getposOffset(anchorobj, "offsetLeft") + horizontaloffset + "px"
			subobj.style.top=this.getposOffset(anchorobj, "offsetTop")+verticaloffset+"px"
			subobj.style.clip=(subobj.dropposition[1]=="top")? "rect(auto auto auto 0)" : "rect(0 auto 0 0)" //hide drop down box initially via clipping
			subobj.style.visibility="visible"
			subobj.startTime=new Date().getTime()
			subobj.contentheight=parseInt(subobj.offsetHeight)
			if (typeof window["hidetimer_"+subobj.id]!="undefined") //clear timer that hides drop down box?
				clearTimeout(window["hidetimer_"+subobj.id])
			this.slideengine(subobj, (subobj.dropposition[1]=="top")? "up" : "down")
		}
		
		var position = $('#FontLink').offset();
		$('#FontMenu').offset({ top: position.top + 15, left: position.left });
	}
	
	
});


function createXMLHttpRequest(){var a;if(window.XMLHttpRequest){try{a=new XMLHttpRequest()}catch(b){a=false}}else{if(window.ActiveXObject){try{a=new ActiveXObject("Microsoft.XMLHTTP")}catch(b){a=false}}}return a}var req=createXMLHttpRequest();function getState(){country=document.getElementById("country").value;if(country!=""){req.open("get","state_list.php?country_id="+country);req.onreadystatechange=handleResponse;req.send(null)}getCity()}function getState1(){country=document.getElementById("country").value;document.getElementById("city_list_tr").style.display="none";if(country!=""){req.open("get","state_list1.php?country_id="+country);req.onreadystatechange=handleResponse;req.send(null)}}function handleResponse(){if(req.readyState==4){var a=req.responseText;document.getElementById("state_div").innerHTML=a;document.getElementById("state_div").style.display=""}getCity()}var req1=createXMLHttpRequest();function getCity(){state=document.getElementById("state").value;if(state!=""){req1.open("get","city_list.php?state_id="+state);req1.onreadystatechange=handleResponse1;req1.send(null)}}function getCity1(){document.getElementById("city_list_tr").style.display="";state=document.getElementById("state").value;if(state!=""){req1.open("get","city_list1.php?state_id="+state);req1.onreadystatechange=handleResponse1;req1.send(null)}}function handleResponse1(){if(req1.readyState==4){var a=req1.responseText;document.getElementById("city_div").innerHTML=a;document.getElementById("city_div").style.display=""}}function get_eveState(){eve_country=document.getElementById("eve_country").value;if(eve_country!=""){req.open("get","eve_state_list.php?country_id="+eve_country);req.onreadystatechange=handleResponse;req.send(null)}}function get_eveCity(){eve_state=document.getElementById("eve_state").value;if(eve_state!=""){req1.open("get","eve_city_list.php?state_id="+eve_state);req1.onreadystatechange=handleResponse1;req1.send(null)}}function get_eveState1(){eve_country=document.getElementById("eve_country").value;event_id=document.getElementById("event_id").value;if(eve_country!=""){req.open("get","eve_state_list1.php?country_id="+eve_country+"&event_id="+event_id);req.onreadystatechange=handleResponse2;req.send(null)}}function handleResponse2(){if(req.readyState==4){var a=req.responseText;document.getElementById("state_div").innerHTML=a;document.getElementById("state_div").style.display=""}get_eveCity1()}function get_eveCity1(){eve_state=document.getElementById("eve_state").value;event_id=document.getElementById("event_id").value;if(eve_state!=""){req1.open("get","eve_city_list1.php?state_id="+eve_state+"&event_id="+event_id);req1.onreadystatechange=handleResponse1;req1.send(null)}}function get_eveState2(){eve_country=document.getElementById("eve_country").value;job_id=document.getElementById("job_id").value;if(eve_country!=""){req.open("get","eve_state_list2.php?country_id="+eve_country+"&job_id="+job_id);req.onreadystatechange=handleResponse3;req.send(null)}}function get_eveCity2(){eve_state=document.getElementById("eve_state").value;job_id=document.getElementById("job_id").value;if(eve_state!=""){req1.open("get","eve_city_list2.php?state_id="+eve_state+"&job_id="+job_id);req1.onreadystatechange=handleResponse4;req1.send(null)}}function handleResponse3(){if(req.readyState==4){var a=req.responseText;document.getElementById("state_div").innerHTML=a;document.getElementById("state_div").style.display=""}getCity1()}function handleResponse4(){if(req1.readyState==4){var a=req1.responseText;document.getElementById("city_div").innerHTML=a;document.getElementById("city_div").style.display=""}};
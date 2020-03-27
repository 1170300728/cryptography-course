function ajax_request()
{
	var xmlhttp;
	if (window.XMLHttpRequest) {
		// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	  } else {
		// code for IE6, IE5
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	var key1 = Math.floor(Math.random() * 10000000 + 1);
	var sagp = encAction(key1);
	var result = new Array(3);
	result[0] = '';
	result[1] = '';
	result[2] = '';
	var i;
	for (i = 0; i < 50; i++){
		result[0] += sagp[0][i].toString()
		result[1] += sagp[1][i].toString()
		result[2] += sagp[2][i].toString()
	}
	xmlhttp.open("GET", "/add/" + result[0] + "/" + result[1] + "/" + result[2] + "/", true);
	xmlhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
	xmlhttp.send();
	xmlhttp.onreadystatechange=function() {
		var x = xmlhttp.readyState;
		var y = xmlhttp.status;
	  if (xmlhttp.readyState==4 && xmlhttp.status==200) {
		  var recv = xmlhttp.responseText;
		  var g = sagp[1];
		  var p = sagp[2];
		  var sb = new Array(50);
		  var i;
		  for (i = 0; i < 50; i ++){
			  sb[i] = parseInt(recv[i]);
		  }
		  var keya = getkey(key1, sb, p, g).slice(0, 8);
		  var key = '';
		  var i;
		  for(i = 0; i < keya.length; i ++)
			  key += keya[i];
		  var f = document.form1;
		  var userinput = f.Password.value;
		  var encode = desencode(userinput, key);
		  f.Password.value = encode;
		  document.form1.submit();
		  
	  }
	}
	// ajax 教程：http://www.ziqiangxuetang.com/ajax/ajax-tutorial.html
}

//def des(userinput, keya):
//	window.Alert("Hello from Python!")

function encAction(x){
	//var x = 123;
	//var y = 234;
	var sa = encon(x);
	//var ans = sa[0];
	//var g = sa[1];
	//var p = sa[2];
	//var sb = recon(y, sa[1], sa[2]);
	//var keya = getkey(x, sb, p, g);
	//var keyb = getkey(y, sa[0], p, g);
	return sa;
}

function getkey(b, rec, p, g){
	var t = new Array(50);
	var ans = new Array(50);
	var i;

	for (i = 0; i<50; i++){
		t[i] = rec[i];
		ans[i] = 0;
	}
	ans[0] = 1;
	for (i = 0; i<32; i++){
		if (b & 1 << i){
			ans = mul(ans, t);
			ans = mod(ans, p);
		}
		t = mul(t, t);
		t = mod(t, p);
	}
	return ans;
}

function recon(b, g, p){
	var t = new Array(50);
	var ans = new Array(50);
	var i;
	for (i = 0; i < 50; i++){
		t[i] = g[i];
		ans[i] = 0;
	}
	ans[0] = 1;
	for (i = 0; i<32; i++){
		if (b & 1 << i){
			ans = mul(ans, t);
			ans = mod(ans, p);
		}
		t = mul(t, t);
		t = mod(t, p);
	}
	return ans;
}

function encon(a){
	var i;
	var t = new Array(50);
	var ans = new Array(50);
	var p_n = 0;
	for (i = 0; i < 50; i ++){
		t[i] = 0;
	}
	var g = getg();
	var p = getp(p_n);
	p = reserve(p);
	for (i = 0; i < 50; i ++){
		t[i] = g[i];
		ans[i] = 0;
	}
	ans[0] = 1;
	for (i = 0; i < 32; i ++){
		if (a & 1 << i){
			ans = mul(ans, t);
			ans = mod(ans, p);
		}
		t = mul(t, t);
		t = mod(t, p);
	}
	
	var result = new Array(3);
	result[0] = ans;
	result[1] = g;
	result[2] = p;
	return result;
}

function mul(a, b){
	var na, nb, i, j, n;
	var c = new Array(50);
	var d = new Array(50);
	for (i = 0; i<50; i++)
		c[i] = a[i], d[i] = b[i], a[i] = 0;
	na = getn(c);
	nb = getn(d);
	for (i = 0; i<nb; i++)for (j = 0; j<na; j++){
		a[i + j] += d[i] * c[j];
		if (a[i + j]>9)a[i + 1 + j] += parseInt(a[i + j] / 10), a[i + j] %= 10;
	}
	for (i = 0; i<50&&i<(na + nb); i++){
		if (a[i])n = i + 1;
		if (a[i]>9)a[i + 1] += parseInt(a[i] / 10), a[i] %= 10;
	}
	return a;
}

function mod(a, b){
	var na, nb, i, u, f = 0, n;
	na = getn(a);
	nb = getn(b);
	u = na - nb;
	if (u<0)return a;
	while (u + 1){
		for (i = na - 1, f = 0; i >= u; i--){
			if (a[i]>b[i - u]){ f = 1; break; }
			if (a[i]<b[i - u]){ f = -1; break; }
		}
		if (!f){
			for (i = na - 1; i >= u; i--)a[i] = 0;
			u -= nb;
			if (u<0)break;
			continue;
		}
		if (f == -1)u--;
		if (f == 1){
			for (i = u; i<na; i++){
				a[i] -= b[i - u];
				if (a[i]<0)a[i + 1]--, a[i] += 10;
			}
		}
	}
	for (i = 0; i<na; i++)if (a[i])n = i + 1;
	return a;
}

function reserve(a){
	var i, n;
	n = getn(a);
	for (i = 0; i < parseInt(n / 2); i ++){
		var temp = a[i];
		a[i] = a[n - i - 1];
		a[n - i - 1] = temp;
	}
	return a;
}

function getn(a){
	var i = 49;
	while(i >= 0 && !a[i])
		i --;
	return i + 1;
}

function getp(n){
	var a = new Array(50);
	var p_set = ["71999651", "71999657"];
	var i;
	for (i = 0; i < 8; i ++){
		a[i] = parseInt(p_set[n][i]);
	}
	while(i < 50){
		a[i] = 0;
		i ++;
	}
	return a;
}

function getg(){
	var g = new Array(50);
	g[0] = 1;
	g[1] = 2;
	g[2] = 3;
	g[3] = 4;
	g[4] = 1;
	var i = 5;
	while (i < 50){
		g[i] = 0;
		i ++;
	}
	return g;
}
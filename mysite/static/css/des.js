function desencode(from_code, key){
	from_code = tohex(from_code);
	key = tohex(key);
	key_len = key.length;
	string_len = from_code.length;
	if (key_len < 1 || string_len < 1)
		return 'error'

	key_code = code(from_code, key, string_len, key_len);
	return key_code;
}

function code(from_code, key, code_len, key_len){
	var d = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1];
	var output = '';
	var trun_len = 0;
	var code_string = functionCharToA(from_code, code_len);
	var code_key = functionCharToA(key, key_len);
	var real_len;
	var key_len;
	if (code_len % 16 != 0){
		real_len = code_len + 16 - (code_len % 16);
	}
	else
		real_len = code_len;
	if (key_len % 16 != 0)
		key_len = key_len + 16 - (key_len % 16);
	key_len *= 4;
	trun_len = 4 * real_len;
	
	for (i = 0; i < trun_len; i += 64){
		var run_code = code_string.slice(i, i + 64);
		var l = i % key_len;
		var j;
		var run_key = code_key.slice(l, l + 64);
		
		run_code = codefirstchange(run_code);
		run_key = keyfirstchange(run_key);
		
		for (j = 0; j < 16; j ++){
			var code_r = run_code.slice(32, 64);
			var code_l = run_code.slice(0, 32);
			
			run_code = code_r;
			
			code_r = functionE(code_r);
			
			var key_l = run_key.slice(0, 28);
			var key_r = run_key.slice(28, 56);
			key_l = key_l.slice(d[j], 28) + key_l.slice(0, d[j]);
			key_r = key_r.slice(d[j], 28) + key_r.slice(0, d[j]);
			
			run_key = key_l + key_r;
			key_y = functionKeySecondChange(run_key);
			
			code_r = codeyihuo(code_r, key_y);
			
			code_r = functionS(code_r);
			
			code_r = functionP(code_r);
			
			code_r = codeyihuo(code_l, code_r);
			
			run_code += code_r;
		}
		code_r = run_code.slice(32, 64);
		code_l = run_code.slice(0, 32);
		run_code = code_r + code_l;
		
		output += functionCodeChange(run_code);
	}
	return output;
}

function functionCodeChange(code){
	var ip_1=[40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41,  9, 49, 17, 57, 25];
	var lens = parseInt(code.length / 4);
	var return_list = '';
	var i;
	for (i = 0; i < lens; i ++){
		var list = '';
		var j;
		for (j = 0; j < 4; j ++){
			list += code[ip_1[i*4+j] - 1];
		}
		return_list += parseInt(list, 2).toString(16);
	}
	return return_list;
}

function functionP(code){
	var p=[16,  7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26,  5, 18, 31, 10, 
     2,  8, 24, 14, 32, 27,  3,  9,
     19, 13, 30, 6, 22, 11,  4,  25];
	var return_list = '';
	var i;
	for (i = 0; i < 32; i ++){
		return_list += code[p[i] - 1];
	}
	return return_list;
}

function functionS(key){
	var s=[[[14, 4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
     [0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
     [4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],    
     [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]],

     [[15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],     
     [3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],     
     [0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],     
     [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]],

     [[10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],     
     [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],   
     [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],     
     [1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]],

    [[7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11,  12,  4, 15],     
     [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,9],     
     [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],     
     [3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]],


    [[2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],     
     [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],     
     [4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],     
     [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]],

    [[12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
     [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],     
     [9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],     
     [4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]],

    [[4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],     
     [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],     
     [1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],     
     [6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]],

   [[13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],     
     [1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],     
     [7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],     
     [2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]]];
	var return_list = '';
	var i;
	for (i = 0; i < 8; i ++){
		var row = parseInt(key[i*6].toString() + key[i*6+5].toString(), 2);
		var raw = parseInt(key[i*6+1].toString() + key[i*6+2].toString() + key[i*6+3].toString() + key[i*6+4].toString(), 2);
		return_list += functionTos(s[i][row][raw], 4);
	}
	return return_list;
}

function codeyihuo(code, key){
	var code_len = key.length;
	var return_list = '';
	var i;
	for (i = 0; i < code_len; i ++){
		if (code[i] == key[i])
			return_list += '0';
		else
			return_list += '1';
	}
	return return_list;
}

function functionKeySecondChange(key){
	var pc2= [14, 17, 11, 24,  1,  5,  3, 28,
      15,  6, 21, 10, 23, 19, 12,  4, 
      26,  8, 16,  7, 27, 20, 13,  2, 
      41, 52, 31, 37, 47, 55, 30, 40, 
      51, 45, 33, 48, 44, 49, 39, 56, 
      34, 53, 46, 42, 50, 36, 29, 32];
	var return_list = '';
	var i;
	for (i = 0; i < 48; i ++){
		return_list += key[pc2[i] - 1];
	}
	return return_list;
}

function functionE(code){
	var e = [32, 1,  2,  3,  4,  5,  4,  5, 
       6, 7,  8,  9,  8,  9, 10, 11, 
      12,13, 12, 13, 14, 15, 16, 17,
      16,17, 18, 19, 20, 21, 20, 21,
      22, 23, 24, 25,24, 25, 26, 27,
      28, 29,28, 29, 30, 31, 32,  1];
	var return_list = '';
	var i;
	for (i = 0; i < 48; i ++){
		return_list += code[e[i] - 1];
	}
	return return_list;
}

function codefirstchange(code){
	var ip=  [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9 , 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7];
	var changed_code = '';
	var i;
	for (i = 0; i < 64; i ++){
		changed_code += code[ip[i] - 1];
	}
	return changed_code;
}

function keyfirstchange(key){
	var pc1=[57, 49, 41, 33, 25, 17,  9,
       1, 58, 50, 42, 34, 26, 18,
      10,  2, 59, 51, 43, 35, 27,
      19, 11,  3, 60, 52, 44, 36,
      63, 55, 47, 39, 31, 33, 15,
       7, 62, 54, 46, 38, 30, 22,
      14,  6, 61, 53, 45, 37, 29,
      21, 13,  5, 28, 20, 12, 4];
	var changed_key = '';
	var i;
	for (i = 0; i < 56; i ++){
		changed_key += key[pc1[i] - 1];
	}
	return changed_key;
}

function functionCharToA(code, lens){
	var return_code = '';
	lens = lens % 16;
	var i;
	for (i = 0; i < code.length; i ++){
		code_ord = parseInt(code[i], 16);
		return_code += functionTos(code_ord, 4);
	}
	if (lens != 0){
		for (i = 0; i < 16 - lens; i ++)
			return_code += '0000';
	}
	return return_code;
}

function functionTos(o, lens){
	var return_code = '';
	var i;
	for (i = 0; i < lens; i ++){
		return_code = ((o >> i) & 1) + return_code;
	}
	return return_code;
}

function tohex(string){
	var return_string = '';
	var i;
	for (i = 0; i < string.length; i ++){
		return_string += string.charCodeAt(i).toString(16);
	}
	return return_string;
}
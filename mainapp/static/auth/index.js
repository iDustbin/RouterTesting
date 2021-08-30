// Generate Secure Password
const key_strings = {
	lowercase: 'abcdefghijklmnopqrstuvwxyz',
	uppercase: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
	number: '0123456789',
	symbol: '*;<>()[]{}#$?!^|'
};
function generateSecurePassword(){
  var length = 15;
  let password1 = document.getElementById("password1")
  let password2 = document.getElementById("password2")
	password1.type = 'text';
	password2.type = 'text';
  let value =  generateRandomPassword(length);
  password1.value = value;
  password2.value = value;
}
function generateRandomPassword(length){
	let MAIN_STRING = "";
	let PASSWORD = "";
	
	const options = {
		lowercase: true,
		uppercase: true,
		number: true,
		symbol: true
	};
	
	for(i=0;i<Object.keys(options).length;i++){
		MAIN_STRING += (Object.values(options)[i]) ? key_strings[Object.keys(options)[i]] : "";
	}
	
	if(MAIN_STRING != "" && length > 0){
		for(i=0;i<length;i++){
			PASSWORD += MAIN_STRING[Math.floor(Math.random() * MAIN_STRING.length)];
		}
		return PASSWORD;
	}else{
    return PASSWORD;
	}
	
    	
}

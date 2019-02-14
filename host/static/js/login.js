function isValidateForm() {
	let username = document.getElementById("username-input").value;
	let password = document.getElementById("password-input").value;
	if(username.length < 3) {
		castFormError("Username is too short. It has to be 3 characters or longer");
		return false;
	} else if (username.length > 16) {
		castFormError("Username is too long. It has to be less than 13 characters");
		return false;
	} else if (password.length < 6) {
		castFormError("Password is too short. It has to be 6 characters or longer");
		return false;
	} else if (password.length > 32) {
		castFormError("Password is too long. It has to be 32 characters or shorter");
		return false;
	}
	return true
}

function castFormError(string) {
	
}

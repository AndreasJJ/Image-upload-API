document.getElementById("dashboard-upload-file-upload-input").addEventListener('change', (e) => {
	let container = document.getElementById("dashboard-upload-file-list");
	container.innerHTML = "";
	for(let i = 0; i < e.target.files.length; i++) {
		let fileContainer = document.createElement("DIV"); 
		var filename = document.createTextNode(e.target.files[i].name);
		fileContainer.appendChild(filename)
		container.appendChild(fileContainer)
	}
});
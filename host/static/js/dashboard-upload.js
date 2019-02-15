document.getElementById("dashboard-upload-file-upload").addEventListener('dragover', fileDropHandler)
document.getElementById("dashboard-upload-file-upload").addEventListener('drop', fileDropHandler)

function fileDropHandler(e) {

  // Prevent default behavior (Prevent file from being opened)
  e.preventDefault();

  if (e.dataTransfer.items) {
  	files = []
    // Use DataTransferItemList interface to access the file(s)
    for (var i = 0; i < e.dataTransfer.items.length; i++) {
      // If dropped items aren't files, reject them
      if (e.dataTransfer.items[i].kind === 'file') {
        var file = e.dataTransfer.items[i].getAsFile();
        if(file) {
        	files.push(file)
        }
      }
    }
    addFilesToFileLits(files)
  } else {
    // Use DataTransfer interface to access the file(s)
    addFilesToFileLits(e.dataTransfer.files)
    for (var i = 0; i < e.dataTransfer.files.length; i++) {
      	
    }
  }
}

document.getElementById("dashboard-upload-file-upload-input").addEventListener('change', (e) => {
	addFilesToFileLits(e.target.files);
});

function addFilesToFileLits(files) {
	let container = document.getElementById("dashboard-upload-file-list");
	container.innerHTML = "";
	for(let i = 0; i < files.length; i++) {
		let fileContainer = document.createElement("DIV"); 
		var filename = document.createTextNode(files[i].name);
		fileContainer.appendChild(filename)
		container.appendChild(fileContainer)
	}
}
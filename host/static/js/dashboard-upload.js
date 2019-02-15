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
		let fileContainer = document.createElement("DIV")
    fileContainer.style.display = "flex"
    fileContainer.style.justifyContent = "space-between"
    let fileSpan = document.createElement("SPAN")
		var filename = document.createTextNode(files[i].name)
    fileSpan.appendChild(filename)
		fileContainer.appendChild(fileSpan)
		container.appendChild(fileContainer)
	}
  for (let i = 0; i < files.length; i++) {
    uploadFile(files[i]).then((response) => {
      if(response.status == 200) {
        let fileSpan = document.createElement("SPAN")
        let fileLink = document.createElement("A")
        var filename = document.createTextNode(response.url.replace(/^.*[\\\/]/, ''))
        fileLink.href = "/" + response.url.replace(/^.*[\\\/]/, '')
        fileLink.appendChild(filename)
        fileSpan.appendChild(fileLink)
        container.children[i].appendChild(fileSpan)
        container.children[i].style.backgroundColor = "#4CAF50"
      } else {
        container.children[i].style.backgroundColor = "#f44336"
      }
    })
  }
}

function uploadFile(file) {
  let formData  = new FormData()
  formData.append("file", file)

  const options = {
        method: "POST", 
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        referrer: "no-referrer",
        body: formData,
   }
  
  return fetch("/upload", options).then((response) => response);
}
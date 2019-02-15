var selectImagesEnabled = false
document.getElementById("dashboard-links-select-button").addEventListener('click', selectImages)
document.getElementById("dashboard-links-delete-button").addEventListener('click', deleteImages)
var images = document.getElementsByClassName("dashboard-links-thumbnail")
for (let i = 0; i < images.length; i++) {
	images[i].addEventListener('click', selectImage)
}

function selectImage(e) {
	if(selectImagesEnabled) {
		e.preventDefault()
		if(e.target.classList.contains("dashboard-links-image-selected")) {
			e.target.classList.remove("dashboard-links-image-selected")
		} else {
			e.target.classList.add("dashboard-links-image-selected")
		}
	} 
}

function selectImages(e) {
	if(!selectImagesEnabled) {
		selectImagesEnabled = true
		document.getElementById("dashboard-links-select-button").style.backgroundColor = "#008CBA"
		document.getElementById("dashboard-links-select-button").innerText = "Deselect images"
		document.getElementById("dashboard-links-delete-button").disabled = false
	} else {
		selectImagesEnabled = false
		document.getElementById("dashboard-links-select-button").style.backgroundColor = "#4CAF50"
		document.getElementById("dashboard-links-select-button").innerText = "Select images"
		document.getElementById("dashboard-links-delete-button").disabled = true
		for (let i = 0; i < images.length; i++) {
			images[i].children[0].children[0].classList.remove("dashboard-links-image-selected")
		}
	}
}

function deleteImages(e) {
	selectedImages = []
	for (let i = 0; i < images.length; i++) {
		let image = images[i].children[0].children[0]
		if(image.classList.contains("dashboard-links-image-selected")) {
			let imageUrl = image.src
			filename = imageUrl.replace(/^.*[\\\/]/, '')
			selectedImages.push(filename)
		}
	}
	fetch("/api?operation=delete", {
        method: "POST", 
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
        },
        referrer: "no-referrer",
        body: JSON.stringify(selectedImages),
    }).then((response) => location.reload());
}
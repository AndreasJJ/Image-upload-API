var selectImagesEnabled = false

setEventListenerOnImages()
function setEventListenerOnImages() {
	let images = document.getElementsByClassName("dashboard-links-thumbnail")
	for (let i = 0; i < images.length; i++) {
		images[i].addEventListener('click', selectImage)
	}
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

document.getElementById("dashboard-links-select-button").addEventListener('click', selectImages)
function selectImages(e) {
	let images = document.getElementsByClassName("dashboard-links-thumbnail")
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

document.getElementById("dashboard-links-delete-button").addEventListener('click', deleteImages)
function deleteImages(e) {
	let images = document.getElementsByClassName("dashboard-links-thumbnail")
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

document.getElementById("dashboard-content").addEventListener('scroll', (e) => {

	if(e.target.scrollHeight - e.target.scrollTop === e.target.clientHeight) {
		let imageCount = document.getElementById("dashboard-links-content").children.length
		let amountOfNewImages = 20
		let newImages = getNewImages(imageCount, imageCount+amountOfNewImages).then((response) => {
			for (var i = 0; i < response.links.length; i++) {
				let imagesContainer = document.getElementById("dashboard-links-content")
				let thumbnailContainer = document.createElement("DIV")
				thumbnailContainer.classList.add("dashboard-links-thumbnail")
				let thumbnailLink = document.createElement("A")
				thumbnailLink.href = "/" + response.links[i]
				let image = document.createElement("IMG")	
				image.src = "/" + response.links[i]
				thumbnailLink.appendChild(image)
				thumbnailContainer.appendChild(thumbnailLink)
				imagesContainer.appendChild(thumbnailContainer)
			}
		})
	}
	setEventListenerOnImages()
})

function getNewImages(start, end){
	link = "/api?data=links&start=" + start + "&end=" + end
	return fetch(link, {
	        method: "GET",
	        mode: "cors",
	        cache: "no-cache",
	        credentials: "same-origin",
	        headers: {
	            "Content-Type": "application/json",
	        },
	        referrer: "no-referrer",
	        body: null,
	    }).then(response => response.json());
}

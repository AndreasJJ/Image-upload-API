// Sets up a charts plugin to show an error message if there's no data to show.
Chart.plugins.register({
	beforeDraw: function (chart) {
		if (chart.config.options.elements.center) {
		  //Get ctx from string
		  var ctx = chart.chart.ctx;

		  //Get options from the center object in options
		  var centerConfig = chart.config.options.elements.center;
		  var fontStyle = centerConfig.fontStyle || 'Arial';
		  var txt = centerConfig.text;
		  var color = centerConfig.color || '#000';
		  var sidePadding = centerConfig.sidePadding || 20;
		  var sidePaddingCalculated = (sidePadding/100) * (chart.innerRadius * 2)
		  //Start with a base font of 30px
		  ctx.font = "30px " + fontStyle;

		  //Get the width of the string and also the width of the element minus 10 to give it 5px side padding
		  var stringWidth = ctx.measureText(txt).width;
		  var elementWidth = (chart.innerRadius * 2) - sidePaddingCalculated;

		  // Find out how much the font can grow in width.
		  var widthRatio = elementWidth / stringWidth;
		  var newFontSize = Math.floor(30 * widthRatio);
		  var elementHeight = (chart.innerRadius * 2);

		  // Pick a new font size so it will not be larger than the height of label.
		  var fontSizeToUse = Math.min(newFontSize, elementHeight);

		  //Set font settings to draw it correctly.
		  ctx.textAlign = 'center';
		  ctx.textBaseline = 'middle';
		  var centerX = ((chart.chartArea.left + chart.chartArea.right) / 2);
		  var centerY = ((chart.chartArea.top + chart.chartArea.bottom) / 2);
		  ctx.font = fontSizeToUse+"px " + fontStyle;
		  ctx.fillStyle = color;

		  //Draw text in center
		  ctx.fillText(txt, centerX, centerY);
		}
	},
	afterDraw: function(chart) {
	  	if (chart.data.datasets.length === 0) {
	    	// No data is present
	      var ctx = chart.chart.ctx;
	      var width = chart.chart.width;
	      var height = chart.chart.height;
	      chart.chart.options.responsive = true;
	      chart.chart.options.maintainAspectRatio = false;
	      chart.clear();
	      
	      ctx.save();
	      ctx.textAlign = 'center';
	      ctx.textBaseline = 'middle';
	      ctx.font = "16px normal 'Helvetica Nueue'";
	      ctx.fillText('No data to display', width / 2, height / 2);
	      ctx.restore();
	    }
  	}
});

// Sets up the graph when the window is done loading.
window.onload = function() {
  	let ctx = document.getElementById("myChart");
	if(ctx) {
		ctx = ctx.getContext('2d')
		getUsedStorageSpaceRequest().then((used) => {
			getStorageSpaceRequest().then((_storage_space) => {
				let unused_space = _storage_space.storage_space - used.used
				let storage_space = [used.used, unused_space] 
				let graphColor
				let graphLabel
				let text
				if(unused_space < 0) {
					text = (storage_space[0]/(_storage_space.storage_space)*100).toFixed(2) + "%"
					storage_space = [storage_space[0]/Math.pow(1024,2), 0]
					graphColor  = ["#b224ef", "#cccccc"]
					graphLabel = ['Used Storage Space', 'Unused Storage Space']
				} else if(storage_space[1] != null) {
					text = (storage_space[0]/(_storage_space.storage_space)*100).toFixed(2) + "%"
					storage_space = [storage_space[0]/Math.pow(1024,2), storage_space[1]/Math.pow(1024,2)]
					graphColor  = ["#b224ef", "#cccccc"]
					graphLabel = ['Used Storage Space', 'Unused Storage Space']
				} else {
					text = "N/A"
					storage_space = [storage_space[0]/Math.pow(1024,2), storage_space[1]]
					graphColor = ["#b224ef"]
					graphLabel = ['Used Storage Space']
				}
				var myDoughnutChart = new Chart(ctx, {
				    type: 'doughnut',
				    data: {
						    datasets: [{
						        data: storage_space,
						        backgroundColor: graphColor
						    }],

						    // These labels appear in the legend and in the tooltips when hovering different arcs
						    labels: graphLabel
						},
					options: {
						responsive: true,
						maintainAspectRatio: false,
						tooltips: {
						    callbacks: {
						      label: (item, data) => `${data.datasets[item.datasetIndex].data[item.index].toFixed(2)} MB`,

						    }
						},
						elements: {
							center: {
								text: text,
								color: '#36A2EB', //Default black
								fontStyle: 'Helvetica', //Default Arial
								sidePadding: 15 //Default 20 (as a percentage)
							}
						}
					}
				});
			})
		}).catch((e) => {
			var myDoughnutChart = new Chart(ctx, {
			    type: 'doughnut',
			    data: {},
				options: {}
			});
		})
	}
};

// Function for hiding the side menu when clicking the collapse button.
function onClickCollapseButton() {
	if(document.getElementById("dashboard-side-menu").style.display == "none") {
		document.getElementById("dashboard-grid").removeAttribute("style")
		document.getElementById("dashboard-side-menu").removeAttribute("style")
		document.getElementById("dashboard-header-menu").removeAttribute("style")
		document.getElementById("dashboard-content").removeAttribute("style")

	} else {
		document.getElementById("dashboard-grid").style = "grid-template-columns: 100%;"
		document.getElementById("dashboard-side-menu").style = "display: none;"
		document.getElementById("dashboard-header-menu").style="grid-column-start: 1; grid-column-end: 2;"
		document.getElementById("dashboard-content").style = "grid-column-start: 1; grid-column-end: 2;"
	}
	
}

// Function for logging out when clicking logout button
function onClickLogoutButton() {
	window.location.href = "/logout"
}

// Get used storage space from server
function getUsedStorageSpaceRequest() {
	return fetch("/api?data=storage_used", {
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

// Get unused storage space from server
function getStorageSpaceRequest() {
	return fetch("/api?data=storage_space", {
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
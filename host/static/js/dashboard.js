// Sets up a charts plugin to show an error message if there's no data to show.
Chart.plugins.register({
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
		var getStorageSpace = new Promise(function(resolve, reject) {
		  let used_storage_space = getUsedStorageSpaceRequest()
		  let unused_storage_space = getUnusedStorageSpaceRequest();
		  let storage_space = [used_storage_space, unused_storage_space] 
		  if (used_storage_space != null) {
		    resolve(storage_space);
		  }
		  else {
		    reject(Error("Didnt get valid storage_space"));
		  }
		});
		getStorageSpace.then((storage_space) => {
			let graphColor
			let graphLabel
			if(storage_space[1] != null) {
				graphColor  = ["#b224ef", "#cccccc"]
				graphLabel = ['Used Storage Space', 'Unused Storage Space']
			} else {
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
					      label: (item, data) => `${data.datasets[item.datasetIndex].data[0]} B`,
					    }
					}
				}
			});
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
	var request = new XMLHttpRequest()
	request.open('GET', '/api?data=storage_used', false)
	request.send(null)
	return JSON.parse(request.response).used
}

// Get unused storage space from server
function getUnusedStorageSpaceRequest() {
	var request = new XMLHttpRequest()
	request.open('GET', '/api?data=storage_unused', false)
	request.send(null)
	return JSON.parse(request.response).unused
}
const drawBarChart = (id) => {

    var canvas = document.getElementById('myBarChart');
    
    Chart.defaults.global.defaultFontSize = 16;

  var dataset1 = {
        label: 'Total Load',
        data: [],
        backgroundColor: '#337ab7',
        borderWidth: 2,
        //yAxisID: "y-axis-second"
  };

  var chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    legend: {
           display: false
    },
    scales: {
      xAxes: [{
        barPercentage: 0.5,
        barThickness: 40,
        maxBarThickness: 50,
        minBarLength: 2,
        gridLines: {
          display: false
            },
          ticks: {
              display: true,
              fontSize:20
          },
     scaleLabel: {
                display: true,
                labelString: "Load",
                fontcolor:"black"

            }
      }],
      yAxes: [{
           //id: "y-axis-second",
            gridLines: {
                display: true
            },
            ticks: {
                display: true,
                fontSize:20,
        	            min:0,
        	            max:800,
        	            stepSize:200
            },
        		scaleLabel: {
                display: true,
                labelString: "Load on taxi way",
                fontcolor:"black"
            }
          }]
        }
	  };

    var date2 = new Date(date);

    var data4 = {
        labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        datasets: [dataset1]
    };

    barChart = new Chart(canvas, {
        type: 'bar',
        data: data4,
        options: chartOptions
    });

    // barChart.canvas.parentNode.style.width = '1000px';
    barChart.canvas.parentNode.style.height = '400px';

}

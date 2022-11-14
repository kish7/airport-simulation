const drawStateLineChart = (id) => {

    var dataset0 = {
        ...getDatasetCommonSettings("✈# on SFO", "#BEE4BE")
    };
    
   var dataset1 = {
        ...getDatasetCommonSettings("✈# on Taxiway", "#4286f4")
    };

    var dataset2 = {
        ...getDatasetCommonSettings("✈# on Ramp", "#706e68")
    };

    var dataset3 = {
        ...getDatasetCommonSettings("✈# on Pushback", "#FFD700")
    };

    var data = {
        labels: [],
        datasets: [dataset0, dataset1, dataset2, dataset3]
    };

    var options = {
        plugins: {
            tooltip: {
                mode: 'index',
                intersect: false,
                // callbacks: {
                //     label: (item) => item.dataset.label + ': ' +
                //         "hahaaha"
                // }
            }
        }
    }

    const config = {
        type: 'line',
        data,
        options: options
    };

    lineChart = new Chart(
        document.getElementById(id),
        config
    );
};

const drawIdleLineChart = (id) => {
    var dataset1 = {
        ...getDatasetCommonSettings("✈# idle on Taxiway", "#4286f4")
    };

    var dataset2 = {
        ...getDatasetCommonSettings("✈# idle on Ramp", "#706e68")
    };

    var dataset3 = {
        ...getDatasetCommonSettings("✈# idle on Pushback", "#FFD700")
    };

    var data = {
        labels: [],
        datasets: [dataset1, dataset2, dataset3]
    };

    var options = {
        plugins: {
            tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: (item) => item.dataset.label + ': ' +
                        item.dataset.details[item.dataIndex]
                }
            }
        }
    }

    const config = {
        type: 'line',
        data,
        options: options
    };

    idleLineChart = new Chart(
        document.getElementById(id),
        config
    );
}

const getDatasetCommonSettings = (label, color) => {
    let datasetSettings = {
        label: label,
        fill: true,
        lineTension: 0.4,
        borderColor: color,
        borderCapStyle: 'butt',
        borderDash: [],
        borderJoinStyle: 'miter',
        pointBorderColor: color,
        pointBackgroundColor: "#fff",
        pointHoverBackgroundColor: color,
        pointHoverBorderColor: color,
        pointHoverBorderWidth: 2,
        borderWidth: 3,
        data: [],
        details: []
    }
    return datasetSettings;
}
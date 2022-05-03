var addLoadToMinuteArray = function addLoadToMinuteArray(getStartDate, duration, load, allocation1) {
    var zero = date;
    var end = ultimateDateFormatter(date, 31);
    var minutesSinceBeginning1;
    if ((getStartDate >= zero) && (getStartDate <= end)) { // after zero
        minutesSinceBeginning1 = (getStartDate - zero) / (1000 * 60) - 180;
        for (var i = 0; i < duration; i++) {
            if (minuteLoadBigArmInit[minutesSinceBeginning1 + i] == null) { //  initialize 
                minuteLoadBigArmInit[minutesSinceBeginning1 + i] = new Array(12);
                for (var c = 0; c < 12; c++) {
                    minuteLoadBigArmInit[minutesSinceBeginning1 + i][c] = 0;
                }
            }
            minuteLoadBigArmInit[minutesSinceBeginning1 + i][allocation1] += load; // load/duration; 
        }
    }
};

var calculateSTD = function calculateSTD(currentMinute, minutesSinceBeginning) { // after addLoadToMinuteArray
    var array = [];
    for (var i = 0; i < 60; i++) {
        if (minuteLoadBigArmInit[minutesSinceBeginning - i] == null) {
            minuteLoadBigArmInit[minutesSinceBeginning - i] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        }
        for (var c = 0; c < 12; c++) {
            array.push(minuteLoadBigArmInit[minutesSinceBeginning - i][c]); //12*60=720
        }
    }
    if (i < 1440)
        stdBigArmInit.push(math.std(array));
    return math.std(array);
};

var calculateALLSTD = function calculateALLSTD(chart, status) {
    var array = [];
    var array2 = [];
    for (var i = 0; i < 1440; i++) {
        var temp = [];
        var temp2 = [];
        for (var j = 0; j < 45; j++) { //window
            if (minuteLoadBigArmInit[i + j] == null) {
                for (var k = 0; k < 12; k++) {
                    temp.push(0);
                }
            } else {
                $.each(minuteLoadBigArmInit[i + j], function (key, value) {
                    temp.push(value);
                });
            }
            if (temp_minuteLoadBigArmInit[i + j] == null) {
                for (var p = 0; p < 12; p++) {
                    temp2.push(0);
                }
            } else {
                $.each(temp_minuteLoadBigArmInit[i + j], function (key, value) {
                    temp2.push(value);
                });
            }

        }
        array.push(math.std(temp));
        array2.push(math.std(temp2));
    }
    if (chart == 1) {
        lineChart.data.datasets[0].data = array;
        lineChart.update();
    }
    return array;
}

const updateLineChart = (oldIndex, index, response) => {
    // indicating that the simulator has len(new_states) ticks since the last time this data is retrieved
    let newStates = response["new_states"];
    for (let i = oldIndex; i < index; i++) {
        let totalCount = newStates[i - oldIndex]["stats"].total;
        let taxi = newStates[i - oldIndex]["stats"].taxi;
        let ramp = newStates[i - oldIndex]["stats"].ramp;
        let pushback = newStates[i - oldIndex]["stats"].pushback;
        lineChart.data.labels[i] = newStates[i - oldIndex]["time"]
        lineChart.data.datasets[0].data[i] = totalCount;
        lineChart.data.datasets[1].data[i] = taxi;
        lineChart.data.datasets[2].data[i] = ramp;
        lineChart.data.datasets[3].data[i] = pushback;

        let idleAircrafts = JSON.parse(newStates[i - oldIndex]["stats"].idle_aircrafts);
        
        idleLineChart.data.labels[i] = newStates[i - oldIndex]["time"]
        if(idleAircrafts && idleAircrafts != undefined && Object.keys(idleAircrafts).length != 0){
            console.log(idleAircrafts['taxi']); //
            if(idleAircrafts['taxi'] != undefined){
                idleLineChart.data.datasets[0].data[i] =  Object.keys(idleAircrafts['taxi']).length;
                idleLineChart.data.datasets[0].details[i] = JSON.stringify(idleAircrafts['taxi'])
               
            }
            if(idleAircrafts['ramp'] != undefined){
                idleLineChart.data.datasets[0].data[i] =  Object.keys(idleAircrafts['ramp']).length;
                idleLineChart.data.datasets[0].details[i] = JSON.stringify(idleAircrafts['ramp'])
               
            }
            if(idleAircrafts['pushback'] != undefined){
                idleLineChart.data.datasets[0].data[i] =  Object.keys(idleAircrafts['pushback']).length;
                idleLineChart.data.datasets[0].details[i] = JSON.stringify(idleAircrafts['pushback'])
               
            }
        } else{
            idleLineChart.data.datasets[0].data[i] = 0
            idleLineChart.data.datasets[1].data[i] = 0
            idleLineChart.data.datasets[2].data[i] = 0
        }
        
    }
    lineChart.update();
    idleLineChart.update();
}

const updateBarChart = function updateBarChart(currentDate) {
    var zero = date;
    var minutesSinceBeginning = 0;
    if (currentDate >= zero) {
        minutesSinceBeginning = (currentDate - zero) / (1000 * 60) - 180;
    }
    for (var g = 0; g < 12; g++) {
        if (minuteLoadBigArmInit[minutesSinceBeginning] != undefined) {
            barChart.data.datasets[0].data[g] = minuteLoadBigArmInit[minutesSinceBeginning][g];
        } else {
            alert("No Data in DB, please check.")
            barChart.data.datasets[0].data[g] = 0;
        }

    }
    barChart.update();
}
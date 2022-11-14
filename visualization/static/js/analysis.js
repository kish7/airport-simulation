let lineChart;
let idleLineChart;
let barChart;
let interval;
let index = 0;
let states = [];

// drawBarChart();
drawStateLineChart('state-line-chart');
drawIdleLineChart('idle-line-chart');

/*
click on simulation button
*/
$('#analysis_start').click(()=>{
    console.log("analysis_start clicked");
    let modeAndPlan = getModeAndPlan();
    let plan = modeAndPlan[1];
    this.dataConnector = new AnalysisDataConnector(plan, null) // no callback

    interval = setInterval(function(){ 
        // call static function
        AnalysisDataConnector.loadStates("2022-04-29", plan, index).then(response => {
            console.log(response);
            let oldIndex = index;
            index = response["new_index"];
            if(response["updated"]) {
                states.push(...response["new_states"]);
                updateLineChart(oldIndex, index, response);
            }
        });
    }, AUTO_RUN_INTERVAL * 2); 
});


/*
click on simulation button
*/
$('#analysis_end').click(()=>{
    console.log("analysis_end clicked");
    clearInterval(interval);
    console.log(states);
});


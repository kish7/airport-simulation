"use strict";

const getModeAndPlan = () => {
    let params = [], hash;
    let hashes = window.location.href
        .slice(window.location.href.indexOf("?") + 1)
        .split("&");
    for (var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split("=");
        params.push(hash[0]);
        params[hash[0]] = hash[1];
    }

    if (!("plan" in params)) {
        alert("Plan missing.");
        throw "Plan missing.";
    }

    // default mode: batch
    const mode = ("mode" in params) ? params["mode"] : "batch";
    const plan = params["plan"];

    return [mode, plan];
};

function startVisualization() {
    new VisualizationView(getModeAndPlan());
}

class VisualizationView {
    constructor(modeAndPlan) {
        this.mapView = new MapView(document.getElementById("map"));
        this.mode = modeAndPlan[0];
        this.plan = modeAndPlan[1];

        this.initComponents();
        this.initDataSource();
    }

    initDataSource() {
        this.dataConnector = (this.mode === "batch") ?
            new BatchDataConnector(this.plan, this.initSurfaceData.bind(this)) :
            new StreamingDataConnector(this.plan, this.initSurfaceData.bind(this));
    }

    initSurfaceData() {
        // Set airport as the map center
        const surfaceData = this.dataConnector.getSurfaceData();
        const center = surfaceData["airport_center"];
        this.mapView.init(center["lat"], center["lng"]);

        // Gate
        for (let gate of surfaceData["gates"]) {
            const name = "GATE: " + gate["name"];
            this.mapView.drawGate(gate["lat"], gate["lng"], name);
        }

        // Spot
        for (let spot of surfaceData["spots"]) {
            const name = "SPOT POSITION: " + spot["name"];
            this.mapView.drawSpot(spot["lat"], spot["lng"], name);
        }

        // Runway
        for (let runway of surfaceData["runways"]) {
            this.mapView.drawRunway(parseNodes(runway["nodes"]));
        }

        // Pushback way
        for (let pushback_way of surfaceData["pushback_ways"]) {
            this.mapView.drawPushbackWay(parseNodes(pushback_way["nodes"]));
        }

        // Taxiway
        for (let taxiway of surfaceData["taxiways"]) {
            this.mapView.drawTaxiway(parseNodes(taxiway["nodes"]));
        }

        const initState = this.dataConnector.currentState();
        this.handleStateUpdate(initState);
    }

    initComponents() {
        $("#auto").click(e => {
            console.log("auto");
            e.preventDefault();
            toggleAutoRun();
        });

        $("#prev").click(e => {
            e.preventDefault();
            const state = this.dataConnector.prevState();
            this.handleStateUpdate(state);
        });

        $("#next").click(e => {
            e.preventDefault();
            const state = this.dataConnector.nextState();
            this.handleStateUpdate(state);
        });
    }

    handleStateUpdate(state) {
        $("#current-time").text(state["time"]);

        let allAircraft = [];
        for (let aircraft of state["aircrafts"]) {
            allAircraft.push({
                lat: aircraft["location"]["lat"],
                lng: aircraft["location"]["lng"],
                status: "moving", // TODO
                name: aircraft["callsign"]
            });
        }
        this.mapView.updateAllAircraft(allAircraft);
    }
}

/* Controllers */
var autoRunWorker = null;
var pauseTime = 500;

function toggleAutoRun() {

    if (autoRunWorker) {
        clearInterval(autoRunWorker);
        setAutoRunShow(false);
        autoRunWorker = null;
    } else {
        autoRunWorker = window.setInterval(function () {
            nextState();
        }, pauseTime);
        setAutoRunShow(true);
    }

}


function parseNodes(rawNodes) {
    var nodes = [];
    for (let node of rawNodes) {
        nodes.push({"lat": node[1], "lng": node[0]});
    }
    return nodes;
}


function parseAircraftContent(aircraft) {
    var html = aircraft["callsign"] + "</br>";
    if (aircraft["itinerary"] == null) {
        return html + "No itinerary";
    }
    html += "<table><tr><th>Target</th><th>LatLng</th><th>UC</th><th>SC</th></tr>";
    var index = aircraft["itinerary_index"];
    var uc_delay_index = aircraft["uncertainty_delayed_index"];
    var sc_delay_index = aircraft["scheduler_delayed_index"];
    var i = 0;
    for (let target of aircraft["itinerary"]) {
        var latlng = target["node_location"]["lat"] + "," +
            target["node_location"]["lng"];
        html += "<tr class=\"" + getTargetClassName(i, index) + "\">";
        html += "<td>" + target["node_name"] + "</td><td>" + latlng + "</td>";
        if ($.inArray(i, uc_delay_index) >= 0) {
            html += "<td>V</td>";
        } else {
            html += "<td>&nbsp;</td>";
        }
        if ($.inArray(i, sc_delay_index) >= 0) {
            html += "<td>V</td>";
        } else {
            html += "<td>&nbsp;</td>";
        }
        html += "</tr>";
        i += 1;
    }
    html += "</table>";
    return html;
}

function getTargetClassName(current_index, index) {
    if (current_index < index) {
        return "past-target";
    } else if (current_index == index) {
        return "current-target";
    }
    return "future-target";
}
let rooms = [];

let viewBoxTryCounter = 0;

function tryViewBox(maxTries, viewBoxDimensions) {
    if (viewBoxTryCounter < maxTries) {
        viewBoxTryCounter++;
        $.ajax({
            dataType: "json",
            url: "/getViewBox",
            data: {
                min_x: viewBoxDimensions[0],
                min_y: viewBoxDimensions[1],
                width: viewBoxDimensions[2],
                height: viewBoxDimensions[3]
            },
            async: true,
            type: 'GET'
        }).done(json => {
            if (json.width !== viewBoxDimensions[2] && json.height !== viewBoxDimensions[3])
                tryViewBox();   // It got the wrong values, retry
        }).fail(() => {
            tryViewBox();
        });
    } else {
        document.getElementById("errors").innerHTML += "<br />Sorry, but an internal error has occurred whilst getting SVG ViewBox data. Please try again later..."
    }
}

let initTryCounter = 0;

function init(maxTries) {
    initTryCounter++;

    if (initTryCounter < maxTries) {
        $.ajax({
            dataType: "json",
            url: "/init",
            data: {},
            async: true,
        }).done(json => {
            if (json.status !== 'Ok!')
                init();   // It failed somewhere, retry
        }).fail(() => {
            init();
        });
    } else {
        document.getElementById("errors").innerHTML += "<br />Sorry, but an internal error has occurred whilst starting up. Please try again later..."

    }
}

function getAllData(floor) {

    $.ajax({
        dataType: "json",
        url: "/getAllData",
        data: {"floor": floor},
        async: false,
    }).fail(() => {
        document.getElementById("errors").innerHTML += "<br />Sorry, but an internal error has occurred whilst getting data. Please try again later...";
    }).done((data) => {
        rooms = data.rooms;
    });

}

function getRooms() {
    return rooms;
}

let currentRoomInfo = [];

function getRoomInfo(room) {
    // [[topLeftX, topLeftY, bottomLeftX, bottomLeftY, bottomLeftX, bottomLeftY, topRightX, topRightY] (All as a % of the width or height), color (Do it later), temperature, units]
    $.ajax({
        dataType: "json",
        url: "/getData",
        data: {"room": room},
        async: false,
    }).done(json => {
        if (json.status === "Ok!") {
            currentRoomInfo = [json.coords, json.measure, json.units]
        }
        else {
            document.getElementById("errors").innerHTML += `<br />Sorry, but an internal error has occurred whilst getting data for room ${room}. Please try again later...`;
        }
    }).fail(() => {
        document.getElementById("errors").innerHTML += `<br />Sorry, but an internal error has occurred whilst getting data for room ${room}. Please try again later...`;
    });
}

function getCurrentRoomInfo() {
    return currentRoomInfo;
}
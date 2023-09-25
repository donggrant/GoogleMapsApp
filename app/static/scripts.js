function displayResult(resultText) {
    $("#result").html(resultText);
}

function displayErrorMessage(errorMessage) {
    $("#error-message").text(errorMessage).show();
}

function execute() {
    $("#error-message").hide();
    let action = $("#conversionType").val();
    let input = $("#input").val().trim();
    let payload = { "action": action, "input": input };

    if (!input) {
        displayErrorMessage("Please provide input.");
        return;
    }

    if (action === "addressToLatLng") {
        convertAddressToLatLng(payload);
    } else if (action === "latLngToAddress") {
        if (!input.includes(',')) {
            displayErrorMessage("Please provide a valid Lat-Lng pair separated by a comma.");
            return;
        }
        let [lat, lng] = input.split(",");
        payload["lat"] = parseFloat(lat.trim());
        payload["lng"] = parseFloat(lng.trim());
        convertLatLngToAddress(payload);
    } else if (action === "getBoundingBox") {
        convertBoundingBox(payload);
    }
}

function convertAddressToLatLng(payload) {
    $.ajax({
        url: "/convert",
        type: "POST",
        data: JSON.stringify(payload),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            displayResult("Coordinates: Latitude = " + data.lat + ", Longitude = " + data.lng);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            let errorMessage = "An error occurred: ";
            if (jqXHR.responseJSON && jqXHR.responseJSON.error) {
                errorMessage += jqXHR.responseJSON.error;
            } else {
                errorMessage += textStatus;
            }
            displayErrorMessage(errorMessage);
        }
    });
}

function convertLatLngToAddress(payload) {
    $.ajax({
        url: "/convert",
        type: "POST",
        data: JSON.stringify(payload),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            displayResult("Address: " + data.address);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            let errorMessage = "An error occurred: ";
            if (jqXHR.responseJSON && jqXHR.responseJSON.error) {
                errorMessage += jqXHR.responseJSON.error;
            } else {
                errorMessage += textStatus;
            }
            displayErrorMessage(errorMessage);
        }
    });
}

function convertBoundingBox(payload) {
    $.ajax({
        url: "/bounding_box",
        type: "POST",
        data: JSON.stringify(payload),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            let grid = getGridFromBox(data.NORTHEAST_LAT, data.NORTHEAST_LNG, data.SOUTHWEST_LAT, data.SOUTHWEST_LNG, 5);
            displayResult(
                `Bounding Box: Northeast Lat = ${data.NORTHEAST_LAT}, 
                Northeast Lng = ${data.NORTHEAST_LNG}, 
                Southwest Lat = ${data.SOUTHWEST_LAT}, 
                Southwest Lng = ${data.SOUTHWEST_LNG}\n\n${grid}`
            );
        },
        error: function (jqXHR, textStatus, errorThrown) {
            let errorMessage = "An error occurred: ";
            if (jqXHR.responseJSON && jqXHR.responseJSON.error) {
                errorMessage += jqXHR.responseJSON.error;
            } else {
                errorMessage += textStatus;
            }
            displayErrorMessage(errorMessage);
        }
    });
}

function getGridFromBox(NORTHEAST_LAT, NORTHEAST_LNG, SOUTHWEST_LAT, SOUTHWEST_LNG, DESIRED_GRID_LENGTH) {
    let output = '';
    let epsilon = 0.0000001;
    let intermediate_grid_length = DESIRED_GRID_LENGTH - 1;
    let lat_step_size = ( NORTHEAST_LAT - SOUTHWEST_LAT ) / intermediate_grid_length;
    let lng_step_size = ( NORTHEAST_LNG - SOUTHWEST_LNG ) / intermediate_grid_length;

    for (let lat = SOUTHWEST_LAT; lat <= NORTHEAST_LAT + epsilon; lat += lat_step_size) {
        for (let lng = SOUTHWEST_LNG; lng <= NORTHEAST_LNG + epsilon; lng += lng_step_size) {
            output += lat + ',' + lng + '\n';
        }
    }
    return output;
}
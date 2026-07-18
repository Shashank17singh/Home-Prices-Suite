function getBathValue() {
  var uiBathrooms = document.getElementsByName("uiBathrooms");
  for (var i = 0; i < uiBathrooms.length; i++) {
    if (uiBathrooms[i].checked) {
      return i + 1;
    }
  }
  return -1; // Invalid Value
}

function getBHKValue() {
  var uiBHK = document.getElementsByName("uiBHK");
  for (var i = 0; i < uiBHK.length; i++) {
    if (uiBHK[i].checked) {
      return i + 1;
    }
  }
  return -1; // Invalid Value
}

function onClickedEstimatePrice() {
  console.log("Estimate price button clicked");
  
  var sqft = document.getElementById("uiSqft");
  var bhk = getBHKValue();
  var bathrooms = getBathValue();
  var location = document.getElementById("uiLocations");
  var estPrice = document.getElementById("uiEstimatedPrice");

  // Basic Validation
  if (!sqft || !location || !estPrice) {
    console.error("Required UI elements are missing.");
    return;
  }

  var url = "/api/predict_home_price"; 

  $.post(url, {
    total_sqft: parseFloat(sqft.value),
    bhk: bhk,
    bath: bathrooms,
    location: location.value
  }, function(data, status) {
    console.log(data.estimated_price);
    var fullRupees = Math.round(data.estimated_price * 100000);
    
    // Using &#8377; ensures the Rupee symbol renders correctly
    estPrice.innerHTML = "<h2>&#8377; " + fullRupees.toLocaleString('en-IN') + "</h2>";
  });
}

function onPageLoad() {
  console.log("document loaded");
  var url = "/api/get_location_names"; 
  
  $.get(url, function(data, status) {
    console.log("got response for get_location_names");
    if (data && data.locations) {
      var locations = data.locations;
      var uiLocations = $('#uiLocations');
      uiLocations.empty();
      
      for (var i = 0; i < locations.length; i++) {
        var opt = new Option(locations[i], locations[i]);
        uiLocations.append(opt);
      }
    }
  });
}

window.onload = onPageLoad;

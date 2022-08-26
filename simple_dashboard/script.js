celsius = `&#8451;`

function load(data, div_id, group_key, value_key, html_suffix) {
  console.log("data")
  console.log(data)
  console.log(data[0]['sensehat'])
  const temp_div = document.getElementById(div_id);
  temp_div.innerHTML = data[0][group_key][value_key]+html_suffix;
}

function update() {
  console.log("updating")

  var request = new XMLHttpRequest();
  request.open("GET","data.json",false);
  request.send(null)
  var json_data = JSON.parse(request.responseText);

  //Raum
  load(json_data, 'Temperatur_sensor','sensehat','Temperatur_sensor',celsius);

  //pyweather
  load(json_data, 'Temperatur_pyweather','pyweather','Temperatur',celsius);
  load(json_data,'Ort','pyweather','location',"");

}

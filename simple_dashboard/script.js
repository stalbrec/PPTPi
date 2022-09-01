celsius = `&#8451;`

function load(data, div_id, group_key, value_key, html_suffix) {
  console.log("data")
  console.log(data)
  console.log(data[0]['sense_hat'])
  const temp_div = document.getElementById(div_id);
  console.log(temp_div);
  if(temp_div){
  temp_div.innerHTML = data[0][group_key][value_key]+html_suffix;
  }
}

function update() {
  console.log("updating")

  update_online();
  update_raum();
}

function update_raum() {
  
  var request = new XMLHttpRequest();
  request.open("GET","WetterstationI_current_records.json",false);
  request.send(null)
  var json_data = JSON.parse(request.responseText);
  //sensor
  load(json_data, 'Temperatur_sensor','sense_hat','Temperatur_sensor',celsius);
  load(json_data, 'rel_Luftfeuchtigkeit','sense_hat','rel_Luftfeuchtigkeit',"% relative Luftfeuchtigkeit");
  }

function update_online() {
  
  var request = new XMLHttpRequest();
  request.open("GET","WetterstationI_current_records.json",false);
  request.send(null)
  var json_data = JSON.parse(request.responseText);
  //pyweather
  load(json_data, 'Temperatur_pyweather','pyweather','Temperatur',celsius);
  //load(json_data,'Ort','pyweather','location',"");  
  load(json_data, 'rel_Luftfeuchtigkeit_py', 'pyweather', 'rel_Luftfeuchtigkeit_py', "% relative Luftfeuchtigkeit");
  }

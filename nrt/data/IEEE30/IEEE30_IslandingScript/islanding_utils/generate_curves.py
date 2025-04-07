import pandas as pd

def concat_csv(file_path1, file_path2, csv_path):
  df1 = pd.read_csv(file_path1, sep=';', engine = "python")
  df2 = pd.read_csv(file_path2, sep=';', engine = "python")

  colonnes_communes = [col for col in df2.columns if col in df1.columns]
  df1_filtre = df1[colonnes_communes]


  resultat = pd.concat([ df1_filtre, df2])

  resultat = resultat.loc[:, ~resultat.columns.str.contains('^Unnamed')]
  resultat.to_csv(csv_path, sep=';', index=False)


def csv_to_js(csv_path, js_path):

    df = pd.read_csv(csv_path, sep=';')
    
    js_content = """
var datasRead = [];
var colors = ["#0000CC","#FF0000","#FF9900","#9900FF","#6600FF","#000000"];
var colorUsed = [false,false,false,false,false,false];

// Fonction pour créer les checkboxes
function createCheckboxes() {
    var el = document.getElementById('checkbox');
    el.innerHTML = '';
    
    var table = document.createElement('table');
    table.style.width = '100%';
    table.style.margin = '20px 0';
    
    var headers = document.createElement('tr');
    headers.innerHTML = '<th style="text-align:center">Left</th><th>Curve</th><th style="text-align:center">Right</th>';
    table.appendChild(headers);
    
    for (var i=0; i<datasRead.length; i++) {
        var line = document.createElement("tr");
        
        var leftBox = '<td style="text-align:center"><input type="checkbox" name="choice" onclick="listenCheckbox(this,1)" id="'+datasRead[i].label+'"/></td>';
        var label = '<td style="padding:0 10px"><label for="'+datasRead[i].label+'">'+datasRead[i].label+'</label></td>';
        var rightBox = '<td style="text-align:center"><input type="checkbox" name="choice" onclick="listenCheckbox(this,2)" id="'+datasRead[i].label+'"/></td>';
        
        line.innerHTML = leftBox + label + rightBox;
        table.appendChild(line);
    }
    
    el.appendChild(table);
}

$(function () {
"""

    # Génération des données
    for column in df.columns:
        if column != 'time':
            js_content += f"    var {column} = [];\n"
            for index, row in df.iterrows():
                time = row['time']
                value = row[column]
                js_content += f"    {column}.push([{time}, {value}]);\n"

    # Création du tableau datasRead
    js_content += "\n    datasRead = [\n"
    for column in df.columns:
        if column != 'time':
            js_content += f"        {{ label: \"{column}\", data: {column} }},\n"
    js_content = js_content[:-2] + "\n    ];\n\n"

    # Suite du code
    js_content += """
    // Initialisation
    createCheckboxes();
    resetGraph();
    
    // Titre
    document.getElementById('case_title').innerHTML = '<h1>curves.csv</h1>';
    
    // Sélection automatique de la première courbe
    if(datasRead.length > 0) {
        var firstCheckbox = document.getElementById(datasRead[0].label);
        if(firstCheckbox) {
            firstCheckbox.checked = true;
            listenCheckbox(firstCheckbox, 1);
        }
    }
});

  var eltitle = document.getElementById('case_title');
  // remove old children
  eltitle.innerHTML='';
  var titleHtml="<h1>curves.csv</h1>";
  var line = document.createElement("LABEL");
  eltitle.appendChild(line);
  var frag = document.createElement('div');
  frag.innerHTML = titleHtml;
  line.appendChild(frag);

  updateLegend();
    });

function listenCheckbox(button,yAxis)
{
    var id = button.getAttribute("id");
    var instanceId = '';
    if (yAxis == 1)
    {
        instanceId = id + ' on left axis';
    }
    else if (yAxis == 2)
    {
        instanceId = id + ' on right axis';
    }
    else
    {
        alert("Unknown axis");
        button.checked = false;
    }
    var checked= button.checked;
    if( checked == true ) { // add serie
      var serie=[];
      var index = 0;
      for( var i=0; i< datasRead.length; i++) {
          if( datasRead[i].label == id)    {
              index = i;
              break;
          }
      }
      if(dataId.length > 5) {
          alert("Unable to plot more than 6 curves");
          button.checked = false;
      }
      else {
          serie=datasRead[index].data;
          addData(serie,instanceId,yAxis);
      }
    }
    if( checked == false ) { // remove serie
      removeData(instanceId);
    }

}

function addData(serie,id,yAxis) {
  dataId.push(id);
  // search the first color not used
  var indexColor = 0;
  for(var i=0; i<colors.length; i++) {
    if(colorUsed[i] == false) {
      indexColor = i;
      break;
    }
  }
  colorUsed[indexColor] = true;

  dataToPlot.push(
    {
      label: id,
        yaxis: yAxis,
        data : serie,
        color: colors[indexColor],
        points: { show: false }
    }
    );
  plotData();
  updateLegend();
}

function removeData(id)
{
  var index = 0;
  for( var i=0; i< dataId.length; i++) {
    if(dataId[i] == id) {
      index = i;
      break;
    }
  }
  // find the color used to refresh the colorUsed table
  var indexColor =0;
  for(var i=0; i<colors.length; i++) {
    if(dataToPlot[index].color ==colors[i]) {
      indexColor = i;
    }
  }
  colorUsed[indexColor] = false;

  dataId.splice(index,1);
  dataToPlot.splice(index,1);
  plotData();
  updateLegend();
}


function plotData()
{
  var  placeholder = $("#placeholder");
  plot = $.plot(placeholder, dataToPlot, oldOptions);
}


function updateLegend()
{
  var  legend = document.getElementById("legend");
  legend.innerHTML='';
  var table = document.createElement('table');
  legend.appendChild(table);
  for(var i=0; i<dataToPlot.length; i++){
    var line = document.createElement("tr");
    table.appendChild(line);
    var legendHtml= '<td><div style="width:4px;height:0;border:4px solid ' + dataToPlot[i].color + ';overflow:hidden"></div></td><td>'+ dataToPlot[i].label+'</td>';
    line.innerHTML = legendHtml;
  }
  for(var i=dataToPlot.length; i<7; i++)    {
    var line = document.createElement("tr");
    table.appendChild(line);
    var legendHtml= '<td><div style="width:4px;height:0;border:4px solid #FFFFFF;overflow:hidden"></div></td><td></td>';
    line.innerHTML = legendHtml;
  }

}

function resetGraph()
{
  // remove old curve
  var  placeholder = $("#placeholder");
  dataToPlot = [];
  plot =  $.plot(placeholder, dataToPlot, oldOptions);
  dataId= [];
  colorUsed =[false,false,false,false,false,false];
  var el = document.getElementById('checkbox');
  // remove old children
  el.innerHTML='';
  // Create table for curves selections
  var table = document.createElement('table');
  el.appendChild(table);
  var headers = document.createElement('tr');
  headers.innerHTML = '<th>Left axis</th><th>Curves available</th><th>Right axis</th>';
  table.appendChild(headers);
  // set new children
  for (var i=0; i<datasRead.length; i++) {
    var line = document.createElement("tr");
    table.appendChild(line);

    var radioHtml = '<td style="text-align:center"><input type="checkbox" name="choice" onclick="listenCheckbox(this,1)" id="'+datasRead[i].label+'"/></td><td><label>'+datasRead[i].label+'</label></td><td style="text-align:center"><input type="checkbox" name="choice" onclick="listenCheckbox(this,2)" id="'+datasRead[i].label+'"/></td>';
    line.innerHTML =  radioHtml;
  }

  var  legend = document.getElementById("legend");
  legend.innerHTML='';
}
"""
    
    with open(js_path, 'w') as f:
        f.write(js_content)


def change_js_filename(html_file_path, new_html_path, new_js_filename):
    
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    updated_content = html_content.replace(
        '<script language="javascript" type="text/javascript" src="curves.js"></script>',
        f'<script language="javascript" type="text/javascript" src="{new_js_filename}"></script>'
    )
    
    with open(new_html_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

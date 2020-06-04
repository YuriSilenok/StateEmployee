//xml
var xmlDoc = document.implementation.createDocument(null, "gendocs"),
gendocXML = xmlDoc.getElementsByTagName('gendocs')[0],
instanceXML = gendocXML.appendChild(xmlDoc.createElement("instance")),
imageXML = instanceXML.appendChild(xmlDoc.createElement("image")),
tableXML = instanceXML.appendChild(xmlDoc.createElement("table")),
//html
sidebarDIV = document.getElementById('sidebar'),
sheetsDIV = document.getElementById('sheets'),
columnsDIV = document.getElementById('columns');
//functions
var data_table = null,
canvas = null;
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('file_img').addEventListener("change", file_img_input_change,false);
    document.getElementById('file_table').addEventListener("change", file_table_input_change,false);
});
function file_img_input_change(event){
    console.log(event);
    if (this.files && this.files[0]) {
        imageXML.setAttribute('name',this.files[0].name)
        var reader = new FileReader();
        reader.onload = file_img_input_change_reader_onload;
        reader.onerror = onerror;
        reader.readAsDataURL(this.files[0]);
    }
}
function file_img_input_change_reader_onload(event){
    console.log(event);
    canvas = document.getElementById('img'),
    context = canvas.getContext('2d'),
    img = new Image();
    img.onload = file_img_input_change_reader_onload_img_onload;
    img.src = event.target.result;
}
function file_img_input_change_reader_onload_img_onload(event){
    console.log(event);
    canvas.width = document.getElementById('content').clientWidth - 35;
    canvas.height = img.height * canvas.width / img.width;
    context.drawImage(img, 0, 0, canvas.width, canvas.height);
    canvas.style.display = "block"
}
function onerror(event){
    console.log(event);
}
function file_table_input_change(event){
    console.log(event);
    if (input.files && input.files[0]) {
        tableXML.setAttribute('name',input.files[0].name)
        var reader = new FileReader();
        reader.onload = file_table_input_change_reader_onload;
        reader.onerror = onerror;
        reader.readAsBinaryString(input.files[0]);
    }  
}
function file_table_input_change_reader_onload(event){
    data_table = event.target.result
    var workbook = XLSX.read(data_table,{type: 'binary'}),
    sheetsDIV = document.getElementById('sheets');
    sheetsDIV.innerHTML = 'Листы';
    workbook.SheetNames.forEach(function(sheetName) {
        var sheetINPUT = document.createElement('input');
        sheetINPUT.setAttribute('name','sheet');
        sheetINPUT.setAttribute('type','radio');
        var sheetDIV = document.createElement('div');
        sheetDIV.append(sheetINPUT);
        sheetDIV.innerHTML = sheetDIV.innerHTML + sheetName;
        sheetsDIV.append(sheetDIV);
    });
    sheetsDIV.addEventListener("change",function(){
        var sheetsDIV = document.evaluate('./div',document.getElementById('sheets'), null,XPathResult.ANY_TYPE,null),
        sheetDIV = sheetsDIV.iterateNext();
        while(sheetDIV){
            if(sheetDIV.childNodes[0].checked == true){
                var sheetName = sheetDIV.childNodes[1].textContent,
                workbook = XLSX.read(data_table,{type: 'binary'}),
                sheet = workbook.Sheets[sheetName]
                col = 0,
                cell = sheet[String.fromCharCode(65+col)+1],
                textesXML = tableXML.getElementsByTagName('text');
                for(var i=0; i< textesXML.length; i++){
                    tableXML.removeChild(textesXML[i]);
                }
                tableXML.setAttribute('sheet',sheetName);
                var columnsDIV = document.getElementById('columns');
                columnsDIV.innerHTML = 'Столбцы';
                while(cell){
                    column = cell['v'];
                    col ++;
                    cell = sheet[String.fromCharCode(65+col) + 1];
                    var columnINPUT = document.createElement('input');
                    columnINPUT.setAttribute('name','column');
                    columnINPUT.setAttribute('type','checkbox');
                    var columnDIV = document.createElement('div');
                    columnDIV.append(columnINPUT);
                    columnDIV.innerHTML = columnDIV.innerHTML + column;
                    columnsDIV.append(columnDIV);
                    textXML = xmlDoc.createElement('text');
                    textXML.setAttribute('column',column);
                    tableXML.appendChild(textXML);
                    columnsDIV.addEventListener("change",function(){
                        var columnsDIV = document.evaluate('./div',document.getElementById('columns'), null,XPathResult.ANY_TYPE,null),
                        columnDIV = columnsDIV.iterateNext();
                        while(columnDIV){
                            inp = columnDIV.childNodes[0];
                            if(inp.checked == true){
                                console.log(columnDIV.textContent);
                            }
                            columnDIV = columnsDIV.iterateNext();
                        }
                    });
                }
                break;
            }
            sheetDIV = sheetsDIV.iterateNext();
        }
    });
}
var xmlDoc = document.implementation.createDocument(null, "gendocs");
var gendocXML = xmlDoc.getElementsByTagName('gendocs')[0];
var instanceXML = gendocXML.appendChild(xmlDoc.createElement("instance"));
var imageXML = instanceXML.appendChild(xmlDoc.createElement("image"));
var tableXML = instanceXML.appendChild(xmlDoc.createElement("table"));
document.addEventListener("DOMContentLoaded", DOMContentLoaded, false);
function DOMContentLoaded(event){
    sidebarDIV = document.getElementById('sidebar');
    sheetsDIV = document.getElementById('sheets');
    columnsDIV = document.getElementById('columns');
    fileImgINPUT = document.getElementById('file_img');
    tableDEV = document.getElementById('table');
    fileTableINPUT = document.getElementById('file_table');
    contentDIV = document.getElementById('content');
    imgCANVAS = document.getElementById('img');
    
    fileImgINPUT.addEventListener("change", image_attached, false);
    fileTableINPUT.addEventListener("change", table_attached, false);
    sheetsDIV.addEventListener("change", sheetsDEV_change, false);
    columnsDIV.addEventListener("change", columnsDIV_change, false);
    imgCANVAS.addEventListener("click", click_canvas, false);
}
function click_canvas(event){
    console.log(event);
    
}
function onerror(event){
    console.log(event);
}
function image_attached(event){
    console.log(event);
    if (this.files && this.files[0]) {
        imageXML.setAttribute('name',this.files[0].name)
        var reader = new FileReader();
        reader.onload = image_readed;
        reader.onerror = onerror;
        reader.readAsDataURL(this.files[0]);
    }
}
function image_readed(event){
    console.log(event);
    context = imgCANVAS.getContext('2d');
    img = new Image();
    img.onload = image_onload;
    img.src = event.target.result;
}
function image_onload(event){
    console.log(event);
    imgCANVAS.width = document.getElementById('content').clientWidth - 35;
    imgCANVAS.height = img.height * imgCANVAS.width / img.width;
    context.drawImage(img, 0, 0, imgCANVAS.width, imgCANVAS.height);
    var textes = tableXML.getElementsByTagName('text');
    for(var i = 0; i < textes.length; i++){
        var column = textes[i].attributes.getNamedItem('column').value;
        context.font = "40px serif";
        var x = textes[i].attributes.getNamedItem('x');
        var y = textes[i].attributes.getNamedItem('y');
        if (x == null) x = imgCANVAS.width / 2;
        if (y == null) y = imgCANVAS.height / 2;
        var x = textes[i].attributes.setAttribute('x', x);
        var y = textes[i].attributes.setAttribute('y', y);
        console.log(column,x,y);
        context.fillText(column, x, y);
    }
    fileTableINPUT.removeAttribute("disabled");
}
//file table
function table_attached(event){
    console.log(event);
    if (this.files && this.files[0]) {
        tableXML.setAttribute('name',this.files[0].name)
        var reader = new FileReader();
        reader.onload = table_readed;
        reader.onerror = onerror;
        reader.readAsBinaryString(this.files[0]);
    }  
}
function table_readed(event){
    console.log(event);
    data_table = event.target.result
    var workbook = XLSX.read(data_table,{type: 'binary'}),
    sheetsDIV = document.getElementById('sheets');
    sheetsDIV.innerHTML = 'Листы';
    workbook.SheetNames.forEach(table_readed_forEach);
}
function table_readed_forEach(sheetName){
    console.log(sheetName);
    var sheetINPUT = document.createElement('input');
    sheetINPUT.setAttribute('name','sheet');
    sheetINPUT.setAttribute('type','radio');
    var sheetDIV = document.createElement('div');
    sheetDIV.append(sheetINPUT);
    sheetDIV.innerHTML = sheetDIV.innerHTML + sheetName;
    sheetsDIV.append(sheetDIV);
}
function sheetsDEV_change(event){
    console.log(event);
    var sheetsDIVs = document.evaluate('./div', sheetsDIV, null, XPathResult.ANY_TYPE, null),
    sheetDIV = sheetsDIVs.iterateNext();
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
            }
            break;
        }
        sheetDIV = sheetsDIVs.iterateNext();
    }
}
function columnsDIV_change(event){
    console.log(event);
    var textes = tableXML.getElementsByTagName('text');
    while(textes.length>0){
        tableXML.removeChild(textes[0]);
    }
    var columnsDIV = document.evaluate('./div', document.getElementById('columns'), null,XPathResult.ANY_TYPE, null);
    var columnDIV = columnsDIV.iterateNext();
    while(columnDIV){
        inp = columnDIV.childNodes[0];
        if(inp.checked == true){
            var textXML = xmlDoc.createElement('text');
            textXML.setAttribute('column',columnDIV.textContent);
            tableXML.appendChild(textXML);
        }
        columnDIV = columnsDIV.iterateNext();
    }
    image_onload(event);
}
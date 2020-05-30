function load_img(input){
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var canvas = document.getElementById('img'),
            context = canvas.getContext('2d'),
            img = new Image();
            img.onload = function(){
                canvas.width = document.getElementById('content').clientWidth - 35;
                	canvas.height = img.height * canvas.width / img.width;
                context.drawImage(img,0,0, canvas.width, canvas.height);
                canvas.style.display = "block"
            }
            img.src = e.target.result;
        }
        reader.onerror = function(ex) {console.log(ex);};
        reader.readAsDataURL(input.files[0]);
    }
}
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('file_img').addEventListener("change", function(){load_img(this);},false);
});

function load_table(input){
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            var workbook = XLSX.read(e.target.result,{type: 'binary'});
            var sheetsDEV = document.getElementById('sheets');
            sheetsDEV.innerHTML = '';
            workbook.SheetNames.forEach(function(sheetName) {
                var sheetINPUT = document.createElement('input');
                sheetINPUT.setAttribute('name','sheet');
                sheetINPUT.setAttribute('type','radio');
                var sheetDIV = document.createElement('div');
                sheetDIV.append(sheetINPUT);
                sheetDIV.innerHTML = sheetDIV.innerHTML + sheetName;
                sheetsDEV.append(sheetDIV);
            })
            sheetsDEV.addEventListener("change",function(){
                console.log(this)
            })
        }
        reader.onerror = function(ex) {console.log(ex);};
        reader.readAsBinaryString(input.files[0]);
    }  
}
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('file_table').addEventListener("change", function(){load_table(this);},false);
});
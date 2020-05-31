function load_img(input){
    console.log(input)
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
            console.log('done')
        }
        reader.readAsDataURL(input.files[0]);
    }
}
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('file_img').addEventListener("change", function(){
        load_img(this);
    },false);
});
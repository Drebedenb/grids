function wpguruLink() { //Для добавления источника
    var istS = 'Источник:'; // Слово должно находится в кавычках!
    var copyR = '© оконные-решётки.рф'; // Слово должно находится в кавычках!
    var body_element = document.getElementsByTagName('body')[0];
    var choose = window.getSelection();
    var myLink = document.location.href;
    var authorLink = "<br /><br />" + istS + ' ' + "<a href='" + myLink + "'>" + myLink + "</a><br />" + copyR;
    var copytext = choose + authorLink;
    var addDiv = document.createElement('div');
    addDiv.style.position = 'absolute';
    addDiv.style.left = '-99999px';
    body_element.appendChild(addDiv);
    addDiv.innerHTML = copytext;
    choose.selectAllChildren(addDiv);
    window.setTimeout(function () {
        body_element.removeChild(addDiv);
    }, 0);
}
document.oncopy = wpguruLink;

let img = document.getElementsByTagName('img'); // Для запрета копирования изображения
    for (let i in img) {
        img[i].oncontextmenu = function () {
            return false;
        }
        img[i].ondragstart = function () {
            return false;
        }
    }



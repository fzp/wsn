/**
 * Created by jin-yc10 on 15-4-17.
 */
// OnComplete: 完成时的回调函数，参数是data
function getData(address, onComplete) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            onComplete(xhr.responseText);
        }
    };
    xhr.open('GET', address, true);
    xhr.send(null);
}
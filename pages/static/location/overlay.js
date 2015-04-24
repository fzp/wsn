/**
 * Created by jin-yc10 on 15-4-10.
 */

// 复杂的自定义覆盖物
function NodeOverlay(point, id){
    this._point = point;
    this._id = id;
//    this._overText = mouseoverText;
}

NodeOverlay.prototype = new BMap.Overlay();
NodeOverlay.prototype.initialize = function(map){
    this._map = map;
    var div = this._div = document.createElement("div");
    div.style.position = "absolute";
    div.style.zIndex = BMap.Overlay.getZIndex(this._point.lat);
    div.style.backgroundColor = "#EE5D5B";
    div.style.border = "1px solid #BC3B3A";
    div.style.color = "white";
    div.style.height = "14px";
    div.style.padding = "2px";
    div.style.lineHeight = "10px";
    div.style.whiteSpace = "nowrap";
    div.style.MozUserSelect = "none";
    div.style.fontSize = "8px";
    var span = this._span = document.createElement("span");
    div.appendChild(span);
    span.appendChild(document.createTextNode(this._id));
    var that = this;
    that.__zIndex = div.style.zIndex;

    div.onmouseover = function(){
        this.style.backgroundColor = "#6BADCA";
        this.style.borderColor = "#0000ff";
        this.style.zIndex = 100;
        this.getElementsByTagName("span")[0].innerHTML = that._id;
    };

    div.onmouseout = function(){
        this.style.backgroundColor = "#EE5D5B";
        this.style.borderColor = "#BC3B3A";
        this.style.zIndex = that.__zIndex;
        this.getElementsByTagName("span")[0].innerHTML = that._id;
    };

    map.getPanes().labelPane.appendChild(div);

    return div;
};

NodeOverlay.prototype.draw = function(){
    var map = this._map;
    var pixel = map.pointToOverlayPixel(this._point);
    this._div.style.left = pixel.x + "px";
    this._div.style.top  = pixel.y + "px";
};

NodeOverlay.prototype.recover = function() {
    this._div.style.backgroundColor = "#EE5D5B";
    this._div.style.borderColor = "#BC3B3A";
    this._div.style.zIndex = this.__zIndex;
    this._div.getElementsByTagName("span")[0].innerHTML = this._id;
    this._div.style.height = "14px";
    this._div.style.padding = "2px";
    this._div.style.lineHeight = "10px";
    this._div.style.whiteSpace = "nowrap";
    this._div.style.MozUserSelect = "none";
    this._div.style.fontSize = "8px";
};
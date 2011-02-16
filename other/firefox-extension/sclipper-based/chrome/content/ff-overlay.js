Swaglr.onFirefoxLoad = function(event) {
  document.getElementById("contentAreaContextMenu")
          .addEventListener("popupshowing", function (e){ Swaglr.showFirefoxContextMenu(e); }, false);
};

Swaglr.showFirefoxContextMenu = function(event) {
  // show or hide the menuitem based on what the context menu is on
  //document.getElementById("context-Swaglr").hidden = gContextMenu.onImage;
};

window.addEventListener("load", Swaglr.onFirefoxLoad, false);

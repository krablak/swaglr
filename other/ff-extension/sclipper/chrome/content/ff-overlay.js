sclipper.onFirefoxLoad = function(event) {
  document.getElementById("contentAreaContextMenu")
          .addEventListener("popupshowing", function (e){ sclipper.showFirefoxContextMenu(e); }, false);
};

sclipper.showFirefoxContextMenu = function(event) {
  // show or hide the menuitem based on what the context menu is on
  document.getElementById("context-sclipper").hidden = gContextMenu.onImage;
};

window.addEventListener("load", sclipper.onFirefoxLoad, false);

document.addEventListener("DOMContentLoaded", () => {
  window.tweetHighlighted = () => {
    const settings = {
      node: "<a href='#'>Tweet</a>",
      maxLength: 280,
      extra: "TheThesis.us",
      via: null,
      popupArgs: "width=400,height=400,toolbar=0,location=0",
    };
    let url = "";
    let text = "";
    const shareButton = document.createElement("div");
    shareButton.style.display = "none";
    shareButton.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      window.open(url, "_blank", settings.popupArgs);
    });
    const body = document.querySelector("body");
    body.appendChild(shareButton);
    document.addEventListener("mouseup", (e) => {
      text = getSelectedText();
      //TODO see if we can relocate tthe button if text is rehighlight
      const btnExists = shareButton.style.display !== "none";
      if (btnExists || !text.length) {
        shareButton.style.display = "none"; // destroy the old button
        //} else if (btnExists || text.length) {
        //shareButton.style.display = "none"; // destroy the old button
        //appendShareButton(e); // make a new button
      } else {
        appendShareButton(e);
      }
    });
    //document.addEventListener("click", (e) => {
    //const btnExists = shareButton.style.display !== "none";
    //if (btnExists || !text.length) {
    //return;
    //} else {}
    //});
    const getSelectedText = () => {
      if (window.getSelection) {
        return window.getSelection().toString();
      } else if (document.selection) {
        return document.selection.createRange().text;
      }
      return "";
    };
    const appendShareButton = (e) => {
      url = getTweetURL(text, settings.extra, settings.via);
      shareButton.innerHTML = "";
      shareButton.innerHTML += settings.node;
      shareButton.innerHTML += tweetIcon;
      if (settings.cssClassess && settings.cssClassess.length) {
        shareButton.classList.add(settings.cssClassess);
      }
      shareButton.style.top = `${e.pageY}px`;
      shareButton.style.left = `${e.pageX}px`;
      shareButton.style.position = "absolute";
      shareButton.style.cursor = "pointer";
      shareButton.style.display = "flex";
      shareButton.style.justifyContent = "space-between";
      shareButton.style.alignContent = "center";
      shareButton.style.alignItems = "center";
      shareButton.style.opacity = .95;
      //TODO blur the background eventually
      shareButton.style.fontFamily = "Arial, Helvetica, sans-serif";
      shareButton.style.backgroundColor = "#3898EC";
      shareButton.style.padding = "10px 15px";
      shareButton.style.width = "100px";
      shareButton.style.borderRadius = "5px";
      shareButton.style.color = "white";
      shareButton.firstChild.style.color = "white";
      shareButton.firstChild.style.textDecoration = "none";
      shareButton.lastChild.style.fill = "white";
    };
    const tweetIcon =
      `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"><path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/></svg>`;
    const getTweetURL = function (text, extra, via) {
      let url = "https://twitter.com/intent/tweet?text=";
      const viaUrl = `&via=${via}`;
      const maxLength = settings.maxLength > 280 ? 280 : settings.maxLength;
      const maxAllowedLength = maxLength - viaUrl.length - extra.length;
      let textToTweet = text;
      if (text.length > maxAllowedLength) {
        textToTweet = text.substring(0, maxAllowedLength - 1);
      }
      url += encodeURIComponent(textToTweet);
      if (extra) url += encodeURIComponent(" " + extra);
      if (via) url += viaUrl;
      return url;
    };
  };
  window.tweetHighlighted();
});

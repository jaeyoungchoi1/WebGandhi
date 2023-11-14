function findTextNodes(element) {
  let textNodes = [];
  if (element.nodeType == 3) { // text
    textNodes.push(element);
    console.log(element);
  } else {
    element.childNodes.forEach(child => {
      textNodes = textNodes.concat(findTextNodes(child));
    });
  }
  return textNodes;
}

function sanitizeText(textNode) {
  /*
  chrome.runtime.sendMessage({
    contentScriptQuery: "queryOpenAI",
    text: textNode.nodeValue
  }, response => {
    if (response && response.response) {
      textNode.nodeValue = response.response;
    }
  });
  */
  textNode.nodeValue = "Filtered!!";
}

function startSanitizing() {
  const textNodes = findTextNodes(document.body);
  textNodes.forEach(sanitizeText);
}

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.action == "startSanitizing") {
      startSanitizing();
    }
  }
);
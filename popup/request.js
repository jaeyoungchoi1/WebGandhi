chrome.runtime.sendMessage({
    contentScriptQuery: "queryOpenAI",
    text: "This is a hate speech sentence."
}, response => {
    if (response && response.response) {
        console.log(response.response);
    }
});
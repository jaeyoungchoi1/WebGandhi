document.getElementById('startButton').addEventListener('click', () => {

    const filterType = document.querySelector('input[name="filterType"]:checked').id;
    console.log("selected filter type: "+ filterType);

    if(filterType === 'neutral'){
        chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
            chrome.scripting.executeScript({
                target: {tabId: tabs[0].id},
                files: ['filter_neutral.js']
            });
        });
    }
    else if(filterType === 'pure'){
        chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
            chrome.scripting.executeScript({
                target: {tabId: tabs[0].id},
                files: ['filter_pure.js']
            });
        });
    }
});

document.getElementById('resetButton').addEventListener('click', () => {
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
        chrome.scripting.executeScript({
            target: {tabId: tabs[0].id},
            files: ['reset.js']
        });
    });
});


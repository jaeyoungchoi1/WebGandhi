document.getElementById('startButton').addEventListener('click', () => {
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
        chrome.scripting.executeScript({
            target: {tabId: tabs[0].id},
            files: ['content.js']
        });
    });
});

document.getElementById('resetButton').addEventListener('click', () => {
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
        chrome.scripting.executeScript({
            target: {tabId: tabs[0].id},
            files: ['reset.js']
        });
    });
});

let model;

async function loadModel() {
    model = await tf.loadLayersModel(chrome.runtime.getURL('/model/best_model.json'));
    console.log("모델 로드 완료");
}

loadModel();
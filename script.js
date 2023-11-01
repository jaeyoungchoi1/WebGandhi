document.getElementById('ghandiBtn').addEventListener('click', function() {
    chrome.tabs.executeScript({
        code: 'document.body.innerHTML;'
    }, function(selection) {
        const content = selection[0];

        // OpenAI API 호출 코드
        filterHateWords(content, function(filteredContent) {
            // 웹 페이지 내용을 필터링된 내용으로 업데이트
            chrome.tabs.executeScript({
                code: `document.body.innerHTML = \`${filteredContent}\`;`
            });
        });
    });
});

function filterHateWords(content, callback) {
    // OpenAI API 호출 및 응답 처리 로직
    // ...
    // callback(filteredContent);
}
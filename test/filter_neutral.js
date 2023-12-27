async function callOpenAI(userText) {
    const data = {
        model: "ft:gpt-3.5-turbo-1106:personal::8WEo6lug",
        messages: [
            { role: "system", content: "WebGandhi is a tool for filtering hate speech."},
            { role: "user", content: userText }
        ]
    };

    const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer apikey'
        },
        body: JSON.stringify(data)
    });
    const responseData = await response.json();
    return responseData.choices[0].message.content.trim();
}

async function filterParagraphs() {

    const paragraphs = document.querySelectorAll('.usertxt.ub-word');

    const promises = Array.from(paragraphs).map(async paragraph => {
        // 이미 필터링된 텍스트가 있는지 확인
        if (paragraph.filteredNeutral) {
            return { paragraph, filteredNeutral: paragraph.filteredNeutral };
        }

        const originalText = paragraph.originalText || paragraph.textContent;
        paragraph.originalText = originalText; // 원래 텍스트 저장
        const filteredNeutral = await callOpenAI(originalText);
        paragraph.filteredNeutral = filteredNeutral; // 필터링된 텍스트 저장
        return { paragraph, filteredNeutral };
    });

    const results = await Promise.all(promises);
    results.forEach(({ paragraph, filteredNeutral }) => {
        paragraph.textContent = filteredNeutral;
    });
}

filterParagraphs();
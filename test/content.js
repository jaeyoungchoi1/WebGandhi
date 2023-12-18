async function callOpenAI(userText) {
    const data = {
        model: "ft:gpt-3.5-turbo-1106:personal::8WEo6lug",
        messages: [
            {
                role: "system",
                content: "WebGandhi is a tool for filtering hate speech."
            },
            {
                role: "user",
                content: userText
            }
        ]
    };

    const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer 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' // 여기에 실제 API 키를 입력
        },
        body: JSON.stringify(data)
    });

    const responseData = await response.json();
    return responseData.choices[0].message.content.trim();
}


async function filterParagraphs() {
    const paragraphs = document.querySelectorAll('.usertxt.ub-word');
    for (let paragraph of paragraphs) {
        const originalText = paragraph.textContent;
        paragraph.originalText = originalText; // 원래 텍스트 저장
        const filteredText = await callOpenAI(originalText);
        paragraph.textContent = filteredText;
    }
}

filterParagraphs();
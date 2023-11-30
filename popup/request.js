chrome.runtime.sendMessage({
    contentScriptQuery: "queryOpenAI",
    text: "This is a hate speech sentence."
}, response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
        messages: [{role: 'system', content: promptString}],
        model: 'gpt-3.5-turbo',
    })
}),



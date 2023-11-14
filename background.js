chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.contentScriptQuery == "queryOpenAI") {
      const data = {
        prompt: request.text,
        max_tokens: 60
      };

      fetch('https://api.openai.com/v1/engines/text-davinci-003/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer YOUR_OPENAI_API_KEY' // API 키를 여기에 입력
        },
        body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(data => sendResponse({response: data.choices[0].text}))
      .catch(error => console.error('Error:', error));
      return true; // 이 함수가 비동기로 동작함을 나타냄
    }
  }
);
document.getElementById('saveKeyBtn').addEventListener('click', function() {
  const apiKey = document.getElementById('apiKey').value;
  if (apiKey) {
    chrome.storage.local.set({ 'openAIKey': apiKey }, function() {
      console.log('API Key saved');
      toggleVisibility();
    });
  } else {
    alert('Please enter the API key.');
  }
});

document.getElementById('ghandiBtn').addEventListener('click', function() {
  chrome.storage.local.get('openAIKey', function(data) {
    if (data.openAIKey) {
      // TODO: 사용자가 입력한 API 키를 사용해서 필터링 작업 진행
    } else {
      alert('API key is not set.');
    }
  });
});

function toggleVisibility() {
  const apiKeyForm = document.getElementById('api-key-form');
  const mainContent = document.getElementById('main-content');

  apiKeyForm.style.display = 'none';
  mainContent.style.display = 'block';
}

// 페이지 로드 시 API 키가 저장되어 있으면 메인 콘텐츠를 바로 보여줍니다.
chrome.storage.local.get('openAIKey', function(data) {
  if (data.openAIKey) {
    toggleVisibility();
  }
});
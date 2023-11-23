
document.getElementById('startBtn').addEventListener('click', function() {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {action: "startSanitizing"});
  });
  console.log("start!");

  
});


document.getElementById('startBtn').addEventListener('click', function() {
  // Naver Hyperclova API 요청 설정
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "여기에_API_엔드포인트_URL", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  // 추가적인 헤더 설정이 필요한 경우 여기에 추가

  // 서버로부터 응답을 받을 때 실행될 함수 설정
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // 성공적으로 응답을 받았을 때 수행할 동작
       console.log("Response received: ", this.responseText);
    }
  };

  // API 요청을 위한 데이터 (이 예시에서는 JSON 형식)
  var data = JSON.stringify({
    // 여기에 필요한 데이터 구조에 맞게 작성
  });

  xhr.send(data); // 데이터와 함께 요청 보내기
  console.log("start!");
});

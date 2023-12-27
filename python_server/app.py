from flask import Flask, request, jsonify
import tensorflow as tf
import pickle
import re
from keras.preprocessing.sequence import pad_sequences
import logging
from konlpy.tag import Okt

# Flask 앱 초기화
app = Flask(__name__)

# 모델과 토크나이저 로드
loaded_model = tf.keras.models.load_model('best_model.h5')
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

max_len = 30
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
okt = Okt()

# 예측 함수 정의
def hate_predict(new_sentence):
    new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', new_sentence)
    new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
    score = float(loaded_model.predict(pad_new)) # 예측
    return score

# API 엔드포인트 정의
@app.route('/detecthate', methods=['POST'])
def predict():
    # POST 요청에서 문장을 가져옵니다.
    data = request.get_json()
    app.logger.debug(f"Received POST data: {data}")
    sentence = data['sentence']

    # 예측 수행
    prediction = hate_predict(sentence)

    # 응답 반환
    return jsonify({'prediction': prediction})

# 서버 실행
if __name__ == '__main__':
    app.run(debug=True)

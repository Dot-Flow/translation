from Translate import brl_to_txt as b2t
from Translate import txt_to_brl as t2b
from ContextualErrorCorrection import contextual_error_correction as cec
from FeedbackGeneration import feedback_generator as fg

import json
from flask import Flask, request, jsonify, Response

app = Flask(__name__)


def process_to_text(extracted_json):
    print("Process: translation - to text")
    
    if not isinstance(extracted_json, dict):
        return jsonify({'error': 'Invalid input format'}), 400
    
    extracted_brl = extracted_json['prediction']['brl']
    
    if extracted_brl is None:
        return jsonify({'error': '점자 인식 오류'}), 500
    
    try:
        extracted_json['prediction']['text'] = b2t.translate(extracted_brl)  # 점자 번역 함수
        return extracted_json
    except Exception as e:
        return jsonify({'error': '서버 오류 발생'}), 500

@app.route('/translate/to-text', methods=['POST'])
def translate_to_text():
    extracted_json = process_to_text(request.get_json())
    response = json.dumps({'text': extracted_json['prediction']['text']}, ensure_ascii=False)
    return Response(response, content_type='application/json; charset=utf-8')


def process_correction(extracted_json):
    print("Process: correction")
    
    extracted_text = extracted_json['prediction']['text']
    
    if extracted_text is None:
        return jsonify({'error': '텍스트 추출 오류'}), 500
    
    try:
        extracted_json['correction']['text'] = cec.correct(extracted_text)  # 텍스트 오류 수정 함수
        return extracted_json
    except Exception as e:
        return jsonify({'error': '서버 오류 발생'}), 500

@app.route('/correction', methods=['POST'])
def correction(extracted_json):
    extracted_json = process_correction(extracted_json)
    response = json.dumps({'corrected_text': extracted_json['correction']['text']}, ensure_ascii=False)
    return Response(response, content_type='application/json; charset=utf-8')


def process_to_brl(extracted_json):
    print("Process: translation - to braille")
    
    extracted_text = extracted_json['correction']['text']
    
    if extracted_text is None:
        return jsonify({'error': '텍스트 오류 수정 오류'}), 500
    
    try:
        extracted_json['correction']['brl'] = t2b.translate(extracted_text)  # 텍스트를 점자로 변환 함수
        return extracted_json
    except Exception as e:
        return jsonify({'error': '서버 오류 발생'}), 500
    
@app.route('/translate/to-brl', methods=['POST'])
def translate_to_brl(extracted_json):
    extracted_json = process_to_brl(extracted_json)
    response = json.dumps({'brl': extracted_json['correction']['brl']}, ensure_ascii=False)
    return Response(response, content_type='application/json; charset=utf-8')


def process_feedback_generation(extracted_json):
    print("Process: feedback generation")
    
    try:
        extracted_json = fg.main(extracted_json)  # 피드백 생성 함수
        return extracted_json
    except Exception as e:
        return jsonify({'error': '서버 오류 발생'}), 500
    
@app.route('/feedback/generate', methods=['POST'])
def feedback_generation(extracted_json):
    extracted_json = process_feedback_generation(extracted_json)
    response = json.dumps(extracted_json, ensure_ascii=False)
    return Response(response, content_type='application/json; charset=utf-8')


def process_feedback_loop(extracted_json):
    print("Process: feedback loop")
    
    extracted_json = process_to_text(extracted_json)
    extracted_json = process_correction(extracted_json)
    extracted_json = process_to_brl(extracted_json)
    extracted_json = process_feedback_generation(extracted_json)
    
    return extracted_json

@app.route('/feedback/loop', methods=['POST'])
def feedback_loop():
    extracted_json = request.get_json()
    extracted_json = process_feedback_loop(extracted_json)
    response = json.dumps(extracted_json, ensure_ascii=False)
    return Response(response, content_type='application/json; charset=utf-8')

# curl -X POST -H "Content-Type: application/json" -d @test.json http://127.0.0.1:5000/translate/to-text


if __name__ == '__main__':
    app.run(debug=False)
    
from Translation import brl_to_txt as b2t
from Translation import txt_to_brl as t2b
from ContextualErrorCorrection import contextual_error_correction as cec
from FeedbackGeneration import feedback_generator as fg

import json
from flask import Flask, request, jsonify, Response
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

def process_to_text(request_json):
    print("Process: translation - to text")
    
    if not isinstance(request_json, dict):
        return jsonify({'error': 'Invalid input format'}), 400    
    
    brl_list = request_json['brl']
    
    if brl_list is None:
        return jsonify({'error': '점자 인식 오류'}), 500
    
    try:
        translated_text = b2t.translate(brl_list)  # 점자 번역 함수
        return jsonify({'text': translated_text}), 200
    except Exception as e:
        return jsonify({'error': '서버 오류 발생'}), 500

@app.route('/translate/to-text', methods=['POST'])
def translate_to_text():
    """
    역점역 - 점자 텍스트를 일반 텍스트로 변환합니다.
    ---
    tags:
      - Translation
    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            properties:
                brl:
                    type: array
                    items:
                        type: string
                    description: 점자 문자열의 배열
            example:
                brl:
                - "⠀⠀⠼⠁⠀⠦⠆⠼⠁⠰⠴⠑⠛⠊⠒⠝⠠⠎⠉⠵⠀⠟⠐⠩⠀⠱⠁⠇⠝⠠⠎⠀"
                - "⠫⠰⠕⠫⠀⠑⠗⠍⠀⠋⠵⠀⠕⠨⠕⠃⠓⠪⠀⠇⠶⠚⠻⠀⠑⠛⠨⠐⠮⠐⠀⠀"
    responses:
        200:
            description: 변환된 텍스트를 반환합니다.
            schema:
                type: object
                properties:
                    text:
                        type: array
                        items:
                            type: string
                        description: 변환된 텍스트의 배열
                example:
                    text:
                    - "1 [1]문단에서는 인류 역사에서"
                    - "가치가 매우 큰 이집트 상형 문자를,"
        400:
            description: 잘못된 입력 형식
            schema:
                type: object
                properties:
                    error:
                        type: string
                        description: 오류 메시지
        500:
            description: 서버 오류 발생
            schema:
                type: object
                properties:
                    error:
                        type: string
                        description: 오류 메시지
    """
    return process_to_text(request.get_json())


def process_correction(request_json):
    print("Process: correction")
    
    text_list = request_json['text']
    
    if text_list is None:
        return jsonify({'error': '텍스트 추출 오류'}), 500
    
    try:
        correct_text = cec.correct(text_list)  # 텍스트 오류 수정 함수
        return jsonify({'text': correct_text}), 200
    except Exception as e:
        return jsonify({'error': '서버 오류 발생'}), 500

@app.route('/correction', methods=['POST'])
def correction():
    """
    텍스트 오류 수정 - 텍스트를 외부 api를 사용하여 문맥적 오류를 수정합니다.
    ---
    tags:
      - Correction
    parameters:
        - name: body
          in: body
          required: true
          schema:
            type: object
            properties:
                text:
                    type: array
                    items:
                        type: string
                    description: 텍스트의 배열
            example:
                text:
                - "1 [1]문단에서는 인류 역사에서"
                - "가치가 매우 큰 이집트 상형 문자를,"
    responses:
        200:
            description: 수정된 텍스트를 반환합니다.
            schema:
                type: object
                properties:
                    text:
                        type: array
                        items:
                            type: string
                        description: 수정된 텍스트의 배열    
                example:
                    text:
                    - "1 [1]문단에서는 인류 역사에서"
                    - "가치가 매우 큰 이집트 상형 문자를,"
        400:
            description: 잘못된 입력 형식
            schema:
                type: object
                properties:
                    error:
                        type: string
                        description: 오류 메시지
        500:
            description: 서버 오류 발생
            schema:
                type: object
                properties:
                    error:
                        type: string
                        description: 오류 메시지
    """
    return process_correction(request.get_json())


def process_to_brl(request_json):
    print("Process: translation - to braille")
    
    if not isinstance(request_json, dict):
        return jsonify({'error': 'Invalid input format'}), 400
    
    text_list = request_json['text']
    
    if text_list is None:
        return jsonify({'error': '텍스트 오류 수정 오류'}), 500
    
    try:
        return jsonify({'text': t2b.translate(text_list)})  # 텍스트를 점자로 번역하는 함수
    except Exception as e:
        return jsonify({'error': '서버 오류 발생'}), 500
    
@app.route('/translate/to-brl', methods=['POST'])
def translate_to_brl():
    """
    점역 - 텍스트를 점자로 변환합니다.
    ---
    tags:
      - Translation
    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            properties:
                text:
                    type: array
                    items:
                        type: string
                    description: 텍스트의 배열
            example:
                text:
                - "1 [1]문단에서는 인류 역사에서"
                - "가치가 매우 큰 이집트 상형 문자를,"
    responses:
        200:
            description: 변환된 점자를 반환합니다.
            schema:
                type: object
                properties:
                    text:
                        type: array
                        items:
                            type: string
                        description: 변환된 점자의 배열
                example:
                    text:
                    - "⠀⠀⠼⠁⠀⠦⠆⠼⠁⠰⠴⠑⠛⠊⠒⠝⠠⠎⠉⠵⠀⠟⠐⠩⠀⠱⠁⠇⠝⠠⠎⠀"
                    - "⠫⠰⠕⠫⠀⠑⠗⠍⠀⠋⠵⠀⠕⠨⠕⠃⠓⠪⠀⠇⠶⠚⠻⠀⠑⠛⠨⠐⠮⠐⠀⠀"
        400:
            description: 잘못된 입력 형식
            schema:
                type: object
                properties:
                    error:
                        type: string
                        description: 오류 메시지
        500:
            description: 서버 오류 발생
            schema:
                type: object
                properties:
                    error:
                        type: string
                        description: 오류 메시지
    """
    return process_to_brl(request.get_json())


def process_feedback_generation(request_json):
    print("Process: feedback generation")
    
    if not isinstance(request_json, dict):
        return jsonify({'error': 'Invalid input format'}), 400
    
    
    try:
        return jsonify(fg.main(request_json)), 200  # 피드백 생성 함수
    except Exception as e:
        return jsonify({'error': '서버 오류 발생'}), 500
    
@app.route('/feedback/generate', methods=['POST'])
def feedback_generation():
    """
    피드백 생성 - 역점역/교정/점역이 완료된 데이터를 이용하여 피드백을 생성합니다.
    ---
    tags:
      - Feedback
    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            properties:
                prediction:
                    type: object
                    properties:
                        brl:
                            type: array
                            items:
                                type: string
                            description: 예측된 점자 문자열의 배열
                        boxes:
                            type: array
                            items:
                                type: array
                                items:
                                    type: number
                            description: 박스(좌표)의 배열
                    example:
                        brl:
                        - "⠀⠀⠼⠁⠀⠦⠆⠼⠁⠰⠴⠑⠛⠊⠒⠝⠠⠎⠉⠵⠀⠟⠐⠩⠀⠱⠁⠇⠝⠠⠎⠀"
                        - "⠫⠰⠕⠫⠀⠑⠗⠍⠀⠋⠵⠀⠕⠨⠕⠃⠓⠪⠀⠇⠶⠚⠻⠀⠑⠛⠨⠐⠮⠐⠀⠀"
                        boxes:
                        - [111.28043624821944, 115.46576345825194, 127.65692801864586, 144.27071262105306]
                        - [138.0855162630461,  115.46576345825194, 154.4620080334725,  144.27071262105306]
                        
                correction:
                    type: object
                    properties:
                        brl:
                            type: array
                            items:
                                type: string
                            description: 교정된 점자 문자열의 배열
                    example:
                        brl:
                        - "⠼⠁⠀⠦⠆⠼⠁⠰⠴⠑⠛⠊⠒⠝⠠⠎⠉⠵⠀⠟⠐⠩⠀⠱⠁⠇⠝⠠⠎"
                        - "⠫⠰⠕⠫⠀⠑⠗⠍⠀⠋⠵⠀⠕⠨⠕⠃⠓⠪⠀⠇⠶⠚⠻⠀⠑⠛⠨⠐⠮⠐"
                            
    responses:
        200:
            description: 생성된 피드백(점자 좌표, 1~63의 labels)을 반환합니다.
            schema:
                type: object
                properties:
                    correction:
                        type: object
                        properties:
                            boxes:
                                type: array
                                items:
                                    type: array
                                    items:
                                        type: number
                                description: 교정된 박스(좌표)의 배열
                            labels:
                                type: array
                                items:
                                    type: array
                                    items:
                                        type: integer
                                description: 교정된 점자의 labels 배열
                        example:
                            boxes:
                            - [164.89059627787273, 115.46576345825194, 181.26708804829914, 144.27071262105306]
                            - [192.26506222025554, 115.01201594650486, 208.64155399068196, 143.81696510930598]
                            labels:
                            - [60, 1, 38, 6, 60]
                            - [43, 48, 21, 43, 17]
        400:
            description: 잘못된 입력 형식
            schema:
                type: object
                properties:
                    error:
                        type: string
                        description: 오류 메시지
        500:
            description: 서버 오류 발생
            schema:
                type: object
                properties:
                    error:
                        type: string
                        description: 오류 메시지
    """
    return process_feedback_generation(request.get_json())


def process_feedback_loop(request_json):
    print("Process: feedback loop")
    
    text_json = process_to_text(request_json)
    correct_text_json = process_correction(text_json)
    brl_json = process_to_brl(correct_text_json)
    result_json = process_feedback_generation(brl_json)
    
    return result_json

@app.route('/feedback/loop', methods=['POST'])
def feedback_loop():
    """
    피드백 루프 - 역점역/교정/점역/피드백생성을 순차적으로 수행합니다.
    ---
    tags:
      - Feedback
    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            properties:
                brl:
                    type: array
                    items:
                        type: string
                    description: 점자 문자열의 배열
            example:
                brl:
                - "⠀⠀⠼⠁⠀⠦⠆⠼⠁⠰⠴⠑⠛⠊⠒⠝⠠⠎⠉⠵⠀⠟⠐⠩⠀⠱⠁⠇⠝⠠⠎⠀"
                - "⠫⠰⠕⠫⠀⠑⠗⠍⠀⠋⠵⠀⠕⠨⠕⠃⠓⠪⠀⠇⠶⠚⠻⠀⠑⠛⠨⠐⠮⠐⠀⠀"
    responses:
        200:
            description: 생성된 피드백(점자 좌표, 1~63의 labels)을 반환합니다.
            schema:
                type: object
                properties:
                    correction:
                        type: object
                        properties:
                            boxes:
                                type: array
                                items:
                                    type: array
                                    items:
                                        type: number
                                description: 교정된 박스(좌표)의 배열
                            labels:
                                type: array
                                items:
                                    type: array
                                    items:
                                        type: integer
                                description: 교정된 점자의 labels 배열
                        example:
                            boxes:
                            - [164.89059627787273, 115.46576345825194, 181.26708804829914, 144.27071262105306]
                            - [192.26506222025554, 115.01201594650486, 208.64155399068196, 143.81696510930598]
                            labels:
                            - [60, 1, 38, 6, 60]
                            - [43, 48, 21, 43, 17]
        400:
            description: 잘못된 입력 형식
            schema:
                type: object
                properties:
                    error:
                        type: string
                        description: 오류 메시지
        500:
            description: 서버 오류 발생
            schema:
                type: object
                properties:
                    error:
                        type: string
                        description: 오류 메시지
    """
    return process_feedback_loop(request.get_json())

# curl -X POST -H "Content-Type: application/json" -d @test.json http://127.0.0.1:5000/translate/to-text


if __name__ == '__main__':
    app.run(debug=False)
    
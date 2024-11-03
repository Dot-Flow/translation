import openai

# OpenAI API 키 설정
openai.api_key = ''

def correct(input_sentence):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that corrects contextual errors in sentences."},
        {"role": "user", "content": f"다음 문장에서 문맥 오류를 수정해주세요: '{input_sentence}'"}
    ]
    
    response = openai.chat.completions.create(  # 올바른 호출 방식: ChatCompletion 사용
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=200,
        temperature=0.5
    )
    
    # 수정된 문장 반환
    corrected_sentence = response['choices'][0]['message']['content'].strip()
    return corrected_sentence

if __name__ == "__main__":
    input_sentence = "꾸ㅇ 이룬 어린 왕저에 데한 이야기"
    corrected_sentence = correct(input_sentence)
    print("수정된 문장:", corrected_sentence)

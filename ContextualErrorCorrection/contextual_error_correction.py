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


def test():
    import json
    with open('validate_list.txt', 'r') as f:
        ith_validate = f.readlines()
    for i in ith_validate:
        i = i.strip('\n')
        with open(i, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            
        text_list = json_data['prediction']['text']
        corrected_text_list = text_list
        
        # json_data['prediction']
        # json_data['prediction']['boxes']
        # json_data['prediction']['brl']
        # json_data['prediction']['labels']
        # json_data['prediction']['text']
        
        # json_data['correction']
        # json_data['correction']['boxes']
        # json_data['correction']['brl']
        # json_data['correction']['labels']
        json_data['correction']['text'] = corrected_text_list
        
        with open(i, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
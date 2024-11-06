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
    import json
    # input_sentence = "꾸ㅇ 이룬 어린 왕저에 데한 이야기"
    # corrected_sentence = correct(input_sentence)
    # print("수정된 문장:", corrected_sentence)
    
    with open('validate_list.txt', 'r') as f:
        ith_validate = f.readlines()
    for i in ith_validate:
        i = i.strip('\n')
        with open(i, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        try:
            text_list = json_data['text']
        except:
            continue
        # translated_brl_list = translate(text_list)
        corrected_text_list = text_list
        with open(i, "w", encoding="utf-8") as f:
            result_data = {'text': corrected_text_list}
            json.dump(result_data, f, ensure_ascii=False, indent=4)
            
        file_name = i.split('/')[-1]
        try:
            with open('data/db/' + file_name, "r", encoding="utf-8") as f:
                db_file = json.load(f)
        except:
            with open('data/db/' + file_name, "w", encoding="utf-8") as f:
                db_file = {}
                db_file['prediction'] = {}
                db_file['correction'] = {}
                json.dump(db_file, f, ensure_ascii=False, indent=4)
        db_file['correction']['text'] = corrected_text_list
        with open('data/db/' + file_name, "w", encoding="utf-8") as f:
            json.dump(db_file, f, ensure_ascii=False, indent=4)

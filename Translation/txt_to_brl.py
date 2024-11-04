from .utils.KorToBraille.KorToBraille import KorToBraille
import louis
import re

KOR = 0
ENG = 1
b = KorToBraille()

def split_text(text):
    pattern = re.compile(r'([가-힣]+|[A-Za-z]+|[^가-힣A-Za-z]+)')
    return pattern.findall(text)

def translate(text_list):
    cur_lang = KOR
    brl_list = []
        
    for text in text_list:
        brl_list.append(b.korTranslate(text))
        # 한글, 영어 구분
        # segments = split_text(text)
        # korean_segments = []
        # english_segments = []
        # translated_segments = []
        
        # for segment in segments:
        #     if re.match(r'[가-힣]+', segment):
        #         korean_segments.append(segment)
        #         translated_segments.append(('korean', len(korean_segments) - 1))
        #     elif re.match(r'[A-Za-z]+', segment):
        #         english_segments.append(segment)
        #         translated_segments.append(('english', len(english_segments) - 1))
        #     else:
        #         translated_segments.append(('other', segment))
            
        # # 점역
        # translated_korean_segments = [b.korTranslate(segment) for segment in korean_segments]
    
    return brl_list

if __name__ == "__main__":
    import json
    with open("test.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    translated_brl = []
    for text in json_data["correction"]["text"]:
        translated_brl.append(b.korTranslate(text))
        print(f"입력 텍스트: {text}\n변환된 점자: {translated_brl[-1]}")
    print(translated_brl)
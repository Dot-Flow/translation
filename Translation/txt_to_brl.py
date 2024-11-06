from utils.KorToBraille.KorToBraille import KorToBraille
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
        translated_brl_list = translate(text_list)
        with open(i, "w", encoding="utf-8") as f:
            result_data = {'brl': translated_brl_list}
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
        db_file['correction']['brl'] = translated_brl_list
        with open('data/db/' + file_name, "w", encoding="utf-8") as f:
            json.dump(db_file, f, ensure_ascii=False, indent=4)
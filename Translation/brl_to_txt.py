import textwrap
import louis
import json

# tableList = ["en-ueb-g2.ctb"]
# lineLength = 38

# translation = louis.translate(tableList, "Hello world", 0, 0)
# translation = louis.backTranslateString(tableList, "Hello world!", 0, 0)
                
# print(translation)

# print(louis.translate(["unicode.dis","en-chardefs.cti"], "hello")[0])
# print(louis.backTranslate(["unicode.dis","en-chardefs.cti"], "⠓⠑⠇⠇⠕")[0])
# print(louis.translate(["unicode.dis","ko-g2.ctb"], "안녕하세요 hello")[0])

# tableList = ["unicode.dis","ko-g2.ctb"]
kor_tableList = ["ko-g2.ctb"]
eng_tableList = ["unicode.dis","en-chardefs.cti"]

def lang_detection(text):
    # 한글, 영어 구분
    result = []     # [{lang: KOR, brl: ''}, {lang: ENG, text: ''}]
    
    lang = "KOR"
    
    for idx, char in enumerate(text):
        if lang == "KOR":
            if char == '⠴' and (idx == 0 or text[idx - 1] == chr(0x2800)):
                lang = "ENG"
            else:
                result.append({'lang': lang, 'brl': char})
        elif lang == "ENG":
            if (char == '⠲' or char == '⠐') and (idx + 1 == len(text) or text[idx + 1] == chr(0x2800)):
                result.append({'lang': lang, 'brl': char})
                lang = "KOR"
            else:
                result.append({'lang': lang, 'brl': char})
    return result

def translate(lang, input_brl_list):
    translated_text_list = []
    tableList = kor_tableList # if lang == "KOR" else eng_tableList
    
    for input_brl in input_brl_list:
        translation = louis.backTranslateString(tableList, input_brl, 0, 0)
        translated_text_list.append(translation)
    return translated_text_list


if __name__ == "__main__":
    # with open('data/db/성북소식지04.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    # brl_list = data['correction']['brl']
    # for brl in brl_list:
    #     print(brl)
    #     print(translate([brl]))
    #     print()
    text = "우리나라 기차에는 KTX, 새마을호, 무궁화호 등이 있다."
    brl = "⠍⠐⠕⠉⠐⠣⠀⠈⠕⠰⠣⠝⠉⠵⠀⠴⠠⠠⠅⠞⠭⠐⠀⠠⠗⠑⠣⠮⠚⠥⠐⠀⠑⠍⠈⠍⠶⠚⠧⠚⠥⠀⠊⠪⠶⠕⠀⠕⠌⠊⠲"
    # brl = "⠍⠐⠕⠉⠐⠣"
    brl_list = [
            "⠼⠁⠀⠦⠆⠼⠁⠰⠴⠑⠛⠊⠒⠝⠠⠎⠉⠵⠀⠟⠐⠩⠀⠱⠁⠇⠝⠠⠎",
            "⠫⠰⠕⠫⠀⠑⠗⠍⠀⠋⠵⠀⠕⠨⠕⠃⠓⠪⠀⠇⠶⠚⠻⠀⠑⠛⠨⠐⠮⠐",
            "⠦⠆⠼⠃⠰⠴⠑⠛⠊⠒⠝⠠⠎⠉⠵⠀⠟⠐⠩⠀⠰⠽⠰⠥⠺⠀⠇⠶⠚⠻",
            "⠑⠛⠨⠣⠟⠀⠈⠥⠊⠗⠀⠕⠨⠕⠃⠓⠪⠀⠇⠶⠚⠻⠀⠑⠛⠨⠐⠮⠐",
            "⠦⠆⠼⠉⠰⠴⠑⠛⠊⠒⠝⠠⠎⠉⠵⠀⠈⠥⠊⠗⠀⠕⠨⠕⠃⠓⠪⠀⠇⠶⠚⠻",
            "⠑⠛⠨⠣⠺⠀⠚⠗⠊⠭⠀⠈⠌⠈⠕⠫⠀⠊⠽⠒⠀⠠⠦⠐⠥⠨⠝⠓⠠⠹⠴⠄",
            "⠮⠐⠀⠦⠆⠼⠙⠰⠴⠑⠛⠊⠒⠝⠠⠎⠉⠵⠀⠑⠛⠨⠣⠺⠀⠘⠂⠊⠂",
            "⠈⠧⠨⠻⠮⠀⠘⠥⠱⠀⠨⠍⠉⠵⠀⠈⠥⠊⠗⠀⠕⠨⠕⠃⠓⠪⠀⠇⠶⠚⠻",
            "⠑⠛⠨⠣⠝⠀⠊⠗⠚⠗⠀⠠⠞⠑⠻⠚⠈⠥⠀⠕⠌⠠⠪⠃⠉⠕⠊⠲",
            "⠼⠃⠀⠈⠥⠊⠗⠀⠕⠨⠕⠃⠓⠪⠀⠇⠶⠚⠻⠀⠑⠛⠨⠣⠟",
            "⠠⠦⠚⠕⠝⠐⠥⠈⠮⠐⠕⠙⠪⠴⠄⠉⠵⠀⠰⠥⠈⠕⠝⠉⠵",
            "⠠⠊⠪⠄⠈⠮⠨⠣⠧⠀⠠⠥⠐⠕⠈⠮⠨⠣⠺⠀⠠⠻⠈⠱⠁⠕",
            "⠚⠷⠬⠶⠊⠽⠊⠫⠀⠨⠎⠢⠰⠣⠀⠠⠥⠐⠕⠐⠮⠀⠉⠓⠉⠗⠉⠵",
            "⠑⠛⠨⠐⠥⠀⠘⠠⠈⠍⠗⠎⠌⠉⠵⠊⠝⠐⠀⠕⠀⠈⠧⠨⠻⠕⠀⠑⠛⠨⠣⠺",
            "⠕⠂⠘⠒⠨⠹⠟⠀⠘⠂⠊⠂⠀⠈⠧⠨⠻⠮⠀⠘⠥⠱⠀⠨⠛⠊⠉⠵",
            "⠨⠎⠢⠝⠠⠎⠀⠋⠵⠀⠫⠰⠕⠫⠀⠕⠌⠠⠪⠃⠉⠕⠊⠲",
            "⠿⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠿",
            "⠼⠚⠋⠉⠠⠨⠭⠀⠥⠉⠮⠺⠀⠎⠚⠍⠗",
            "⠕⠂⠇⠶⠐⠂⠀⠉⠂⠑⠊⠀⠘⠒⠘⠭⠊⠽⠉⠵⠀⠠⠗⠶⠚⠧⠂⠲",
            "⠘⠱⠁⠚⠧⠐⠂⠀⠈⠾⠑⠯⠕⠉⠀⠊⠿⠈⠯⠐⠀⠑⠍⠊⠎⠢",
            "⠊⠪⠶⠺⠀⠘⠱⠁⠝⠀⠈⠪⠐⠟⠀⠈⠪⠐⠕⠢⠲",
            "⠑⠛⠜⠶⠐⠂⠀⠨⠍⠐⠥⠀⠈⠾⠑⠯⠕⠉⠀⠈⠿⠌⠙⠍⠢⠀⠊⠪⠶⠺",
            "⠑⠍⠉⠺⠲",
            "⠙⠼⠁⠉⠀⠀⠑⠛⠚⠧⠀⠼⠚⠁⠀⠑"]
    print(brl_list)
    detected_brl_list = []
    for brl in brl_list:
        detected_brl_list.append(lang_detection(brl))
    result = ""
    
    cur_lang = "KOR"
    buffer = ""
    for detected in detected_brl_list:
        buffer = ""
        for d in detected:
            print(d)
            if d['lang'] != cur_lang:
                print(buffer)
                result += translate(cur_lang, [buffer])[0]
                buffer = d['brl']
                cur_lang = d['lang']
            else:
                buffer += d['brl']
        result += translate(cur_lang, [buffer])[0]
        result += '\n'
    
    print(result)
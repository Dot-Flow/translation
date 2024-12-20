import louis
import json
import re

# tableList = ["en-ueb-g2.ctb"]
# lineLength = 38

# translation = louis.translate(tableList, "Hello world", 0, 0)
# translation = louis.backTranslateString(tableList, "Hello world!", 0, 0)
                
# print(translation)

# print(louis.translate(["unicode.dis","en-chardefs.cti"], "hello")[0])
# print(louis.backTranslate(["unicode.dis","en-chardefs.cti"], "⠓⠑⠇⠇⠕")[0])
# print(louis.translate(["unicode.dis","ko-g2.ctb"], "안녕하세요 hello")[0])

# tableList = ["unicode.dis","ko-g2.ctb"]
kor_tableList = ["unicode.dis", "ko-g2.ctb"]
eng_tableList = ["unicode.dis", "en-chardefs.cti", "en-us-g2.ctb"]

def lang_detection(text):
    # 한글, 영어 구분
    result = []
    for idx, char in enumerate(text):
        if ord('a') <= ord(char) <= ord('z') or ord('A') <= ord(char) <= ord('Z'):
            result.append({'lang': 'ENG', 'text': char})
        else:
            result.append({'lang': 'KOR', 'text': char})
    return result

def translate(lang, input_brl):
    tableList = kor_tableList if lang == "KOR" else eng_tableList
    return louis.translateString(tableList, input_brl, 0, 0)

def main(text_list):
    detected_text_list = []
    for text in text_list:
        detected_text_list.append(lang_detection(text))
    result = ""
    
    cur_lang = "KOR"
    buffer = ""
    for detected in detected_text_list:
        buffer = ""
        for d in detected:
            print(d)
            if d['lang'] != cur_lang:
                print(buffer)
                result += translate(cur_lang, buffer)
                buffer = '⠴' + d['text'] if d['lang'] == 'ENG' else d['text']
                cur_lang = d['lang']
            else:
                buffer += d['text']
        result += translate(cur_lang, buffer)
        result += '\n'
    
    print(result)
    return result
    
if __name__ == '__main__':
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
            "⠙⠼⠁⠉⠀⠀⠑⠛⠚⠧⠀⠼⠚⠁⠀⠑",
            "⠴⠺⠑⠇⠉⠕⠍⠑⠲⠀⠣⠒⠉⠻⠚⠠⠝⠬⠀⠘⠒⠫⠃⠠⠪⠃⠉⠕⠊⠀⠴⠠⠓⠑⠇⠇⠕"]
    print([text])
    main([text])
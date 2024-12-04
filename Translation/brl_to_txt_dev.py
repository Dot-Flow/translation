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
tableList = ["ko-g2.ctb"]

def translate(input_brl_list):
    translated_text_list = []
    for input_brl in input_brl_list:
        translation = louis.backTranslateString(tableList, input_brl, 0, 0)
        translated_text_list.append(translation)
    return translated_text_list


if __name__ == "__main__":
    with open('data/db/성북소식지04.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    brl_list = data['correction']['brl']
    for brl in brl_list:
        print(brl)
        print(translate([brl]))
        print()
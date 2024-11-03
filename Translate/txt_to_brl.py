from .utils.KorToBraille.KorToBraille import KorToBraille

b = KorToBraille()
def translate(extracted_json):
    text_list = extracted_json['correction']['text']
    brl_list = []
    for text in text_list:
        brl_list.append(b.korTranslate(text))
    extracted_json["correction"]["brl"] = brl_list
    return extracted_json

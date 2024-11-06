import difflib
import json
from PIL import Image, ImageDraw

# import FeedbackGeneration.validate

def generate_ground_truth(predicted_brl, corrected_brl, image_coordinates):
    matcher = difflib.SequenceMatcher(None, predicted_brl, corrected_brl)
    mapping = []
    for opcode in matcher.get_opcodes():
        tag, i1, i2, j1, j2 = opcode
        if tag == 'equal':
            for o, c in zip(range(i1, i2), range(j1, j2)):
                mapping.append((o, c, image_coordinates[o], tag))
        elif tag == 'replace':
            for o, c in zip(range(i1, i2), range(j1, j2)):
                mapping.append((o, c, image_coordinates[o], tag))
        elif tag == 'delete':
            for o in range(i1, i2):
                mapping.append((o, None, image_coordinates[o], tag))
        elif tag == 'insert':
            for c in range(j1, j2):
                mapping.append((None, c, None, tag))

    # 오류 유형 처리
    ground_truth = []
    for map_item in mapping:
        o_idx, c_idx, coord, tag = map_item
        if o_idx is not None and c_idx is not None:
            ground_truth.append({
                'ocr_char': predicted_brl[o_idx],
                'correct_char': corrected_brl[c_idx],
                'coordinates': coord,
                'tag': tag,
            })
        elif o_idx is not None:
            ground_truth.append({
                'ocr_char': predicted_brl[o_idx],
                'correct_char': '⠀',
                'coordinates': coord,
                'tag': tag,
            })
        elif c_idx is not None:
            ground_truth.append({
                'ocr_char': '⠀',
                'correct_char': corrected_brl[c_idx],
                'coordinates': None,
                'tag': tag,
            })

    # equal 태그를 가진 아이템의 개수 세기
    equal_count = sum(1 for item in ground_truth if item['tag'] == 'equal' if item['correct_char'] != '⠀')

    return ground_truth, equal_count

def brl_to_labels(brl_by_lines):
    labels_by_lines = []
    for brl in brl_by_lines:
        labels = []
        for char in brl:
            if char == '⠀':
                continue
            label = ord(char) - 0x2800
            labels.append(label)
        labels_by_lines.append(labels)
    return labels_by_lines

def main(request_json, img_path=None):
    predicted_brl_by_lines = request_json['prediction']['brl']
    corrected_brl_by_lines = request_json['correction']['brl']
    boxes_by_lines = request_json['prediction']['boxes']
    answer_count = request_json['answer_count']
    
    if img_path is not None:
        try:
            img = Image.open(img_path)
            draw = ImageDraw.Draw(img)
        except:
            img = None
            draw = None
    
    corrected_coordinates_by_lines = []
    equal_count_result = 0
    for predicted_brl, corrected_brl, boxes in zip(predicted_brl_by_lines, corrected_brl_by_lines, boxes_by_lines):
        # print(corrected_brl)
        ground_truth, equal_count = generate_ground_truth(predicted_brl, corrected_brl, boxes)
        equal_count_result += equal_count
        # print(ground_truth)
        # print(equal_count)
        # print(equal_count_result)
        # validation_result = validate.main(ground_truth)
        corrected_coordinates = []
        for gt in ground_truth:
            coordinates = gt['coordinates']
            
            if coordinates is None:
                """
                TODO: 이미지 좌표가 없는 경우 처리
                case 1. OCR이 인식하지 못한 문자
                    -> 줄의 시작이나 끝에 있는 문자일 가능성이 높음.
                case 2. 교정 결과에 없는 문자
                    -> 점자가 아닌 부분을 점자로 인식한 경우일 가능성이 높음.
                """
                pass
            
            if gt['ocr_char'] == gt['correct_char']:
                if gt['correct_char'] != '⠀':
                    # print(gt)
                    corrected_coordinates.append(coordinates)
                continue
    
            
            corrected_coordinates.append(coordinates)
            
            char_to_draw = str(ord(gt['ocr_char']) - 0x2800) + "->" + str(ord(gt['correct_char']) - 0x2800)
            try:
                draw.rectangle(coordinates, outline='red')
                draw.text((coordinates[0], coordinates[1] - 10), char_to_draw, fill='black')
            except:
                pass
        corrected_coordinates_by_lines.append(corrected_coordinates)
    
    corrected_brl_count = sum(1 for corrected_brl in corrected_brl_by_lines for char in corrected_brl if char != '⠀')
    
    # request_json['correction']['boxes'] =  corrected_coordinates_by_lines
    # request_json['correction']['labels'] = brl_to_labels(corrected_brl_by_lines)
    # img.save('result.jpg')
    print('Done.')
    print('Equal count:', equal_count_result)
    print('Corrected count:', corrected_brl_count)
    if answer_count is not None:
        print('Answer count:', answer_count)
    # print('Result image is saved as result.jpg')
    print('Retruned JSON is updated.')
    return {
        'correction': {
            'boxes': corrected_coordinates_by_lines,
            'labels': brl_to_labels(corrected_brl_by_lines),
        },
        'equal_count': equal_count_result,
        'corrected_count': corrected_brl_count,
        'answer_count': answer_count,
    }, img
    
    
if __name__ == '__main__':
    with open('validate_list.txt', 'r') as f:
        ith_validate = f.readlines()
    db_path = 'data/db/'
    img_result_path = 'data/s3/'
    for i in ith_validate:
        i = i.strip('\n')
        i = db_path + i.split('/')[-1]
        img_path = i.replace('json', 'jpg')
        print(i)
        
        with open(i, 'r') as f:
            request_json = json.load(f)
        # input_json ={
        #     "prediction": {
        #         "boxes": request_json['prediction']['boxes'],
        #         "brl": request_json['prediction']['brl']
        #     },
        #     "correction": {
        #         "brl": request_json['correction']['brl']
        #     }
        # }
        
        result_json, result_img = main(request_json, img_path)
        with open(i, 'w') as f:
            json.dump(result_json, f, indent=4)
        if result_img is not None:
            result_img.save(img_result_path + img_path.split('/')[-1])
    
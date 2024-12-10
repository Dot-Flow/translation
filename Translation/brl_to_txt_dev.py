from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os


def translate(input_brl_list):
    # WebDriver Manager를 사용하여 chromedriver 자동 설치 및 설정
    service = Service(ChromeDriverManager().install())
    
    # ChromeOptions 객체 생성
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 헤드리스 모드 설정
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=service, options=options)
    
    # 해당 페이지로 이동
    driver.get("https://t.hi098123.com/braille")
    
    # 변환할 텍스트를 입력 (예시: 'happy')
    try:
        input_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "input")))
    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        return
    # input_box.clear()  # 입력 필드 초기화
    
    for input_brl in input_brl_list:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "input")))
        input_box.send_keys(input_brl)  # 변환할 텍스트 입력
        input_box.send_keys("\n")
    
    # 역점역 버튼 클릭 (JavaScript 사용)
    try:
        convert_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='bar']/button[@data-name='역점역 (점자해석/묵역)']"))
        )
        driver.execute_script("arguments[0].click();", convert_button)
    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        return
    
    # 변환된 점자 결과를 가져오기
    try:
        output_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "plain"))
        )
        result_text = output_box.text  # 결과 텍스트 가져오기
        result_text_list = result_text.split("\n")
    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        return

    print(f"입력 텍스트: {input_brl}\n변환된 점자: {result_text_list}")
    
    # 브라우저 종료
    driver.quit()
    
    return result_text_list

def test():
    with open('validate_list.txt', 'r') as f:
        ith_validate = f.readlines()
    for i in ith_validate:
        i = i.strip('\n')
        print(i)
        with open(i, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        
        try:
            boxes_list = json_data['boxes']
            brl_list = json_data['brl']
            # labels_list = json_data['labels']
        except:
            # boxes_list = json_data['prediction']['boxes']
            # brl_list = json_data['prediction']['brl']
            # labels_list = json_data['prediction']['labels']
            continue
        
        translated_text_list = translate(brl_list)
        result_data = {}
        result_data['prediction'] = {}
        result_data['prediction']['boxes'] = boxes_list
        result_data['prediction']['brl'] = brl_list
        # result_data['prediction']['labels'] = labels_list if 'labels' in json_data else []
        result_data['prediction']['text'] = translated_text_list
        
        result_data['correction'] = {}
        result_data['correction']['boxes'] = []
        result_data['correction']['brl'] = []
        result_data['correction']['labels'] = []
        result_data['correction']['text'] = []
        
        with open(i, "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    # test()
    import time
    cur_time = time.time()
    print(cur_time)
    translate([
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
            "⠙⠼⠁⠉⠀⠀⠑⠛⠚⠧⠀⠼⠚⠁⠀⠑"
        ])
    print(time.time() - cur_time)
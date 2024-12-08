import unittest
import requests
import json

with open("test.json", "r", encoding="utf-8") as f:
    test_json = json.load(f)

class TestFlaskApp(unittest.TestCase):
    BASE_URL = 'http://52.23.254.128:8080'

    def test_translate_to_text(self):
        url = f'{self.BASE_URL}/translate/to-text'
        data = {'brl': test_json['prediction']['brl']}
        
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        print('test_translate_to_text passed')

    def test_correction(self):
        url = f'{self.BASE_URL}/correction'
        data = {'text': test_json['prediction']['text']}
        
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        print('test_correction passed')

    def test_translate_to_brl(self):
        url = f'{self.BASE_URL}/translate/to-brl'
        data = {'text': test_json['correction']['text']}
        
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        print('test_translate_to_brl passed')

    def test_feedback_generation(self):
        url = f'{self.BASE_URL}/feedback/generate'
        data = {
            "prediction": {
                "brl": test_json['prediction']['brl'],
                "boxes": test_json['prediction']['boxes']
            },
            "correction": {
                "brl": test_json['correction']['brl']
            }
        }
        
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        print('test_feedback_generation passed')

    def test_feedback_loop(self):
        url = f'{self.BASE_URL}/feedback/loop'
        data = {"brl": test_json['prediction']['brl']}
        
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        print('test_feedback_loop passed')

if __name__ == '__main__':
    # unittest.main()
    
    BASE_URL = 'http://52.23.254.128:8080'
    url = f'{BASE_URL}/translate/to-text'
    data = {'brl': [
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
        ]}
    
    
    response = requests.post(url, json=data)
    print(response.json())
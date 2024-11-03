# Translation
점역
역점역
Feedback data gen

# JSON file
```json
{
    "id": uuid int,
    "image_path": "kakao/data/images/KakaoTalk_20241008_234355161_07.jpg",-> #TODO: S3로 변경
    "date": "2024-10-27 12:40:57",
    "ImageWidth": null,
    "ImageHeight": null,
    "prediction": {
        "boxes": [
            [
                x1,
                y1,
                x2,
                y2
            ],
            ...
        ],
        "labels": [ -> 공백 포함
            [
                (line 1)
                0~63 label,
                ...
            ],
            [
                (line 2)
                0~63 label,
                ...
            ],
            ...
        ],
        "brl": [
            "⠼⠃ ⠦⠆⠼⠉⠰⠴⠑⠛⠊⠒⠝  ⠠⠊⠐⠪⠑⠡",
            ...
        ],
        "text": [
            "2 [3]문단에 따르면",
            ...
        ]
    },
    "correction": {
        "boxes": [
            [
                x1,
                y1,
                x2,
                y2
            ],
            ...,
        ],
        "labels": [ -> 공백 미포함
            [
                (line 1)
                1~63 label,
                ...
            ],
            [
                (line 2)
                1~63 label,
                ...
            ],
            ...
        ],
        "brl": [
            "⠼⠃ ⠦⠆⠼⠉⠰⠴⠑⠛⠊⠒⠝  ⠠⠊⠐⠪⠑⠡",
            ...
        ],
        "text": [
            "2 [3]문단에 따르면",
            ...
        ]
    },
}
```

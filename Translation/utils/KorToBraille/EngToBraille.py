import textwrap
import louis

tableList = ["en-ueb-g2.ctb"]
lineLength = 38

# translation = louis.translate(tableList, "Hello world", 0, 0)
# translation = louis.backTranslateString(tableList, "Hello world!", 0, 0)
                
# print(translation)

# print(louis.translate(["unicode.dis","en-chardefs.cti"], "hello")[0])
# print(louis.backTranslate(["unicode.dis","en-chardefs.cti"], "⠓⠑⠇⠇⠕")[0])
print(louis.translate(["unicode.dis","ko-g2.ctb"], "안녕하세요 hello")[0])
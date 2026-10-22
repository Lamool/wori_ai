import pyfiglet

# sentence = "Hello"
# py_sentence = pyfiglet.figlet_format(sentence)
# print(py_sentence)

def good_sentence(sentence:str):
    """입력된 문자를 pyfiglet 형식으로 출력
        매개변수 : sentence(str)
    """
    py_sentence = pyfiglet.figlet_format(sentence)
    print(py_sentence)
    
good_sentence("GOOD")
good_sentence("HELLO")
good_sentence("BYE")


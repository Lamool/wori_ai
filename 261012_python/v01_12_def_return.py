import pyfiglet
from termcolor import colored

def make_highlight(text:str):
    """
    입력된 문자열을 pyfigle, termcolor를 이용해서 꾸며준다.
        
        매개변수 : text(str)
    """
    py_text = pyfiglet.figlet_format(text)
    color_py_text = colored(py_text, "red")
    return color_py_text

# make_highlight("Hello")

# make_highlight 함수를 터미널에서 출력되게 해주세요.
# 방법 1.
highlight_text = make_highlight("Hello")
print(highlight_text)

# 방법 2.
print(make_highlight("Hello"))

import pyfiglet
from termcolor import colored

# 구현 : pyfiglet + colored를 적용한 sentence 출력

# 내가 직접 한 거
sentence = pyfiglet.figlet_format("Hello")
# print(sentence)

color_sentence = colored(sentence, "blue", "on_white", attrs=["bold"])
print(color_sentence)

# 같이
sentence2 = "GOOD"
py_sentence = pyfiglet.figlet_format(sentence2)
# print(py_sentence)

color_py_sentence = colored(py_sentence, "yellow")
print(color_py_sentence)
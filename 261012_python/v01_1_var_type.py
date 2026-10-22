x = 10                      # int(정수)
y = 3.14                    # float(실수)
name = "Python"             # 문자열(큰 따옴표 | 작은 따옴표 모두 가능)
is_fun = True               # 논리값(True | False)
colors = ["red", "green"]   # 리스트(순서 있음 (-> 순서가 있다는 건 인덱스 번호가 들어 있다), 수정 가능)
coords = (10,29)            # 튜플(순서 있음, 수정 불가)
person = {"name" : "Jin"}   # 딕셔너리(키-값 쌍)
nums = {1, 2, 3}            # 집합, set(중복 불가, 순서없음)
nothing = None              # NoneType(값 없음)

print(type(colors))         # <class 'list'>
print(isinstance(x, int))   # True

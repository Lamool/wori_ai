user_input = input("피트로 환산할 미터 값을 입력해주세요 : ")

try:
    meters = float(user_input)
    feet = meters * 3.28084
    print(f"{meters}m는 {feet}ft 입니다.")  
except ValueError:
    print("숫자를 입력해주세요!")
    
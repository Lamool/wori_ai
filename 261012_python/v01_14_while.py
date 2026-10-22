def meters_to_feet(meters:float):
    """
    미터를 피트로 환산
    """
    return meters * 3.28084

while True:
    user_input = input("피트로 환산할 미터 값을 입력해주세요 : ")
    try:
        user_meters = float(user_input)
        feet = meters_to_feet(user_meters)
        print(f"{user__meters}m는 {feet}ft 입니다.")
        break
    except ValueError:
        print("숫자를 입력해주세요. 다시 시도하세요.")
# 여러분들만의 클래스 정의

# 클래스
class Car:
    # 속성 3개 이상
    def __init__(self, speed, color, model):
        self.speed = speed
        self.color = color
        self.model = model

    # 메서드 2개 이상
    def car_speed(self):
        print(f"속도가 {self.speed}입니다.")
    
    def car_info(self):
        print(f"자동차는 {self.color}이며, 모델은 {self.model}입니다.")
     
# 객체 2개 이상   
car1 = Car(50, "검정색", "현대")
car2 = Car(30, "회색", "기아")

car1.car_speed()
car2.car_info()
print(car1.color)

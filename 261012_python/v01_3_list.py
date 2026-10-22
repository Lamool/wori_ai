colors = ["red", "green", "blue"]

# print(colors[0])          # red
# print(colors[-1])         # blue
# print(colors[0:2])        # ['red', 'green']

colors[-1] = "black"
print(colors)               # ['red', 'green', 'black']

colors.append('pink')
print(colors)               # ['red', 'green', 'black', 'pink']

colors.insert(0, "white")
print(colors)               # ['white', 'red', 'green', 'black', 'pink']

colors.remove("white")
print(colors)               # ['red', 'green', 'black', 'pink']


numbers = [8, 5, 3, 2, 7]

numbers.sort()              # 오름차순정렬 => [2, 3, 5, 7, 8]
print(numbers)

numbers.sort(reverse=True)  # 내림차순정렬 => [8, 7, 5, 3, 2]
print(numbers)

numbers.reverse()           # 순서 뒤집기
print(numbers)              # [2, 3, 5, 7, 8]
#
print(2 in numbers)         # True (포함 여부. numbers에 2가 포함되었으니 True)
# Python 공부내용 페이지

# Python 자료구조 종류 List, Tuple, Set, Dictionary

# 리스트 수정 / 문자열 인덱싱
# currencys = ["etc-krw","eth-krw","btc-krw"]
# currencys[0] = "alt-krw"
# for currency in currencys:
#     print(currency[:3])


# 리스트 슬라이싱
# portfolio = ["BTC","ETH","XRP","BCH","DASH"]
# print(portfolio[:3])


# 리스트 삽입 - append("") : 마지막 위치에 삽입
# 리스트 삽입 - insert(index,"") : 원하는 인덱스 위치에 삽입
# 리스트 삭제 - del listname[index]

# portfolio = []
# portfolio.append("BTC")
# portfolio.append("ETH")
# portfolio.append("XRP")
# print(portfolio)

# portfolio.insert(2,"DASH")
# print(portfolio)

# del portfolio[1]
# print(portfolio)


# 최댓값 / 최솟값 / 평균값
# from statistics import mean

# ripple_close = [503, 505, 508, 501, 530]
# print(max(ripple_close)) 
# print(min(ripple_close))
# print(mean(ripple_close))

# result = sum(ripple_close)
# length = len(ripple_close)
# print(f"average : {result/length}")

# 문자열 포매팅 : 문자열을 만들때 원하는 위치에 특정한 값(변수)를 삽입해서 보기좋게 출력하는 방법
# 특히 문자열에서 특정 부분만 바꾸고 나머지 부분은 그대로 두고 싶을 때 사용함

# 문자열 포매팅 (1) format 함수
# format함수 사용법 - "{index0},{index1}".format(값0, 값1)
# a = 2
# b = 3
# print("{0} x {1} = {2}".format(a, b, a*b))

# 직접 대입
# s1 = "name : {0}".format("HJ")
# print(s1)

# 변수로 대입
# age = 55
# s2 = "age : {0}".format(age)
# print(s2)

# 이름으로 대입
# s3 = "phone-number : {num}, gender : {gen}".format(num=1041298864, gen="male")
# print(s3)

# 참고 : 10진수인 숫자는 0으로 시작하는 숫자표기를 쓰지않음 2진법(2b), 8진법(2o)
# 문자열 타입에서 원하는 개수만큼 0 채우기 - zfill 함수(날짜에 0이 들어갈 때 유용함)
# zfill(0을 추가한 후 문자열의 길이) 

# text = '2'

# a = text.zfill(2)
# b = text.zfill(5)
# c = text.zfill(1)
# print(a,b,c)

# format 함수로 구구단 출력하기 (자릿수 맞추면서)

# for a in range(1,10):
#     for b in range(1,10):
#         print("{0} x {1} = {2:2}".format(a, b, a*b))

# 문자열 포맷팅 (2) f-string 방식
# f-string 사용법 : f"문자열 {변수} 문자열"

# 2022년 달력 출력
# month = 1
# while month<=12:
#     print(f"2022년 {month:2}월")
#     month += 1

# f-string과 딕셔너리
# 주의) " " 안에 또 " "를 넣으면 인식 못함 ' '로 대체 해야함 
# dic = {"name" : "HJ", "gender" : "male", "age" : "28"}
# result = f"my name : {dic['name']}\ngender : {dic['gender']}\nage : {dic['age']}"
# print(result)

# f-string과 리스트
# n = [100, 200, 300]
# print(f"list : {n[0]}, {n[1]}, {n[2]}")

# for list in n:
#     print(f"list with for loop : {list}")

# 튜플은 리스트처럼 순서는 있지만 수정 할 수 없다.
# 튜플 생성
# portfolio = ("ETC", "ETH", "BTC")
# print(type(portfolio))

# 튜플 인덱싱과 슬라이싱
# print(portfolio[0], portfolio[1])
# print(portfolio[:2])

# 딕셔너리는 두 값의 관계를 저장하는데 효과적인 자료구조입니다. 또한 순서가 없습니다.
# 딕셔너리의 구조 - {key : value}  
# 딕셔너리 생성
# prices = {"BTC" : 8300000, "XRP" : 514 }

# 딕셔너리 인덱싱 - 오직 key값을 통해서만 value값에 접근(인덱싱) 할 수 있습니다.
# print(prices["BTC"])

# 딕셔너리 데이터 추가
# prices["ETH"] = 600000
# print(prices)

# 딕셔너리 데이터 삭제
# del prices["BTC"]
# print(prices)

# 딕셔너리에서 key 값만 얻기
# prices = {"BTC" : 8300000, "XRP" : 514, "ETH" : 600000}
# print(prices.keys())

# 여기서 dict_keys(['BTC', ...]) 이런식으로 나오는데 우리가 배운 list와는 다른 type임
# list로 바꿔보자
# print(list(prices.keys())) 

# value 값만 List로 출력해보자
# print(list(prices.values()))

# 비동기 함수
# import asyncio 
 
# async def make_americano():
#     print("Americano Start")
#     await asyncio.sleep(3)
#     print("Americano End")
 
# async def make_latte():
#     print("Latte Start")
#     await asyncio.sleep(5)
#     print("Latte End")
 
# async def main():
#     coro1 = make_americano()
#     coro2 = make_latte()
#     await asyncio.gather(
#        coro1,
#        coro2
#     )
 
# print("Main Start")
# asyncio.run(main())
# print("Main End")


# SELECT CART_ID, NAME, COUNT(NAME) AS QUANTITY
# FROM CART_PRODUCTS
# GROUP BY NAME
# HAVING COUNT(NAME) > 0
# ORDER BY CART_ID ASC, NAME ASC;

# def solution(id_list, report, k):
#     id_list = ['muzi', 'apeach','frodo','neo' ]
#     report = []
#     for idx in range(len(id_list)):
#         report.append(id_list[idx])
#     print(report)
#     answer = []
    
#     return answer

## 해시 - 폰켓몬 ##
# nums = [3,3,3,2,2,4]
# print(list(set(nums)))

# print(len(set(nums)))

## 해시 - 완주하지 못한 선수 ##
## try1(정확도 20 효율성 0 실패) ##

# def solution(p,c):
#     answer = []
#     if len(set(p)) == len(p):
#         for i in range(len(p)):
#             if p[i] in c:   
#                 continue
#             answer.append(p[i])
    
#         return answer[0]
    
#     else:
#         for j in range(len(set(p))):
#             p.remove(list(set(p))[j])
        
#         return p[0]

# participant = ["kiki", "eden", "kiki"]
# completion = ["eden", "kiki"]

# print(solution(participant,completion))

## 중복 예외처리 연습 ##
# fruit_list = ['apple', 'banana', 'tomato', 'apple']
# fruit_set_list = list(set(fruit_list))

# if len(fruit_list) == len(fruit_set_list):
#     print("중복이 없습니다.")

# else:
#     for i in range(len(fruit_set_list)): 
#         fruit_list.remove(fruit_set_list[i])
#     print(fruit_list)

# arr = []
# for i in range(5):
#     arr.append(0)

# print(arr)
# print(new_arr)

# name = "hj"
# print(f"제 이름은 {name} 입니다.")

# name = ['박현재','신혜란','유준민']
# for i in range(3):
#     print(f"안녕하세요 저는 {name[i]} 입니다.")

# 리스트 컴프리헨션
# game = ["짝" if (i+1)%3==0 else i+1 for i in range(10)]
# print(game)

# str = 'macluarin'
# mac_list = [str[i] for i in range(9)]
# print(mac_list)

# print([c for c in str])

# 딕셔너리 컴프리헨션 
# arr1 = [1,2,3,4,5]
# arr2 = ['a','b','c','d','e']

# new_dict = { obj[0]:obj[1] for obj in zip(arr1,arr2) }
# new_dict_indexing = {arr1[i]:arr2[i] for i in range(5)}

# f-string

# name = '현재'

# introduce = f'안녕하세요 {name} 입니다.'
# print(introduce)


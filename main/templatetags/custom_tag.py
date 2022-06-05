from django import template

register = template.Library()

# 특정 키로 딕셔너리 조회하는 함수
# 출처 : https://www.pymoon.com/entry/djang-%ED%85%9C%ED%94%8C%EB%A6%BF%EC%97%90%EC%84%9C-custom-tag-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0

@register.simple_tag
def getvalue(dict, key):
    return dict.get(key)
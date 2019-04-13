# @Time    : 2019/3/28 16:13
# @Author  : xufqing
from rest_framework import status

# 成功
OK = status.HTTP_200_OK

NO_CONTENT = status.HTTP_204_NO_CONTENT
# 失败
BAD = status.HTTP_400_BAD_REQUEST
# 无权限
FORBIDDEN = status.HTTP_403_FORBIDDEN
# 未认证
UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED
# 创建
CREATED = status.HTTP_201_CREATED
# NOT_FOUND
NOT_FOUND = status.HTTP_404_NOT_FOUND

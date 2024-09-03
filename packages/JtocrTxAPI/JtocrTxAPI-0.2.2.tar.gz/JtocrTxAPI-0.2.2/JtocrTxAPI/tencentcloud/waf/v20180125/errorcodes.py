# -*- coding: utf8 -*-
# Copyright (c) 2017-2021 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# CAM签名/鉴权错误。
AUTHFAILURE = 'AuthFailure'

# DryRun 操作，代表请求将会是成功的，只是多传了 DryRun 参数。
DRYRUNOPERATION = 'DryRunOperation'

# 操作失败。
FAILEDOPERATION = 'FailedOperation'

# 调用CLS日志服务API失败
FAILEDOPERATION_CLSDBOPERATIONFAILED = 'FailedOperation.CLSDBOperationFailed'

# CLS内部错误。
FAILEDOPERATION_CLSINTERNALERROR = 'FailedOperation.CLSInternalError'

# 操作Mysql数据库失败
FAILEDOPERATION_MYSQLDBOPERATIONFAILED = 'FailedOperation.MysqlDBOperationFailed'

# 操作Redis数据库失败
FAILEDOPERATION_REDISOPERATIONFAILED = 'FailedOperation.RedisOperationFailed'

# 内部错误。
INTERNALERROR = 'InternalError'

# DBErr
INTERNALERROR_DBERR = 'InternalError.DBErr'

# 存在内部错误，请联系我们
INTERNALERROR_UNKNOWNERR = 'InternalError.UnknownErr'

# 参数错误。
INVALIDPARAMETER = 'InvalidParameter'

# 证书内容非法。
INVALIDPARAMETER_INVALIDCERTIFICATE = 'InvalidParameter.InvalidCertificate'

# 逻辑错误：SQL检索语句中的逻辑错误也可能导致错误。例如，使用错误的运算符、使用错误的条件等
INVALIDPARAMETER_LOGICERR = 'InvalidParameter.LogicErr'

# 根据ID查询证书失败。
INVALIDPARAMETER_QUERYCERTBYSSLIDFAILED = 'InvalidParameter.QueryCertBySSLIDFailed'

# 语法错误：逻辑表达式语法解析出错
INVALIDPARAMETER_QUERYSTRINGSYNTAXERR = 'InvalidParameter.QueryStringSyntaxErr'

# 参数取值错误。
INVALIDPARAMETERVALUE = 'InvalidParameterValue'

# 超过配额限制。
LIMITEXCEEDED = 'LimitExceeded'

# SpecificationErr
LIMITEXCEEDED_SPECIFICATIONERR = 'LimitExceeded.SpecificationErr'

# 缺少参数错误。
MISSINGPARAMETER = 'MissingParameter'

# 操作被拒绝。
OPERATIONDENIED = 'OperationDenied'

# 请求的次数超过了频率限制。
REQUESTLIMITEXCEEDED = 'RequestLimitExceeded'

# 资源被占用。
RESOURCEINUSE = 'ResourceInUse'

# 资源不足。
RESOURCEINSUFFICIENT = 'ResourceInsufficient'

# 资源不存在。
RESOURCENOTFOUND = 'ResourceNotFound'

# 资源不可用。
RESOURCEUNAVAILABLE = 'ResourceUnavailable'

# 资源售罄。
RESOURCESSOLDOUT = 'ResourcesSoldOut'

# 未授权操作。
UNAUTHORIZEDOPERATION = 'UnauthorizedOperation'

# 未知参数错误。
UNKNOWNPARAMETER = 'UnknownParameter'

# 操作不支持。
UNSUPPORTEDOPERATION = 'UnsupportedOperation'

# InvalidRequest
UNSUPPORTEDOPERATION_INVALIDREQUEST = 'UnsupportedOperation.InvalidRequest'

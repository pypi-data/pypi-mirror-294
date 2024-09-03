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

import json

from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.abstract_client import AbstractClient
from tencentcloud.mongodb.v20190725 import models


class MongodbClient(AbstractClient):
    _apiVersion = '2019-07-25'
    _endpoint = 'mongodb.tencentcloudapi.com'
    _service = 'mongodb'


    def AssignProject(self, request):
        """本接口(AssignProject)用于指定云数据库实例的所属项目。

        :param request: Request instance for AssignProject.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.AssignProjectRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.AssignProjectResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AssignProject", params, headers=headers)
            response = json.loads(body)
            model = models.AssignProjectResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateAccountUser(self, request):
        """本接口（CreateAccountUser）用于自定义实例访问账号。

        :param request: Request instance for CreateAccountUser.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.CreateAccountUserRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.CreateAccountUserResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateAccountUser", params, headers=headers)
            response = json.loads(body)
            model = models.CreateAccountUserResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateBackupDBInstance(self, request):
        """本接口（CreateBackupDBInstance）用于备份实例。

        :param request: Request instance for CreateBackupDBInstance.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.CreateBackupDBInstanceRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.CreateBackupDBInstanceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateBackupDBInstance", params, headers=headers)
            response = json.loads(body)
            model = models.CreateBackupDBInstanceResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateBackupDownloadTask(self, request):
        """本接口用来创建某个备份文件的下载任务

        :param request: Request instance for CreateBackupDownloadTask.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.CreateBackupDownloadTaskRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.CreateBackupDownloadTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateBackupDownloadTask", params, headers=headers)
            response = json.loads(body)
            model = models.CreateBackupDownloadTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateDBInstance(self, request):
        """本接口(CreateDBInstance)用于创建包年包月的MongoDB云数据库实例。接口支持的售卖规格，可从查询云数据库的售卖规格（DescribeSpecInfo）获取。

        :param request: Request instance for CreateDBInstance.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.CreateDBInstanceRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.CreateDBInstanceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDBInstance", params, headers=headers)
            response = json.loads(body)
            model = models.CreateDBInstanceResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateDBInstanceHour(self, request):
        """本接口（CreateDBInstanceHour）用于创建按量计费的MongoDB云数据库实例。

        :param request: Request instance for CreateDBInstanceHour.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.CreateDBInstanceHourRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.CreateDBInstanceHourResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDBInstanceHour", params, headers=headers)
            response = json.loads(body)
            model = models.CreateDBInstanceHourResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteAccountUser(self, request):
        """本接口（DeleteAccountUser）用于删除实例的自定义账号。

        :param request: Request instance for DeleteAccountUser.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.DeleteAccountUserRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.DeleteAccountUserResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteAccountUser", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteAccountUserResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAccountUsers(self, request):
        """本接口（DescribeAccountUsers）用于获取当前实例的全部账号。

        :param request: Request instance for DescribeAccountUsers.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.DescribeAccountUsersRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.DescribeAccountUsersResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAccountUsers", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAccountUsersResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAsyncRequestInfo(self, request):
        """查询异步任务状态接口

        :param request: Request instance for DescribeAsyncRequestInfo.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.DescribeAsyncRequestInfoRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.DescribeAsyncRequestInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAsyncRequestInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAsyncRequestInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeBackupDownloadTask(self, request):
        """查询备份下载任务信息

        :param request: Request instance for DescribeBackupDownloadTask.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.DescribeBackupDownloadTaskRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.DescribeBackupDownloadTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBackupDownloadTask", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeBackupDownloadTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeClientConnections(self, request):
        """本接口（DescribeClientConnections）用于查询实例客户端连接信息，包括连接 IP 和连接数量。

        :param request: Request instance for DescribeClientConnections.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.DescribeClientConnectionsRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.DescribeClientConnectionsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeClientConnections", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeClientConnectionsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeCurrentOp(self, request):
        """本接口(DescribeCurrentOp)用于查询MongoDB云数据库实例的当前正在执行的操作。

        :param request: Request instance for DescribeCurrentOp.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.DescribeCurrentOpRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.DescribeCurrentOpResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeCurrentOp", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeCurrentOpResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDBBackups(self, request):
        """本接口（DescribeDBBackups）用于查询实例备份列表，目前只支持查询7天内的备份记录。

        :param request: Request instance for DescribeDBBackups.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.DescribeDBBackupsRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.DescribeDBBackupsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDBBackups", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDBBackupsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDBInstanceDeal(self, request):
        """本接口（DescribeDBInstanceDeal）用于获取MongoDB购买、续费及变配订单详细。

        :param request: Request instance for DescribeDBInstanceDeal.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.DescribeDBInstanceDealRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.DescribeDBInstanceDealResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDBInstanceDeal", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDBInstanceDealResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDBInstanceNodeProperty(self, request):
        """本接口用于查询节点的属性，包括节点所在可用区、节点名称、地址、角色、状态、主从延迟、优先级、投票权、标签等属性。

        :param request: Request instance for DescribeDBInstanceNodeProperty.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.DescribeDBInstanceNodePropertyRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.DescribeDBInstanceNodePropertyResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDBInstanceNodeProperty", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDBInstanceNodePropertyResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDBInstances(self, request):
        """本接口（DescribeDBInstances）用于查询云数据库实例列表，支持通过项目ID、实例ID、实例状态等过滤条件来筛选主实例、灾备实例和只读实例信息列表。

        :param request: Request instance for DescribeDBInstances.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.DescribeDBInstancesRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.DescribeDBInstancesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDBInstances", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDBInstancesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeInstanceParams(self, request):
        """本接口（DescribeInstanceParams）用于查询当前实例可修改的参数列表。

        :param request: Request instance for DescribeInstanceParams.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.DescribeInstanceParamsRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.DescribeInstanceParamsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeInstanceParams", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeInstanceParamsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSecurityGroup(self, request):
        """本接口（DescribeSecurityGroup）用于查询实例绑定的安全组。

        :param request: Request instance for DescribeSecurityGroup.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.DescribeSecurityGroupRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.DescribeSecurityGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSecurityGroup", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSecurityGroupResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSlowLogPatterns(self, request):
        """本接口（DescribeSlowLogPatterns）用于获取数据库实例慢日志的统计信息。

        :param request: Request instance for DescribeSlowLogPatterns.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.DescribeSlowLogPatternsRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.DescribeSlowLogPatternsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSlowLogPatterns", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSlowLogPatternsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSlowLogs(self, request):
        """本接口（DescribeSlowLogs）用于获取云数据库慢日志信息。接口只支持查询最近7天内慢日志。

        :param request: Request instance for DescribeSlowLogs.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.DescribeSlowLogsRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.DescribeSlowLogsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSlowLogs", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSlowLogsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSpecInfo(self, request):
        """本接口(DescribeSpecInfo)用于查询实例的售卖规格。

        :param request: Request instance for DescribeSpecInfo.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.DescribeSpecInfoRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.DescribeSpecInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSpecInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSpecInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def FlushInstanceRouterConfig(self, request):
        """在所有mongos上执行FlushRouterConfig命令

        :param request: Request instance for FlushInstanceRouterConfig.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.FlushInstanceRouterConfigRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.FlushInstanceRouterConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("FlushInstanceRouterConfig", params, headers=headers)
            response = json.loads(body)
            model = models.FlushInstanceRouterConfigResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def InquirePriceCreateDBInstances(self, request):
        """本接口（InquirePriceCreateDBInstances）用于创建数据库实例询价。本接口参数中必须传入region参数，否则无法通过校验。本接口仅允许针对购买限制范围内的实例配置进行询价。

        :param request: Request instance for InquirePriceCreateDBInstances.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.InquirePriceCreateDBInstancesRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.InquirePriceCreateDBInstancesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("InquirePriceCreateDBInstances", params, headers=headers)
            response = json.loads(body)
            model = models.InquirePriceCreateDBInstancesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def InquirePriceModifyDBInstanceSpec(self, request):
        """本接口 (InquirePriceModifyDBInstanceSpec) 用于查询实例配置变更后的价格。

        :param request: Request instance for InquirePriceModifyDBInstanceSpec.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.InquirePriceModifyDBInstanceSpecRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.InquirePriceModifyDBInstanceSpecResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("InquirePriceModifyDBInstanceSpec", params, headers=headers)
            response = json.loads(body)
            model = models.InquirePriceModifyDBInstanceSpecResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def InquirePriceRenewDBInstances(self, request):
        """本接口 (InquiryPriceRenewDBInstances) 用于续费包年包月实例询价。

        :param request: Request instance for InquirePriceRenewDBInstances.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.InquirePriceRenewDBInstancesRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.InquirePriceRenewDBInstancesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("InquirePriceRenewDBInstances", params, headers=headers)
            response = json.loads(body)
            model = models.InquirePriceRenewDBInstancesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def IsolateDBInstance(self, request):
        """本接口(IsolateDBInstance)用于隔离MongoDB云数据库按量计费实例。隔离后实例保留在回收站中，不能再写入数据。隔离一定时间后，实例会彻底删除，回收站保存时间请参考按量计费的服务条款。在隔离中的按量计费实例无法恢复，请谨慎操作。

        :param request: Request instance for IsolateDBInstance.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.IsolateDBInstanceRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.IsolateDBInstanceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("IsolateDBInstance", params, headers=headers)
            response = json.loads(body)
            model = models.IsolateDBInstanceResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def KillOps(self, request):
        """本接口(KillOps)用于终止MongoDB云数据库实例上执行的特定操作。

        :param request: Request instance for KillOps.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.KillOpsRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.KillOpsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("KillOps", params, headers=headers)
            response = json.loads(body)
            model = models.KillOpsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyDBInstanceNetworkAddress(self, request):
        """本接口(ModifyDBInstanceNetworkAddress)用于修改云数据库实例的网络信息，可进行基础网络转VPC网络和VPC网络之间的变换。

        :param request: Request instance for ModifyDBInstanceNetworkAddress.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.ModifyDBInstanceNetworkAddressRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.ModifyDBInstanceNetworkAddressResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyDBInstanceNetworkAddress", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyDBInstanceNetworkAddressResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyDBInstanceSecurityGroup(self, request):
        """本接口（ModifyDBInstanceSecurityGroup）用于修改实例绑定的安全组

        :param request: Request instance for ModifyDBInstanceSecurityGroup.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.ModifyDBInstanceSecurityGroupRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.ModifyDBInstanceSecurityGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyDBInstanceSecurityGroup", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyDBInstanceSecurityGroupResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyDBInstanceSpec(self, request):
        """本接口(ModifyDBInstanceSpec)用于调整MongoDB云数据库实例配置。接口支持的售卖规格，可从查询云数据库的售卖规格（DescribeSpecInfo）获取。

        :param request: Request instance for ModifyDBInstanceSpec.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.ModifyDBInstanceSpecRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.ModifyDBInstanceSpecResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyDBInstanceSpec", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyDBInstanceSpecResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def OfflineIsolatedDBInstance(self, request):
        """本接口(OfflineIsolatedDBInstance)用于立即下线隔离状态的云数据库实例。进行操作的实例状态必须为隔离状态。

        :param request: Request instance for OfflineIsolatedDBInstance.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.OfflineIsolatedDBInstanceRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.OfflineIsolatedDBInstanceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("OfflineIsolatedDBInstance", params, headers=headers)
            response = json.loads(body)
            model = models.OfflineIsolatedDBInstanceResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RenameInstance(self, request):
        """本接口(RenameInstance)用于修改云数据库实例的名称。

        :param request: Request instance for RenameInstance.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.RenameInstanceRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.RenameInstanceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RenameInstance", params, headers=headers)
            response = json.loads(body)
            model = models.RenameInstanceResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RenewDBInstances(self, request):
        """本接口(RenewDBInstance)用于续费云数据库实例，仅支持付费模式为包年包月的实例。按量计费实例不需要续费。

        :param request: Request instance for RenewDBInstances.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.RenewDBInstancesRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.RenewDBInstancesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RenewDBInstances", params, headers=headers)
            response = json.loads(body)
            model = models.RenewDBInstancesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ResetDBInstancePassword(self, request):
        """修改实例用户的密码

        :param request: Request instance for ResetDBInstancePassword.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.ResetDBInstancePasswordRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.ResetDBInstancePasswordResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ResetDBInstancePassword", params, headers=headers)
            response = json.loads(body)
            model = models.ResetDBInstancePasswordResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SetAccountUserPrivilege(self, request):
        """本接口（SetAccountUserPrivilege）用于设置实例的账号权限。

        :param request: Request instance for SetAccountUserPrivilege.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.SetAccountUserPrivilegeRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.SetAccountUserPrivilegeResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("SetAccountUserPrivilege", params, headers=headers)
            response = json.loads(body)
            model = models.SetAccountUserPrivilegeResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def TerminateDBInstances(self, request):
        """本接口（TerminateDBInstances）可将包年包月实例退还隔离。

        :param request: Request instance for TerminateDBInstances.
        :type request: :class:`tencentcloud.mongodb.v20190725.models.TerminateDBInstancesRequest`
        :rtype: :class:`tencentcloud.mongodb.v20190725.models.TerminateDBInstancesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("TerminateDBInstances", params, headers=headers)
            response = json.loads(body)
            model = models.TerminateDBInstancesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)
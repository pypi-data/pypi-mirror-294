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

import warnings

from tencentcloud.common.abstract_model import AbstractModel


class AssignProjectRequest(AbstractModel):
    """AssignProject请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceIds: 实例ID列表，格式如：cmgo-p8vnipr5。与云数据库控制台页面中显示的实例ID相同
        :type InstanceIds: list of str
        :param _ProjectId: 项目ID，用户已创建项目的唯一ID,非自定义
        :type ProjectId: int
        """
        self._InstanceIds = None
        self._ProjectId = None

    @property
    def InstanceIds(self):
        return self._InstanceIds

    @InstanceIds.setter
    def InstanceIds(self, InstanceIds):
        self._InstanceIds = InstanceIds

    @property
    def ProjectId(self):
        return self._ProjectId

    @ProjectId.setter
    def ProjectId(self, ProjectId):
        self._ProjectId = ProjectId


    def _deserialize(self, params):
        self._InstanceIds = params.get("InstanceIds")
        self._ProjectId = params.get("ProjectId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AssignProjectResponse(AbstractModel):
    """AssignProject返回参数结构体

    """

    def __init__(self):
        r"""
        :param _FlowIds: 返回的异步任务ID列表
        :type FlowIds: list of int non-negative
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._FlowIds = None
        self._RequestId = None

    @property
    def FlowIds(self):
        return self._FlowIds

    @FlowIds.setter
    def FlowIds(self, FlowIds):
        self._FlowIds = FlowIds

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._FlowIds = params.get("FlowIds")
        self._RequestId = params.get("RequestId")


class Auth(AbstractModel):
    """用户权限

    """

    def __init__(self):
        r"""
        :param _Mask: 当前账号具有的权限信息。<ul><li>0：无权限。</li><li>1：只读。</li><li>2：只写。</li><li>3：读写。</li></ul>
        :type Mask: int
        :param _NameSpace: 指具有当前账号权限的数据库名。
<ul><li>* ：表示所有数据库。</li><li>db.name：表示特定name的数据库。</li></ul>
        :type NameSpace: str
        """
        self._Mask = None
        self._NameSpace = None

    @property
    def Mask(self):
        return self._Mask

    @Mask.setter
    def Mask(self, Mask):
        self._Mask = Mask

    @property
    def NameSpace(self):
        return self._NameSpace

    @NameSpace.setter
    def NameSpace(self, NameSpace):
        self._NameSpace = NameSpace


    def _deserialize(self, params):
        self._Mask = params.get("Mask")
        self._NameSpace = params.get("NameSpace")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BackupDownloadTask(AbstractModel):
    """备份下载任务

    """

    def __init__(self):
        r"""
        :param _CreateTime: 任务创建时间
        :type CreateTime: str
        :param _BackupName: 备份文件名
        :type BackupName: str
        :param _ReplicaSetId: 分片名称
        :type ReplicaSetId: str
        :param _BackupSize: 备份数据大小，单位为字节
        :type BackupSize: int
        :param _Status: 任务状态。0-等待执行，1-正在下载，2-下载完成，3-下载失败，4-等待重试
        :type Status: int
        :param _Percent: 任务进度百分比
        :type Percent: int
        :param _TimeSpend: 耗时，单位为秒
        :type TimeSpend: int
        :param _Url: 备份数据下载链接
        :type Url: str
        :param _BackupMethod: 备份文件备份类型，0-逻辑备份，1-物理备份
        :type BackupMethod: int
        :param _BackupDesc: 发起备份时指定的备注信息
注意：此字段可能返回 null，表示取不到有效值。
        :type BackupDesc: str
        """
        self._CreateTime = None
        self._BackupName = None
        self._ReplicaSetId = None
        self._BackupSize = None
        self._Status = None
        self._Percent = None
        self._TimeSpend = None
        self._Url = None
        self._BackupMethod = None
        self._BackupDesc = None

    @property
    def CreateTime(self):
        return self._CreateTime

    @CreateTime.setter
    def CreateTime(self, CreateTime):
        self._CreateTime = CreateTime

    @property
    def BackupName(self):
        return self._BackupName

    @BackupName.setter
    def BackupName(self, BackupName):
        self._BackupName = BackupName

    @property
    def ReplicaSetId(self):
        return self._ReplicaSetId

    @ReplicaSetId.setter
    def ReplicaSetId(self, ReplicaSetId):
        self._ReplicaSetId = ReplicaSetId

    @property
    def BackupSize(self):
        return self._BackupSize

    @BackupSize.setter
    def BackupSize(self, BackupSize):
        self._BackupSize = BackupSize

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def Percent(self):
        return self._Percent

    @Percent.setter
    def Percent(self, Percent):
        self._Percent = Percent

    @property
    def TimeSpend(self):
        return self._TimeSpend

    @TimeSpend.setter
    def TimeSpend(self, TimeSpend):
        self._TimeSpend = TimeSpend

    @property
    def Url(self):
        return self._Url

    @Url.setter
    def Url(self, Url):
        self._Url = Url

    @property
    def BackupMethod(self):
        return self._BackupMethod

    @BackupMethod.setter
    def BackupMethod(self, BackupMethod):
        self._BackupMethod = BackupMethod

    @property
    def BackupDesc(self):
        return self._BackupDesc

    @BackupDesc.setter
    def BackupDesc(self, BackupDesc):
        self._BackupDesc = BackupDesc


    def _deserialize(self, params):
        self._CreateTime = params.get("CreateTime")
        self._BackupName = params.get("BackupName")
        self._ReplicaSetId = params.get("ReplicaSetId")
        self._BackupSize = params.get("BackupSize")
        self._Status = params.get("Status")
        self._Percent = params.get("Percent")
        self._TimeSpend = params.get("TimeSpend")
        self._Url = params.get("Url")
        self._BackupMethod = params.get("BackupMethod")
        self._BackupDesc = params.get("BackupDesc")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BackupDownloadTaskStatus(AbstractModel):
    """创建备份下载任务结果

    """

    def __init__(self):
        r"""
        :param _ReplicaSetId: 分片名
        :type ReplicaSetId: str
        :param _Status: 任务当前状态。0-等待执行，1-正在下载，2-下载完成，3-下载失败，4-等待重试
        :type Status: int
        """
        self._ReplicaSetId = None
        self._Status = None

    @property
    def ReplicaSetId(self):
        return self._ReplicaSetId

    @ReplicaSetId.setter
    def ReplicaSetId(self, ReplicaSetId):
        self._ReplicaSetId = ReplicaSetId

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status


    def _deserialize(self, params):
        self._ReplicaSetId = params.get("ReplicaSetId")
        self._Status = params.get("Status")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BackupInfo(AbstractModel):
    """备份信息

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID
        :type InstanceId: str
        :param _BackupType: 备份方式，0-自动备份，1-手动备份
        :type BackupType: int
        :param _BackupName: 备份名称
        :type BackupName: str
        :param _BackupDesc: 备份备注
注意：此字段可能返回 null，表示取不到有效值。
        :type BackupDesc: str
        :param _BackupSize: 备份文件大小，单位KB
注意：此字段可能返回 null，表示取不到有效值。
        :type BackupSize: int
        :param _StartTime: 备份开始时间
注意：此字段可能返回 null，表示取不到有效值。
        :type StartTime: str
        :param _EndTime: 备份结束时间
注意：此字段可能返回 null，表示取不到有效值。
        :type EndTime: str
        :param _Status: 备份状态，1-备份中，2-备份成功
        :type Status: int
        :param _BackupMethod: 备份方法，0-逻辑备份，1-物理备份
        :type BackupMethod: int
        """
        self._InstanceId = None
        self._BackupType = None
        self._BackupName = None
        self._BackupDesc = None
        self._BackupSize = None
        self._StartTime = None
        self._EndTime = None
        self._Status = None
        self._BackupMethod = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def BackupType(self):
        return self._BackupType

    @BackupType.setter
    def BackupType(self, BackupType):
        self._BackupType = BackupType

    @property
    def BackupName(self):
        return self._BackupName

    @BackupName.setter
    def BackupName(self, BackupName):
        self._BackupName = BackupName

    @property
    def BackupDesc(self):
        return self._BackupDesc

    @BackupDesc.setter
    def BackupDesc(self, BackupDesc):
        self._BackupDesc = BackupDesc

    @property
    def BackupSize(self):
        return self._BackupSize

    @BackupSize.setter
    def BackupSize(self, BackupSize):
        self._BackupSize = BackupSize

    @property
    def StartTime(self):
        return self._StartTime

    @StartTime.setter
    def StartTime(self, StartTime):
        self._StartTime = StartTime

    @property
    def EndTime(self):
        return self._EndTime

    @EndTime.setter
    def EndTime(self, EndTime):
        self._EndTime = EndTime

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def BackupMethod(self):
        return self._BackupMethod

    @BackupMethod.setter
    def BackupMethod(self, BackupMethod):
        self._BackupMethod = BackupMethod


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._BackupType = params.get("BackupType")
        self._BackupName = params.get("BackupName")
        self._BackupDesc = params.get("BackupDesc")
        self._BackupSize = params.get("BackupSize")
        self._StartTime = params.get("StartTime")
        self._EndTime = params.get("EndTime")
        self._Status = params.get("Status")
        self._BackupMethod = params.get("BackupMethod")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClientConnection(AbstractModel):
    """客户端连接信息，包括客户端IP和连接数

    """

    def __init__(self):
        r"""
        :param _IP: 连接的客户端IP
        :type IP: str
        :param _Count: 对应客户端IP的连接数
        :type Count: int
        :param _InternalService: 是否为内部ip
        :type InternalService: bool
        """
        self._IP = None
        self._Count = None
        self._InternalService = None

    @property
    def IP(self):
        return self._IP

    @IP.setter
    def IP(self, IP):
        self._IP = IP

    @property
    def Count(self):
        return self._Count

    @Count.setter
    def Count(self, Count):
        self._Count = Count

    @property
    def InternalService(self):
        return self._InternalService

    @InternalService.setter
    def InternalService(self, InternalService):
        self._InternalService = InternalService


    def _deserialize(self, params):
        self._IP = params.get("IP")
        self._Count = params.get("Count")
        self._InternalService = params.get("InternalService")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAccountUserRequest(AbstractModel):
    """CreateAccountUser请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例 ID。例如：cmgo-p8vn****。请登录 [MongoDB 控制台](https://console.cloud.tencent.com/mongodb)在实例列表复制实例 ID。
        :type InstanceId: str
        :param _UserName: 新账号名称。其格式要求如下：<ul><li>字符范围[1,32]。</li><li>可输入[A,Z]、[a,z]、[1,9]范围的字符以及下划线“_”与短划线“-”。</li></ul>
        :type UserName: str
        :param _Password: 新账号密码。密码复杂度要求如下：<ul><li>字符长度范围[8,32]。</li><li>至少包含字母、数字和特殊字符（叹号“!”、at"@"、井号“#”、百分号“%”、插入符“^”、星号“*”、小括号“()”、下划线“_”）中的两种。</li></ul>
        :type Password: str
        :param _MongoUserPassword: mongouser 账号对应的密码。mongouser 为系统默认账号，即为创建实例时，设置的密码。
        :type MongoUserPassword: str
        :param _UserDesc: 账号备注信息。
        :type UserDesc: str
        :param _AuthRole: 账号的读写权限信息。
        :type AuthRole: list of Auth
        """
        self._InstanceId = None
        self._UserName = None
        self._Password = None
        self._MongoUserPassword = None
        self._UserDesc = None
        self._AuthRole = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def UserName(self):
        return self._UserName

    @UserName.setter
    def UserName(self, UserName):
        self._UserName = UserName

    @property
    def Password(self):
        return self._Password

    @Password.setter
    def Password(self, Password):
        self._Password = Password

    @property
    def MongoUserPassword(self):
        return self._MongoUserPassword

    @MongoUserPassword.setter
    def MongoUserPassword(self, MongoUserPassword):
        self._MongoUserPassword = MongoUserPassword

    @property
    def UserDesc(self):
        return self._UserDesc

    @UserDesc.setter
    def UserDesc(self, UserDesc):
        self._UserDesc = UserDesc

    @property
    def AuthRole(self):
        return self._AuthRole

    @AuthRole.setter
    def AuthRole(self, AuthRole):
        self._AuthRole = AuthRole


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._UserName = params.get("UserName")
        self._Password = params.get("Password")
        self._MongoUserPassword = params.get("MongoUserPassword")
        self._UserDesc = params.get("UserDesc")
        if params.get("AuthRole") is not None:
            self._AuthRole = []
            for item in params.get("AuthRole"):
                obj = Auth()
                obj._deserialize(item)
                self._AuthRole.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAccountUserResponse(AbstractModel):
    """CreateAccountUser返回参数结构体

    """

    def __init__(self):
        r"""
        :param _FlowId: 创建任务ID。
        :type FlowId: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._FlowId = None
        self._RequestId = None

    @property
    def FlowId(self):
        return self._FlowId

    @FlowId.setter
    def FlowId(self, FlowId):
        self._FlowId = FlowId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._FlowId = params.get("FlowId")
        self._RequestId = params.get("RequestId")


class CreateBackupDBInstanceRequest(AbstractModel):
    """CreateBackupDBInstance请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例 ID。例如：cmgo-p8vn****。请登录 [MongoDB 控制台](https://console.cloud.tencent.com/mongodb)在实例列表复制实例 ID。
        :type InstanceId: str
        :param _BackupMethod: 设置备份方式。
- 0：逻辑备份。
- 1：物理备份。
        :type BackupMethod: int
        :param _BackupRemark: 备份备注信息。
        :type BackupRemark: str
        """
        self._InstanceId = None
        self._BackupMethod = None
        self._BackupRemark = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def BackupMethod(self):
        return self._BackupMethod

    @BackupMethod.setter
    def BackupMethod(self, BackupMethod):
        self._BackupMethod = BackupMethod

    @property
    def BackupRemark(self):
        return self._BackupRemark

    @BackupRemark.setter
    def BackupRemark(self, BackupRemark):
        self._BackupRemark = BackupRemark


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._BackupMethod = params.get("BackupMethod")
        self._BackupRemark = params.get("BackupRemark")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateBackupDBInstanceResponse(AbstractModel):
    """CreateBackupDBInstance返回参数结构体

    """

    def __init__(self):
        r"""
        :param _AsyncRequestId: 查询备份流程的状态。
        :type AsyncRequestId: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._AsyncRequestId = None
        self._RequestId = None

    @property
    def AsyncRequestId(self):
        return self._AsyncRequestId

    @AsyncRequestId.setter
    def AsyncRequestId(self, AsyncRequestId):
        self._AsyncRequestId = AsyncRequestId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._AsyncRequestId = params.get("AsyncRequestId")
        self._RequestId = params.get("RequestId")


class CreateBackupDownloadTaskRequest(AbstractModel):
    """CreateBackupDownloadTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID，格式如：cmgo-p8vnipr5。与云数据库控制台页面中显示的实例ID相同。
        :type InstanceId: str
        :param _BackupName: 要下载的备份文件名，可通过DescribeDBBackups接口获取。
        :type BackupName: str
        :param _BackupSets: 指定要下载的副本集的节点名称 或 分片集群的分片名称列表。
如副本集cmgo-p8vnipr5，示例(固定取值)：BackupSets.0=cmgo-p8vnipr5_0，可下载全量数据。
如分片集群cmgo-p8vnipr5，示例：BackupSets.0=cmgo-p8vnipr5_0&BackupSets.1=cmgo-p8vnipr5_1，即下载分片0和分片1的数据，分片集群如需全量下载，请按示例方式传入全部分片名称。
        :type BackupSets: list of ReplicaSetInfo
        """
        self._InstanceId = None
        self._BackupName = None
        self._BackupSets = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def BackupName(self):
        return self._BackupName

    @BackupName.setter
    def BackupName(self, BackupName):
        self._BackupName = BackupName

    @property
    def BackupSets(self):
        return self._BackupSets

    @BackupSets.setter
    def BackupSets(self, BackupSets):
        self._BackupSets = BackupSets


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._BackupName = params.get("BackupName")
        if params.get("BackupSets") is not None:
            self._BackupSets = []
            for item in params.get("BackupSets"):
                obj = ReplicaSetInfo()
                obj._deserialize(item)
                self._BackupSets.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateBackupDownloadTaskResponse(AbstractModel):
    """CreateBackupDownloadTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Tasks: 下载任务状态
        :type Tasks: list of BackupDownloadTaskStatus
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Tasks = None
        self._RequestId = None

    @property
    def Tasks(self):
        return self._Tasks

    @Tasks.setter
    def Tasks(self, Tasks):
        self._Tasks = Tasks

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Tasks") is not None:
            self._Tasks = []
            for item in params.get("Tasks"):
                obj = BackupDownloadTaskStatus()
                obj._deserialize(item)
                self._Tasks.append(obj)
        self._RequestId = params.get("RequestId")


class CreateDBInstanceHourRequest(AbstractModel):
    """CreateDBInstanceHour请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Memory: 实例内存大小，单位：GB。
        :type Memory: int
        :param _Volume: 实例硬盘大小，单位：GB。
        :type Volume: int
        :param _ReplicateSetNum: 指副本集数量。
- 创建副本集实例，该参数只能为1。
- 创建分片实例，指分片的数量。具体售卖规格，请通过接口 [DescribeSpecInfo](https://cloud.tencent.com/document/product/240/38567) 获取。
        :type ReplicateSetNum: int
        :param _NodeNum: 指每个副本集内节点个数。具体售卖规格，请通过接口 [DescribeSpecInfo](https://cloud.tencent.com/document/product/240/38567) 获取。
        :type NodeNum: int
        :param _MongoVersion: 指版本信息。具体售卖规格，请通过接口 [DescribeSpecInfo](https://cloud.tencent.com/document/product/240/38567) 获取。
- MONGO_36_WT：MongoDB 3.6 WiredTiger存储引擎版本。
- MONGO_40_WT：MongoDB 4.0 WiredTiger存储引擎版本。
- MONGO_42_WT：MongoDB 4.2 WiredTiger存储引擎版本。
- MONGO_44_WT：MongoDB 4.4 WiredTiger存储引擎版本。
        :type MongoVersion: str
        :param _MachineCode: 机器类型。
- HIO：高IO型。
- HIO10G：高IO万兆。
        :type MachineCode: str
        :param _GoodsNum: 实例数量，最小值1，最大值为10。
        :type GoodsNum: int
        :param _Zone: 可用区信息，输入格式如：ap-guangzhou-2。
- 具体信息，请通过接口 [DescribeSpecInfo](https://cloud.tencent.com/document/product/240/38567) 获取。
- 该参数为主可用区，如果多可用区部署，Zone必须是AvailabilityZoneList中的一个。
        :type Zone: str
        :param _ClusterType: 实例架构类型。
- REPLSET：副本集。
- SHARD：分片集群。
        :type ClusterType: str
        :param _VpcId: 私有网络ID。如果不设置该参数，则默认选择基础网络。
        :type VpcId: str
        :param _SubnetId: 私有网络下的子网 ID，如果配置参数 VpcId，则 SubnetId必须配置。
        :type SubnetId: str
        :param _Password: 实例密码。自定义密码长度为8-32个字符，至少包含字母、数字和字符（!@#%^*()_）中的两种。
        :type Password: str
        :param _ProjectId: 项目ID。若不设置该参数，则为默认项目。
        :type ProjectId: int
        :param _Tags: 实例标签信息。
        :type Tags: list of TagInfo
        :param _Clone: 实例类型。
- 1：正式实例。
- 3：只读实例。
- 4：灾备实例。
        :type Clone: int
        :param _Father: 父实例 ID。当参数**Clone**为3或者4时，即实例为只读或灾备实例时，该参数必须配置。
        :type Father: str
        :param _SecurityGroup: 安全组。
        :type SecurityGroup: list of str
        :param _RestoreTime: 克隆实例回档时间。
- 若为克隆实例，则必须配置该参数。输入格式示例：2021-08-13 16:30:00。
- 回档时间范围：仅能回档7天内时间点的数据。
        :type RestoreTime: str
        :param _InstanceName: 实例名称。仅支持长度为60个字符的中文、英文、数字、下划线_、分隔符- 。
        :type InstanceName: str
        :param _AvailabilityZoneList: 多可用区部署的节点列表。具体信息，请通过接口 [DescribeSpecInfo](https://cloud.tencent.com/document/product/240/38567)获取。
- 多可用区部署节点只能部署在3个不同可用区。不支持将集群的大多数节点部署在同一个可用区。例如：3节点集群不支持2个节点部署在同一个区。
- 不支持4.2及以上版本。
- 不支持只读灾备实例。
- 不能选择基础网络。
        :type AvailabilityZoneList: list of str
        :param _MongosCpu: Mongos CPU 核数。购买分片集群时，必须填写。

        :type MongosCpu: int
        :param _MongosMemory: Mongos 内存大小。购买分片集群时，必须填写。


        :type MongosMemory: int
        :param _MongosNodeNum: Mongos 数量。购买分片集群时，必须填写。


        :type MongosNodeNum: int
        :param _ReadonlyNodeNum: 只读节点数量，最大不超过7个。
        :type ReadonlyNodeNum: int
        :param _ReadonlyNodeAvailabilityZoneList: 指只读节点所属可用区。跨可用区部署实例，参数**ReadonlyNodeNum**不为**0**时，必须配置该参数。
        :type ReadonlyNodeAvailabilityZoneList: list of str
        :param _HiddenZone: Hidden节点所属可用区。跨可用区部署实例，必须配置该参数。
        :type HiddenZone: str
        """
        self._Memory = None
        self._Volume = None
        self._ReplicateSetNum = None
        self._NodeNum = None
        self._MongoVersion = None
        self._MachineCode = None
        self._GoodsNum = None
        self._Zone = None
        self._ClusterType = None
        self._VpcId = None
        self._SubnetId = None
        self._Password = None
        self._ProjectId = None
        self._Tags = None
        self._Clone = None
        self._Father = None
        self._SecurityGroup = None
        self._RestoreTime = None
        self._InstanceName = None
        self._AvailabilityZoneList = None
        self._MongosCpu = None
        self._MongosMemory = None
        self._MongosNodeNum = None
        self._ReadonlyNodeNum = None
        self._ReadonlyNodeAvailabilityZoneList = None
        self._HiddenZone = None

    @property
    def Memory(self):
        return self._Memory

    @Memory.setter
    def Memory(self, Memory):
        self._Memory = Memory

    @property
    def Volume(self):
        return self._Volume

    @Volume.setter
    def Volume(self, Volume):
        self._Volume = Volume

    @property
    def ReplicateSetNum(self):
        return self._ReplicateSetNum

    @ReplicateSetNum.setter
    def ReplicateSetNum(self, ReplicateSetNum):
        self._ReplicateSetNum = ReplicateSetNum

    @property
    def NodeNum(self):
        return self._NodeNum

    @NodeNum.setter
    def NodeNum(self, NodeNum):
        self._NodeNum = NodeNum

    @property
    def MongoVersion(self):
        return self._MongoVersion

    @MongoVersion.setter
    def MongoVersion(self, MongoVersion):
        self._MongoVersion = MongoVersion

    @property
    def MachineCode(self):
        return self._MachineCode

    @MachineCode.setter
    def MachineCode(self, MachineCode):
        self._MachineCode = MachineCode

    @property
    def GoodsNum(self):
        return self._GoodsNum

    @GoodsNum.setter
    def GoodsNum(self, GoodsNum):
        self._GoodsNum = GoodsNum

    @property
    def Zone(self):
        return self._Zone

    @Zone.setter
    def Zone(self, Zone):
        self._Zone = Zone

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId

    @property
    def Password(self):
        return self._Password

    @Password.setter
    def Password(self, Password):
        self._Password = Password

    @property
    def ProjectId(self):
        return self._ProjectId

    @ProjectId.setter
    def ProjectId(self, ProjectId):
        self._ProjectId = ProjectId

    @property
    def Tags(self):
        return self._Tags

    @Tags.setter
    def Tags(self, Tags):
        self._Tags = Tags

    @property
    def Clone(self):
        return self._Clone

    @Clone.setter
    def Clone(self, Clone):
        self._Clone = Clone

    @property
    def Father(self):
        return self._Father

    @Father.setter
    def Father(self, Father):
        self._Father = Father

    @property
    def SecurityGroup(self):
        return self._SecurityGroup

    @SecurityGroup.setter
    def SecurityGroup(self, SecurityGroup):
        self._SecurityGroup = SecurityGroup

    @property
    def RestoreTime(self):
        return self._RestoreTime

    @RestoreTime.setter
    def RestoreTime(self, RestoreTime):
        self._RestoreTime = RestoreTime

    @property
    def InstanceName(self):
        return self._InstanceName

    @InstanceName.setter
    def InstanceName(self, InstanceName):
        self._InstanceName = InstanceName

    @property
    def AvailabilityZoneList(self):
        return self._AvailabilityZoneList

    @AvailabilityZoneList.setter
    def AvailabilityZoneList(self, AvailabilityZoneList):
        self._AvailabilityZoneList = AvailabilityZoneList

    @property
    def MongosCpu(self):
        return self._MongosCpu

    @MongosCpu.setter
    def MongosCpu(self, MongosCpu):
        self._MongosCpu = MongosCpu

    @property
    def MongosMemory(self):
        return self._MongosMemory

    @MongosMemory.setter
    def MongosMemory(self, MongosMemory):
        self._MongosMemory = MongosMemory

    @property
    def MongosNodeNum(self):
        return self._MongosNodeNum

    @MongosNodeNum.setter
    def MongosNodeNum(self, MongosNodeNum):
        self._MongosNodeNum = MongosNodeNum

    @property
    def ReadonlyNodeNum(self):
        return self._ReadonlyNodeNum

    @ReadonlyNodeNum.setter
    def ReadonlyNodeNum(self, ReadonlyNodeNum):
        self._ReadonlyNodeNum = ReadonlyNodeNum

    @property
    def ReadonlyNodeAvailabilityZoneList(self):
        return self._ReadonlyNodeAvailabilityZoneList

    @ReadonlyNodeAvailabilityZoneList.setter
    def ReadonlyNodeAvailabilityZoneList(self, ReadonlyNodeAvailabilityZoneList):
        self._ReadonlyNodeAvailabilityZoneList = ReadonlyNodeAvailabilityZoneList

    @property
    def HiddenZone(self):
        return self._HiddenZone

    @HiddenZone.setter
    def HiddenZone(self, HiddenZone):
        self._HiddenZone = HiddenZone


    def _deserialize(self, params):
        self._Memory = params.get("Memory")
        self._Volume = params.get("Volume")
        self._ReplicateSetNum = params.get("ReplicateSetNum")
        self._NodeNum = params.get("NodeNum")
        self._MongoVersion = params.get("MongoVersion")
        self._MachineCode = params.get("MachineCode")
        self._GoodsNum = params.get("GoodsNum")
        self._Zone = params.get("Zone")
        self._ClusterType = params.get("ClusterType")
        self._VpcId = params.get("VpcId")
        self._SubnetId = params.get("SubnetId")
        self._Password = params.get("Password")
        self._ProjectId = params.get("ProjectId")
        if params.get("Tags") is not None:
            self._Tags = []
            for item in params.get("Tags"):
                obj = TagInfo()
                obj._deserialize(item)
                self._Tags.append(obj)
        self._Clone = params.get("Clone")
        self._Father = params.get("Father")
        self._SecurityGroup = params.get("SecurityGroup")
        self._RestoreTime = params.get("RestoreTime")
        self._InstanceName = params.get("InstanceName")
        self._AvailabilityZoneList = params.get("AvailabilityZoneList")
        self._MongosCpu = params.get("MongosCpu")
        self._MongosMemory = params.get("MongosMemory")
        self._MongosNodeNum = params.get("MongosNodeNum")
        self._ReadonlyNodeNum = params.get("ReadonlyNodeNum")
        self._ReadonlyNodeAvailabilityZoneList = params.get("ReadonlyNodeAvailabilityZoneList")
        self._HiddenZone = params.get("HiddenZone")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDBInstanceHourResponse(AbstractModel):
    """CreateDBInstanceHour返回参数结构体

    """

    def __init__(self):
        r"""
        :param _DealId: 订单ID。
        :type DealId: str
        :param _InstanceIds: 创建的实例ID列表。
        :type InstanceIds: list of str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._DealId = None
        self._InstanceIds = None
        self._RequestId = None

    @property
    def DealId(self):
        return self._DealId

    @DealId.setter
    def DealId(self, DealId):
        self._DealId = DealId

    @property
    def InstanceIds(self):
        return self._InstanceIds

    @InstanceIds.setter
    def InstanceIds(self, InstanceIds):
        self._InstanceIds = InstanceIds

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._DealId = params.get("DealId")
        self._InstanceIds = params.get("InstanceIds")
        self._RequestId = params.get("RequestId")


class CreateDBInstanceRequest(AbstractModel):
    """CreateDBInstance请求参数结构体

    """

    def __init__(self):
        r"""
        :param _NodeNum: 指每个副本集内节点个数。具体售卖规格，请通过接口 [DescribeSpecInfo](https://cloud.tencent.com/document/product/240/38567) 获取。
        :type NodeNum: int
        :param _Memory: 实例内存大小，单位：GB。
        :type Memory: int
        :param _Volume: 实例硬盘大小，单位：GB。
        :type Volume: int
        :param _MongoVersion: 指版本信息。具体售卖规格，请通过接口 [DescribeSpecInfo](https://cloud.tencent.com/document/product/240/38567) 获取。
- MONGO_36_WT：MongoDB 3.6 WiredTiger存储引擎版本。
- MONGO_40_WT：MongoDB 4.0 WiredTiger存储引擎版本。
- MONGO_42_WT：MongoDB 4.2 WiredTiger存储引擎版本。
- MONGO_44_WT：MongoDB 4.4 WiredTiger存储引擎版本。
        :type MongoVersion: str
        :param _GoodsNum: 实例数量, 最小值1，最大值为10。
        :type GoodsNum: int
        :param _Zone: 可用区信息，输入格式如：ap-guangzhou-2。
- 具体信息，请通过接口 [DescribeSpecInfo](https://cloud.tencent.com/document/product/240/38567) 获取。
- 该参数为主可用区，如果多可用区部署，Zone必须是AvailabilityZoneList中的一个。
        :type Zone: str
        :param _Period: 实例时长，单位：月，可选值包括 [1,2,3,4,5,6,7,8,9,10,11,12,24,36]。
        :type Period: int
        :param _MachineCode: 机器类型。
- HIO：高IO型。
- HIO10G：高IO万兆。
        :type MachineCode: str
        :param _ClusterType: 实例架构类型。
- REPLSET：副本集。
- SHARD：分片集群。
        :type ClusterType: str
        :param _ReplicateSetNum: 指副本集数量。
- 创建副本集实例，该参数只能为1。
- 创建分片实例，指分片的数量。具体售卖规格，请通过接口 [DescribeSpecInfo](https://cloud.tencent.com/document/product/240/38567) 获取。
        :type ReplicateSetNum: int
        :param _ProjectId: 项目ID。若不设置该参数，则为默认项目。
        :type ProjectId: int
        :param _VpcId: 私有网络ID。如果不设置该参数，则默认选择基础网络。
        :type VpcId: str
        :param _SubnetId: 私有网络下的子网 ID，如果配置参数 VpcId，则 SubnetId必须配置。
        :type SubnetId: str
        :param _Password: 实例密码。自定义密码长度为8-32个字符，至少包含字母、数字和字符（!@#%^*()_）中的两种。
        :type Password: str
        :param _Tags: 实例标签信息。
        :type Tags: list of TagInfo
        :param _AutoRenewFlag: 自动续费标记。
- 0：不自动续费。默认为不自动续费。
- 1：自动续费。
        :type AutoRenewFlag: int
        :param _AutoVoucher: 是否自动选择代金券。
- 1：是。
- 0：否。默认为0。
        :type AutoVoucher: int
        :param _Clone: 实例类型。
- 1：正式实例。
- 3：只读实例。
- 4：灾备实例。
        :type Clone: int
        :param _Father: 父实例 ID。当参数**Clone**为3或者4时，即实例为只读或灾备实例时，该参数必须配置。
        :type Father: str
        :param _SecurityGroup: 安全组。
        :type SecurityGroup: list of str
        :param _RestoreTime: 克隆实例回档时间。
- 若为克隆实例，则必须配置该参数。输入格式示例：2021-08-13 16:30:00。
- 回档时间范围：仅能回档7天内时间点的数据。
        :type RestoreTime: str
        :param _InstanceName: 实例名称。仅支持长度为60个字符的中文、英文、数字、下划线_、分隔符- 。
        :type InstanceName: str
        :param _AvailabilityZoneList: 多可用区部署的节点列表。具体信息，请通过接口 [DescribeSpecInfo](https://cloud.tencent.com/document/product/240/38567)获取。
- 多可用区部署节点只能部署在3个不同可用区。不支持将集群的大多数节点部署在同一个可用区。例如：3节点集群不支持2个节点部署在同一个区。
- 不支持4.2及以上版本。
- 不支持只读灾备实例。
- 不能选择基础网络。
        :type AvailabilityZoneList: list of str
        :param _MongosCpu: Mongos CPU 核数，购买MongoDB 4.2 及以上WiredTiger存储引擎版本的分片集群时，必须填写。具体售卖规格，请通过接口 [DescribeSpecInfo](https://cloud.tencent.com/document/product/240/38567) 获取。
        :type MongosCpu: int
        :param _MongosMemory: Mongos 内存大小。购买MongoDB 4.2 及以上WiredTiger存储引擎版本的分片集群时，必须填写。具体售卖规格，请通过接口 [DescribeSpecInfo](https://cloud.tencent.com/document/product/240/38567) 获取。
        :type MongosMemory: int
        :param _MongosNodeNum: Mongos 数量。购买MongoDB 4.2 及以上WiredTiger存储引擎版本的分片集群时，必须填写。具体售卖规格，请通过接口 [DescribeSpecInfo](https://cloud.tencent.com/document/product/240/38567) 获取。为了保障高可用，取值范围为[3,32]。
        :type MongosNodeNum: int
        :param _ReadonlyNodeNum: 只读节点数量，取值范围[0,5]。
        :type ReadonlyNodeNum: int
        :param _ReadonlyNodeAvailabilityZoneList: 指只读节点所属可用区。跨可用区部署实例，参数**ReadonlyNodeNum**不为**0**时，必须配置该参数。
        :type ReadonlyNodeAvailabilityZoneList: list of str
        :param _HiddenZone: Hidden节点所属可用区。跨可用区部署实例，必须配置该参数。
        :type HiddenZone: str
        """
        self._NodeNum = None
        self._Memory = None
        self._Volume = None
        self._MongoVersion = None
        self._GoodsNum = None
        self._Zone = None
        self._Period = None
        self._MachineCode = None
        self._ClusterType = None
        self._ReplicateSetNum = None
        self._ProjectId = None
        self._VpcId = None
        self._SubnetId = None
        self._Password = None
        self._Tags = None
        self._AutoRenewFlag = None
        self._AutoVoucher = None
        self._Clone = None
        self._Father = None
        self._SecurityGroup = None
        self._RestoreTime = None
        self._InstanceName = None
        self._AvailabilityZoneList = None
        self._MongosCpu = None
        self._MongosMemory = None
        self._MongosNodeNum = None
        self._ReadonlyNodeNum = None
        self._ReadonlyNodeAvailabilityZoneList = None
        self._HiddenZone = None

    @property
    def NodeNum(self):
        return self._NodeNum

    @NodeNum.setter
    def NodeNum(self, NodeNum):
        self._NodeNum = NodeNum

    @property
    def Memory(self):
        return self._Memory

    @Memory.setter
    def Memory(self, Memory):
        self._Memory = Memory

    @property
    def Volume(self):
        return self._Volume

    @Volume.setter
    def Volume(self, Volume):
        self._Volume = Volume

    @property
    def MongoVersion(self):
        return self._MongoVersion

    @MongoVersion.setter
    def MongoVersion(self, MongoVersion):
        self._MongoVersion = MongoVersion

    @property
    def GoodsNum(self):
        return self._GoodsNum

    @GoodsNum.setter
    def GoodsNum(self, GoodsNum):
        self._GoodsNum = GoodsNum

    @property
    def Zone(self):
        return self._Zone

    @Zone.setter
    def Zone(self, Zone):
        self._Zone = Zone

    @property
    def Period(self):
        return self._Period

    @Period.setter
    def Period(self, Period):
        self._Period = Period

    @property
    def MachineCode(self):
        return self._MachineCode

    @MachineCode.setter
    def MachineCode(self, MachineCode):
        self._MachineCode = MachineCode

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType

    @property
    def ReplicateSetNum(self):
        return self._ReplicateSetNum

    @ReplicateSetNum.setter
    def ReplicateSetNum(self, ReplicateSetNum):
        self._ReplicateSetNum = ReplicateSetNum

    @property
    def ProjectId(self):
        return self._ProjectId

    @ProjectId.setter
    def ProjectId(self, ProjectId):
        self._ProjectId = ProjectId

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId

    @property
    def Password(self):
        return self._Password

    @Password.setter
    def Password(self, Password):
        self._Password = Password

    @property
    def Tags(self):
        return self._Tags

    @Tags.setter
    def Tags(self, Tags):
        self._Tags = Tags

    @property
    def AutoRenewFlag(self):
        return self._AutoRenewFlag

    @AutoRenewFlag.setter
    def AutoRenewFlag(self, AutoRenewFlag):
        self._AutoRenewFlag = AutoRenewFlag

    @property
    def AutoVoucher(self):
        return self._AutoVoucher

    @AutoVoucher.setter
    def AutoVoucher(self, AutoVoucher):
        self._AutoVoucher = AutoVoucher

    @property
    def Clone(self):
        return self._Clone

    @Clone.setter
    def Clone(self, Clone):
        self._Clone = Clone

    @property
    def Father(self):
        return self._Father

    @Father.setter
    def Father(self, Father):
        self._Father = Father

    @property
    def SecurityGroup(self):
        return self._SecurityGroup

    @SecurityGroup.setter
    def SecurityGroup(self, SecurityGroup):
        self._SecurityGroup = SecurityGroup

    @property
    def RestoreTime(self):
        return self._RestoreTime

    @RestoreTime.setter
    def RestoreTime(self, RestoreTime):
        self._RestoreTime = RestoreTime

    @property
    def InstanceName(self):
        return self._InstanceName

    @InstanceName.setter
    def InstanceName(self, InstanceName):
        self._InstanceName = InstanceName

    @property
    def AvailabilityZoneList(self):
        return self._AvailabilityZoneList

    @AvailabilityZoneList.setter
    def AvailabilityZoneList(self, AvailabilityZoneList):
        self._AvailabilityZoneList = AvailabilityZoneList

    @property
    def MongosCpu(self):
        return self._MongosCpu

    @MongosCpu.setter
    def MongosCpu(self, MongosCpu):
        self._MongosCpu = MongosCpu

    @property
    def MongosMemory(self):
        return self._MongosMemory

    @MongosMemory.setter
    def MongosMemory(self, MongosMemory):
        self._MongosMemory = MongosMemory

    @property
    def MongosNodeNum(self):
        return self._MongosNodeNum

    @MongosNodeNum.setter
    def MongosNodeNum(self, MongosNodeNum):
        self._MongosNodeNum = MongosNodeNum

    @property
    def ReadonlyNodeNum(self):
        return self._ReadonlyNodeNum

    @ReadonlyNodeNum.setter
    def ReadonlyNodeNum(self, ReadonlyNodeNum):
        self._ReadonlyNodeNum = ReadonlyNodeNum

    @property
    def ReadonlyNodeAvailabilityZoneList(self):
        return self._ReadonlyNodeAvailabilityZoneList

    @ReadonlyNodeAvailabilityZoneList.setter
    def ReadonlyNodeAvailabilityZoneList(self, ReadonlyNodeAvailabilityZoneList):
        self._ReadonlyNodeAvailabilityZoneList = ReadonlyNodeAvailabilityZoneList

    @property
    def HiddenZone(self):
        return self._HiddenZone

    @HiddenZone.setter
    def HiddenZone(self, HiddenZone):
        self._HiddenZone = HiddenZone


    def _deserialize(self, params):
        self._NodeNum = params.get("NodeNum")
        self._Memory = params.get("Memory")
        self._Volume = params.get("Volume")
        self._MongoVersion = params.get("MongoVersion")
        self._GoodsNum = params.get("GoodsNum")
        self._Zone = params.get("Zone")
        self._Period = params.get("Period")
        self._MachineCode = params.get("MachineCode")
        self._ClusterType = params.get("ClusterType")
        self._ReplicateSetNum = params.get("ReplicateSetNum")
        self._ProjectId = params.get("ProjectId")
        self._VpcId = params.get("VpcId")
        self._SubnetId = params.get("SubnetId")
        self._Password = params.get("Password")
        if params.get("Tags") is not None:
            self._Tags = []
            for item in params.get("Tags"):
                obj = TagInfo()
                obj._deserialize(item)
                self._Tags.append(obj)
        self._AutoRenewFlag = params.get("AutoRenewFlag")
        self._AutoVoucher = params.get("AutoVoucher")
        self._Clone = params.get("Clone")
        self._Father = params.get("Father")
        self._SecurityGroup = params.get("SecurityGroup")
        self._RestoreTime = params.get("RestoreTime")
        self._InstanceName = params.get("InstanceName")
        self._AvailabilityZoneList = params.get("AvailabilityZoneList")
        self._MongosCpu = params.get("MongosCpu")
        self._MongosMemory = params.get("MongosMemory")
        self._MongosNodeNum = params.get("MongosNodeNum")
        self._ReadonlyNodeNum = params.get("ReadonlyNodeNum")
        self._ReadonlyNodeAvailabilityZoneList = params.get("ReadonlyNodeAvailabilityZoneList")
        self._HiddenZone = params.get("HiddenZone")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDBInstanceResponse(AbstractModel):
    """CreateDBInstance返回参数结构体

    """

    def __init__(self):
        r"""
        :param _DealId: 订单ID
        :type DealId: str
        :param _InstanceIds: 创建的实例ID列表
        :type InstanceIds: list of str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._DealId = None
        self._InstanceIds = None
        self._RequestId = None

    @property
    def DealId(self):
        return self._DealId

    @DealId.setter
    def DealId(self, DealId):
        self._DealId = DealId

    @property
    def InstanceIds(self):
        return self._InstanceIds

    @InstanceIds.setter
    def InstanceIds(self, InstanceIds):
        self._InstanceIds = InstanceIds

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._DealId = params.get("DealId")
        self._InstanceIds = params.get("InstanceIds")
        self._RequestId = params.get("RequestId")


class CurrentOp(AbstractModel):
    """云数据库实例当前操作

    """

    def __init__(self):
        r"""
        :param _OpId: 操作序号
注意：此字段可能返回 null，表示取不到有效值。
        :type OpId: int
        :param _Ns: 操作所在的命名空间，形式如db.collection
注意：此字段可能返回 null，表示取不到有效值。
        :type Ns: str
        :param _Query: 操作执行语句
注意：此字段可能返回 null，表示取不到有效值。
        :type Query: str
        :param _Op: 操作类型，可能的取值：aggregate、count、delete、distinct、find、findAndModify、getMore、insert、mapReduce、update和command
注意：此字段可能返回 null，表示取不到有效值。
        :type Op: str
        :param _ReplicaSetName: 操作所在的分片名称
        :type ReplicaSetName: str
        :param _State: 筛选条件，节点状态，可能的取值为：Primary、Secondary
注意：此字段可能返回 null，表示取不到有效值。
        :type State: str
        :param _Operation: 操作详细信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Operation: str
        :param _NodeName: 操作所在的节点名称
        :type NodeName: str
        :param _MicrosecsRunning: 操作已执行时间（ms）
注意：此字段可能返回 null，表示取不到有效值。
        :type MicrosecsRunning: int
        """
        self._OpId = None
        self._Ns = None
        self._Query = None
        self._Op = None
        self._ReplicaSetName = None
        self._State = None
        self._Operation = None
        self._NodeName = None
        self._MicrosecsRunning = None

    @property
    def OpId(self):
        return self._OpId

    @OpId.setter
    def OpId(self, OpId):
        self._OpId = OpId

    @property
    def Ns(self):
        return self._Ns

    @Ns.setter
    def Ns(self, Ns):
        self._Ns = Ns

    @property
    def Query(self):
        return self._Query

    @Query.setter
    def Query(self, Query):
        self._Query = Query

    @property
    def Op(self):
        return self._Op

    @Op.setter
    def Op(self, Op):
        self._Op = Op

    @property
    def ReplicaSetName(self):
        return self._ReplicaSetName

    @ReplicaSetName.setter
    def ReplicaSetName(self, ReplicaSetName):
        self._ReplicaSetName = ReplicaSetName

    @property
    def State(self):
        return self._State

    @State.setter
    def State(self, State):
        self._State = State

    @property
    def Operation(self):
        return self._Operation

    @Operation.setter
    def Operation(self, Operation):
        self._Operation = Operation

    @property
    def NodeName(self):
        return self._NodeName

    @NodeName.setter
    def NodeName(self, NodeName):
        self._NodeName = NodeName

    @property
    def MicrosecsRunning(self):
        return self._MicrosecsRunning

    @MicrosecsRunning.setter
    def MicrosecsRunning(self, MicrosecsRunning):
        self._MicrosecsRunning = MicrosecsRunning


    def _deserialize(self, params):
        self._OpId = params.get("OpId")
        self._Ns = params.get("Ns")
        self._Query = params.get("Query")
        self._Op = params.get("Op")
        self._ReplicaSetName = params.get("ReplicaSetName")
        self._State = params.get("State")
        self._Operation = params.get("Operation")
        self._NodeName = params.get("NodeName")
        self._MicrosecsRunning = params.get("MicrosecsRunning")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DBInstanceInfo(AbstractModel):
    """实例信息

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID
        :type InstanceId: str
        :param _Region: 地域信息
        :type Region: str
        """
        self._InstanceId = None
        self._Region = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Region(self):
        return self._Region

    @Region.setter
    def Region(self, Region):
        self._Region = Region


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._Region = params.get("Region")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DBInstancePrice(AbstractModel):
    """数据库实例价格

    """

    def __init__(self):
        r"""
        :param _UnitPrice: 单价
注意：此字段可能返回 null，表示取不到有效值。
        :type UnitPrice: float
        :param _OriginalPrice: 原价
        :type OriginalPrice: float
        :param _DiscountPrice: 折扣价
        :type DiscountPrice: float
        """
        self._UnitPrice = None
        self._OriginalPrice = None
        self._DiscountPrice = None

    @property
    def UnitPrice(self):
        return self._UnitPrice

    @UnitPrice.setter
    def UnitPrice(self, UnitPrice):
        self._UnitPrice = UnitPrice

    @property
    def OriginalPrice(self):
        return self._OriginalPrice

    @OriginalPrice.setter
    def OriginalPrice(self, OriginalPrice):
        self._OriginalPrice = OriginalPrice

    @property
    def DiscountPrice(self):
        return self._DiscountPrice

    @DiscountPrice.setter
    def DiscountPrice(self, DiscountPrice):
        self._DiscountPrice = DiscountPrice


    def _deserialize(self, params):
        self._UnitPrice = params.get("UnitPrice")
        self._OriginalPrice = params.get("OriginalPrice")
        self._DiscountPrice = params.get("DiscountPrice")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteAccountUserRequest(AbstractModel):
    """DeleteAccountUser请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 指定待删除账号的实例 ID。例如：cmgo-p8vn****。请登录 [MongoDB 控制台](https://console.cloud.tencent.com/mongodb)在实例列表复制实例 ID。

        :type InstanceId: str
        :param _UserName: 配置待删除的账号名。
        :type UserName: str
        :param _MongoUserPassword: 配置 mongouser 对应的密码。mongouser为系统默认账号，输入其对应的密码。
        :type MongoUserPassword: str
        """
        self._InstanceId = None
        self._UserName = None
        self._MongoUserPassword = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def UserName(self):
        return self._UserName

    @UserName.setter
    def UserName(self, UserName):
        self._UserName = UserName

    @property
    def MongoUserPassword(self):
        return self._MongoUserPassword

    @MongoUserPassword.setter
    def MongoUserPassword(self, MongoUserPassword):
        self._MongoUserPassword = MongoUserPassword


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._UserName = params.get("UserName")
        self._MongoUserPassword = params.get("MongoUserPassword")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteAccountUserResponse(AbstractModel):
    """DeleteAccountUser返回参数结构体

    """

    def __init__(self):
        r"""
        :param _FlowId: 账户删除任务ID。
        :type FlowId: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._FlowId = None
        self._RequestId = None

    @property
    def FlowId(self):
        return self._FlowId

    @FlowId.setter
    def FlowId(self, FlowId):
        self._FlowId = FlowId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._FlowId = params.get("FlowId")
        self._RequestId = params.get("RequestId")


class DescribeAccountUsersRequest(AbstractModel):
    """DescribeAccountUsers请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 指定待获取账号的实例ID。例如：cmgo-p8vn****。请登录 [MongoDB 控制台](https://console.cloud.tencent.com/mongodb)在实例列表复制实例 ID。
        :type InstanceId: str
        """
        self._InstanceId = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAccountUsersResponse(AbstractModel):
    """DescribeAccountUsers返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Users: 实例账号列表。
        :type Users: list of UserInfo
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Users = None
        self._RequestId = None

    @property
    def Users(self):
        return self._Users

    @Users.setter
    def Users(self, Users):
        self._Users = Users

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Users") is not None:
            self._Users = []
            for item in params.get("Users"):
                obj = UserInfo()
                obj._deserialize(item)
                self._Users.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeAsyncRequestInfoRequest(AbstractModel):
    """DescribeAsyncRequestInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param _AsyncRequestId: 异步请求Id，涉及到异步流程的接口返回，如CreateBackupDBInstance
        :type AsyncRequestId: str
        """
        self._AsyncRequestId = None

    @property
    def AsyncRequestId(self):
        return self._AsyncRequestId

    @AsyncRequestId.setter
    def AsyncRequestId(self, AsyncRequestId):
        self._AsyncRequestId = AsyncRequestId


    def _deserialize(self, params):
        self._AsyncRequestId = params.get("AsyncRequestId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAsyncRequestInfoResponse(AbstractModel):
    """DescribeAsyncRequestInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Status: 状态。返回参数有：initial-初始化、running-运行中、paused-任务执行失败，已暂停、undoed-任务执行失败，已回滚、failed-任务执行失败, 已终止、success-成功
        :type Status: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Status = None
        self._RequestId = None

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Status = params.get("Status")
        self._RequestId = params.get("RequestId")


class DescribeBackupDownloadTaskRequest(AbstractModel):
    """DescribeBackupDownloadTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID，格式如：cmgo-p8vnipr5。与云数据库控制台页面中显示的实例ID相同
        :type InstanceId: str
        :param _BackupName: 备份文件名，用来过滤指定文件的下载任务
        :type BackupName: str
        :param _StartTime: 指定查询时间范围内的任务，StartTime指定开始时间，不填默认不限制开始时间
        :type StartTime: str
        :param _EndTime: 指定查询时间范围内的任务，EndTime指定截止时间，不填默认不限制截止时间
        :type EndTime: str
        :param _Limit: 此次查询返回的条数，取值范围为1-100，默认为20
        :type Limit: int
        :param _Offset: 指定此次查询返回的页数，默认为0
        :type Offset: int
        :param _OrderBy: 排序字段，取值为createTime，finishTime两种，默认为createTime
        :type OrderBy: str
        :param _OrderByType: 排序方式，取值为asc，desc两种，默认desc
        :type OrderByType: str
        :param _Status: 根据任务状态过滤。0-等待执行，1-正在下载，2-下载完成，3-下载失败，4-等待重试。不填默认返回所有类型
        :type Status: list of int
        """
        self._InstanceId = None
        self._BackupName = None
        self._StartTime = None
        self._EndTime = None
        self._Limit = None
        self._Offset = None
        self._OrderBy = None
        self._OrderByType = None
        self._Status = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def BackupName(self):
        return self._BackupName

    @BackupName.setter
    def BackupName(self, BackupName):
        self._BackupName = BackupName

    @property
    def StartTime(self):
        return self._StartTime

    @StartTime.setter
    def StartTime(self, StartTime):
        self._StartTime = StartTime

    @property
    def EndTime(self):
        return self._EndTime

    @EndTime.setter
    def EndTime(self, EndTime):
        self._EndTime = EndTime

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def OrderBy(self):
        return self._OrderBy

    @OrderBy.setter
    def OrderBy(self, OrderBy):
        self._OrderBy = OrderBy

    @property
    def OrderByType(self):
        return self._OrderByType

    @OrderByType.setter
    def OrderByType(self, OrderByType):
        self._OrderByType = OrderByType

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._BackupName = params.get("BackupName")
        self._StartTime = params.get("StartTime")
        self._EndTime = params.get("EndTime")
        self._Limit = params.get("Limit")
        self._Offset = params.get("Offset")
        self._OrderBy = params.get("OrderBy")
        self._OrderByType = params.get("OrderByType")
        self._Status = params.get("Status")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBackupDownloadTaskResponse(AbstractModel):
    """DescribeBackupDownloadTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 满足查询条件的所有条数
        :type TotalCount: int
        :param _Tasks: 下载任务列表
        :type Tasks: list of BackupDownloadTask
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._Tasks = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def Tasks(self):
        return self._Tasks

    @Tasks.setter
    def Tasks(self, Tasks):
        self._Tasks = Tasks

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("Tasks") is not None:
            self._Tasks = []
            for item in params.get("Tasks"):
                obj = BackupDownloadTask()
                obj._deserialize(item)
                self._Tasks.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeClientConnectionsRequest(AbstractModel):
    """DescribeClientConnections请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 指定待查询的实例ID，例如：cmgo-p8vn****。请登录 [MongoDB 控制台](https://console.cloud.tencent.com/mongodb)在实例列表复制实例 ID。

        :type InstanceId: str
        :param _Limit: 单次请求返回的数量。最小值为1，最大值为1000，默认值为1000。
        :type Limit: int
        :param _Offset: 偏移量，默认值为0。Offset=Limit*(页码-1)。
        :type Offset: int
        """
        self._InstanceId = None
        self._Limit = None
        self._Offset = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._Limit = params.get("Limit")
        self._Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClientConnectionsResponse(AbstractModel):
    """DescribeClientConnections返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Clients: 客户端连接信息，包括客户端 IP 和对应 IP 的连接数量。
        :type Clients: list of ClientConnection
        :param _TotalCount: 满足条件的记录总条数，可用于分页查询。
        :type TotalCount: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Clients = None
        self._TotalCount = None
        self._RequestId = None

    @property
    def Clients(self):
        return self._Clients

    @Clients.setter
    def Clients(self, Clients):
        self._Clients = Clients

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Clients") is not None:
            self._Clients = []
            for item in params.get("Clients"):
                obj = ClientConnection()
                obj._deserialize(item)
                self._Clients.append(obj)
        self._TotalCount = params.get("TotalCount")
        self._RequestId = params.get("RequestId")


class DescribeCurrentOpRequest(AbstractModel):
    """DescribeCurrentOp请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID，格式如：cmgo-p8vnipr5。与云数据库控制台页面中显示的实例ID相同
        :type InstanceId: str
        :param _Ns: 筛选条件，操作所属的命名空间namespace，格式为db.collection
        :type Ns: str
        :param _MillisecondRunning: 筛选条件，操作已经执行的时间（单位：毫秒），结果将返回超过设置时间的操作，默认值为0，取值范围为[0, 3600000]
        :type MillisecondRunning: int
        :param _Op: 筛选条件，操作类型，可能的取值：none，update，insert，query，command，getmore，remove和killcursors
        :type Op: str
        :param _ReplicaSetName: 筛选条件，分片名称
        :type ReplicaSetName: str
        :param _State: 筛选条件，节点状态，可能的取值为：primary
secondary
        :type State: str
        :param _Limit: 单次请求返回的数量，默认值为100，取值范围为[0,100]
        :type Limit: int
        :param _Offset: 偏移量，默认值为0，取值范围为[0,10000]
        :type Offset: int
        :param _OrderBy: 返回结果集排序的字段，目前支持："MicrosecsRunning"/"microsecsrunning"，默认为升序排序
        :type OrderBy: str
        :param _OrderByType: 返回结果集排序方式，可能的取值："ASC"/"asc"或"DESC"/"desc"
        :type OrderByType: str
        """
        self._InstanceId = None
        self._Ns = None
        self._MillisecondRunning = None
        self._Op = None
        self._ReplicaSetName = None
        self._State = None
        self._Limit = None
        self._Offset = None
        self._OrderBy = None
        self._OrderByType = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Ns(self):
        return self._Ns

    @Ns.setter
    def Ns(self, Ns):
        self._Ns = Ns

    @property
    def MillisecondRunning(self):
        return self._MillisecondRunning

    @MillisecondRunning.setter
    def MillisecondRunning(self, MillisecondRunning):
        self._MillisecondRunning = MillisecondRunning

    @property
    def Op(self):
        return self._Op

    @Op.setter
    def Op(self, Op):
        self._Op = Op

    @property
    def ReplicaSetName(self):
        return self._ReplicaSetName

    @ReplicaSetName.setter
    def ReplicaSetName(self, ReplicaSetName):
        self._ReplicaSetName = ReplicaSetName

    @property
    def State(self):
        return self._State

    @State.setter
    def State(self, State):
        self._State = State

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def OrderBy(self):
        return self._OrderBy

    @OrderBy.setter
    def OrderBy(self, OrderBy):
        self._OrderBy = OrderBy

    @property
    def OrderByType(self):
        return self._OrderByType

    @OrderByType.setter
    def OrderByType(self, OrderByType):
        self._OrderByType = OrderByType


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._Ns = params.get("Ns")
        self._MillisecondRunning = params.get("MillisecondRunning")
        self._Op = params.get("Op")
        self._ReplicaSetName = params.get("ReplicaSetName")
        self._State = params.get("State")
        self._Limit = params.get("Limit")
        self._Offset = params.get("Offset")
        self._OrderBy = params.get("OrderBy")
        self._OrderByType = params.get("OrderByType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeCurrentOpResponse(AbstractModel):
    """DescribeCurrentOp返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 符合查询条件的操作总数
        :type TotalCount: int
        :param _CurrentOps: 当前操作列表
        :type CurrentOps: list of CurrentOp
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._CurrentOps = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def CurrentOps(self):
        return self._CurrentOps

    @CurrentOps.setter
    def CurrentOps(self, CurrentOps):
        self._CurrentOps = CurrentOps

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("CurrentOps") is not None:
            self._CurrentOps = []
            for item in params.get("CurrentOps"):
                obj = CurrentOp()
                obj._deserialize(item)
                self._CurrentOps.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeDBBackupsRequest(AbstractModel):
    """DescribeDBBackups请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID，格式如：cmgo-p8vnipr5。与云数据库控制台页面中显示的实例ID相同
        :type InstanceId: str
        :param _BackupMethod: 备份方式，当前支持：0-逻辑备份，1-物理备份，2-所有备份。默认为逻辑备份。
        :type BackupMethod: int
        :param _Limit: 分页大小，最大值为100，不设置默认查询所有。
        :type Limit: int
        :param _Offset: 分页偏移量，最小值为0，默认值为0。
        :type Offset: int
        """
        self._InstanceId = None
        self._BackupMethod = None
        self._Limit = None
        self._Offset = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def BackupMethod(self):
        return self._BackupMethod

    @BackupMethod.setter
    def BackupMethod(self, BackupMethod):
        self._BackupMethod = BackupMethod

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._BackupMethod = params.get("BackupMethod")
        self._Limit = params.get("Limit")
        self._Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBBackupsResponse(AbstractModel):
    """DescribeDBBackups返回参数结构体

    """

    def __init__(self):
        r"""
        :param _BackupList: 备份列表
        :type BackupList: list of BackupInfo
        :param _TotalCount: 备份总数
        :type TotalCount: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._BackupList = None
        self._TotalCount = None
        self._RequestId = None

    @property
    def BackupList(self):
        return self._BackupList

    @BackupList.setter
    def BackupList(self, BackupList):
        self._BackupList = BackupList

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("BackupList") is not None:
            self._BackupList = []
            for item in params.get("BackupList"):
                obj = BackupInfo()
                obj._deserialize(item)
                self._BackupList.append(obj)
        self._TotalCount = params.get("TotalCount")
        self._RequestId = params.get("RequestId")


class DescribeDBInstanceDealRequest(AbstractModel):
    """DescribeDBInstanceDeal请求参数结构体

    """

    def __init__(self):
        r"""
        :param _DealId: 订单ID，通过CreateDBInstance等接口返回
        :type DealId: str
        """
        self._DealId = None

    @property
    def DealId(self):
        return self._DealId

    @DealId.setter
    def DealId(self, DealId):
        self._DealId = DealId


    def _deserialize(self, params):
        self._DealId = params.get("DealId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBInstanceDealResponse(AbstractModel):
    """DescribeDBInstanceDeal返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Status: 订单状态，1：未支付，2：已支付，3：发货中，4：发货成功，5：发货失败，6：退款，7：订单关闭，8：超时未支付关闭。
        :type Status: int
        :param _OriginalPrice: 订单原价。
        :type OriginalPrice: float
        :param _DiscountPrice: 订单折扣价格。
        :type DiscountPrice: float
        :param _Action: 订单行为，purchase：新购，renew：续费，upgrade：升配，downgrade：降配，refund：退货退款。
        :type Action: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Status = None
        self._OriginalPrice = None
        self._DiscountPrice = None
        self._Action = None
        self._RequestId = None

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def OriginalPrice(self):
        return self._OriginalPrice

    @OriginalPrice.setter
    def OriginalPrice(self, OriginalPrice):
        self._OriginalPrice = OriginalPrice

    @property
    def DiscountPrice(self):
        return self._DiscountPrice

    @DiscountPrice.setter
    def DiscountPrice(self, DiscountPrice):
        self._DiscountPrice = DiscountPrice

    @property
    def Action(self):
        return self._Action

    @Action.setter
    def Action(self, Action):
        self._Action = Action

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Status = params.get("Status")
        self._OriginalPrice = params.get("OriginalPrice")
        self._DiscountPrice = params.get("DiscountPrice")
        self._Action = params.get("Action")
        self._RequestId = params.get("RequestId")


class DescribeDBInstanceNodePropertyRequest(AbstractModel):
    """DescribeDBInstanceNodeProperty请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID，格式如：cmgo-p8vnipr5。与云数据库控制台页面中显示的实例ID相同。
        :type InstanceId: str
        :param _NodeIds: 节点ID。
        :type NodeIds: list of str
        :param _Roles: 节点角色。可选值包括：
<ul><li>PRIMARY：主节点。</li><li>SECONDARY：从节点。</li><li>READONLY：只读节点。</li><li>ARBITER：仲裁节点。</li></ul>
        :type Roles: list of str
        :param _OnlyHidden: 该参数指定节点是否为Hidden节点，默认为false。
        :type OnlyHidden: bool
        :param _Priority: 该参数指定选举新主节点的优先级。其取值范围为[0,100]，数值越高，优先级越高。
        :type Priority: int
        :param _Votes: 该参数指定节点投票权。
<ul><li>1：具有投票权。</li><li>0：无投票权。</li></ul>
        :type Votes: int
        :param _Tags: 节点标签。
        :type Tags: list of NodeTag
        """
        self._InstanceId = None
        self._NodeIds = None
        self._Roles = None
        self._OnlyHidden = None
        self._Priority = None
        self._Votes = None
        self._Tags = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def NodeIds(self):
        return self._NodeIds

    @NodeIds.setter
    def NodeIds(self, NodeIds):
        self._NodeIds = NodeIds

    @property
    def Roles(self):
        return self._Roles

    @Roles.setter
    def Roles(self, Roles):
        self._Roles = Roles

    @property
    def OnlyHidden(self):
        return self._OnlyHidden

    @OnlyHidden.setter
    def OnlyHidden(self, OnlyHidden):
        self._OnlyHidden = OnlyHidden

    @property
    def Priority(self):
        return self._Priority

    @Priority.setter
    def Priority(self, Priority):
        self._Priority = Priority

    @property
    def Votes(self):
        return self._Votes

    @Votes.setter
    def Votes(self, Votes):
        self._Votes = Votes

    @property
    def Tags(self):
        return self._Tags

    @Tags.setter
    def Tags(self, Tags):
        self._Tags = Tags


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._NodeIds = params.get("NodeIds")
        self._Roles = params.get("Roles")
        self._OnlyHidden = params.get("OnlyHidden")
        self._Priority = params.get("Priority")
        self._Votes = params.get("Votes")
        if params.get("Tags") is not None:
            self._Tags = []
            for item in params.get("Tags"):
                obj = NodeTag()
                obj._deserialize(item)
                self._Tags.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBInstanceNodePropertyResponse(AbstractModel):
    """DescribeDBInstanceNodeProperty返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Mongos: Mongos节点属性。
注意：此字段可能返回 null，表示取不到有效值。
        :type Mongos: list of NodeProperty
        :param _ReplicateSets: 副本集节点信息。
        :type ReplicateSets: list of ReplicateSetInfo
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Mongos = None
        self._ReplicateSets = None
        self._RequestId = None

    @property
    def Mongos(self):
        return self._Mongos

    @Mongos.setter
    def Mongos(self, Mongos):
        self._Mongos = Mongos

    @property
    def ReplicateSets(self):
        return self._ReplicateSets

    @ReplicateSets.setter
    def ReplicateSets(self, ReplicateSets):
        self._ReplicateSets = ReplicateSets

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Mongos") is not None:
            self._Mongos = []
            for item in params.get("Mongos"):
                obj = NodeProperty()
                obj._deserialize(item)
                self._Mongos.append(obj)
        if params.get("ReplicateSets") is not None:
            self._ReplicateSets = []
            for item in params.get("ReplicateSets"):
                obj = ReplicateSetInfo()
                obj._deserialize(item)
                self._ReplicateSets.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeDBInstancesRequest(AbstractModel):
    """DescribeDBInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceIds: 实例 ID 列表。例如：cmgo-p8vn****。请登录 [MongoDB 控制台](https://console.cloud.tencent.com/mongodb)在实例列表复制实例 ID。
        :type InstanceIds: list of str
        :param _InstanceType: 实例类型。取值范围如下：<ul><li>0：所有实例。</li><li>1：正式实例。</li><li>2：临时实例。</li><li>3：只读实例。</li><li>-1：正式实例、只读、灾备实例。</li></ul>
        :type InstanceType: int
        :param _ClusterType: 集群类型，取值范围如下：<ul><li>0：副本集实例。</li><li>1：分片实例。</li><li>-1：所有实例。</li></ul>
        :type ClusterType: int
        :param _Status: 实例状态，取值范围如下所示：<ul><li>0：待初始化。</li><li>1：流程执行中。</li><li>2：实例有效。</li><li>-2：已隔离（包年包月实例）。</li><li>-3：已隔离（按量计费实例）。</li></ul>
        :type Status: list of int
        :param _VpcId: 私有网络的 ID。
- 基础网络则无需配置该参数。
- 请登录 [MongoDB 控制台](https://console.cloud.tencent.com/mongodb)在实例列表中，单击私有网络名称，在**私有网络**页面获取其 ID。
        :type VpcId: str
        :param _SubnetId: 私有网络的子网ID。
- 基础网络则无需配置该参数。
- 请登录 [MongoDB 控制台](https://console.cloud.tencent.com/mongodb)在实例列表中，单击私有网络名称，在**私有网络**页面获取其子网 ID。
        :type SubnetId: str
        :param _PayMode: 付费类型，取值范围如下：<ul><li>0：查询按量计费实例。</li><li>1：查询包年包月实例。</li><li>-1：查询按量计费与包年包月实例。</li></ul>
        :type PayMode: int
        :param _Limit: 单次请求返回的数量。默认值为20，取值范围为[1,100]。
        :type Limit: int
        :param _Offset: 偏移量，默认值为0。
        :type Offset: int
        :param _OrderBy: 配置返回结果排序依据的字段。目前支持依据"ProjectId"、"InstanceName"、"CreateTime"排序。
        :type OrderBy: str
        :param _OrderByType: 配置返回结果的排序方式。
- ASC：升序。
- DESC：降序。
        :type OrderByType: str
        :param _ProjectIds: 项目 ID。请登录 [MongoDB 控制台](https://console.cloud.tencent.com/mongodb)，在右上角的账户信息下拉菜单中，选择项目管理查询项目。
        :type ProjectIds: list of int non-negative
        :param _SearchKey: 配置查询搜索的关键词。支持配置为实例ID、实例名称或者内网 IP 地址。
        :type SearchKey: str
        :param _Tags: 标签信息，包含标签键与标签值。
        :type Tags: list of TagInfo
        """
        self._InstanceIds = None
        self._InstanceType = None
        self._ClusterType = None
        self._Status = None
        self._VpcId = None
        self._SubnetId = None
        self._PayMode = None
        self._Limit = None
        self._Offset = None
        self._OrderBy = None
        self._OrderByType = None
        self._ProjectIds = None
        self._SearchKey = None
        self._Tags = None

    @property
    def InstanceIds(self):
        return self._InstanceIds

    @InstanceIds.setter
    def InstanceIds(self, InstanceIds):
        self._InstanceIds = InstanceIds

    @property
    def InstanceType(self):
        return self._InstanceType

    @InstanceType.setter
    def InstanceType(self, InstanceType):
        self._InstanceType = InstanceType

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId

    @property
    def PayMode(self):
        return self._PayMode

    @PayMode.setter
    def PayMode(self, PayMode):
        self._PayMode = PayMode

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def OrderBy(self):
        return self._OrderBy

    @OrderBy.setter
    def OrderBy(self, OrderBy):
        self._OrderBy = OrderBy

    @property
    def OrderByType(self):
        return self._OrderByType

    @OrderByType.setter
    def OrderByType(self, OrderByType):
        self._OrderByType = OrderByType

    @property
    def ProjectIds(self):
        return self._ProjectIds

    @ProjectIds.setter
    def ProjectIds(self, ProjectIds):
        self._ProjectIds = ProjectIds

    @property
    def SearchKey(self):
        return self._SearchKey

    @SearchKey.setter
    def SearchKey(self, SearchKey):
        self._SearchKey = SearchKey

    @property
    def Tags(self):
        return self._Tags

    @Tags.setter
    def Tags(self, Tags):
        self._Tags = Tags


    def _deserialize(self, params):
        self._InstanceIds = params.get("InstanceIds")
        self._InstanceType = params.get("InstanceType")
        self._ClusterType = params.get("ClusterType")
        self._Status = params.get("Status")
        self._VpcId = params.get("VpcId")
        self._SubnetId = params.get("SubnetId")
        self._PayMode = params.get("PayMode")
        self._Limit = params.get("Limit")
        self._Offset = params.get("Offset")
        self._OrderBy = params.get("OrderBy")
        self._OrderByType = params.get("OrderByType")
        self._ProjectIds = params.get("ProjectIds")
        self._SearchKey = params.get("SearchKey")
        if params.get("Tags") is not None:
            self._Tags = []
            for item in params.get("Tags"):
                obj = TagInfo()
                obj._deserialize(item)
                self._Tags.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBInstancesResponse(AbstractModel):
    """DescribeDBInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 符合查询条件的实例总数。
        :type TotalCount: int
        :param _InstanceDetails: 实例详细信息列表。
        :type InstanceDetails: list of InstanceDetail
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._InstanceDetails = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def InstanceDetails(self):
        return self._InstanceDetails

    @InstanceDetails.setter
    def InstanceDetails(self, InstanceDetails):
        self._InstanceDetails = InstanceDetails

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("InstanceDetails") is not None:
            self._InstanceDetails = []
            for item in params.get("InstanceDetails"):
                obj = InstanceDetail()
                obj._deserialize(item)
                self._InstanceDetails.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeInstanceParamsRequest(AbstractModel):
    """DescribeInstanceParams请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 指定待查询参数列表的实例ID。例如：cmgo-p8vn****。请登录 [MongoDB 控制台](https://console.cloud.tencent.com/mongodb)在实例列表复制实例 ID。
        :type InstanceId: str
        """
        self._InstanceId = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeInstanceParamsResponse(AbstractModel):
    """DescribeInstanceParams返回参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceEnumParam: 参数值为枚举类型参数集合。
        :type InstanceEnumParam: list of InstanceEnumParam
        :param _InstanceIntegerParam: 参数值为 Integer 类型参数集合。
        :type InstanceIntegerParam: list of InstanceIntegerParam
        :param _InstanceTextParam: 参数值为 Text 类型的参数集合。
        :type InstanceTextParam: list of InstanceTextParam
        :param _InstanceMultiParam: 参数值为混合类型的参数集合。
        :type InstanceMultiParam: list of InstanceMultiParam
        :param _TotalCount: 当前实例支持修改的参数个数统计 如0
        :type TotalCount: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._InstanceEnumParam = None
        self._InstanceIntegerParam = None
        self._InstanceTextParam = None
        self._InstanceMultiParam = None
        self._TotalCount = None
        self._RequestId = None

    @property
    def InstanceEnumParam(self):
        return self._InstanceEnumParam

    @InstanceEnumParam.setter
    def InstanceEnumParam(self, InstanceEnumParam):
        self._InstanceEnumParam = InstanceEnumParam

    @property
    def InstanceIntegerParam(self):
        return self._InstanceIntegerParam

    @InstanceIntegerParam.setter
    def InstanceIntegerParam(self, InstanceIntegerParam):
        self._InstanceIntegerParam = InstanceIntegerParam

    @property
    def InstanceTextParam(self):
        return self._InstanceTextParam

    @InstanceTextParam.setter
    def InstanceTextParam(self, InstanceTextParam):
        self._InstanceTextParam = InstanceTextParam

    @property
    def InstanceMultiParam(self):
        return self._InstanceMultiParam

    @InstanceMultiParam.setter
    def InstanceMultiParam(self, InstanceMultiParam):
        self._InstanceMultiParam = InstanceMultiParam

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("InstanceEnumParam") is not None:
            self._InstanceEnumParam = []
            for item in params.get("InstanceEnumParam"):
                obj = InstanceEnumParam()
                obj._deserialize(item)
                self._InstanceEnumParam.append(obj)
        if params.get("InstanceIntegerParam") is not None:
            self._InstanceIntegerParam = []
            for item in params.get("InstanceIntegerParam"):
                obj = InstanceIntegerParam()
                obj._deserialize(item)
                self._InstanceIntegerParam.append(obj)
        if params.get("InstanceTextParam") is not None:
            self._InstanceTextParam = []
            for item in params.get("InstanceTextParam"):
                obj = InstanceTextParam()
                obj._deserialize(item)
                self._InstanceTextParam.append(obj)
        if params.get("InstanceMultiParam") is not None:
            self._InstanceMultiParam = []
            for item in params.get("InstanceMultiParam"):
                obj = InstanceMultiParam()
                obj._deserialize(item)
                self._InstanceMultiParam.append(obj)
        self._TotalCount = params.get("TotalCount")
        self._RequestId = params.get("RequestId")


class DescribeSecurityGroupRequest(AbstractModel):
    """DescribeSecurityGroup请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例 ID。例如：cmgo-p8vn****。
        :type InstanceId: str
        """
        self._InstanceId = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSecurityGroupResponse(AbstractModel):
    """DescribeSecurityGroup返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Groups: 实例绑定的安全组信息。
        :type Groups: list of SecurityGroup
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Groups = None
        self._RequestId = None

    @property
    def Groups(self):
        return self._Groups

    @Groups.setter
    def Groups(self, Groups):
        self._Groups = Groups

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Groups") is not None:
            self._Groups = []
            for item in params.get("Groups"):
                obj = SecurityGroup()
                obj._deserialize(item)
                self._Groups.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeSlowLogPatternsRequest(AbstractModel):
    """DescribeSlowLogPatterns请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID，格式如：cmgo-p8vnipr5。与云数据库控制台页面中显示的实例ID相同
        :type InstanceId: str
        :param _StartTime: 慢日志起始时间，格式：yyyy-mm-dd hh:mm:ss，如：2019-06-01 10:00:00。查询起止时间间隔不能超过24小时，只允许查询最近7天内慢日志。
        :type StartTime: str
        :param _EndTime: 慢日志终止时间，格式：yyyy-mm-dd hh:mm:ss，如：2019-06-02 12:00:00。查询起止时间间隔不能超过24小时，只允许查询最近7天内慢日志。
        :type EndTime: str
        :param _SlowMS: 慢日志执行时间阈值，返回执行时间超过该阈值的慢日志，单位为毫秒(ms)，最小为100毫秒。
        :type SlowMS: int
        :param _Offset: 偏移量，最小值为0，最大值为10000，默认值为0。
        :type Offset: int
        :param _Limit: 分页大小，最小值为1，最大值为100，默认值为20。
        :type Limit: int
        :param _Format: 慢日志返回格式，可设置为json，不传默认返回原生慢日志格式。
        :type Format: str
        """
        self._InstanceId = None
        self._StartTime = None
        self._EndTime = None
        self._SlowMS = None
        self._Offset = None
        self._Limit = None
        self._Format = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def StartTime(self):
        return self._StartTime

    @StartTime.setter
    def StartTime(self, StartTime):
        self._StartTime = StartTime

    @property
    def EndTime(self):
        return self._EndTime

    @EndTime.setter
    def EndTime(self, EndTime):
        self._EndTime = EndTime

    @property
    def SlowMS(self):
        return self._SlowMS

    @SlowMS.setter
    def SlowMS(self, SlowMS):
        self._SlowMS = SlowMS

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Format(self):
        return self._Format

    @Format.setter
    def Format(self, Format):
        self._Format = Format


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._StartTime = params.get("StartTime")
        self._EndTime = params.get("EndTime")
        self._SlowMS = params.get("SlowMS")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        self._Format = params.get("Format")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSlowLogPatternsResponse(AbstractModel):
    """DescribeSlowLogPatterns返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Count: 慢日志统计信息总数
        :type Count: int
        :param _SlowLogPatterns: 慢日志统计信息
        :type SlowLogPatterns: list of SlowLogPattern
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Count = None
        self._SlowLogPatterns = None
        self._RequestId = None

    @property
    def Count(self):
        return self._Count

    @Count.setter
    def Count(self, Count):
        self._Count = Count

    @property
    def SlowLogPatterns(self):
        return self._SlowLogPatterns

    @SlowLogPatterns.setter
    def SlowLogPatterns(self, SlowLogPatterns):
        self._SlowLogPatterns = SlowLogPatterns

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Count = params.get("Count")
        if params.get("SlowLogPatterns") is not None:
            self._SlowLogPatterns = []
            for item in params.get("SlowLogPatterns"):
                obj = SlowLogPattern()
                obj._deserialize(item)
                self._SlowLogPatterns.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeSlowLogsRequest(AbstractModel):
    """DescribeSlowLogs请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID，格式如：cmgo-p8vnipr5。与云数据库控制台页面中显示的实例ID相同
        :type InstanceId: str
        :param _StartTime: 慢日志起始时间，格式：yyyy-mm-dd hh:mm:ss，如：2019-06-01 10:00:00。查询起止时间间隔不能超过24小时，只允许查询最近7天内慢日志。
        :type StartTime: str
        :param _EndTime: 慢日志终止时间，格式：yyyy-mm-dd hh:mm:ss，如：2019-06-02 12:00:00。查询起止时间间隔不能超过24小时，只允许查询最近7天内慢日志。
        :type EndTime: str
        :param _SlowMS: 慢日志执行时间阈值，返回执行时间超过该阈值的慢日志，单位为毫秒(ms)，最小为100毫秒。
        :type SlowMS: int
        :param _Offset: 偏移量，最小值为0，最大值为10000，默认值为0。
        :type Offset: int
        :param _Limit: 分页大小，最小值为1，最大值为100，默认值为20。
        :type Limit: int
        :param _Format: 慢日志返回格式。默认返回原生慢日志格式，4.4及以上版本可设置为json。
        :type Format: str
        """
        self._InstanceId = None
        self._StartTime = None
        self._EndTime = None
        self._SlowMS = None
        self._Offset = None
        self._Limit = None
        self._Format = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def StartTime(self):
        return self._StartTime

    @StartTime.setter
    def StartTime(self, StartTime):
        self._StartTime = StartTime

    @property
    def EndTime(self):
        return self._EndTime

    @EndTime.setter
    def EndTime(self, EndTime):
        self._EndTime = EndTime

    @property
    def SlowMS(self):
        return self._SlowMS

    @SlowMS.setter
    def SlowMS(self, SlowMS):
        self._SlowMS = SlowMS

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Format(self):
        return self._Format

    @Format.setter
    def Format(self, Format):
        self._Format = Format


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._StartTime = params.get("StartTime")
        self._EndTime = params.get("EndTime")
        self._SlowMS = params.get("SlowMS")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        self._Format = params.get("Format")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSlowLogsResponse(AbstractModel):
    """DescribeSlowLogs返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Count: 慢日志总数
        :type Count: int
        :param _SlowLogs: 慢日志详情
注意：此字段可能返回 null，表示取不到有效值。
        :type SlowLogs: list of str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Count = None
        self._SlowLogs = None
        self._RequestId = None

    @property
    def Count(self):
        return self._Count

    @Count.setter
    def Count(self, Count):
        self._Count = Count

    @property
    def SlowLogs(self):
        return self._SlowLogs

    @SlowLogs.setter
    def SlowLogs(self, SlowLogs):
        self._SlowLogs = SlowLogs

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Count = params.get("Count")
        self._SlowLogs = params.get("SlowLogs")
        self._RequestId = params.get("RequestId")


class DescribeSpecInfoRequest(AbstractModel):
    """DescribeSpecInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Zone: 待查询可用区
        :type Zone: str
        """
        self._Zone = None

    @property
    def Zone(self):
        return self._Zone

    @Zone.setter
    def Zone(self, Zone):
        self._Zone = Zone


    def _deserialize(self, params):
        self._Zone = params.get("Zone")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSpecInfoResponse(AbstractModel):
    """DescribeSpecInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param _SpecInfoList: 实例售卖规格信息列表
        :type SpecInfoList: list of SpecificationInfo
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._SpecInfoList = None
        self._RequestId = None

    @property
    def SpecInfoList(self):
        return self._SpecInfoList

    @SpecInfoList.setter
    def SpecInfoList(self, SpecInfoList):
        self._SpecInfoList = SpecInfoList

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("SpecInfoList") is not None:
            self._SpecInfoList = []
            for item in params.get("SpecInfoList"):
                obj = SpecificationInfo()
                obj._deserialize(item)
                self._SpecInfoList.append(obj)
        self._RequestId = params.get("RequestId")


class FlushInstanceRouterConfigRequest(AbstractModel):
    """FlushInstanceRouterConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID
        :type InstanceId: str
        """
        self._InstanceId = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FlushInstanceRouterConfigResponse(AbstractModel):
    """FlushInstanceRouterConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class InquirePriceCreateDBInstancesRequest(AbstractModel):
    """InquirePriceCreateDBInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Zone: 实例所属区域及可用区信息。格式：ap-guangzhou-2。
        :type Zone: str
        :param _NodeNum: 每个分片的主从节点数量。<br>取值范围：请通过接口<a href="https://cloud.tencent.com/document/product/240/38567">DescribeSpecInfo</a>查询，其返回的数据结构SpecItems中的参数MinNodeNum与MaxNodeNum分别对应其最小值与最大值。</li></ul>
        :type NodeNum: int
        :param _Memory: 实例内存大小。<ul><li>单位：GB。</li><li>取值范围：请通过接口<a href="https://cloud.tencent.com/document/product/240/38567">DescribeSpecInfo</a>查询，其返回的数据结构SpecItems中的参数CPU与Memory分别对应CPU核数与内存规格。</li></ul>
        :type Memory: int
        :param _Volume: 实例硬盘大小。<ul><li>单位：GB。</li><li>取值范围：请通过接口<a href="https://cloud.tencent.com/document/product/240/38567">DescribeSpecInfo</a>查询，其返回的数据结构SpecItems中的参数MinStorage与MaxStorage分别对应其最小磁盘规格与最大磁盘规格。</br>
        :type Volume: int
        :param _MongoVersion: 实例版本信息。<ul><li>具体支持的版本，请通过接口<a href="https://cloud.tencent.com/document/product/240/38567">DescribeSpecInfo</a>查询，其返回的数据结构SpecItems中的参数MongoVersionCode为实例所支持的版本信息。</li><li>版本信息与版本号对应关系如下：<ul><li>MONGO_3_WT：MongoDB 3.2 WiredTiger存储引擎版本。</li><li>MONGO_3_ROCKS：MongoDB 3.2 RocksDB存储引擎版本。</li><li>MONGO_36_WT：MongoDB 3.6 WiredTiger存储引擎版本。</li><li>MONGO_40_WT：MongoDB 4.0 WiredTiger存储引擎版本。</li><li>MONGO_42_WT：MongoDB 4.2 WiredTiger存储引擎版本。</li><li>MONGO_44_WT：MongoDB 4.4 WiredTiger存储引擎版本。</li></ul>
        :type MongoVersion: str
        :param _MachineCode: 机器类型。<ul><li>HIO：高IO型。</li><li>HIO10G：高IO万兆型。</li></ul>
        :type MachineCode: str
        :param _GoodsNum: 实例数量，取值范围为[1,10]。
        :type GoodsNum: int
        :param _ClusterType: 实例类型。<ul><li>REPLSET：副本集。</li><li>SHARD：分片集群。</li><li>STANDALONE：单节点。</li></ul>
        :type ClusterType: str
        :param _ReplicateSetNum: 副本集个数。<ul><li>创建副本集实例时，该参数固定设置为1。</li><li>创建分片集群时，指分片数量，请通过接口<a href="https://cloud.tencent.com/document/product/240/38567">DescribeSpecInfo</a>查询，其返回的数据结构SpecItems中的参数MinReplicateSetNum与MaxReplicateSetNum分别对应其最小值与最大值。</li><li>若为单节点实例，该参数固定设置为0。</li></ul>
        :type ReplicateSetNum: int
        :param _Period: 选择包年包月计费模式时，您需要设定购买实例的时长。即<b>InstanceChargeType</b>设定为<b>PREPAID</b>时，该参数必须配置。<ul><li>单位：月。</li><li>可选值包括[1,2,3,4,5,6,7,8,9,10,11,12,24,36]。</li></ul>
        :type Period: int
        :param _InstanceChargeType: 实例付费方式。<ul><li>PREPAID：包年包月计费。</li><li>POSTPAID_BY_HOUR：按量计费。</li></ul>
        :type InstanceChargeType: str
        :param _MongosCpu: 分片实例询价必填参数，指 Mongos CPU核数，取值范围为[1,16]。
        :type MongosCpu: int
        :param _MongosMemory: 分片实例询价必填参数，指 Mongos 内存，取值范围为[2,32]，单位：GB。
        :type MongosMemory: int
        :param _MongosNum: 分片实例询价必填参数，指 Mongos 个数，取值范围为[3,32]。
        :type MongosNum: int
        :param _ConfigServerCpu: 分片实例询价必填参数，指 ConfigServer CPU核数，取值为1，单位：GB。
        :type ConfigServerCpu: int
        :param _ConfigServerMemory: 分片实例询价必填参数，指 ConfigServer 内存大小，取值为2，单位：GB。
        :type ConfigServerMemory: int
        :param _ConfigServerVolume: 分片实例询价必填参数，指 ConfigServer 磁盘大小，取值为 20，单位：GB。
        :type ConfigServerVolume: int
        """
        self._Zone = None
        self._NodeNum = None
        self._Memory = None
        self._Volume = None
        self._MongoVersion = None
        self._MachineCode = None
        self._GoodsNum = None
        self._ClusterType = None
        self._ReplicateSetNum = None
        self._Period = None
        self._InstanceChargeType = None
        self._MongosCpu = None
        self._MongosMemory = None
        self._MongosNum = None
        self._ConfigServerCpu = None
        self._ConfigServerMemory = None
        self._ConfigServerVolume = None

    @property
    def Zone(self):
        return self._Zone

    @Zone.setter
    def Zone(self, Zone):
        self._Zone = Zone

    @property
    def NodeNum(self):
        return self._NodeNum

    @NodeNum.setter
    def NodeNum(self, NodeNum):
        self._NodeNum = NodeNum

    @property
    def Memory(self):
        return self._Memory

    @Memory.setter
    def Memory(self, Memory):
        self._Memory = Memory

    @property
    def Volume(self):
        return self._Volume

    @Volume.setter
    def Volume(self, Volume):
        self._Volume = Volume

    @property
    def MongoVersion(self):
        return self._MongoVersion

    @MongoVersion.setter
    def MongoVersion(self, MongoVersion):
        self._MongoVersion = MongoVersion

    @property
    def MachineCode(self):
        return self._MachineCode

    @MachineCode.setter
    def MachineCode(self, MachineCode):
        self._MachineCode = MachineCode

    @property
    def GoodsNum(self):
        return self._GoodsNum

    @GoodsNum.setter
    def GoodsNum(self, GoodsNum):
        self._GoodsNum = GoodsNum

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType

    @property
    def ReplicateSetNum(self):
        return self._ReplicateSetNum

    @ReplicateSetNum.setter
    def ReplicateSetNum(self, ReplicateSetNum):
        self._ReplicateSetNum = ReplicateSetNum

    @property
    def Period(self):
        return self._Period

    @Period.setter
    def Period(self, Period):
        self._Period = Period

    @property
    def InstanceChargeType(self):
        return self._InstanceChargeType

    @InstanceChargeType.setter
    def InstanceChargeType(self, InstanceChargeType):
        self._InstanceChargeType = InstanceChargeType

    @property
    def MongosCpu(self):
        return self._MongosCpu

    @MongosCpu.setter
    def MongosCpu(self, MongosCpu):
        self._MongosCpu = MongosCpu

    @property
    def MongosMemory(self):
        return self._MongosMemory

    @MongosMemory.setter
    def MongosMemory(self, MongosMemory):
        self._MongosMemory = MongosMemory

    @property
    def MongosNum(self):
        return self._MongosNum

    @MongosNum.setter
    def MongosNum(self, MongosNum):
        self._MongosNum = MongosNum

    @property
    def ConfigServerCpu(self):
        return self._ConfigServerCpu

    @ConfigServerCpu.setter
    def ConfigServerCpu(self, ConfigServerCpu):
        self._ConfigServerCpu = ConfigServerCpu

    @property
    def ConfigServerMemory(self):
        return self._ConfigServerMemory

    @ConfigServerMemory.setter
    def ConfigServerMemory(self, ConfigServerMemory):
        self._ConfigServerMemory = ConfigServerMemory

    @property
    def ConfigServerVolume(self):
        return self._ConfigServerVolume

    @ConfigServerVolume.setter
    def ConfigServerVolume(self, ConfigServerVolume):
        self._ConfigServerVolume = ConfigServerVolume


    def _deserialize(self, params):
        self._Zone = params.get("Zone")
        self._NodeNum = params.get("NodeNum")
        self._Memory = params.get("Memory")
        self._Volume = params.get("Volume")
        self._MongoVersion = params.get("MongoVersion")
        self._MachineCode = params.get("MachineCode")
        self._GoodsNum = params.get("GoodsNum")
        self._ClusterType = params.get("ClusterType")
        self._ReplicateSetNum = params.get("ReplicateSetNum")
        self._Period = params.get("Period")
        self._InstanceChargeType = params.get("InstanceChargeType")
        self._MongosCpu = params.get("MongosCpu")
        self._MongosMemory = params.get("MongosMemory")
        self._MongosNum = params.get("MongosNum")
        self._ConfigServerCpu = params.get("ConfigServerCpu")
        self._ConfigServerMemory = params.get("ConfigServerMemory")
        self._ConfigServerVolume = params.get("ConfigServerVolume")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquirePriceCreateDBInstancesResponse(AbstractModel):
    """InquirePriceCreateDBInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Price: 价格
        :type Price: :class:`tencentcloud.mongodb.v20190725.models.DBInstancePrice`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Price = None
        self._RequestId = None

    @property
    def Price(self):
        return self._Price

    @Price.setter
    def Price(self, Price):
        self._Price = Price

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Price") is not None:
            self._Price = DBInstancePrice()
            self._Price._deserialize(params.get("Price"))
        self._RequestId = params.get("RequestId")


class InquirePriceModifyDBInstanceSpecRequest(AbstractModel):
    """InquirePriceModifyDBInstanceSpec请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例 ID，格式如：cmgo-p8vn****。与云数据库控制台页面中显示的实例ID相同。
        :type InstanceId: str
        :param _Memory: 变更配置后实例内存大小，单位：GB。
        :type Memory: int
        :param _Volume: 变更配置后实例磁盘大小，单位：GB。
        :type Volume: int
        :param _NodeNum: 实例节点数。默认为不变更节点数，暂不支持变更。
        :type NodeNum: int
        :param _ReplicateSetNum: 实例分片数。默认为不变更分片数，暂不支持变更。
        :type ReplicateSetNum: int
        """
        self._InstanceId = None
        self._Memory = None
        self._Volume = None
        self._NodeNum = None
        self._ReplicateSetNum = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Memory(self):
        return self._Memory

    @Memory.setter
    def Memory(self, Memory):
        self._Memory = Memory

    @property
    def Volume(self):
        return self._Volume

    @Volume.setter
    def Volume(self, Volume):
        self._Volume = Volume

    @property
    def NodeNum(self):
        return self._NodeNum

    @NodeNum.setter
    def NodeNum(self, NodeNum):
        self._NodeNum = NodeNum

    @property
    def ReplicateSetNum(self):
        return self._ReplicateSetNum

    @ReplicateSetNum.setter
    def ReplicateSetNum(self, ReplicateSetNum):
        self._ReplicateSetNum = ReplicateSetNum


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._Memory = params.get("Memory")
        self._Volume = params.get("Volume")
        self._NodeNum = params.get("NodeNum")
        self._ReplicateSetNum = params.get("ReplicateSetNum")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquirePriceModifyDBInstanceSpecResponse(AbstractModel):
    """InquirePriceModifyDBInstanceSpec返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Price: 价格。
        :type Price: :class:`tencentcloud.mongodb.v20190725.models.DBInstancePrice`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Price = None
        self._RequestId = None

    @property
    def Price(self):
        return self._Price

    @Price.setter
    def Price(self, Price):
        self._Price = Price

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Price") is not None:
            self._Price = DBInstancePrice()
            self._Price._deserialize(params.get("Price"))
        self._RequestId = params.get("RequestId")


class InquirePriceRenewDBInstancesRequest(AbstractModel):
    """InquirePriceRenewDBInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceIds: 实例ID，格式如：cmgo-p8vnipr5。与云数据库控制台页面中显示的实例ID相同，接口单次最多只支持5个实例进行操作。
        :type InstanceIds: list of str
        :param _InstanceChargePrepaid: 预付费模式（即包年包月）相关参数设置。通过该参数可以指定包年包月实例的续费时长、是否设置自动续费等属性。
        :type InstanceChargePrepaid: :class:`tencentcloud.mongodb.v20190725.models.InstanceChargePrepaid`
        """
        self._InstanceIds = None
        self._InstanceChargePrepaid = None

    @property
    def InstanceIds(self):
        return self._InstanceIds

    @InstanceIds.setter
    def InstanceIds(self, InstanceIds):
        self._InstanceIds = InstanceIds

    @property
    def InstanceChargePrepaid(self):
        return self._InstanceChargePrepaid

    @InstanceChargePrepaid.setter
    def InstanceChargePrepaid(self, InstanceChargePrepaid):
        self._InstanceChargePrepaid = InstanceChargePrepaid


    def _deserialize(self, params):
        self._InstanceIds = params.get("InstanceIds")
        if params.get("InstanceChargePrepaid") is not None:
            self._InstanceChargePrepaid = InstanceChargePrepaid()
            self._InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquirePriceRenewDBInstancesResponse(AbstractModel):
    """InquirePriceRenewDBInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Price: 价格
        :type Price: :class:`tencentcloud.mongodb.v20190725.models.DBInstancePrice`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Price = None
        self._RequestId = None

    @property
    def Price(self):
        return self._Price

    @Price.setter
    def Price(self, Price):
        self._Price = Price

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Price") is not None:
            self._Price = DBInstancePrice()
            self._Price._deserialize(params.get("Price"))
        self._RequestId = params.get("RequestId")


class InstanceChargePrepaid(AbstractModel):
    """描述了实例的计费模式

    """

    def __init__(self):
        r"""
        :param _Period: 购买实例的时长，单位：月。取值范围：1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, 36。默认为1。
（InquirePriceRenewDBInstances，RenewDBInstances调用时必填）
        :type Period: int
        :param _RenewFlag: 自动续费标识。取值范围：
NOTIFY_AND_AUTO_RENEW：通知过期且自动续费
NOTIFY_AND_MANUAL_RENEW：通知过期不自动续费
DISABLE_NOTIFY_AND_MANUAL_RENEW：不通知过期不自动续费

默认取值：NOTIFY_AND_MANUAL_RENEW。若该参数指定为NOTIFY_AND_AUTO_RENEW，在账户余额充足的情况下，实例到期后将按月自动续费。
（InquirePriceRenewDBInstances，RenewDBInstances调用时必填）
        :type RenewFlag: str
        """
        self._Period = None
        self._RenewFlag = None

    @property
    def Period(self):
        return self._Period

    @Period.setter
    def Period(self, Period):
        self._Period = Period

    @property
    def RenewFlag(self):
        return self._RenewFlag

    @RenewFlag.setter
    def RenewFlag(self, RenewFlag):
        self._RenewFlag = RenewFlag


    def _deserialize(self, params):
        self._Period = params.get("Period")
        self._RenewFlag = params.get("RenewFlag")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceDetail(AbstractModel):
    """实例详情

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID。
        :type InstanceId: str
        :param _InstanceName: 实例名称。
        :type InstanceName: str
        :param _PayMode: 付费类型，可能的返回值：1-包年包月；0-按量计费
        :type PayMode: int
        :param _ProjectId: 项目ID。
        :type ProjectId: int
        :param _ClusterType: 集群类型，可能的返回值：0-副本集实例，1-分片实例。
        :type ClusterType: int
        :param _Region: 地域信息。
        :type Region: str
        :param _Zone: 可用区信息。
        :type Zone: str
        :param _NetType: 网络类型，可能的返回值：0-基础网络，1-私有网络
        :type NetType: int
        :param _VpcId: 私有网络的ID。
        :type VpcId: str
        :param _SubnetId: 私有网络的子网ID。
        :type SubnetId: str
        :param _Status: 实例状态，可能的返回值：0-待初始化，1-流程处理中，2-运行中，-2-实例已过期。
        :type Status: int
        :param _Vip: 实例IP。
        :type Vip: str
        :param _Vport: 端口号。
        :type Vport: int
        :param _CreateTime: 实例创建时间。
        :type CreateTime: str
        :param _DeadLine: 实例到期时间。
        :type DeadLine: str
        :param _MongoVersion: 实例版本信息。
        :type MongoVersion: str
        :param _Memory: 实例内存规格，单位为MB。
        :type Memory: int
        :param _Volume: 实例磁盘规格，单位为MB。
        :type Volume: int
        :param _CpuNum: 实例CPU核心数。
        :type CpuNum: int
        :param _MachineType: 实例机器类型。
        :type MachineType: str
        :param _SecondaryNum: 实例从节点数。
        :type SecondaryNum: int
        :param _ReplicationSetNum: 实例分片数。
        :type ReplicationSetNum: int
        :param _AutoRenewFlag: 实例自动续费标志，可能的返回值：0-手动续费，1-自动续费，2-确认不续费。
        :type AutoRenewFlag: int
        :param _UsedVolume: 已用容量，单位MB。
        :type UsedVolume: int
        :param _MaintenanceStart: 维护窗口起始时间。
        :type MaintenanceStart: str
        :param _MaintenanceEnd: 维护窗口结束时间。
        :type MaintenanceEnd: str
        :param _ReplicaSets: 分片信息。
        :type ReplicaSets: list of ShardInfo
        :param _ReadonlyInstances: 只读实例信息。
        :type ReadonlyInstances: list of DBInstanceInfo
        :param _StandbyInstances: 灾备实例信息。
        :type StandbyInstances: list of DBInstanceInfo
        :param _CloneInstances: 临时实例信息。
        :type CloneInstances: list of DBInstanceInfo
        :param _RelatedInstance: 关联实例信息，对于正式实例，该字段表示它的临时实例信息；对于临时实例，则表示它的正式实例信息;如果为只读/灾备实例,则表示他的主实例信息。
        :type RelatedInstance: :class:`tencentcloud.mongodb.v20190725.models.DBInstanceInfo`
        :param _Tags: 实例标签信息集合。
        :type Tags: list of TagInfo
        :param _InstanceVer: 实例版本标记。
        :type InstanceVer: int
        :param _ClusterVer: 实例版本标记。
        :type ClusterVer: int
        :param _Protocol: 协议信息，可能的返回值：1-mongodb，2-dynamodb。
        :type Protocol: int
        :param _InstanceType: 实例类型，可能的返回值，1-正式实例，2-临时实例，3-只读实例，4-灾备实例
        :type InstanceType: int
        :param _InstanceStatusDesc: 实例状态描述
        :type InstanceStatusDesc: str
        :param _RealInstanceId: 实例对应的物理实例id，回档并替换过的实例有不同的InstanceId和RealInstanceId，从barad获取监控数据等场景下需要用物理id获取
        :type RealInstanceId: str
        :param _MongosNodeNum: mongos节点个数。
注意：此字段可能返回 null，表示取不到有效值。
        :type MongosNodeNum: int
        :param _MongosMemory: mongos节点内存。
注意：此字段可能返回 null，表示取不到有效值。
        :type MongosMemory: int
        :param _MongosCpuNum: mongos节点CPU核数。
注意：此字段可能返回 null，表示取不到有效值。
        :type MongosCpuNum: int
        :param _ConfigServerNodeNum: Config Server节点个数。
注意：此字段可能返回 null，表示取不到有效值。
        :type ConfigServerNodeNum: int
        :param _ConfigServerMemory: Config Server节点内存。
注意：此字段可能返回 null，表示取不到有效值。
        :type ConfigServerMemory: int
        :param _ConfigServerVolume: Config Server节点磁盘大小。
注意：此字段可能返回 null，表示取不到有效值。
        :type ConfigServerVolume: int
        :param _ConfigServerCpuNum: Config Server节点CPU核数。
注意：此字段可能返回 null，表示取不到有效值。
        :type ConfigServerCpuNum: int
        :param _ReadonlyNodeNum: readonly节点个数。
注意：此字段可能返回 null，表示取不到有效值。
        :type ReadonlyNodeNum: int
        """
        self._InstanceId = None
        self._InstanceName = None
        self._PayMode = None
        self._ProjectId = None
        self._ClusterType = None
        self._Region = None
        self._Zone = None
        self._NetType = None
        self._VpcId = None
        self._SubnetId = None
        self._Status = None
        self._Vip = None
        self._Vport = None
        self._CreateTime = None
        self._DeadLine = None
        self._MongoVersion = None
        self._Memory = None
        self._Volume = None
        self._CpuNum = None
        self._MachineType = None
        self._SecondaryNum = None
        self._ReplicationSetNum = None
        self._AutoRenewFlag = None
        self._UsedVolume = None
        self._MaintenanceStart = None
        self._MaintenanceEnd = None
        self._ReplicaSets = None
        self._ReadonlyInstances = None
        self._StandbyInstances = None
        self._CloneInstances = None
        self._RelatedInstance = None
        self._Tags = None
        self._InstanceVer = None
        self._ClusterVer = None
        self._Protocol = None
        self._InstanceType = None
        self._InstanceStatusDesc = None
        self._RealInstanceId = None
        self._MongosNodeNum = None
        self._MongosMemory = None
        self._MongosCpuNum = None
        self._ConfigServerNodeNum = None
        self._ConfigServerMemory = None
        self._ConfigServerVolume = None
        self._ConfigServerCpuNum = None
        self._ReadonlyNodeNum = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def InstanceName(self):
        return self._InstanceName

    @InstanceName.setter
    def InstanceName(self, InstanceName):
        self._InstanceName = InstanceName

    @property
    def PayMode(self):
        return self._PayMode

    @PayMode.setter
    def PayMode(self, PayMode):
        self._PayMode = PayMode

    @property
    def ProjectId(self):
        return self._ProjectId

    @ProjectId.setter
    def ProjectId(self, ProjectId):
        self._ProjectId = ProjectId

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType

    @property
    def Region(self):
        return self._Region

    @Region.setter
    def Region(self, Region):
        self._Region = Region

    @property
    def Zone(self):
        return self._Zone

    @Zone.setter
    def Zone(self, Zone):
        self._Zone = Zone

    @property
    def NetType(self):
        return self._NetType

    @NetType.setter
    def NetType(self, NetType):
        self._NetType = NetType

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def Vip(self):
        return self._Vip

    @Vip.setter
    def Vip(self, Vip):
        self._Vip = Vip

    @property
    def Vport(self):
        return self._Vport

    @Vport.setter
    def Vport(self, Vport):
        self._Vport = Vport

    @property
    def CreateTime(self):
        return self._CreateTime

    @CreateTime.setter
    def CreateTime(self, CreateTime):
        self._CreateTime = CreateTime

    @property
    def DeadLine(self):
        return self._DeadLine

    @DeadLine.setter
    def DeadLine(self, DeadLine):
        self._DeadLine = DeadLine

    @property
    def MongoVersion(self):
        return self._MongoVersion

    @MongoVersion.setter
    def MongoVersion(self, MongoVersion):
        self._MongoVersion = MongoVersion

    @property
    def Memory(self):
        return self._Memory

    @Memory.setter
    def Memory(self, Memory):
        self._Memory = Memory

    @property
    def Volume(self):
        return self._Volume

    @Volume.setter
    def Volume(self, Volume):
        self._Volume = Volume

    @property
    def CpuNum(self):
        return self._CpuNum

    @CpuNum.setter
    def CpuNum(self, CpuNum):
        self._CpuNum = CpuNum

    @property
    def MachineType(self):
        return self._MachineType

    @MachineType.setter
    def MachineType(self, MachineType):
        self._MachineType = MachineType

    @property
    def SecondaryNum(self):
        return self._SecondaryNum

    @SecondaryNum.setter
    def SecondaryNum(self, SecondaryNum):
        self._SecondaryNum = SecondaryNum

    @property
    def ReplicationSetNum(self):
        return self._ReplicationSetNum

    @ReplicationSetNum.setter
    def ReplicationSetNum(self, ReplicationSetNum):
        self._ReplicationSetNum = ReplicationSetNum

    @property
    def AutoRenewFlag(self):
        return self._AutoRenewFlag

    @AutoRenewFlag.setter
    def AutoRenewFlag(self, AutoRenewFlag):
        self._AutoRenewFlag = AutoRenewFlag

    @property
    def UsedVolume(self):
        return self._UsedVolume

    @UsedVolume.setter
    def UsedVolume(self, UsedVolume):
        self._UsedVolume = UsedVolume

    @property
    def MaintenanceStart(self):
        return self._MaintenanceStart

    @MaintenanceStart.setter
    def MaintenanceStart(self, MaintenanceStart):
        self._MaintenanceStart = MaintenanceStart

    @property
    def MaintenanceEnd(self):
        return self._MaintenanceEnd

    @MaintenanceEnd.setter
    def MaintenanceEnd(self, MaintenanceEnd):
        self._MaintenanceEnd = MaintenanceEnd

    @property
    def ReplicaSets(self):
        return self._ReplicaSets

    @ReplicaSets.setter
    def ReplicaSets(self, ReplicaSets):
        self._ReplicaSets = ReplicaSets

    @property
    def ReadonlyInstances(self):
        return self._ReadonlyInstances

    @ReadonlyInstances.setter
    def ReadonlyInstances(self, ReadonlyInstances):
        self._ReadonlyInstances = ReadonlyInstances

    @property
    def StandbyInstances(self):
        return self._StandbyInstances

    @StandbyInstances.setter
    def StandbyInstances(self, StandbyInstances):
        self._StandbyInstances = StandbyInstances

    @property
    def CloneInstances(self):
        return self._CloneInstances

    @CloneInstances.setter
    def CloneInstances(self, CloneInstances):
        self._CloneInstances = CloneInstances

    @property
    def RelatedInstance(self):
        return self._RelatedInstance

    @RelatedInstance.setter
    def RelatedInstance(self, RelatedInstance):
        self._RelatedInstance = RelatedInstance

    @property
    def Tags(self):
        return self._Tags

    @Tags.setter
    def Tags(self, Tags):
        self._Tags = Tags

    @property
    def InstanceVer(self):
        return self._InstanceVer

    @InstanceVer.setter
    def InstanceVer(self, InstanceVer):
        self._InstanceVer = InstanceVer

    @property
    def ClusterVer(self):
        return self._ClusterVer

    @ClusterVer.setter
    def ClusterVer(self, ClusterVer):
        self._ClusterVer = ClusterVer

    @property
    def Protocol(self):
        return self._Protocol

    @Protocol.setter
    def Protocol(self, Protocol):
        self._Protocol = Protocol

    @property
    def InstanceType(self):
        return self._InstanceType

    @InstanceType.setter
    def InstanceType(self, InstanceType):
        self._InstanceType = InstanceType

    @property
    def InstanceStatusDesc(self):
        return self._InstanceStatusDesc

    @InstanceStatusDesc.setter
    def InstanceStatusDesc(self, InstanceStatusDesc):
        self._InstanceStatusDesc = InstanceStatusDesc

    @property
    def RealInstanceId(self):
        return self._RealInstanceId

    @RealInstanceId.setter
    def RealInstanceId(self, RealInstanceId):
        self._RealInstanceId = RealInstanceId

    @property
    def MongosNodeNum(self):
        return self._MongosNodeNum

    @MongosNodeNum.setter
    def MongosNodeNum(self, MongosNodeNum):
        self._MongosNodeNum = MongosNodeNum

    @property
    def MongosMemory(self):
        return self._MongosMemory

    @MongosMemory.setter
    def MongosMemory(self, MongosMemory):
        self._MongosMemory = MongosMemory

    @property
    def MongosCpuNum(self):
        return self._MongosCpuNum

    @MongosCpuNum.setter
    def MongosCpuNum(self, MongosCpuNum):
        self._MongosCpuNum = MongosCpuNum

    @property
    def ConfigServerNodeNum(self):
        return self._ConfigServerNodeNum

    @ConfigServerNodeNum.setter
    def ConfigServerNodeNum(self, ConfigServerNodeNum):
        self._ConfigServerNodeNum = ConfigServerNodeNum

    @property
    def ConfigServerMemory(self):
        return self._ConfigServerMemory

    @ConfigServerMemory.setter
    def ConfigServerMemory(self, ConfigServerMemory):
        self._ConfigServerMemory = ConfigServerMemory

    @property
    def ConfigServerVolume(self):
        return self._ConfigServerVolume

    @ConfigServerVolume.setter
    def ConfigServerVolume(self, ConfigServerVolume):
        self._ConfigServerVolume = ConfigServerVolume

    @property
    def ConfigServerCpuNum(self):
        return self._ConfigServerCpuNum

    @ConfigServerCpuNum.setter
    def ConfigServerCpuNum(self, ConfigServerCpuNum):
        self._ConfigServerCpuNum = ConfigServerCpuNum

    @property
    def ReadonlyNodeNum(self):
        return self._ReadonlyNodeNum

    @ReadonlyNodeNum.setter
    def ReadonlyNodeNum(self, ReadonlyNodeNum):
        self._ReadonlyNodeNum = ReadonlyNodeNum


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._InstanceName = params.get("InstanceName")
        self._PayMode = params.get("PayMode")
        self._ProjectId = params.get("ProjectId")
        self._ClusterType = params.get("ClusterType")
        self._Region = params.get("Region")
        self._Zone = params.get("Zone")
        self._NetType = params.get("NetType")
        self._VpcId = params.get("VpcId")
        self._SubnetId = params.get("SubnetId")
        self._Status = params.get("Status")
        self._Vip = params.get("Vip")
        self._Vport = params.get("Vport")
        self._CreateTime = params.get("CreateTime")
        self._DeadLine = params.get("DeadLine")
        self._MongoVersion = params.get("MongoVersion")
        self._Memory = params.get("Memory")
        self._Volume = params.get("Volume")
        self._CpuNum = params.get("CpuNum")
        self._MachineType = params.get("MachineType")
        self._SecondaryNum = params.get("SecondaryNum")
        self._ReplicationSetNum = params.get("ReplicationSetNum")
        self._AutoRenewFlag = params.get("AutoRenewFlag")
        self._UsedVolume = params.get("UsedVolume")
        self._MaintenanceStart = params.get("MaintenanceStart")
        self._MaintenanceEnd = params.get("MaintenanceEnd")
        if params.get("ReplicaSets") is not None:
            self._ReplicaSets = []
            for item in params.get("ReplicaSets"):
                obj = ShardInfo()
                obj._deserialize(item)
                self._ReplicaSets.append(obj)
        if params.get("ReadonlyInstances") is not None:
            self._ReadonlyInstances = []
            for item in params.get("ReadonlyInstances"):
                obj = DBInstanceInfo()
                obj._deserialize(item)
                self._ReadonlyInstances.append(obj)
        if params.get("StandbyInstances") is not None:
            self._StandbyInstances = []
            for item in params.get("StandbyInstances"):
                obj = DBInstanceInfo()
                obj._deserialize(item)
                self._StandbyInstances.append(obj)
        if params.get("CloneInstances") is not None:
            self._CloneInstances = []
            for item in params.get("CloneInstances"):
                obj = DBInstanceInfo()
                obj._deserialize(item)
                self._CloneInstances.append(obj)
        if params.get("RelatedInstance") is not None:
            self._RelatedInstance = DBInstanceInfo()
            self._RelatedInstance._deserialize(params.get("RelatedInstance"))
        if params.get("Tags") is not None:
            self._Tags = []
            for item in params.get("Tags"):
                obj = TagInfo()
                obj._deserialize(item)
                self._Tags.append(obj)
        self._InstanceVer = params.get("InstanceVer")
        self._ClusterVer = params.get("ClusterVer")
        self._Protocol = params.get("Protocol")
        self._InstanceType = params.get("InstanceType")
        self._InstanceStatusDesc = params.get("InstanceStatusDesc")
        self._RealInstanceId = params.get("RealInstanceId")
        self._MongosNodeNum = params.get("MongosNodeNum")
        self._MongosMemory = params.get("MongosMemory")
        self._MongosCpuNum = params.get("MongosCpuNum")
        self._ConfigServerNodeNum = params.get("ConfigServerNodeNum")
        self._ConfigServerMemory = params.get("ConfigServerMemory")
        self._ConfigServerVolume = params.get("ConfigServerVolume")
        self._ConfigServerCpuNum = params.get("ConfigServerCpuNum")
        self._ReadonlyNodeNum = params.get("ReadonlyNodeNum")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceEnumParam(AbstractModel):
    """实例可修改参数枚举类型集合。

    """

    def __init__(self):
        r"""
        :param _CurrentValue: 参数当前值。
        :type CurrentValue: str
        :param _DefaultValue: 参数默认值。
        :type DefaultValue: str
        :param _EnumValue: 枚举值，所有支持的值。
        :type EnumValue: list of str
        :param _NeedRestart: 参数修改之后是否需要重启生效。
- 1：需要重启后生效。
- 0：无需重启，设置成功即可生效。
        :type NeedRestart: str
        :param _ParamName: 参数名称。
        :type ParamName: str
        :param _Tips: 参数说明。
        :type Tips: list of str
        :param _ValueType: 参数值类型说明。
        :type ValueType: str
        :param _Status: 是否为运行中参数值。
- 1：运行中参数值。
- 0：非运行中参数值。
        :type Status: int
        """
        self._CurrentValue = None
        self._DefaultValue = None
        self._EnumValue = None
        self._NeedRestart = None
        self._ParamName = None
        self._Tips = None
        self._ValueType = None
        self._Status = None

    @property
    def CurrentValue(self):
        return self._CurrentValue

    @CurrentValue.setter
    def CurrentValue(self, CurrentValue):
        self._CurrentValue = CurrentValue

    @property
    def DefaultValue(self):
        return self._DefaultValue

    @DefaultValue.setter
    def DefaultValue(self, DefaultValue):
        self._DefaultValue = DefaultValue

    @property
    def EnumValue(self):
        return self._EnumValue

    @EnumValue.setter
    def EnumValue(self, EnumValue):
        self._EnumValue = EnumValue

    @property
    def NeedRestart(self):
        return self._NeedRestart

    @NeedRestart.setter
    def NeedRestart(self, NeedRestart):
        self._NeedRestart = NeedRestart

    @property
    def ParamName(self):
        return self._ParamName

    @ParamName.setter
    def ParamName(self, ParamName):
        self._ParamName = ParamName

    @property
    def Tips(self):
        return self._Tips

    @Tips.setter
    def Tips(self, Tips):
        self._Tips = Tips

    @property
    def ValueType(self):
        return self._ValueType

    @ValueType.setter
    def ValueType(self, ValueType):
        self._ValueType = ValueType

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status


    def _deserialize(self, params):
        self._CurrentValue = params.get("CurrentValue")
        self._DefaultValue = params.get("DefaultValue")
        self._EnumValue = params.get("EnumValue")
        self._NeedRestart = params.get("NeedRestart")
        self._ParamName = params.get("ParamName")
        self._Tips = params.get("Tips")
        self._ValueType = params.get("ValueType")
        self._Status = params.get("Status")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceIntegerParam(AbstractModel):
    """实例可修改参数 Integer 类型集合。

    """

    def __init__(self):
        r"""
        :param _CurrentValue: 参数当前值。
        :type CurrentValue: str
        :param _DefaultValue: 参数默认值。
        :type DefaultValue: str
        :param _Max: 参数最大值。
        :type Max: str
        :param _Min: 最小值。
        :type Min: str
        :param _NeedRestart: 参数修改之后是否需要重启生效。
- 1:需要重启后生效。
- 0：无需重启，设置成功即可生效。
        :type NeedRestart: str
        :param _ParamName: 参数名称。
        :type ParamName: str
        :param _Tips: 参数说明。
        :type Tips: list of str
        :param _ValueType: 参数类型。
        :type ValueType: str
        :param _Status: 是否为运行中参数值。
- 1：运行中参数值。
- 0：非运行中参数值。
        :type Status: int
        :param _Unit: 冗余字段，可忽略。
        :type Unit: str
        """
        self._CurrentValue = None
        self._DefaultValue = None
        self._Max = None
        self._Min = None
        self._NeedRestart = None
        self._ParamName = None
        self._Tips = None
        self._ValueType = None
        self._Status = None
        self._Unit = None

    @property
    def CurrentValue(self):
        return self._CurrentValue

    @CurrentValue.setter
    def CurrentValue(self, CurrentValue):
        self._CurrentValue = CurrentValue

    @property
    def DefaultValue(self):
        return self._DefaultValue

    @DefaultValue.setter
    def DefaultValue(self, DefaultValue):
        self._DefaultValue = DefaultValue

    @property
    def Max(self):
        return self._Max

    @Max.setter
    def Max(self, Max):
        self._Max = Max

    @property
    def Min(self):
        return self._Min

    @Min.setter
    def Min(self, Min):
        self._Min = Min

    @property
    def NeedRestart(self):
        return self._NeedRestart

    @NeedRestart.setter
    def NeedRestart(self, NeedRestart):
        self._NeedRestart = NeedRestart

    @property
    def ParamName(self):
        return self._ParamName

    @ParamName.setter
    def ParamName(self, ParamName):
        self._ParamName = ParamName

    @property
    def Tips(self):
        return self._Tips

    @Tips.setter
    def Tips(self, Tips):
        self._Tips = Tips

    @property
    def ValueType(self):
        return self._ValueType

    @ValueType.setter
    def ValueType(self, ValueType):
        self._ValueType = ValueType

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def Unit(self):
        return self._Unit

    @Unit.setter
    def Unit(self, Unit):
        self._Unit = Unit


    def _deserialize(self, params):
        self._CurrentValue = params.get("CurrentValue")
        self._DefaultValue = params.get("DefaultValue")
        self._Max = params.get("Max")
        self._Min = params.get("Min")
        self._NeedRestart = params.get("NeedRestart")
        self._ParamName = params.get("ParamName")
        self._Tips = params.get("Tips")
        self._ValueType = params.get("ValueType")
        self._Status = params.get("Status")
        self._Unit = params.get("Unit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceMultiParam(AbstractModel):
    """实例可修改参数Multi类型集合。

    """

    def __init__(self):
        r"""
        :param _CurrentValue: 参数当前值。
        :type CurrentValue: str
        :param _DefaultValue: 参数默认值。
        :type DefaultValue: str
        :param _EnumValue: 参考值范围。
        :type EnumValue: list of str
        :param _NeedRestart: 参数修改后是否需要重启才会生效。
- 1：需要重启后生效。
- 0：无需重启，设置成功即可生效。
        :type NeedRestart: str
        :param _ParamName: 参数名称。
        :type ParamName: str
        :param _Status: 是否为运行中参数值。
- 1：运行中参数值。
- 0：非运行中参数值。
        :type Status: int
        :param _Tips: 参数说明。
        :type Tips: list of str
        :param _ValueType: 当前值的类型描述，默认为multi。
        :type ValueType: str
        """
        self._CurrentValue = None
        self._DefaultValue = None
        self._EnumValue = None
        self._NeedRestart = None
        self._ParamName = None
        self._Status = None
        self._Tips = None
        self._ValueType = None

    @property
    def CurrentValue(self):
        return self._CurrentValue

    @CurrentValue.setter
    def CurrentValue(self, CurrentValue):
        self._CurrentValue = CurrentValue

    @property
    def DefaultValue(self):
        return self._DefaultValue

    @DefaultValue.setter
    def DefaultValue(self, DefaultValue):
        self._DefaultValue = DefaultValue

    @property
    def EnumValue(self):
        return self._EnumValue

    @EnumValue.setter
    def EnumValue(self, EnumValue):
        self._EnumValue = EnumValue

    @property
    def NeedRestart(self):
        return self._NeedRestart

    @NeedRestart.setter
    def NeedRestart(self, NeedRestart):
        self._NeedRestart = NeedRestart

    @property
    def ParamName(self):
        return self._ParamName

    @ParamName.setter
    def ParamName(self, ParamName):
        self._ParamName = ParamName

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def Tips(self):
        return self._Tips

    @Tips.setter
    def Tips(self, Tips):
        self._Tips = Tips

    @property
    def ValueType(self):
        return self._ValueType

    @ValueType.setter
    def ValueType(self, ValueType):
        self._ValueType = ValueType


    def _deserialize(self, params):
        self._CurrentValue = params.get("CurrentValue")
        self._DefaultValue = params.get("DefaultValue")
        self._EnumValue = params.get("EnumValue")
        self._NeedRestart = params.get("NeedRestart")
        self._ParamName = params.get("ParamName")
        self._Status = params.get("Status")
        self._Tips = params.get("Tips")
        self._ValueType = params.get("ValueType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceTextParam(AbstractModel):
    """实例可修改参数为 Text 类型的参数集合。

    """

    def __init__(self):
        r"""
        :param _CurrentValue: 参数当前值。
        :type CurrentValue: str
        :param _DefaultValue: 参数默认值。
        :type DefaultValue: str
        :param _NeedRestart: 修改参数值之后是否需要重启。
        :type NeedRestart: str
        :param _ParamName: 参数名称。
        :type ParamName: str
        :param _TextValue: Text 类型参数对应的值。
        :type TextValue: str
        :param _Tips: 参数说明。
        :type Tips: list of str
        :param _ValueType: 参数值类型说明。
        :type ValueType: str
        :param _Status: 是否为运行中的参数值。
- 1：运行中参数值。
- 0：非运行中参数值。
        :type Status: str
        """
        self._CurrentValue = None
        self._DefaultValue = None
        self._NeedRestart = None
        self._ParamName = None
        self._TextValue = None
        self._Tips = None
        self._ValueType = None
        self._Status = None

    @property
    def CurrentValue(self):
        return self._CurrentValue

    @CurrentValue.setter
    def CurrentValue(self, CurrentValue):
        self._CurrentValue = CurrentValue

    @property
    def DefaultValue(self):
        return self._DefaultValue

    @DefaultValue.setter
    def DefaultValue(self, DefaultValue):
        self._DefaultValue = DefaultValue

    @property
    def NeedRestart(self):
        return self._NeedRestart

    @NeedRestart.setter
    def NeedRestart(self, NeedRestart):
        self._NeedRestart = NeedRestart

    @property
    def ParamName(self):
        return self._ParamName

    @ParamName.setter
    def ParamName(self, ParamName):
        self._ParamName = ParamName

    @property
    def TextValue(self):
        return self._TextValue

    @TextValue.setter
    def TextValue(self, TextValue):
        self._TextValue = TextValue

    @property
    def Tips(self):
        return self._Tips

    @Tips.setter
    def Tips(self, Tips):
        self._Tips = Tips

    @property
    def ValueType(self):
        return self._ValueType

    @ValueType.setter
    def ValueType(self, ValueType):
        self._ValueType = ValueType

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status


    def _deserialize(self, params):
        self._CurrentValue = params.get("CurrentValue")
        self._DefaultValue = params.get("DefaultValue")
        self._NeedRestart = params.get("NeedRestart")
        self._ParamName = params.get("ParamName")
        self._TextValue = params.get("TextValue")
        self._Tips = params.get("Tips")
        self._ValueType = params.get("ValueType")
        self._Status = params.get("Status")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class IsolateDBInstanceRequest(AbstractModel):
    """IsolateDBInstance请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID，格式如：cmgo-p8vnipr5。与云数据库控制台页面中显示的实例ID相同
        :type InstanceId: str
        """
        self._InstanceId = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class IsolateDBInstanceResponse(AbstractModel):
    """IsolateDBInstance返回参数结构体

    """

    def __init__(self):
        r"""
        :param _AsyncRequestId: 异步任务的请求 ID，可使用此 ID 查询异步任务的执行结果。
        :type AsyncRequestId: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._AsyncRequestId = None
        self._RequestId = None

    @property
    def AsyncRequestId(self):
        return self._AsyncRequestId

    @AsyncRequestId.setter
    def AsyncRequestId(self, AsyncRequestId):
        self._AsyncRequestId = AsyncRequestId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._AsyncRequestId = params.get("AsyncRequestId")
        self._RequestId = params.get("RequestId")


class KillOpsRequest(AbstractModel):
    """KillOps请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID，格式如：cmgo-p8vnipr5。与云数据库控制台页面中显示的实例ID相同
        :type InstanceId: str
        :param _Operations: 待终止的操作
        :type Operations: list of Operation
        """
        self._InstanceId = None
        self._Operations = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Operations(self):
        return self._Operations

    @Operations.setter
    def Operations(self, Operations):
        self._Operations = Operations


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        if params.get("Operations") is not None:
            self._Operations = []
            for item in params.get("Operations"):
                obj = Operation()
                obj._deserialize(item)
                self._Operations.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KillOpsResponse(AbstractModel):
    """KillOps返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ModifyDBInstanceNetworkAddressRequest(AbstractModel):
    """ModifyDBInstanceNetworkAddress请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID
        :type InstanceId: str
        :param _OldIpExpiredTime: 原IP保留时长，单位为分钟；原IP会在约定时间后释放，在释放前原IP和新IP均可访问；0表示立即回收原IP
        :type OldIpExpiredTime: int
        :param _NewUniqVpcId: 切换后IP地址的归属私有网络统一ID，若为基础网络，该字段为空
        :type NewUniqVpcId: str
        :param _NewUniqSubnetId: 切换后IP地址的归属子网统一ID，若为基础网络，该字段为空
        :type NewUniqSubnetId: str
        :param _NetworkAddresses: 待修改IP信息
        :type NetworkAddresses: list of ModifyNetworkAddress
        """
        self._InstanceId = None
        self._OldIpExpiredTime = None
        self._NewUniqVpcId = None
        self._NewUniqSubnetId = None
        self._NetworkAddresses = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def OldIpExpiredTime(self):
        return self._OldIpExpiredTime

    @OldIpExpiredTime.setter
    def OldIpExpiredTime(self, OldIpExpiredTime):
        self._OldIpExpiredTime = OldIpExpiredTime

    @property
    def NewUniqVpcId(self):
        return self._NewUniqVpcId

    @NewUniqVpcId.setter
    def NewUniqVpcId(self, NewUniqVpcId):
        self._NewUniqVpcId = NewUniqVpcId

    @property
    def NewUniqSubnetId(self):
        return self._NewUniqSubnetId

    @NewUniqSubnetId.setter
    def NewUniqSubnetId(self, NewUniqSubnetId):
        self._NewUniqSubnetId = NewUniqSubnetId

    @property
    def NetworkAddresses(self):
        return self._NetworkAddresses

    @NetworkAddresses.setter
    def NetworkAddresses(self, NetworkAddresses):
        self._NetworkAddresses = NetworkAddresses


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._OldIpExpiredTime = params.get("OldIpExpiredTime")
        self._NewUniqVpcId = params.get("NewUniqVpcId")
        self._NewUniqSubnetId = params.get("NewUniqSubnetId")
        if params.get("NetworkAddresses") is not None:
            self._NetworkAddresses = []
            for item in params.get("NetworkAddresses"):
                obj = ModifyNetworkAddress()
                obj._deserialize(item)
                self._NetworkAddresses.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDBInstanceNetworkAddressResponse(AbstractModel):
    """ModifyDBInstanceNetworkAddress返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ModifyDBInstanceSecurityGroupRequest(AbstractModel):
    """ModifyDBInstanceSecurityGroup请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例 ID。例如：cmgo-7pje****。
        :type InstanceId: str
        :param _SecurityGroupIds: 目标安全组 ID。请通过接口[DescribeSecurityGroup](https://cloud.tencent.com/document/product/240/55675)查看具体的安全组 ID。
        :type SecurityGroupIds: list of str
        """
        self._InstanceId = None
        self._SecurityGroupIds = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def SecurityGroupIds(self):
        return self._SecurityGroupIds

    @SecurityGroupIds.setter
    def SecurityGroupIds(self, SecurityGroupIds):
        self._SecurityGroupIds = SecurityGroupIds


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._SecurityGroupIds = params.get("SecurityGroupIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDBInstanceSecurityGroupResponse(AbstractModel):
    """ModifyDBInstanceSecurityGroup返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ModifyDBInstanceSpecRequest(AbstractModel):
    """ModifyDBInstanceSpec请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID，格式如：cmgo-p8vnipr5。与云数据库控制台页面中显示的实例ID相同
        :type InstanceId: str
        :param _Memory: 实例配置变更后的内存大小，单位：GB。内存和磁盘必须同时升配或同时降配
        :type Memory: int
        :param _Volume: 实例配置变更后的硬盘大小，单位：GB。内存和磁盘必须同时升配或同时降配。降配时，新的磁盘参数必须大于已用磁盘容量的1.2倍
        :type Volume: int
        :param _OplogSize: 实例配置变更后oplog的大小，单位：GB，默认为磁盘空间的10%，允许设置的最小值为磁盘的10%，最大值为磁盘的90%
        :type OplogSize: int
        :param _NodeNum: 实例变更后的节点数，取值范围具体参照查询云数据库的售卖规格返回参数。默认为不变更节点数
        :type NodeNum: int
        :param _ReplicateSetNum: 实例变更后的分片数，取值范围具体参照查询云数据库的售卖规格返回参数。只能增加不能减少，默认为不变更分片数
        :type ReplicateSetNum: int
        :param _InMaintenance: 实例配置变更的切换时间，参数为：0(默认)、1。0-调整完成时，1-维护时间内。注：调整节点数和分片数不支持在【维护时间内】变更。
        :type InMaintenance: int
        """
        self._InstanceId = None
        self._Memory = None
        self._Volume = None
        self._OplogSize = None
        self._NodeNum = None
        self._ReplicateSetNum = None
        self._InMaintenance = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Memory(self):
        return self._Memory

    @Memory.setter
    def Memory(self, Memory):
        self._Memory = Memory

    @property
    def Volume(self):
        return self._Volume

    @Volume.setter
    def Volume(self, Volume):
        self._Volume = Volume

    @property
    def OplogSize(self):
        return self._OplogSize

    @OplogSize.setter
    def OplogSize(self, OplogSize):
        self._OplogSize = OplogSize

    @property
    def NodeNum(self):
        return self._NodeNum

    @NodeNum.setter
    def NodeNum(self, NodeNum):
        self._NodeNum = NodeNum

    @property
    def ReplicateSetNum(self):
        return self._ReplicateSetNum

    @ReplicateSetNum.setter
    def ReplicateSetNum(self, ReplicateSetNum):
        self._ReplicateSetNum = ReplicateSetNum

    @property
    def InMaintenance(self):
        return self._InMaintenance

    @InMaintenance.setter
    def InMaintenance(self, InMaintenance):
        self._InMaintenance = InMaintenance


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._Memory = params.get("Memory")
        self._Volume = params.get("Volume")
        self._OplogSize = params.get("OplogSize")
        self._NodeNum = params.get("NodeNum")
        self._ReplicateSetNum = params.get("ReplicateSetNum")
        self._InMaintenance = params.get("InMaintenance")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDBInstanceSpecResponse(AbstractModel):
    """ModifyDBInstanceSpec返回参数结构体

    """

    def __init__(self):
        r"""
        :param _DealId: 订单ID
        :type DealId: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._DealId = None
        self._RequestId = None

    @property
    def DealId(self):
        return self._DealId

    @DealId.setter
    def DealId(self, DealId):
        self._DealId = DealId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._DealId = params.get("DealId")
        self._RequestId = params.get("RequestId")


class ModifyNetworkAddress(AbstractModel):
    """修改数据库地址

    """

    def __init__(self):
        r"""
        :param _NewIPAddress: 新IP地址。
        :type NewIPAddress: str
        :param _OldIpAddress: 原IP地址。
        :type OldIpAddress: str
        """
        self._NewIPAddress = None
        self._OldIpAddress = None

    @property
    def NewIPAddress(self):
        return self._NewIPAddress

    @NewIPAddress.setter
    def NewIPAddress(self, NewIPAddress):
        self._NewIPAddress = NewIPAddress

    @property
    def OldIpAddress(self):
        return self._OldIpAddress

    @OldIpAddress.setter
    def OldIpAddress(self, OldIpAddress):
        self._OldIpAddress = OldIpAddress


    def _deserialize(self, params):
        self._NewIPAddress = params.get("NewIPAddress")
        self._OldIpAddress = params.get("OldIpAddress")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NodeProperty(AbstractModel):
    """节点属性

    """

    def __init__(self):
        r"""
        :param _Zone: 节点所在的可用区。
注意：此字段可能返回 null，表示取不到有效值。
        :type Zone: str
        :param _NodeName: 节点名称。
注意：此字段可能返回 null，表示取不到有效值。
        :type NodeName: str
        :param _Address: 节点访问地址。
注意：此字段可能返回 null，表示取不到有效值。
        :type Address: str
        :param _Role: 角色。
注意：此字段可能返回 null，表示取不到有效值。
        :type Role: str
        :param _Hidden: 是否为Hidden节点
注意：此字段可能返回 null，表示取不到有效值。
        :type Hidden: bool
        :param _Status: 节点状态，包括：ORMAL/STARTUP/RECOVERING/STARTUP2/UNKNOWN/DOWN/ROLLBACK/REMOVED等。
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: str
        :param _SlaveDelay: 主从延迟，单位秒。
注意：此字段可能返回 null，表示取不到有效值。
        :type SlaveDelay: int
        :param _Priority: 节点优先级。
注意：此字段可能返回 null，表示取不到有效值。
        :type Priority: int
        :param _Votes: 节点投票权。
注意：此字段可能返回 null，表示取不到有效值。
        :type Votes: int
        :param _Tags: 节点标签。
注意：此字段可能返回 null，表示取不到有效值。
        :type Tags: list of NodeTag
        :param _ReplicateSetId: 副本集Id。
注意：此字段可能返回 null，表示取不到有效值。
        :type ReplicateSetId: str
        """
        self._Zone = None
        self._NodeName = None
        self._Address = None
        self._Role = None
        self._Hidden = None
        self._Status = None
        self._SlaveDelay = None
        self._Priority = None
        self._Votes = None
        self._Tags = None
        self._ReplicateSetId = None

    @property
    def Zone(self):
        return self._Zone

    @Zone.setter
    def Zone(self, Zone):
        self._Zone = Zone

    @property
    def NodeName(self):
        return self._NodeName

    @NodeName.setter
    def NodeName(self, NodeName):
        self._NodeName = NodeName

    @property
    def Address(self):
        return self._Address

    @Address.setter
    def Address(self, Address):
        self._Address = Address

    @property
    def Role(self):
        return self._Role

    @Role.setter
    def Role(self, Role):
        self._Role = Role

    @property
    def Hidden(self):
        return self._Hidden

    @Hidden.setter
    def Hidden(self, Hidden):
        self._Hidden = Hidden

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def SlaveDelay(self):
        return self._SlaveDelay

    @SlaveDelay.setter
    def SlaveDelay(self, SlaveDelay):
        self._SlaveDelay = SlaveDelay

    @property
    def Priority(self):
        return self._Priority

    @Priority.setter
    def Priority(self, Priority):
        self._Priority = Priority

    @property
    def Votes(self):
        return self._Votes

    @Votes.setter
    def Votes(self, Votes):
        self._Votes = Votes

    @property
    def Tags(self):
        return self._Tags

    @Tags.setter
    def Tags(self, Tags):
        self._Tags = Tags

    @property
    def ReplicateSetId(self):
        return self._ReplicateSetId

    @ReplicateSetId.setter
    def ReplicateSetId(self, ReplicateSetId):
        self._ReplicateSetId = ReplicateSetId


    def _deserialize(self, params):
        self._Zone = params.get("Zone")
        self._NodeName = params.get("NodeName")
        self._Address = params.get("Address")
        self._Role = params.get("Role")
        self._Hidden = params.get("Hidden")
        self._Status = params.get("Status")
        self._SlaveDelay = params.get("SlaveDelay")
        self._Priority = params.get("Priority")
        self._Votes = params.get("Votes")
        if params.get("Tags") is not None:
            self._Tags = []
            for item in params.get("Tags"):
                obj = NodeTag()
                obj._deserialize(item)
                self._Tags.append(obj)
        self._ReplicateSetId = params.get("ReplicateSetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NodeTag(AbstractModel):
    """节点Tag

    """

    def __init__(self):
        r"""
        :param _TagKey: 节点Tag key
注意：此字段可能返回 null，表示取不到有效值。
        :type TagKey: str
        :param _TagValue: 节点Tag Value
注意：此字段可能返回 null，表示取不到有效值。
        :type TagValue: str
        """
        self._TagKey = None
        self._TagValue = None

    @property
    def TagKey(self):
        return self._TagKey

    @TagKey.setter
    def TagKey(self, TagKey):
        self._TagKey = TagKey

    @property
    def TagValue(self):
        return self._TagValue

    @TagValue.setter
    def TagValue(self, TagValue):
        self._TagValue = TagValue


    def _deserialize(self, params):
        self._TagKey = params.get("TagKey")
        self._TagValue = params.get("TagValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OfflineIsolatedDBInstanceRequest(AbstractModel):
    """OfflineIsolatedDBInstance请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID，格式如：cmgo-p8vnipr5。与云数据库控制台页面中显示的实例ID相同
        :type InstanceId: str
        """
        self._InstanceId = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OfflineIsolatedDBInstanceResponse(AbstractModel):
    """OfflineIsolatedDBInstance返回参数结构体

    """

    def __init__(self):
        r"""
        :param _AsyncRequestId: 异步任务的请求 ID，可使用此 ID 查询异步任务的执行结果。
        :type AsyncRequestId: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._AsyncRequestId = None
        self._RequestId = None

    @property
    def AsyncRequestId(self):
        return self._AsyncRequestId

    @AsyncRequestId.setter
    def AsyncRequestId(self, AsyncRequestId):
        self._AsyncRequestId = AsyncRequestId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._AsyncRequestId = params.get("AsyncRequestId")
        self._RequestId = params.get("RequestId")


class Operation(AbstractModel):
    """需要终止的操作

    """

    def __init__(self):
        r"""
        :param _ReplicaSetName: 操作所在的分片名
        :type ReplicaSetName: str
        :param _NodeName: 操作所在的节点名
        :type NodeName: str
        :param _OpId: 操作序号
        :type OpId: int
        """
        self._ReplicaSetName = None
        self._NodeName = None
        self._OpId = None

    @property
    def ReplicaSetName(self):
        return self._ReplicaSetName

    @ReplicaSetName.setter
    def ReplicaSetName(self, ReplicaSetName):
        self._ReplicaSetName = ReplicaSetName

    @property
    def NodeName(self):
        return self._NodeName

    @NodeName.setter
    def NodeName(self, NodeName):
        self._NodeName = NodeName

    @property
    def OpId(self):
        return self._OpId

    @OpId.setter
    def OpId(self, OpId):
        self._OpId = OpId


    def _deserialize(self, params):
        self._ReplicaSetName = params.get("ReplicaSetName")
        self._NodeName = params.get("NodeName")
        self._OpId = params.get("OpId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RenameInstanceRequest(AbstractModel):
    """RenameInstance请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID，格式如：cmgo-p8vnipr5。与云数据库控制台页面中显示的实例ID相同
        :type InstanceId: str
        :param _NewName: 自定义实例名称，名称只支持长度为60个字符的中文、英文、数字、下划线_、分隔符 -
        :type NewName: str
        """
        self._InstanceId = None
        self._NewName = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def NewName(self):
        return self._NewName

    @NewName.setter
    def NewName(self, NewName):
        self._NewName = NewName


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._NewName = params.get("NewName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RenameInstanceResponse(AbstractModel):
    """RenameInstance返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class RenewDBInstancesRequest(AbstractModel):
    """RenewDBInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceIds: 一个或多个待操作的实例ID。可通过DescribeInstances接口返回值中的InstanceId获取。每次请求批量实例的上限为100。
        :type InstanceIds: list of str
        :param _InstanceChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的续费时长、是否设置自动续费等属性。包年包月实例该参数为必传参数。
        :type InstanceChargePrepaid: :class:`tencentcloud.mongodb.v20190725.models.InstanceChargePrepaid`
        """
        self._InstanceIds = None
        self._InstanceChargePrepaid = None

    @property
    def InstanceIds(self):
        return self._InstanceIds

    @InstanceIds.setter
    def InstanceIds(self, InstanceIds):
        self._InstanceIds = InstanceIds

    @property
    def InstanceChargePrepaid(self):
        return self._InstanceChargePrepaid

    @InstanceChargePrepaid.setter
    def InstanceChargePrepaid(self, InstanceChargePrepaid):
        self._InstanceChargePrepaid = InstanceChargePrepaid


    def _deserialize(self, params):
        self._InstanceIds = params.get("InstanceIds")
        if params.get("InstanceChargePrepaid") is not None:
            self._InstanceChargePrepaid = InstanceChargePrepaid()
            self._InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RenewDBInstancesResponse(AbstractModel):
    """RenewDBInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ReplicaSetInfo(AbstractModel):
    """分片信息

    """

    def __init__(self):
        r"""
        :param _ReplicaSetId: 副本集ID
        :type ReplicaSetId: str
        """
        self._ReplicaSetId = None

    @property
    def ReplicaSetId(self):
        return self._ReplicaSetId

    @ReplicaSetId.setter
    def ReplicaSetId(self, ReplicaSetId):
        self._ReplicaSetId = ReplicaSetId


    def _deserialize(self, params):
        self._ReplicaSetId = params.get("ReplicaSetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ReplicateSetInfo(AbstractModel):
    """副本集信息

    """

    def __init__(self):
        r"""
        :param _Nodes: 节点属性
注意：此字段可能返回 null，表示取不到有效值。
        :type Nodes: list of NodeProperty
        """
        self._Nodes = None

    @property
    def Nodes(self):
        return self._Nodes

    @Nodes.setter
    def Nodes(self, Nodes):
        self._Nodes = Nodes


    def _deserialize(self, params):
        if params.get("Nodes") is not None:
            self._Nodes = []
            for item in params.get("Nodes"):
                obj = NodeProperty()
                obj._deserialize(item)
                self._Nodes.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResetDBInstancePasswordRequest(AbstractModel):
    """ResetDBInstancePassword请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例Id
        :type InstanceId: str
        :param _UserName: 实例账号名
        :type UserName: str
        :param _Password: 新密码，新密码长度不能少于8位
        :type Password: str
        """
        self._InstanceId = None
        self._UserName = None
        self._Password = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def UserName(self):
        return self._UserName

    @UserName.setter
    def UserName(self, UserName):
        self._UserName = UserName

    @property
    def Password(self):
        return self._Password

    @Password.setter
    def Password(self, Password):
        self._Password = Password


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._UserName = params.get("UserName")
        self._Password = params.get("Password")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResetDBInstancePasswordResponse(AbstractModel):
    """ResetDBInstancePassword返回参数结构体

    """

    def __init__(self):
        r"""
        :param _AsyncRequestId: 异步请求Id，用户查询该流程的运行状态
        :type AsyncRequestId: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._AsyncRequestId = None
        self._RequestId = None

    @property
    def AsyncRequestId(self):
        return self._AsyncRequestId

    @AsyncRequestId.setter
    def AsyncRequestId(self, AsyncRequestId):
        self._AsyncRequestId = AsyncRequestId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._AsyncRequestId = params.get("AsyncRequestId")
        self._RequestId = params.get("RequestId")


class SecurityGroup(AbstractModel):
    """安全组信息

    """

    def __init__(self):
        r"""
        :param _ProjectId: 所属项目id
        :type ProjectId: int
        :param _CreateTime: 创建时间
        :type CreateTime: str
        :param _Inbound: 入站规则
        :type Inbound: list of SecurityGroupBound
        :param _Outbound: 出站规则
        :type Outbound: list of SecurityGroupBound
        :param _SecurityGroupId: 安全组id
        :type SecurityGroupId: str
        :param _SecurityGroupName: 安全组名称
        :type SecurityGroupName: str
        :param _SecurityGroupRemark: 安全组备注
        :type SecurityGroupRemark: str
        """
        self._ProjectId = None
        self._CreateTime = None
        self._Inbound = None
        self._Outbound = None
        self._SecurityGroupId = None
        self._SecurityGroupName = None
        self._SecurityGroupRemark = None

    @property
    def ProjectId(self):
        return self._ProjectId

    @ProjectId.setter
    def ProjectId(self, ProjectId):
        self._ProjectId = ProjectId

    @property
    def CreateTime(self):
        return self._CreateTime

    @CreateTime.setter
    def CreateTime(self, CreateTime):
        self._CreateTime = CreateTime

    @property
    def Inbound(self):
        return self._Inbound

    @Inbound.setter
    def Inbound(self, Inbound):
        self._Inbound = Inbound

    @property
    def Outbound(self):
        return self._Outbound

    @Outbound.setter
    def Outbound(self, Outbound):
        self._Outbound = Outbound

    @property
    def SecurityGroupId(self):
        return self._SecurityGroupId

    @SecurityGroupId.setter
    def SecurityGroupId(self, SecurityGroupId):
        self._SecurityGroupId = SecurityGroupId

    @property
    def SecurityGroupName(self):
        return self._SecurityGroupName

    @SecurityGroupName.setter
    def SecurityGroupName(self, SecurityGroupName):
        self._SecurityGroupName = SecurityGroupName

    @property
    def SecurityGroupRemark(self):
        return self._SecurityGroupRemark

    @SecurityGroupRemark.setter
    def SecurityGroupRemark(self, SecurityGroupRemark):
        self._SecurityGroupRemark = SecurityGroupRemark


    def _deserialize(self, params):
        self._ProjectId = params.get("ProjectId")
        self._CreateTime = params.get("CreateTime")
        if params.get("Inbound") is not None:
            self._Inbound = []
            for item in params.get("Inbound"):
                obj = SecurityGroupBound()
                obj._deserialize(item)
                self._Inbound.append(obj)
        if params.get("Outbound") is not None:
            self._Outbound = []
            for item in params.get("Outbound"):
                obj = SecurityGroupBound()
                obj._deserialize(item)
                self._Outbound.append(obj)
        self._SecurityGroupId = params.get("SecurityGroupId")
        self._SecurityGroupName = params.get("SecurityGroupName")
        self._SecurityGroupRemark = params.get("SecurityGroupRemark")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SecurityGroupBound(AbstractModel):
    """安全组规则

    """

    def __init__(self):
        r"""
        :param _Action: 执行规则。ACCEPT或DROP
        :type Action: str
        :param _CidrIp: ip段。
        :type CidrIp: str
        :param _PortRange: 端口范围
        :type PortRange: str
        :param _IpProtocol: 传输层协议。tcp，udp或ALL
        :type IpProtocol: str
        :param _Id: 安全组id代表的地址集合
        :type Id: str
        :param _AddressModule: 地址组id代表的地址集合
        :type AddressModule: str
        :param _ServiceModule: 服务组id代表的协议和端口集合
        :type ServiceModule: str
        :param _Desc: 描述
        :type Desc: str
        """
        self._Action = None
        self._CidrIp = None
        self._PortRange = None
        self._IpProtocol = None
        self._Id = None
        self._AddressModule = None
        self._ServiceModule = None
        self._Desc = None

    @property
    def Action(self):
        return self._Action

    @Action.setter
    def Action(self, Action):
        self._Action = Action

    @property
    def CidrIp(self):
        return self._CidrIp

    @CidrIp.setter
    def CidrIp(self, CidrIp):
        self._CidrIp = CidrIp

    @property
    def PortRange(self):
        return self._PortRange

    @PortRange.setter
    def PortRange(self, PortRange):
        self._PortRange = PortRange

    @property
    def IpProtocol(self):
        return self._IpProtocol

    @IpProtocol.setter
    def IpProtocol(self, IpProtocol):
        self._IpProtocol = IpProtocol

    @property
    def Id(self):
        return self._Id

    @Id.setter
    def Id(self, Id):
        self._Id = Id

    @property
    def AddressModule(self):
        return self._AddressModule

    @AddressModule.setter
    def AddressModule(self, AddressModule):
        self._AddressModule = AddressModule

    @property
    def ServiceModule(self):
        return self._ServiceModule

    @ServiceModule.setter
    def ServiceModule(self, ServiceModule):
        self._ServiceModule = ServiceModule

    @property
    def Desc(self):
        return self._Desc

    @Desc.setter
    def Desc(self, Desc):
        self._Desc = Desc


    def _deserialize(self, params):
        self._Action = params.get("Action")
        self._CidrIp = params.get("CidrIp")
        self._PortRange = params.get("PortRange")
        self._IpProtocol = params.get("IpProtocol")
        self._Id = params.get("Id")
        self._AddressModule = params.get("AddressModule")
        self._ServiceModule = params.get("ServiceModule")
        self._Desc = params.get("Desc")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SetAccountUserPrivilegeRequest(AbstractModel):
    """SetAccountUserPrivilege请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 指定待设置账号的实例ID。例如：cmgo-p8vn****。请登录 [MongoDB 控制台](https://console.cloud.tencent.com/mongodb)在实例列表复制实例 ID。
        :type InstanceId: str
        :param _UserName: 设置账号名称。
        :type UserName: str
        :param _AuthRole: 设置权限信息。
        :type AuthRole: list of Auth
        """
        self._InstanceId = None
        self._UserName = None
        self._AuthRole = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def UserName(self):
        return self._UserName

    @UserName.setter
    def UserName(self, UserName):
        self._UserName = UserName

    @property
    def AuthRole(self):
        return self._AuthRole

    @AuthRole.setter
    def AuthRole(self, AuthRole):
        self._AuthRole = AuthRole


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._UserName = params.get("UserName")
        if params.get("AuthRole") is not None:
            self._AuthRole = []
            for item in params.get("AuthRole"):
                obj = Auth()
                obj._deserialize(item)
                self._AuthRole.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SetAccountUserPrivilegeResponse(AbstractModel):
    """SetAccountUserPrivilege返回参数结构体

    """

    def __init__(self):
        r"""
        :param _FlowId: 任务ID。
        :type FlowId: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._FlowId = None
        self._RequestId = None

    @property
    def FlowId(self):
        return self._FlowId

    @FlowId.setter
    def FlowId(self, FlowId):
        self._FlowId = FlowId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._FlowId = params.get("FlowId")
        self._RequestId = params.get("RequestId")


class ShardInfo(AbstractModel):
    """实例分片详情

    """

    def __init__(self):
        r"""
        :param _UsedVolume: 分片已使用容量
        :type UsedVolume: float
        :param _ReplicaSetId: 分片ID
        :type ReplicaSetId: str
        :param _ReplicaSetName: 分片名
        :type ReplicaSetName: str
        :param _Memory: 分片内存规格，单位为MB
        :type Memory: int
        :param _Volume: 分片磁盘规格，单位为MB
        :type Volume: int
        :param _OplogSize: 分片Oplog大小，单位为MB
        :type OplogSize: int
        :param _SecondaryNum: 分片从节点数
        :type SecondaryNum: int
        :param _RealReplicaSetId: 分片物理id
        :type RealReplicaSetId: str
        """
        self._UsedVolume = None
        self._ReplicaSetId = None
        self._ReplicaSetName = None
        self._Memory = None
        self._Volume = None
        self._OplogSize = None
        self._SecondaryNum = None
        self._RealReplicaSetId = None

    @property
    def UsedVolume(self):
        return self._UsedVolume

    @UsedVolume.setter
    def UsedVolume(self, UsedVolume):
        self._UsedVolume = UsedVolume

    @property
    def ReplicaSetId(self):
        return self._ReplicaSetId

    @ReplicaSetId.setter
    def ReplicaSetId(self, ReplicaSetId):
        self._ReplicaSetId = ReplicaSetId

    @property
    def ReplicaSetName(self):
        return self._ReplicaSetName

    @ReplicaSetName.setter
    def ReplicaSetName(self, ReplicaSetName):
        self._ReplicaSetName = ReplicaSetName

    @property
    def Memory(self):
        return self._Memory

    @Memory.setter
    def Memory(self, Memory):
        self._Memory = Memory

    @property
    def Volume(self):
        return self._Volume

    @Volume.setter
    def Volume(self, Volume):
        self._Volume = Volume

    @property
    def OplogSize(self):
        return self._OplogSize

    @OplogSize.setter
    def OplogSize(self, OplogSize):
        self._OplogSize = OplogSize

    @property
    def SecondaryNum(self):
        return self._SecondaryNum

    @SecondaryNum.setter
    def SecondaryNum(self, SecondaryNum):
        self._SecondaryNum = SecondaryNum

    @property
    def RealReplicaSetId(self):
        return self._RealReplicaSetId

    @RealReplicaSetId.setter
    def RealReplicaSetId(self, RealReplicaSetId):
        self._RealReplicaSetId = RealReplicaSetId


    def _deserialize(self, params):
        self._UsedVolume = params.get("UsedVolume")
        self._ReplicaSetId = params.get("ReplicaSetId")
        self._ReplicaSetName = params.get("ReplicaSetName")
        self._Memory = params.get("Memory")
        self._Volume = params.get("Volume")
        self._OplogSize = params.get("OplogSize")
        self._SecondaryNum = params.get("SecondaryNum")
        self._RealReplicaSetId = params.get("RealReplicaSetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SlowLogPattern(AbstractModel):
    """用于描述MongoDB数据库慢日志统计信息

    """

    def __init__(self):
        r"""
        :param _Pattern: 慢日志模式
        :type Pattern: str
        :param _MaxTime: 最大执行时间
        :type MaxTime: int
        :param _AverageTime: 平均执行时间
        :type AverageTime: int
        :param _Total: 该模式慢日志条数
        :type Total: int
        """
        self._Pattern = None
        self._MaxTime = None
        self._AverageTime = None
        self._Total = None

    @property
    def Pattern(self):
        return self._Pattern

    @Pattern.setter
    def Pattern(self, Pattern):
        self._Pattern = Pattern

    @property
    def MaxTime(self):
        return self._MaxTime

    @MaxTime.setter
    def MaxTime(self, MaxTime):
        self._MaxTime = MaxTime

    @property
    def AverageTime(self):
        return self._AverageTime

    @AverageTime.setter
    def AverageTime(self, AverageTime):
        self._AverageTime = AverageTime

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total


    def _deserialize(self, params):
        self._Pattern = params.get("Pattern")
        self._MaxTime = params.get("MaxTime")
        self._AverageTime = params.get("AverageTime")
        self._Total = params.get("Total")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SpecItem(AbstractModel):
    """mongodb售卖规格

    """

    def __init__(self):
        r"""
        :param _SpecCode: 规格信息标识
        :type SpecCode: str
        :param _Status: 规格有效标志，取值：0-停止售卖，1-开放售卖
        :type Status: int
        :param _Cpu: 计算资源规格，单位为CPU核心数
        :type Cpu: int
        :param _Memory: 内存规格，单位为MB
        :type Memory: int
        :param _DefaultStorage: 默认磁盘规格，单位MB
        :type DefaultStorage: int
        :param _MaxStorage: 最大磁盘规格，单位MB
        :type MaxStorage: int
        :param _MinStorage: 最小磁盘规格，单位MB
        :type MinStorage: int
        :param _Qps: 可承载qps信息
        :type Qps: int
        :param _Conns: 连接数限制
        :type Conns: int
        :param _MongoVersionCode: 实例mongodb版本信息
        :type MongoVersionCode: str
        :param _MongoVersionValue: 实例mongodb版本号
        :type MongoVersionValue: int
        :param _Version: 实例mongodb版本号（短）
        :type Version: str
        :param _EngineName: 存储引擎
        :type EngineName: str
        :param _ClusterType: 集群类型，取值：1-分片集群，0-副本集集群
        :type ClusterType: int
        :param _MinNodeNum: 最小副本集从节点数
        :type MinNodeNum: int
        :param _MaxNodeNum: 最大副本集从节点数
        :type MaxNodeNum: int
        :param _MinReplicateSetNum: 最小分片数
        :type MinReplicateSetNum: int
        :param _MaxReplicateSetNum: 最大分片数
        :type MaxReplicateSetNum: int
        :param _MinReplicateSetNodeNum: 最小分片从节点数
        :type MinReplicateSetNodeNum: int
        :param _MaxReplicateSetNodeNum: 最大分片从节点数
        :type MaxReplicateSetNodeNum: int
        :param _MachineType: 机器类型，取值：0-HIO，4-HIO10G
        :type MachineType: str
        """
        self._SpecCode = None
        self._Status = None
        self._Cpu = None
        self._Memory = None
        self._DefaultStorage = None
        self._MaxStorage = None
        self._MinStorage = None
        self._Qps = None
        self._Conns = None
        self._MongoVersionCode = None
        self._MongoVersionValue = None
        self._Version = None
        self._EngineName = None
        self._ClusterType = None
        self._MinNodeNum = None
        self._MaxNodeNum = None
        self._MinReplicateSetNum = None
        self._MaxReplicateSetNum = None
        self._MinReplicateSetNodeNum = None
        self._MaxReplicateSetNodeNum = None
        self._MachineType = None

    @property
    def SpecCode(self):
        return self._SpecCode

    @SpecCode.setter
    def SpecCode(self, SpecCode):
        self._SpecCode = SpecCode

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def Cpu(self):
        return self._Cpu

    @Cpu.setter
    def Cpu(self, Cpu):
        self._Cpu = Cpu

    @property
    def Memory(self):
        return self._Memory

    @Memory.setter
    def Memory(self, Memory):
        self._Memory = Memory

    @property
    def DefaultStorage(self):
        return self._DefaultStorage

    @DefaultStorage.setter
    def DefaultStorage(self, DefaultStorage):
        self._DefaultStorage = DefaultStorage

    @property
    def MaxStorage(self):
        return self._MaxStorage

    @MaxStorage.setter
    def MaxStorage(self, MaxStorage):
        self._MaxStorage = MaxStorage

    @property
    def MinStorage(self):
        return self._MinStorage

    @MinStorage.setter
    def MinStorage(self, MinStorage):
        self._MinStorage = MinStorage

    @property
    def Qps(self):
        return self._Qps

    @Qps.setter
    def Qps(self, Qps):
        self._Qps = Qps

    @property
    def Conns(self):
        return self._Conns

    @Conns.setter
    def Conns(self, Conns):
        self._Conns = Conns

    @property
    def MongoVersionCode(self):
        return self._MongoVersionCode

    @MongoVersionCode.setter
    def MongoVersionCode(self, MongoVersionCode):
        self._MongoVersionCode = MongoVersionCode

    @property
    def MongoVersionValue(self):
        return self._MongoVersionValue

    @MongoVersionValue.setter
    def MongoVersionValue(self, MongoVersionValue):
        self._MongoVersionValue = MongoVersionValue

    @property
    def Version(self):
        return self._Version

    @Version.setter
    def Version(self, Version):
        self._Version = Version

    @property
    def EngineName(self):
        return self._EngineName

    @EngineName.setter
    def EngineName(self, EngineName):
        self._EngineName = EngineName

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType

    @property
    def MinNodeNum(self):
        return self._MinNodeNum

    @MinNodeNum.setter
    def MinNodeNum(self, MinNodeNum):
        self._MinNodeNum = MinNodeNum

    @property
    def MaxNodeNum(self):
        return self._MaxNodeNum

    @MaxNodeNum.setter
    def MaxNodeNum(self, MaxNodeNum):
        self._MaxNodeNum = MaxNodeNum

    @property
    def MinReplicateSetNum(self):
        return self._MinReplicateSetNum

    @MinReplicateSetNum.setter
    def MinReplicateSetNum(self, MinReplicateSetNum):
        self._MinReplicateSetNum = MinReplicateSetNum

    @property
    def MaxReplicateSetNum(self):
        return self._MaxReplicateSetNum

    @MaxReplicateSetNum.setter
    def MaxReplicateSetNum(self, MaxReplicateSetNum):
        self._MaxReplicateSetNum = MaxReplicateSetNum

    @property
    def MinReplicateSetNodeNum(self):
        return self._MinReplicateSetNodeNum

    @MinReplicateSetNodeNum.setter
    def MinReplicateSetNodeNum(self, MinReplicateSetNodeNum):
        self._MinReplicateSetNodeNum = MinReplicateSetNodeNum

    @property
    def MaxReplicateSetNodeNum(self):
        return self._MaxReplicateSetNodeNum

    @MaxReplicateSetNodeNum.setter
    def MaxReplicateSetNodeNum(self, MaxReplicateSetNodeNum):
        self._MaxReplicateSetNodeNum = MaxReplicateSetNodeNum

    @property
    def MachineType(self):
        return self._MachineType

    @MachineType.setter
    def MachineType(self, MachineType):
        self._MachineType = MachineType


    def _deserialize(self, params):
        self._SpecCode = params.get("SpecCode")
        self._Status = params.get("Status")
        self._Cpu = params.get("Cpu")
        self._Memory = params.get("Memory")
        self._DefaultStorage = params.get("DefaultStorage")
        self._MaxStorage = params.get("MaxStorage")
        self._MinStorage = params.get("MinStorage")
        self._Qps = params.get("Qps")
        self._Conns = params.get("Conns")
        self._MongoVersionCode = params.get("MongoVersionCode")
        self._MongoVersionValue = params.get("MongoVersionValue")
        self._Version = params.get("Version")
        self._EngineName = params.get("EngineName")
        self._ClusterType = params.get("ClusterType")
        self._MinNodeNum = params.get("MinNodeNum")
        self._MaxNodeNum = params.get("MaxNodeNum")
        self._MinReplicateSetNum = params.get("MinReplicateSetNum")
        self._MaxReplicateSetNum = params.get("MaxReplicateSetNum")
        self._MinReplicateSetNodeNum = params.get("MinReplicateSetNodeNum")
        self._MaxReplicateSetNodeNum = params.get("MaxReplicateSetNodeNum")
        self._MachineType = params.get("MachineType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SpecificationInfo(AbstractModel):
    """实例规格信息

    """

    def __init__(self):
        r"""
        :param _Region: 地域信息
        :type Region: str
        :param _Zone: 可用区信息
        :type Zone: str
        :param _SpecItems: 售卖规格信息
        :type SpecItems: list of SpecItem
        :param _SupportMultiAZ: 是否支持跨可用区部署 1-支持，0-不支持
        :type SupportMultiAZ: int
        """
        self._Region = None
        self._Zone = None
        self._SpecItems = None
        self._SupportMultiAZ = None

    @property
    def Region(self):
        return self._Region

    @Region.setter
    def Region(self, Region):
        self._Region = Region

    @property
    def Zone(self):
        return self._Zone

    @Zone.setter
    def Zone(self, Zone):
        self._Zone = Zone

    @property
    def SpecItems(self):
        return self._SpecItems

    @SpecItems.setter
    def SpecItems(self, SpecItems):
        self._SpecItems = SpecItems

    @property
    def SupportMultiAZ(self):
        return self._SupportMultiAZ

    @SupportMultiAZ.setter
    def SupportMultiAZ(self, SupportMultiAZ):
        self._SupportMultiAZ = SupportMultiAZ


    def _deserialize(self, params):
        self._Region = params.get("Region")
        self._Zone = params.get("Zone")
        if params.get("SpecItems") is not None:
            self._SpecItems = []
            for item in params.get("SpecItems"):
                obj = SpecItem()
                obj._deserialize(item)
                self._SpecItems.append(obj)
        self._SupportMultiAZ = params.get("SupportMultiAZ")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TagInfo(AbstractModel):
    """实例标签信息

    """

    def __init__(self):
        r"""
        :param _TagKey: 标签键
        :type TagKey: str
        :param _TagValue: 标签值
        :type TagValue: str
        """
        self._TagKey = None
        self._TagValue = None

    @property
    def TagKey(self):
        return self._TagKey

    @TagKey.setter
    def TagKey(self, TagKey):
        self._TagKey = TagKey

    @property
    def TagValue(self):
        return self._TagValue

    @TagValue.setter
    def TagValue(self, TagValue):
        self._TagValue = TagValue


    def _deserialize(self, params):
        self._TagKey = params.get("TagKey")
        self._TagValue = params.get("TagValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TerminateDBInstancesRequest(AbstractModel):
    """TerminateDBInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 指定预隔离实例ID。格式如：cmgo-p8vnipr5。
        :type InstanceId: str
        """
        self._InstanceId = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TerminateDBInstancesResponse(AbstractModel):
    """TerminateDBInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class UserInfo(AbstractModel):
    """账户基本信息

    """

    def __init__(self):
        r"""
        :param _UserName: 账号名。
        :type UserName: str
        :param _AuthRole: 账号权限详情。
        :type AuthRole: list of Auth
        :param _CreateTime: 账号创建时间。
        :type CreateTime: str
        :param _UpdateTime: 账号更新时间。
        :type UpdateTime: str
        :param _UserDesc: 备注信息。
        :type UserDesc: str
        """
        self._UserName = None
        self._AuthRole = None
        self._CreateTime = None
        self._UpdateTime = None
        self._UserDesc = None

    @property
    def UserName(self):
        return self._UserName

    @UserName.setter
    def UserName(self, UserName):
        self._UserName = UserName

    @property
    def AuthRole(self):
        return self._AuthRole

    @AuthRole.setter
    def AuthRole(self, AuthRole):
        self._AuthRole = AuthRole

    @property
    def CreateTime(self):
        return self._CreateTime

    @CreateTime.setter
    def CreateTime(self, CreateTime):
        self._CreateTime = CreateTime

    @property
    def UpdateTime(self):
        return self._UpdateTime

    @UpdateTime.setter
    def UpdateTime(self, UpdateTime):
        self._UpdateTime = UpdateTime

    @property
    def UserDesc(self):
        return self._UserDesc

    @UserDesc.setter
    def UserDesc(self, UserDesc):
        self._UserDesc = UserDesc


    def _deserialize(self, params):
        self._UserName = params.get("UserName")
        if params.get("AuthRole") is not None:
            self._AuthRole = []
            for item in params.get("AuthRole"):
                obj = Auth()
                obj._deserialize(item)
                self._AuthRole.append(obj)
        self._CreateTime = params.get("CreateTime")
        self._UpdateTime = params.get("UpdateTime")
        self._UserDesc = params.get("UserDesc")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        
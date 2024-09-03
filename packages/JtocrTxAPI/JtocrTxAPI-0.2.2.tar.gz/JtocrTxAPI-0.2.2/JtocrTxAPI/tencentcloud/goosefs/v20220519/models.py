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


class CreateDataRepositoryTaskRequest(AbstractModel):
    """CreateDataRepositoryTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param _TaskType: 数据流通任务类型, FS_TO_COS(文件系统到COS Bucket),或者COS_TO_FS(COS Bucket到文件系统)
        :type TaskType: str
        :param _Bucket: COS存储桶名
        :type Bucket: str
        :param _FileSystemId: 文件系统ID
        :type FileSystemId: str
        :param _TaskPath: 对于FS_TO_COS, TaskPath是Bucket映射目录的相对路径, 对于COS_TO_FS是COS上的路径。如果置为空, 则表示全部数据
        :type TaskPath: str
        :param _TaskName: 任务名称
        :type TaskName: str
        :param _RepositoryType: 数据流通方式 MSP_AFM 手动加载  RAW_AFM 按需加载
        :type RepositoryType: str
        :param _TextLocation: 文件列表下载地址，以http开头
        :type TextLocation: str
        """
        self._TaskType = None
        self._Bucket = None
        self._FileSystemId = None
        self._TaskPath = None
        self._TaskName = None
        self._RepositoryType = None
        self._TextLocation = None

    @property
    def TaskType(self):
        return self._TaskType

    @TaskType.setter
    def TaskType(self, TaskType):
        self._TaskType = TaskType

    @property
    def Bucket(self):
        return self._Bucket

    @Bucket.setter
    def Bucket(self, Bucket):
        self._Bucket = Bucket

    @property
    def FileSystemId(self):
        return self._FileSystemId

    @FileSystemId.setter
    def FileSystemId(self, FileSystemId):
        self._FileSystemId = FileSystemId

    @property
    def TaskPath(self):
        return self._TaskPath

    @TaskPath.setter
    def TaskPath(self, TaskPath):
        self._TaskPath = TaskPath

    @property
    def TaskName(self):
        return self._TaskName

    @TaskName.setter
    def TaskName(self, TaskName):
        self._TaskName = TaskName

    @property
    def RepositoryType(self):
        return self._RepositoryType

    @RepositoryType.setter
    def RepositoryType(self, RepositoryType):
        self._RepositoryType = RepositoryType

    @property
    def TextLocation(self):
        return self._TextLocation

    @TextLocation.setter
    def TextLocation(self, TextLocation):
        self._TextLocation = TextLocation


    def _deserialize(self, params):
        self._TaskType = params.get("TaskType")
        self._Bucket = params.get("Bucket")
        self._FileSystemId = params.get("FileSystemId")
        self._TaskPath = params.get("TaskPath")
        self._TaskName = params.get("TaskName")
        self._RepositoryType = params.get("RepositoryType")
        self._TextLocation = params.get("TextLocation")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDataRepositoryTaskResponse(AbstractModel):
    """CreateDataRepositoryTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TaskId: 任务ID
        :type TaskId: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TaskId = None
        self._RequestId = None

    @property
    def TaskId(self):
        return self._TaskId

    @TaskId.setter
    def TaskId(self, TaskId):
        self._TaskId = TaskId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TaskId = params.get("TaskId")
        self._RequestId = params.get("RequestId")


class DescribeDataRepositoryTaskStatusRequest(AbstractModel):
    """DescribeDataRepositoryTaskStatus请求参数结构体

    """

    def __init__(self):
        r"""
        :param _TaskId: task id
        :type TaskId: str
        :param _FileSystemId: file system id
        :type FileSystemId: str
        """
        self._TaskId = None
        self._FileSystemId = None

    @property
    def TaskId(self):
        return self._TaskId

    @TaskId.setter
    def TaskId(self, TaskId):
        self._TaskId = TaskId

    @property
    def FileSystemId(self):
        return self._FileSystemId

    @FileSystemId.setter
    def FileSystemId(self, FileSystemId):
        self._FileSystemId = FileSystemId


    def _deserialize(self, params):
        self._TaskId = params.get("TaskId")
        self._FileSystemId = params.get("FileSystemId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDataRepositoryTaskStatusResponse(AbstractModel):
    """DescribeDataRepositoryTaskStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TaskId: 任务id
        :type TaskId: str
        :param _Status: 任务状态 0(初始化中), 1(运行中), 2(已完成), 3(任务失败)
        :type Status: int
        :param _FinishedFileNumber: 已完成的文件数量
        :type FinishedFileNumber: int
        :param _FinishedCapacity: 已完成的数据量
        :type FinishedCapacity: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TaskId = None
        self._Status = None
        self._FinishedFileNumber = None
        self._FinishedCapacity = None
        self._RequestId = None

    @property
    def TaskId(self):
        return self._TaskId

    @TaskId.setter
    def TaskId(self, TaskId):
        self._TaskId = TaskId

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def FinishedFileNumber(self):
        return self._FinishedFileNumber

    @FinishedFileNumber.setter
    def FinishedFileNumber(self, FinishedFileNumber):
        self._FinishedFileNumber = FinishedFileNumber

    @property
    def FinishedCapacity(self):
        return self._FinishedCapacity

    @FinishedCapacity.setter
    def FinishedCapacity(self, FinishedCapacity):
        self._FinishedCapacity = FinishedCapacity

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TaskId = params.get("TaskId")
        self._Status = params.get("Status")
        self._FinishedFileNumber = params.get("FinishedFileNumber")
        self._FinishedCapacity = params.get("FinishedCapacity")
        self._RequestId = params.get("RequestId")
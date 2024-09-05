from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ModelData(_message.Message):
    __slots__ = ("name", "version", "package_definition")
    class JavaPackages(_message.Message):
        __slots__ = ("agents", "data_items", "portables")
        AGENTS_FIELD_NUMBER: _ClassVar[int]
        DATA_ITEMS_FIELD_NUMBER: _ClassVar[int]
        PORTABLES_FIELD_NUMBER: _ClassVar[int]
        agents: _containers.RepeatedScalarFieldContainer[str]
        data_items: _containers.RepeatedScalarFieldContainer[str]
        portables: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, agents: _Optional[_Iterable[str]] = ..., data_items: _Optional[_Iterable[str]] = ..., portables: _Optional[_Iterable[str]] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    name: str
    version: str
    package_definition: ModelData.JavaPackages
    def __init__(self, name: _Optional[str] = ..., version: _Optional[str] = ..., package_definition: _Optional[_Union[ModelData.JavaPackages, _Mapping]] = ...) -> None: ...

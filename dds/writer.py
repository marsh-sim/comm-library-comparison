from dataclasses import dataclass

from cyclonedds.domain import DomainParticipant
from cyclonedds.pub import DataWriter
from cyclonedds.topic import Topic

from cyclonedds.idl import IdlStruct


@dataclass
class HelloType(IdlStruct, typename="HelloType"):
    data: float


dp = DomainParticipant(1)

tp = Topic(dp, "Hello", HelloType)

dw = DataWriter(dp, tp)

sample = HelloType(data=1.23)
dw.write(sample)

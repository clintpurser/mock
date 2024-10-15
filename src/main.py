
import asyncio
from typing import Any, ClassVar, Dict, Final, List, Mapping, Optional, Sequence
from typing_extensions import Self
from viam.components.sensor import *
from viam.module.module import Module
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import SensorReading, ValueTypes, struct_to_dict


class MockSensor(Sensor, EasyResource): 
    MODEL: ClassVar[Model] = Model(ModelFamily("cdp", "mock"), "mock-sensor")
    mock_data: List[Dict[str, ValueTypes]]
    current_position: int

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:        
        if len(config.attributes.fields.get("mock_data", [])) > 0:
            raise Exception("A mock_data must be defined")
        
        # for reading in config.attributes.fields.get("mock_data", []):
            # if not isinstance(reading, Struct):
            #     raise Exception("mock_data must only be populated with maps of data")
        return []

    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        self.mock_data = [struct_to_dict(x) for x in config.attributes.fields["mock_data"].list_value]
        self.current_position = 0

    async def get_readings(self, *, extra: Optional[Mapping[str, Any]]=None, timeout: Optional[float]=None, **kwargs) -> Mapping[str, SensorReading]:
        reading = self.mock_data[self.current_position]

        self.current_position += 1
        if self.current_position >= len(self.mock_data): 
            self.current_position = 0

        return reading


if __name__ == '__main__':
    asyncio.run(Module.run_from_registry())



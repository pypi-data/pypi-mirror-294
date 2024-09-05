##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.19                                                            #
# Generated on 2024-09-04T23:07:02.495771                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.airflow.sensors.base_sensor

class ExternalTaskSensorDecorator(metaflow.plugins.airflow.sensors.base_sensor.AirflowSensorDecorator, metaclass=type):
    def serialize_operator_args(self):
        ...
    def validate(self, flow):
        ...
    ...

class S3KeySensorDecorator(metaflow.plugins.airflow.sensors.base_sensor.AirflowSensorDecorator, metaclass=type):
    def validate(self, flow):
        ...
    ...

SUPPORTED_SENSORS: list


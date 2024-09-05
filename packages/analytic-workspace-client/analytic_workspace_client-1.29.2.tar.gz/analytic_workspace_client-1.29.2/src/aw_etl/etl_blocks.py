from typing import Protocol, Optional

try:
    from pyspark.sql import SparkSession
except ImportError:
    raise Exception('Для использования Spark установите библиотеку с опцией [dev]: `pip install analytic-workspace-client[dev]`')


from aw_etl.models import Vault
from aw_etl.compiler import CompiledModule


class InvalidEtlBlock(Exception):
    """ """


class ETLBlockApplication(Protocol):
    """ """
    @property
    def spark(self) -> SparkSession:
        """ """

    @property
    def is_spark_initialized(self) -> bool:
        """ """

    @property
    def model_module(self) -> Optional[CompiledModule]:
        """ """

    @property
    def vault(self) -> Vault:
        """ """

    @property
    def run_mode(self) -> str:
        """ """

    
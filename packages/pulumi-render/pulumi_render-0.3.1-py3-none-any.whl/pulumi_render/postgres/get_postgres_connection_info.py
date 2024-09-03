# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetPostgresConnectionInfoResult',
    'AwaitableGetPostgresConnectionInfoResult',
    'get_postgres_connection_info',
    'get_postgres_connection_info_output',
]

@pulumi.output_type
class GetPostgresConnectionInfoResult:
    def __init__(__self__, items=None):
        if items and not isinstance(items, dict):
            raise TypeError("Expected argument 'items' to be a dict")
        pulumi.set(__self__, "items", items)

    @property
    @pulumi.getter
    def items(self) -> 'outputs.PostgresConnectionInfo':
        return pulumi.get(self, "items")


class AwaitableGetPostgresConnectionInfoResult(GetPostgresConnectionInfoResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPostgresConnectionInfoResult(
            items=self.items)


def get_postgres_connection_info(postgres_id: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPostgresConnectionInfoResult:
    """
    Use this data source to access information about an existing resource.
    """
    __args__ = dict()
    __args__['postgresId'] = postgres_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('render:postgres:getPostgresConnectionInfo', __args__, opts=opts, typ=GetPostgresConnectionInfoResult).value

    return AwaitableGetPostgresConnectionInfoResult(
        items=pulumi.get(__ret__, 'items'))


@_utilities.lift_output_func(get_postgres_connection_info)
def get_postgres_connection_info_output(postgres_id: Optional[pulumi.Input[str]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPostgresConnectionInfoResult]:
    """
    Use this data source to access information about an existing resource.
    """
    ...

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
    'ListActiveConnectionsResult',
    'AwaitableListActiveConnectionsResult',
    'list_active_connections',
    'list_active_connections_output',
]

@pulumi.output_type
class ListActiveConnectionsResult:
    def __init__(__self__, items=None):
        if items and not isinstance(items, list):
            raise TypeError("Expected argument 'items' to be a list")
        pulumi.set(__self__, "items", items)

    @property
    @pulumi.getter
    def items(self) -> Sequence['outputs.ListActiveConnectionsItemProperties']:
        return pulumi.get(self, "items")


class AwaitableListActiveConnectionsResult(ListActiveConnectionsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListActiveConnectionsResult(
            items=self.items)


def list_active_connections(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListActiveConnectionsResult:
    """
    Use this data source to access information about an existing resource.
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('render:metrics:listActiveConnections', __args__, opts=opts, typ=ListActiveConnectionsResult).value

    return AwaitableListActiveConnectionsResult(
        items=pulumi.get(__ret__, 'items'))


@_utilities.lift_output_func(list_active_connections)
def list_active_connections_output(opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListActiveConnectionsResult]:
    """
    Use this data source to access information about an existing resource.
    """
    ...

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
from ._enums import *

__all__ = [
    'ListBlueprintsResult',
    'AwaitableListBlueprintsResult',
    'list_blueprints',
    'list_blueprints_output',
]

@pulumi.output_type
class ListBlueprintsResult:
    def __init__(__self__, items=None):
        if items and not isinstance(items, list):
            raise TypeError("Expected argument 'items' to be a list")
        pulumi.set(__self__, "items", items)

    @property
    @pulumi.getter
    def items(self) -> Sequence['outputs.BlueprintWithCursor']:
        return pulumi.get(self, "items")


class AwaitableListBlueprintsResult(ListBlueprintsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListBlueprintsResult(
            items=self.items)


def list_blueprints(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListBlueprintsResult:
    """
    Use this data source to access information about an existing resource.
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('render:blueprints:listBlueprints', __args__, opts=opts, typ=ListBlueprintsResult).value

    return AwaitableListBlueprintsResult(
        items=pulumi.get(__ret__, 'items'))


@_utilities.lift_output_func(list_blueprints)
def list_blueprints_output(opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListBlueprintsResult]:
    """
    Use this data source to access information about an existing resource.
    """
    ...

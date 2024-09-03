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
    'GetRegistryCredentialResult',
    'AwaitableGetRegistryCredentialResult',
    'get_registry_credential',
    'get_registry_credential_output',
]

@pulumi.output_type
class GetRegistryCredentialResult:
    def __init__(__self__, items=None):
        if items and not isinstance(items, dict):
            raise TypeError("Expected argument 'items' to be a dict")
        pulumi.set(__self__, "items", items)

    @property
    @pulumi.getter
    def items(self) -> 'outputs.RegistryCredential':
        return pulumi.get(self, "items")


class AwaitableGetRegistryCredentialResult(GetRegistryCredentialResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRegistryCredentialResult(
            items=self.items)


def get_registry_credential(registry_credential_id: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRegistryCredentialResult:
    """
    Use this data source to access information about an existing resource.

    :param str registry_credential_id: The ID of the registry credential
    """
    __args__ = dict()
    __args__['registryCredentialId'] = registry_credential_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('render:registrycredentials:getRegistryCredential', __args__, opts=opts, typ=GetRegistryCredentialResult).value

    return AwaitableGetRegistryCredentialResult(
        items=pulumi.get(__ret__, 'items'))


@_utilities.lift_output_func(get_registry_credential)
def get_registry_credential_output(registry_credential_id: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRegistryCredentialResult]:
    """
    Use this data source to access information about an existing resource.

    :param str registry_credential_id: The ID of the registry credential
    """
    ...

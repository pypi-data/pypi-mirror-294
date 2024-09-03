# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'CidrBlockAndDescriptionArgs',
]

@pulumi.input_type
class CidrBlockAndDescriptionArgs:
    def __init__(__self__, *,
                 cidr_block: pulumi.Input[str],
                 description: pulumi.Input[str]):
        """
        :param pulumi.Input[str] description: User-provided description of the CIDR block
        """
        pulumi.set(__self__, "cidr_block", cidr_block)
        pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> pulumi.Input[str]:
        return pulumi.get(self, "cidr_block")

    @cidr_block.setter
    def cidr_block(self, value: pulumi.Input[str]):
        pulumi.set(self, "cidr_block", value)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Input[str]:
        """
        User-provided description of the CIDR block
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: pulumi.Input[str]):
        pulumi.set(self, "description", value)



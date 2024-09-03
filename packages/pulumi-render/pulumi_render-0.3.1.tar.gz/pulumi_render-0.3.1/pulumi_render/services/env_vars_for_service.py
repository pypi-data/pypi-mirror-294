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
from ._inputs import *

__all__ = ['EnvVarsForServiceArgs', 'EnvVarsForService']

@pulumi.input_type
class EnvVarsForServiceArgs:
    def __init__(__self__, *,
                 env_vars: Optional[pulumi.Input[Sequence[pulumi.Input['EnvVarInputArgs']]]] = None,
                 service_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a EnvVarsForService resource.
        :param pulumi.Input[str] service_id: The ID of the service
        """
        if env_vars is not None:
            pulumi.set(__self__, "env_vars", env_vars)
        if service_id is not None:
            pulumi.set(__self__, "service_id", service_id)

    @property
    @pulumi.getter(name="envVars")
    def env_vars(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EnvVarInputArgs']]]]:
        return pulumi.get(self, "env_vars")

    @env_vars.setter
    def env_vars(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EnvVarInputArgs']]]]):
        pulumi.set(self, "env_vars", value)

    @property
    @pulumi.getter(name="serviceId")
    def service_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the service
        """
        return pulumi.get(self, "service_id")

    @service_id.setter
    def service_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_id", value)


class EnvVarsForService(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 env_vars: Optional[pulumi.Input[Sequence[pulumi.Input[Union['EnvVarInputArgs', 'EnvVarInputArgsDict']]]]] = None,
                 service_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a EnvVarsForService resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] service_id: The ID of the service
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[EnvVarsForServiceArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a EnvVarsForService resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param EnvVarsForServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EnvVarsForServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 env_vars: Optional[pulumi.Input[Sequence[pulumi.Input[Union['EnvVarInputArgs', 'EnvVarInputArgsDict']]]]] = None,
                 service_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EnvVarsForServiceArgs.__new__(EnvVarsForServiceArgs)

            __props__.__dict__["env_vars"] = env_vars
            __props__.__dict__["service_id"] = service_id
        super(EnvVarsForService, __self__).__init__(
            'render:services:EnvVarsForService',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'EnvVarsForService':
        """
        Get an existing EnvVarsForService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = EnvVarsForServiceArgs.__new__(EnvVarsForServiceArgs)

        __props__.__dict__["env_vars"] = None
        return EnvVarsForService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="envVars")
    def env_vars(self) -> pulumi.Output[Optional[Sequence['outputs.EnvVarInput']]]:
        return pulumi.get(self, "env_vars")


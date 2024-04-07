import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest

from parcel_status.parcel_status_stack import ParcelStatusStack

def test_lambda_created():
    app = core.App()
    stack = ParcelStatusStack(app, "parcel-status")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::Lambda::Function", {
        "Runtime": "python3.12"
    })

def test_lambda_running():
    app = core.App()
    stack = ParcelStatusStack(app, "parcel-status")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::Lambda::Function", 1)
    template.has_resource_properties("AWS::Lambda::Function", {
        "Runtime": "python3.12"
    })


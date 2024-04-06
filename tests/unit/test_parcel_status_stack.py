import aws_cdk as core
import aws_cdk.assertions as assertions

from parcel_status.parcel_status_stack import ParcelStatusStack

# example tests. To run these tests, uncomment this file along with the example
# resource in parcel_status/parcel_status_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ParcelStatusStack(app, "parcel-status")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

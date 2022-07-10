import aws_cdk as core
import aws_cdk.assertions as assertions

from stack.lambda_event_sample_stack import LambdaEventSampleStack

# example tests. To run these tests, uncomment this file along with the example
# resource in lambda_event_sample/lambda_event_sample_stack.py


# def test_sqs_queue_created():
#     app = core.App()
#     stack = LambdaEventSampleStack(app, "lambda-event-sample")
#     template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

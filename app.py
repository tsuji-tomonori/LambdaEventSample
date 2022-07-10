#!/usr/bin/env python3
import aws_cdk as cdk

from stack.lambda_event_sample_stack import LambdaEventSampleStack


app = cdk.App()

stack = LambdaEventSampleStack(app, "LambdaEventSampleStack")
cdk.Tags.of(stack).add("service", "LambdaEventSample")

app.synth()

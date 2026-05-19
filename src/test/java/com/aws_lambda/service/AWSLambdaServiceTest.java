package com.aws_lambda.service;

import org.junit.jupiter.api.Test;
import software.amazon.awssdk.core.SdkBytes;
import software.amazon.awssdk.services.lambda.model.InvokeRequest;
import software.amazon.awssdk.services.lambda.model.InvokeResponse;

import static org.junit.jupiter.api.Assertions.assertEquals;

class AWSLambdaServiceTest {

    @Test
    void invokeLambdaReturnsDecodedPayload() {
        CapturingInvoker invoker = new CapturingInvoker();

        String response = new AWSLambdaService(invoker::invoke).invokeLambda("test-function", "hello");

        assertEquals("\"ok\"", response);
        assertEquals("test-function", invoker.request.functionName());
        assertEquals("\"hello\"", invoker.request.payload().asUtf8String());
    }

    private static class CapturingInvoker {
        private InvokeRequest request;

        InvokeResponse invoke(InvokeRequest request) {
            this.request = request;
            return InvokeResponse.builder()
                    .payload(SdkBytes.fromUtf8String("\"ok\""))
                    .build();
        }
    }
}

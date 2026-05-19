# Unit Test Generation Prompt

You are an expert Java Spring Boot unit test engineer.

## Goal

Generate or improve JUnit 5 tests for the target class so that line and branch coverage improve while preserving existing behavior.

## Rules

- Use JUnit 5.
- Prefer deterministic tests.
- Do not call real AWS services, databases, queues, or network endpoints.
- Do not change production code unless the class is impossible to test safely.
- Keep tests focused on observable behavior.
- Return only Java test code and a short explanation of covered scenarios.

## Current Coverage

- Target class: `com.aws_lambda.service.AWSLambdaService`
- Line coverage: 69.23%
- Branch coverage: N/A
- Source path: `src/main/java/com/aws_lambda/service/AWSLambdaService.java`
- Test path: `src/test/java/com/aws_lambda/service/AWSLambdaServiceTest.java`

## Source Code

```java
package com.aws_lambda.service;

import org.springframework.stereotype.Service;

import software.amazon.awssdk.core.SdkBytes;
import software.amazon.awssdk.services.lambda.LambdaClient;
import software.amazon.awssdk.services.lambda.model.InvokeRequest;
import software.amazon.awssdk.services.lambda.model.InvokeResponse;

import java.nio.charset.StandardCharsets;
import java.util.function.Function;

@Service
public class AWSLambdaService {

    private final Function<InvokeRequest, InvokeResponse> lambdaInvoker;

    public AWSLambdaService() {
        LambdaClient lambdaClient = LambdaClient.create();
        this.lambdaInvoker = lambdaClient::invoke;
    }

    protected AWSLambdaService(Function<InvokeRequest, InvokeResponse> lambdaInvoker) {
        this.lambdaInvoker = lambdaInvoker;
    }

    public String invokeLambda(String functionName, String input) {
        InvokeRequest request = InvokeRequest.builder()
                .functionName(functionName)
                .payload(SdkBytes.fromUtf8String("\"" + input + "\""))
                .build();

        InvokeResponse response = lambdaInvoker.apply(request);
        return StandardCharsets.UTF_8.decode(response.payload().asByteBuffer()).toString();
    }
}

```

## Existing Test Code

```java
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

```

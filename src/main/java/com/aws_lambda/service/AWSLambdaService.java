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

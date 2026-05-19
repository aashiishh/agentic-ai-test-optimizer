package com.aws_lambda.controller;

import com.aws_lambda.service.AWSLambdaService;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class LambdaControllerTest {

    @Test
    void invokeLambdaDelegatesToServiceWithConfiguredFunctionName() {
        CapturingLambdaService service = new CapturingLambdaService();

        String response = new LambdaController(service).invokeLambda("demo-input");

        assertEquals("demo-output", response);
        assertEquals("myFirstFunction", service.functionName);
        assertEquals("demo-input", service.input);
    }

    private static class CapturingLambdaService extends AWSLambdaService {
        private String functionName;
        private String input;

        CapturingLambdaService() {
            super(request -> null);
        }

        @Override
        public String invokeLambda(String functionName, String input) {
            this.functionName = functionName;
            this.input = input;
            return "demo-output";
        }
    }
}

package com.aws_lambda;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class LambdaHandlerTest {

    @Test
    void handleRequestReturnsGreetingAndLogsInput() {
        CapturingLogger logger = new CapturingLogger();
        TestContext context = new TestContext(logger);

        String response = new LambdaHandler().handleRequest("Hackathon", context);

        assertEquals("Hello, Hackathon!", response);
        assertEquals("Input: Hackathon", logger.message);
    }

    private static class CapturingLogger implements LambdaLogger {
        private String message;

        @Override
        public void log(String message) {
            this.message = message;
        }

        @Override
        public void log(byte[] message) {
            this.message = new String(message);
        }
    }

    private record TestContext(LambdaLogger logger) implements Context {
        @Override
        public String getAwsRequestId() {
            return "request-id";
        }

        @Override
        public String getLogGroupName() {
            return "log-group";
        }

        @Override
        public String getLogStreamName() {
            return "log-stream";
        }

        @Override
        public String getFunctionName() {
            return "function";
        }

        @Override
        public String getFunctionVersion() {
            return "1";
        }

        @Override
        public String getInvokedFunctionArn() {
            return "arn";
        }

        @Override
        public com.amazonaws.services.lambda.runtime.CognitoIdentity getIdentity() {
            return null;
        }

        @Override
        public com.amazonaws.services.lambda.runtime.ClientContext getClientContext() {
            return null;
        }

        @Override
        public int getRemainingTimeInMillis() {
            return 1000;
        }

        @Override
        public int getMemoryLimitInMB() {
            return 128;
        }

        @Override
        public LambdaLogger getLogger() {
            return logger;
        }
    }
}

package com.aws_lambda;
// Import necessary AWS Lambda libraries
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;

public class LambdaHandler implements RequestHandler<String, String> {
    @Override
    public String handleRequest(String input, Context context) {
        // Log the input received
        context.getLogger().log("Input: " + input);

        // Process the input and return a response
        String output = "Hello, " + input + "!";
        return output;
    }         
}

package com.aws_lambda.controller;

import com.aws_lambda.service.AWSLambdaService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/lambda")
public class LambdaController {

    private final AWSLambdaService lambdaService;

    public LambdaController(AWSLambdaService lambdaService) {
        this.lambdaService = lambdaService;
    }

    @GetMapping("/invoke")
    public String invokeLambda(@RequestParam String input) {
        return lambdaService.invokeLambda("myFirstFunction", input);
    }
}

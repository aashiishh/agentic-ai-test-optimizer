package com.hackathon.orders;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;

import java.math.BigDecimal;

@RestController
@RequestMapping("/orders")
public class OrderDiscountController {

    private final OrderDiscountService orderDiscountService;

    public OrderDiscountController(OrderDiscountService orderDiscountService) {
        this.orderDiscountService = orderDiscountService;
    }

    @GetMapping("/discount")
    public BigDecimal calculateDiscount(
            @RequestParam BigDecimal amount,
            @RequestParam String tier,
            @RequestParam(defaultValue = "false") boolean coupon
    ) {
        try {
            return orderDiscountService.calculateFinalAmount(amount, tier, coupon);
        } catch (IllegalArgumentException exception) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, exception.getMessage(), exception);
        }
    }
}

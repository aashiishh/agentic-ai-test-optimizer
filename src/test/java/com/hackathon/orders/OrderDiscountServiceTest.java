package com.hackathon.orders;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;

class OrderDiscountServiceTest {

    private final OrderDiscountService service = new OrderDiscountService();

    @Test
    void calculateFinalAmountReturnsOriginalAmountForRegularCustomerWithoutCoupon() {
        BigDecimal finalAmount = service.calculateFinalAmount(new BigDecimal("500"), "REGULAR", false);

        assertEquals(new BigDecimal("500.00"), finalAmount);
    }
}

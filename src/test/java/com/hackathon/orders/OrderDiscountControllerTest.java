package com.hackathon.orders;

import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class OrderDiscountControllerTest {

    @Test
    void calculateDiscountDelegatesToOrderDiscountService() {
        OrderDiscountController controller = new OrderDiscountController(new OrderDiscountService());

        BigDecimal finalAmount = controller.calculateDiscount(
                new BigDecimal("1000"),
                "PLATINUM",
                true
        );

        assertEquals(new BigDecimal("750.00"), finalAmount);
    }

    @Test
    void calculateDiscountReturnsBadRequestForInvalidAmount() {
        OrderDiscountController controller = new OrderDiscountController(new OrderDiscountService());

        ResponseStatusException exception = assertThrows(
                ResponseStatusException.class,
                () -> controller.calculateDiscount(new BigDecimal("-1"), "GOLD", false)
        );

        assertEquals(HttpStatus.BAD_REQUEST, exception.getStatusCode());
    }
}

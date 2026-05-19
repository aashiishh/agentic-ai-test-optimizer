package com.hackathon.orders;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class OrderDiscountServiceTest {

    private final OrderDiscountService service = new OrderDiscountService();

    @Test
    void calculateFinalAmountReturnsOriginalAmountForRegularCustomerWithoutCoupon() {
        BigDecimal finalAmount = service.calculateFinalAmount(new BigDecimal("500"), "REGULAR", false);

        assertEquals(new BigDecimal("500.00"), finalAmount);
    }

    @ParameterizedTest
    @CsvSource({
            "PLATINUM,1000,false,800.00",
            "GOLD,1000,false,850.00",
            "SILVER,1000,false,900.00",
            "GOLD,1000,true,800.00",
            "SILVER,999.99,true,899.99"
    })
    void calculateFinalAmountAppliesTierAndEligibleCouponDiscounts(
            String customerTier,
            String orderAmount,
            boolean couponApplied,
            String expectedAmount
    ) {
        BigDecimal finalAmount = service.calculateFinalAmount(
                new BigDecimal(orderAmount),
                customerTier,
                couponApplied
        );

        assertEquals(new BigDecimal(expectedAmount), finalAmount);
    }

    @Test
    void calculateFinalAmountRejectsNullAmount() {
        assertThrows(
                IllegalArgumentException.class,
                () -> service.calculateFinalAmount(null, "GOLD", false)
        );
    }

    @Test
    void calculateFinalAmountRejectsNegativeAmount() {
        assertThrows(
                IllegalArgumentException.class,
                () -> service.calculateFinalAmount(new BigDecimal("-1"), "GOLD", false)
        );
    }
}

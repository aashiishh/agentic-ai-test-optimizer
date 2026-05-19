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

- Target class: `com.hackathon.orders.OrderDiscountService`
- Line coverage: 64.29%
- Branch coverage: 42.86%
- Source path: `src/main/java/com/hackathon/orders/OrderDiscountService.java`
- Test path: `src/test/java/com/hackathon/orders/OrderDiscountServiceTest.java`

## Source Code

```java
package com.hackathon.orders;

import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;

@Service
public class OrderDiscountService {

    public BigDecimal calculateFinalAmount(BigDecimal orderAmount, String customerTier, boolean couponApplied) {
        if (orderAmount == null || orderAmount.signum() < 0) {
            throw new IllegalArgumentException("Order amount must be zero or positive");
        }

        BigDecimal discount = BigDecimal.ZERO;

        if ("PLATINUM".equalsIgnoreCase(customerTier)) {
            discount = new BigDecimal("0.20");
        } else if ("GOLD".equalsIgnoreCase(customerTier)) {
            discount = new BigDecimal("0.15");
        } else if ("SILVER".equalsIgnoreCase(customerTier)) {
            discount = new BigDecimal("0.10");
        }

        if (couponApplied && orderAmount.compareTo(new BigDecimal("1000")) >= 0) {
            discount = discount.add(new BigDecimal("0.05"));
        }

        BigDecimal payableAmount = orderAmount.subtract(orderAmount.multiply(discount));
        return payableAmount.setScale(2, RoundingMode.HALF_UP);
    }
}

```

## Existing Test Code

```java
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

```

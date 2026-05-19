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

# Manual AI Mode Coverage Comparison

This comparison demonstrates the future LLM workflow without using a paid API key.

## What Happened

The dry-run agent selected `com.hackathon.orders.OrderDiscountService` because it had the weakest coverage.

Using the generated prompt, additional JUnit tests were added for:

- platinum, gold, and silver customer tiers
- coupon applied for eligible orders
- coupon ignored below the threshold
- null order amount validation
- negative order amount validation

## Before

- Line coverage: 74.29%
- Branch coverage: 42.86%
- Instruction coverage: 64.96%
- Weakest target: `com.hackathon.orders.OrderDiscountService`

## After

- Line coverage: 88.57%
- Branch coverage: 100.00%
- Instruction coverage: 91.24%
- Improved target: `com.hackathon.orders.OrderDiscountService`

## Result

- Line coverage improved by 14.28 percentage points.
- Branch coverage improved by 57.14 percentage points.
- The project moved above the 80 percent line coverage target.
- The generated tests passed successfully.

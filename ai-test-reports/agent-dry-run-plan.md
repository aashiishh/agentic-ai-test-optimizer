# AI Test Agent Dry Run Plan

This dry run does not call an LLM API. It prepares the target context that will be sent to the model in the next phase.

## Selected Target

- Class: `com.hackathon.orders.OrderDiscountService`
- Source: `src/main/java/com/hackathon/orders/OrderDiscountService.java`
- Test: `src/test/java/com/hackathon/orders/OrderDiscountServiceTest.java`
- Line coverage: 64.29%
- Branch coverage: 42.86%

## Next Automated Phase

1. Send `llm-test-generation-prompt.md` to the configured LLM provider.
2. Write the returned JUnit test to the target test path.
3. Run `./mvnw test`.
4. Regenerate coverage.
5. Compare before/after metrics.
6. Open a pull request if tests pass and coverage improves.

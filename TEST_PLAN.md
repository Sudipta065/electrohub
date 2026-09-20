# ElectroHub Test Plan and Evidence Guide

## Objective

Verify that the online electronics store meets its functional, data-integrity, security and usability requirements. Automated tests cover repeatable core rules; manual tests provide visual and browser evidence for the assignment report.

## Test environment

- Local browser: current Chrome, Edge or Firefox
- Automated framework: pytest and Flask test client
- Automated database: isolated in-memory SQLite
- Production database: hosted PostgreSQL

## Automated test cases

| ID | Requirement | Test | Expected result |
|---|---|---|---|
| AT01 | Account creation | Register with valid information | Account is created and customer is logged in |
| AT02 | Unique accounts | Register twice with the same email | Second registration is rejected |
| AT03 | Authentication | Log in with invalid credentials | Access is rejected without revealing which field failed |
| AT04 | Product catalogue | Open catalogue | Database products are displayed |
| AT05 | Search | Search using a matching/non-matching brand | Correct products are included/excluded |
| AT06 | Error handling | Request a missing product | HTTP 404 is returned |
| AT07 | Cart | Add two units of an available product | Cart accepts the item |
| AT08 | Checkout | Checkout a valid cart | Order/payment records are created and inventory decreases |
| AT09 | Checkout validation | Checkout an empty cart | Checkout is rejected |
| AT10 | Authorization | Customer opens administrator page | HTTP 403 is returned |

Run with:

```bash
pytest -v --cov=app --cov-report=term-missing
```

Capture the final terminal output as automated testing evidence.

## Manual test cases

| ID | Scenario | Steps | Expected result/evidence |
|---|---|---|---|
| MT01 | Responsive interface | Open home/catalog at desktop and mobile widths | Navigation and product grid remain usable; capture both sizes |
| MT02 | Customer journey | Register → search → view product → add to cart → checkout | Each screen succeeds; capture order confirmation |
| MT03 | Stock validation | Add more units than available | Clear stock error appears and data remains unchanged |
| MT04 | Admin product creation | Log in as admin and create a product | Product appears in dashboard and catalogue |
| MT05 | Order management | Change order from Confirmed to Processing | Updated status appears in admin and customer order history |
| MT06 | CSRF protection | Submit a state-changing request without a token outside test mode | Server returns HTTP 400 |
| MT07 | Password security | Inspect the `users` record | Only a password hash is stored, not the original password |
| MT08 | Database persistence | Restart local application and log in again | Account, cart/orders and products remain available |

## Acceptance criteria

- All automated test cases pass.
- No critical or high-severity defect remains open.
- Main customer and administrator workflows work on desktop and mobile.
- Invalid stock, empty cart and unauthorized access are rejected.
- Database records remain consistent after successful and failed operations.

## Report evidence checklist

- Screenshot of successful pytest output
- Home page, product catalogue and product-detail screenshots
- Cart and successful order screenshots
- Administrator dashboard and new-product screenshots
- PostgreSQL table view showing related order, item and payment records
- Deployed Vercel URL and GitHub repository URL

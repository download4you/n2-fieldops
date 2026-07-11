# Verification

| Risk | Minimum |
|---|---|
| Text/config | Parse or syntax check plus diff review |
| Local logic | Focused unit test plus affected static checks |
| Cross-component | Focused integration and relevant unit tests |
| Auth/data/migration | Negative cases, recovery/rollback, broader suite |
| Runtime/deployment | Build/start smoke test and active-config check |

Start with the narrowest test capable of disproving the change; broaden with risk or failures.

# Deployment strategies

**Grounded: 2026-08-26**

## Preview deployments

When the user requests manual testing on pull or merge requests, add a preview deployment (GitHub example first, GitLab review app second):

```yaml
# Deploy preview on PR (Vercel/Netlify/etc.)
deploy-preview:
  runs-on: ubuntu-latest
  if: github.event_name == 'pull_request'
  steps:
    - uses: actions/checkout@v7
    - name: Deploy preview
      env:
        VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
      run: npx vercel --token="$VERCEL_TOKEN"
```

```yaml
# Review app on MR (.gitlab-ci.yml)
review:
  stage: deploy
  script: ./deploy-review.sh "$CI_ENVIRONMENT_SLUG"
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    on_stop: stop-review
  rules:
    - if: $CI_PIPELINE_SOURCE == 'merge_request_event'
```

Stop the review app with a paired `stop-review` job (`environment: { name: review/$CI_COMMIT_REF_SLUG, action: stop }`, `when: manual`). See https://docs.gitlab.com/ci/review_apps/.

## Feature flags

Feature flags decouple deployment from release. Put incomplete or risky features behind flags to:

- Ship code without enabling it. Merge to main early, enable when ready.
- Roll back without redeploying. Disable the flag instead of reverting code.
- Canary new features. Enable for 1% of users, then 10%, then 100%.
- Run A/B tests. Compare behavior with and without the feature.

```typescript
// Simple feature flag pattern
if (featureFlags.isEnabled('new-checkout-flow', { userId })) {
  return renderNewCheckout();
}
return renderLegacyCheckout();
```

**Flag lifecycle:** Create → Enable for testing → Canary → Full rollout → Remove the flag and dead code. Flags that live forever become technical debt. Set a cleanup date when you create them.

## Staged rollouts

```
PR merged to main
    │
    ▼
  Staging deployment (auto)
    │ Manual verification
    ▼
  Production deployment (manual trigger or auto after staging)
    │
    ▼
  Monitor for errors (15-minute window)
    │
    ├── Errors detected → Rollback
    └── Clean → Done
```

## Rollback plan

Every deployment should be reversible:

```yaml
# Manual rollback workflow
name: Rollback
on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to rollback to'
        required: true

jobs:
  rollback:
    runs-on: ubuntu-latest
    steps:
      - name: Rollback deployment
        run: |
          # Deploy the specified previous version
          npx vercel rollback ${{ inputs.version }}
```

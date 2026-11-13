---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Audit these dependencies with the audit-dependencies skill. You have no network access and no
scanner installed, and you may not install anything. Reply with the report as your final
message.

`composer.json`
```json
{
  "require": {
    "php": "^8.2",
    "laravel/framework": "^10.0",
    "guzzlehttp/guzzle": "^7.4",
    "phpoffice/phpspreadsheet": "^1.28"
  }
}
```

There is no `composer.lock` in the repository.

`.github/workflows/deploy.yml`
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: some-org/ssh-deploy@master
        with:
          key: ${{ secrets.DEPLOY_KEY }}
      - run: ssh -o StrictHostKeyChecking=no deploy@prod.example.com ./release.sh
```

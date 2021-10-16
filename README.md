# 🍽️ menu

## Development

```
honcho start

```

## Deployment

```
dokku buildpacks:clear
dokku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git
dokku buildpacks:add heroku/python
dokku ps:scale jobs=1
tail -n +3 .env | xargs dokku config:set
git push dokku
```

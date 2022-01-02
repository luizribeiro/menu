# 🍽️ menu

[![CI](https://github.com/luizribeiro/menu/actions/workflows/ci.yaml/badge.svg)](https://github.com/luizribeiro/menu/actions/workflows/ci.yaml)

## Development

```
honcho start
yarn webpack watch --mode development
```

Or, if you want to debug or do hot reloading in Python:

```
FLASK_ENV=development flask run --host=0.0.0.0
```

## Deployment

```
dokku buildpacks:clear
dokku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git
dokku buildpacks:add heroku/python
dokku buildpacks:add heroku/nodejs
dokku ps:scale jobs=1
tail -n +3 .env | xargs dokku config:set
dokku domains:add menu.thepromisedlan.club
dokku config:set --no-restart "DOKKU_LETSENCRYPT_EMAIL=luizribeiro@gmail.com"
git remote set-url dokku dokku@dokku:menu
git push dokku
dokku letsencrypt:enable
```

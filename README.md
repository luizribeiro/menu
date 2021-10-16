# 🍽️ menu

```
FLASK_APP=app.py FLASK_ENV=development flask run
dokku buildpacks:clear
dokku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git
dokku buildpacks:add heroku/python
dokku ps:scale jobs=1
git push dokku
```

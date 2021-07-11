# blog_back

---

*My first django project. Mistakes were made.*

---

It's a project where authors can publish posts. Users can rate and comment them, as well as subscribe to their favorite authors.

With this project, I learned about:

* Django
* Django templates
* Unittest  
* Bootstrap.js
* DRF
* JWT auth
* Docker
* reCAPTCHA v2

*Also, especially for this project, I started to learn the [Vue.js 3](https://v3.vuejs.org/).*

### Project links:

* Project site: https://kz-projects.tk/blog/
* Vue 3 frontend: https://github.com/KirillZorikov/blog_front/
* Api: https://kz-api.tk/blog/api/v1/
* Admin panel: https://kz-api.tk/blog/admin_panel/
* Docker images: [backend](https://hub.docker.com/repository/docker/kzorikov/blog_back)


There is also a [django_templates](https://github.com/KirillZorikov/blog_back/tree/main/django_templates) part covered with unit tests. This part is outdated and needs to be improved.

### Tech:

Backend side:

* [Python 3.8.5](https://www.python.org/)
* [Django 2.2.6](https://www.djangoproject.com/) 
* [DRF](https://www.django-rest-framework.org/)
* [Nginx](https://www.nginx.com/)
* [Gunicorn](https://gunicorn.org/)
* [Docker](https://www.docker.com/)
* [reCAPTCHA v2](https://developers.google.com/recaptcha/docs/display)

*See the full list of backend dependencies here: [requirements.txt](https://github.com/KirillZorikov/blog_back/blob/main/requirements.txt)*

Frontend side:

* [Vue 3](https://v3.vuejs.org/)
* [Bootstrap.js 4](https://getbootstrap.com/docs/4.0/getting-started/introduction/)
* [CKEditor 5](https://ckeditor.com/docs/ckeditor5/latest/builds/guides/integration/frameworks/vuejs-v3.html)

*See the full list of frontend dependencies here: [package.json](https://github.com/KirillZorikov/blog_front/blob/main/package.json)*

## Project deployment

### Project run
```
docker-compose up
```

### Apply migrations
```
docker-compose exec blog_prod python manage.py migrate
```

### Collect static
```
docker-compose exec blog_prod python manage.py collectstatic
```

### Create superuser
```
docker-compose exec blog_prod python manage.py createsuperuser
```



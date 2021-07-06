# blog_back

<hr/>

*My first django project. Mistakes were made.*

<hr/>

It's a project where authors can publish posts. Users can rate and comment them, as well as subscribe to their favorite authors.

With this project, I learned about:

* Django
* Django templates
* Unittest  
* Bootstrap.js
* DRF
* JWT auth

*Also, especially for this project, I started to learn the [Vue.js 3](https://v3.vuejs.org/).*

### Project links:

* Project site: https://kz-projects.tk/blog
* Vue 3 frontend: https://github.com/KirillZorikov/blog_front
* Api: https://kz-api.tk/blog/api/v1
* Admin panel: https://kz-api.tk/blog/admin_panel
* Docker images: [backend](https://hub.docker.com/repository/docker/kzorikov/blog_back), [frontend](https://hub.docker.com/repository/docker/kzorikov/blog_front)


There is also a [django_templates](https://github.com/KirillZorikov/blog_back/tree/main/django_templates) dir covered with unit tests. This part is outdated and needs to be improved.

## Project setup
```
docker-compose build
```

## Project run
```
docker-compose up
```

## Apply migrations
```
docker-compose exec blog_prod python manage.py migrate
```

## Create superuser
```
docker-compose exec blog_prod python manage.py createsuperuser
```



# Welcome potential new LinkGraph developer!!

For you to be reading this means you will have passed an initial round of testing and interviews. I’m very happy you’ve
made it here!

It’s my hope that you’ll be successful with your `Toy` project, and we have the opportunity to work together. We’ll get
to that below.

First - some things I wanted to share with you:

Django is called a Python Framework for “perfectionists with deadlines”. I’ve built so many powerful and dynamic
applications with it, that I can honestly say that is 100% true! Django changed my life and helped me immensely as a
developer. I’ve been able to build 2 previous startups with it, thanks in part to it, they were both very successful,
and I eventually sold both of them.

I believe building good code is like building a work of art. There are wise choices and poor choices, it helps to have
good taste, lots of practice, and a commitment to mastery. I also believe it’s important to help all developers working
on the team improve as engineers and continue to grow. On our team you’ll find the core values in our engineering
culture are:
excellence, humility, and velocity. We do daily standups, maintain a SCRUM board, and track/reward developer
productivity through issue weights. We give quarterly bonuses to developers for hitting certain issue velocity targets.
I hope we get the chance to work together soon!

_- Manick Bhan, CTO and Founder of LinkGraph_

# The Toy Project

## Part 1: A Simple Blog App with Django

_Expected time: 2 to 6 hours_

We’re going to be building a Blog Application to help a team of writers and editors manage the content they’re creating.
Your goal should be to demonstrate your knowledge of Django and Python best practices.

- use Django 3.1, Python 3, and Django Rest Framework
- run Django application inside a clean virtualenv
- code should pass flake8 linting

### Your Models:

**Article**\
created_at\
title\
content\
status\
written_by (Writer)\
edited_by (Writer)

**Writer**\
is_editor (boolean)\
name\
_- connect to Django User auth model_

### Your Pages:

**Dashboard** (located at “/”)

- this page should show a short writer summary table.
- _hint: the single Django ORM query to get this information should be elegant and clean._

| Writer | Total Articles Written | Total Articles Written Last 30 |
|--------|------------------------|--------------------------------|
| name   | x                      | x                              |
| name   | x                      | x                              |

**Writer Article Detail Page** (located at “/article/<article_id>/”)

- this page should be accessible to all writers and allow them to create a new article instance into the DB.

- the two fields they can edit are title and content
- status should be _read only_
- _hint: use a form_

**Article Approval Page** (located at “/article-approval”)

- this page should be viewable by editors only
- editors should view a list of articles that have not been approved or rejected, and click a button to easily “approve”
  or “reject” an article

**Articles Edited Page** (located at “/articles-edited”)

- this page should be viewable by editors only
- this page should show all the articles approved/rejected by the logged editor.

### Test Cases

- Write at least 3 test cases

## (Optional) Part 2: Demonstrate Docker Knowledge

_Expected time: 1 to 2 hours, depending on experience_

- Create a docker-compose file with 3 services:
    1. blogapp
    2. postgres
    3. redis

- make sure your blogapp mounts a “volume” so that all local file changes to your project propagate inside the docker
  container
- use “depends_on” correctly
- use the “container_name” in a way that makes it easy to find and reference your services


- Create a Makefile that performs with the following commands...\
  **make build**: builds and starts the docker container\
  **make up**: starts the docker container\
  **make ssh**: SSH into the blogapp container\
  **make server**: executes the django python manage.py runserver command inside the running blogapp container\
  **make down**: stops the docker container\
  **make flake8**: runs flake8 linting on the app\
  **make test**: runs your python tests

## (Optional) Part 3: Demonstrate Kubernetes Knowledge

_Expected time: 1 to 2 hours, depending on experience_

Create kubernetes manifests or helm charts to run your blog app inside a kubernetes cluster.

Notes for Your Submission

1) Send the URL to your code on a public GitHub repo.
2) Send include screenshots of all 4 pages of the application.

Thanks, developer! I hope you do a great job, so we can hire you and bring you onto our team.

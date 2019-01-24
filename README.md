# Hello, my name is Zdravomil, the Linter!

## Introduction
Zdravomil is a bot developed in the process of simplifying delivery
of valid and nice containers.
It is triggered by pushes in dit-git repository for dockerfiles
and it uses linters from [colin](https://github.com/user-cont/colin/).

The linter tests are inspired by:
 - [Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
 - [Fedora guidelines](https://fedoraproject.org/wiki/Container:Guidelines)
 - [Container best practices](https://github.com/projectatomic/container-best-practices/)

## How it works

To use zdravomil, you should ensure that your repository has
[github2fedmsg](https://github.com/fedora-infra/github2fedmsg) webhook configured
and there exists at least one Zdravomil instance with
[ucho bot](https://github.com/user-cont/ucho) running (we do not provide this as a service right now).

The Zdravomil instance waits for celery tasks from ucho and when there is new pull request, or comment on a pull request,
Zdravomil runs [colin](https://github.com/user-cont/colin/) linters and posts the results as a github pull request review.

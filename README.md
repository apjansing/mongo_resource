# Custom Resource for [Concourse](https://concourse-ci.org/)

- [Custom Resource for Concourse](#custom-resource-for-concourse)
  - [How the Resource is Written](#how-the-resource-is-written)

This repository is to hold my second ever Concourse resource. I have written one for work and wanted to see if I could do it again for a database I once used and so I could potentially help someone else write their own Concourse resource.

## How the Resource is Written

**!THIS IS AN WORK IN PROGRESS!**

Resources are made up of three parts (as [described here](https://concourse-ci.org/implementing-resource-types.html)):
 * [`/opt/resource/check`](https://concourse-ci.org/implementing-resource-types.html#resource-check)
 * [`/opt/resource/in`](https://concourse-ci.org/implementing-resource-types.html#resource-in)
 * [`/opt/resource/out`](https://concourse-ci.org/implementing-resource-types.html#resource-out)

These resources can be written in any language as long as you can make the `check`, `in`, and `out` executable and be without extensions. I will be writing my `check`, `in`, and `out` in Python.

## Changelog

### v0.1.0

- Test release
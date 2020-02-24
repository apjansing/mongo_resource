# [Accumulo](https://accumulo.apache.org/) Resource for [Concourse](https://concourse-ci.org/)

- [Accumulo Resource for [Concourse](https://concourse-ci.org/)](#accumulo-resource-for-concourse)
  - [What is Accumulo?](#what-is-accumulo)
  - [How the Resource is Written](#how-the-resource-is-written)

This repository is to hold my second ever Concourse resource. I have written one for work and wanted to see if I could do it again for a database I once used and so I could potentially help someone else write their own Concourse resource.

## What is Accumulo?

To quickly summarize what Accumulo is, I've stitched together a couple statements from [Accumulo's site and documentation](https://accumulo.apache.org/).

> Accumulo is distributed key/value store that has cell-based access controls and server-side programming constructs (called [Iterators](https://accumulo.apache.org/docs/2.x/development/iterators)) that allow users to implement custom retrieval or computational purpose within Accumulo TabletServers.

## How the Resource is Written

Resources are made up of three parts (as [described here](https://concourse-ci.org/implementing-resource-types.html)):
 * [`/opt/resource/check`](https://concourse-ci.org/implementing-resource-types.html#resource-check)
 * [`/opt/resource/in`](https://concourse-ci.org/implementing-resource-types.html#resource-in)
 * [`/opt/resource/out`](https://concourse-ci.org/implementing-resource-types.html#resource-out)

These resources can be written in any language as long as you can make the `check`, `in`, and `out` executable and be without extensions. I will be writing my `check`, `in`, and `out` in Python.
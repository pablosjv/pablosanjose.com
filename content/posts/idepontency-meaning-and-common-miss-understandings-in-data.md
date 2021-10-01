---
title: "Idempotence - Meaning and Common Miss-understandings in Data Pipelines"
date: 2021-10-11
draft: false
slug: idepontency-meaning-and-common-miss-understandings-in-data
city: Madrid, S
toc: true
math: true
tags:
- dev
- data
- machine-learning
---


If you have been in the software industry long enough, you have probably heard of the term __*idempotency*__ when talking about infrastructure as code, data pipelines, CRUD operations... It is a common and a useful term. 


But, what does it really mean? and why it is important in the first place?


## Formal formulation


Of course, I like to go to wikipedia:


> __*Idempotence*__ *is the property of certain operations in mathematics and computer science whereby they can be applied multiple times without changing the result beyond the initial application*.


Formally it means that if $f(x) \rightarrow y$ then $f(f(x)) \rightarrow y$. In other words, you can apply the same function over itself and obtain the same result.


This basic definition can be extended if we apply declarative programming. In this paradigm, we define the final state of a system or data, but we don't explicitly define how to achieve it. For certain applications this can mean that  $f(x) \rightarrow y$ $\forall x \in \{\text{Any system state}\}$. This is extremely powerful.


## Computer Science Applications


This is specially useful when we translate it to the __*state*__ of a system. For example, in a backend application:

1. In a CRUD operation in a REST API, calling the POST `/create-user` endpoint with the same parameters has an idempotent effect if we just create the user 1 time.
1. Similarly, if we call a DELETE `/delete-user` endpoint multiple times will delete the user one time and the rest of the calls will don't do anything.

We can see this in practice with multiple types of IaaC tools too, which work declarative. In all of this tools, we define (with YAML or other) the final state of the system. :

1. Kubernetes deployments → Deployment of a docker image with $n $ replicas
1. Terraform → This environment has $n$ EC2 machines
1. Ansible playbooks → The following linux packages are installed.

## Idempotence in Data Pipelines


Having the definition in mind, and concrete examples of its application: should we also apply this to data pipelines? Yes! But, should it be a requirement? No! Let me explain.


> *Data pipelines* __*must*__ *be* __*reproducible*__*.* 


This has some similarities with idempotence, but is not the same. When working with data, we must be able to recreate results for traceability, auditing, and resilience against data loss. However, when looking at the formal definition of idempotence, $f(f(x)) \rightarrow y$ , most of the time it doesn't make sense.


In data pipelines our $x$ is not a state, its a dataset. And our $y$ is a different dataset. In our data pipelines we should be overwriting our data, but instead creating new dataset with our transformations. In this case, all we need is a __*deterministic process*__. We only need that $f(x) \rightarrow y$ at any point in time.


The exception to this rule is when loading data tables in our data warehouse or other storage systems. In this case you want that idempotence. A load of the same data yields always the same result in the final table.


## Reproducibility is Hard - Here is some advice


Even if we don't need to achieve idempotence in our data pipelines, creating reproducible pipelines can already be very hard. Some simple guidelines are:

* Never overwrite datasets. There can be exceptions, but in general data extractions and transformations will create new datasets or tables in your storage system.
* Dates and random seeds are passed by configuration. Never make your pipeline dependent of the moment in time it is executed. This will allow you to run pipelines as they were ran in the past.
* Separate the ETL (Extraction, Transformation, and Load) in separate pipelines. This will allow you the flexibility to rerun a particular section of the data process without modifying production tables (load).
* Version control and tag everything: code, jobs, models, and data. Use a common standard like Semantic Versioning to create the production tags, so they have a clear meaning for all the organization.

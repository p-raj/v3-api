Process
-------

Process is the singular unit, a __task__ that can be executed.
From our perspective it might be the smallest unit of task as well,
but from the 3rd party developers perspective, it may be huge.

For instance, a Process may be:

 - Send Email
 - Send a Push
 - Call a single API
 - Execute a python script


---

### Schema

First, we except schema X (let's call it [Process Schema Spec]),
it contains the set of keys we need to complete any process.
_It may be dependent of the __type__ of process for now._

There are 2 conversions of the PSSpec. PSSpec generates 2 [CoreAPI] Documents.

 - Doc1 (Client). We are using CoreAPI client to call the resource server and return response.
 - Doc2 (Server). Now we need to create a CoreAPI document that will be served to other services/clients,
    so that the client can call the process server.

Eg.

```
            -----  PSSpec  -----
            |                   |
        Client                Server

Client (/api/v1/members/)
Server (/api/v1/processes/<uuid>/execute/)

(Incoming Req.)                                             (Outgoing req.)
--------------> [/api/v1/processes/<uuid>/execute/] -------> [/api/v1/members/] ---
                                                                                    |
--------------> [/api/v1/processes/<uuid>/execute/] <-------------------------------
(Outgoing Resp.)                                             (Incoming resp.)
```

---

### Why [CoreAPI] Documents ?

 - It helps us ease the conversion to other formats using different renderers.
     - [OpenAPIRenderer] - create an OpenAPI compatible document.
 - The document can also be directly used to fire an HTTP request using the coreapi client.



[OpenAPIRenderer]: https://github.com/marcgibbons/django-rest-swagger/blob/e0f5439e4fed8cc84dbae2bbab71af4a0004e1c0/rest_framework_swagger/renderers.py#L25
[CoreAPI]: http://www.coreapi.org/
[Process Schema Spec]: psspec.md
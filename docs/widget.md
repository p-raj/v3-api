Widget
-------

_It is recommended to read document on [Process] before proceeding._

To properly understand the working of the Widget, we need to learn about both the sides of Widget i.e Server & Client.

## Server

Widget is described by us as the Sigma (&Sigma;) of [Process](es), but it is much more & is responsible for

 - managing the template of client widget
 - holding the context of the processes

---

### Managing the template of client

The widget holds all the templates that the widget may transition to in its lifecycle.

> Currently, the template is directly served by the widget & it can be rendered on iOS, Android & Web.


### Holding the context of the processes

Each process needs a context to run. By context, we mean some meta data, some configuration that should/may not be exposed to the client, because

 - it is sensitive, would cause a security flaw if exposed
 - it is static & doesn't make sense to ask for it again from the client.
 - it needs to be filled by the admin, it wouldn't make sense for the user to fill it out, or the user may not be aware of such information

Some examples would be:

 - The API key of the 3rd party service being used
 - The collection name where the form needs to be submitted on [Keen]


### Schema

As mentioned earlier,

 - Process is the singular unit, a __task__ that can be executed.
 - Widget is described as the Sigma (&Sigma;) of [Process](es).

Process generates an OpenAPI compatible document, using the OpenAPIRenderer as described in the [Process] document. We won't go in those details here again.

A sample document looks like:

```json
{
    "swagger": "2.0",
    "info": {
        "title": "",
        "version": "1.0.0"
    },
    "paths": {
        "apis": {
            "post": {...}
        }
    },
    "definitions": {},
    "securityDefinitions": {}
}
```

Notice the keys __"paths"."apis"."post"__, these remain constant and can be directly joined together to form the OpenAPI specification for the client. To make sure we are on the same page let's visualize this.

```json
{                          {                          {
  // process 1               // process 2                 // process 3
  "paths": {                 "paths": {                   "paths": {
      "apis": {                  "apis": {                    "apis": {
          "post": {...}              "post": {...}                "post": {...}
      }                          }                            }
  }                          }                            }
}                          }                          }
```

The processes simply gets merged to form the widget schema.

```json
{
    "swagger": "2.0",
    "info": {
        "title": "Widget",
        "version": "1.0.0"
    },
    "paths": {
        "/p/1": {                 // process 1
            "post": {...}
        },
        "/p/2": {                 // process 2
            "post": {...}
        },
        "/p/3": {                 // process 3
            "post": {...}
        }
    },
    "definitions": {},
    "securityDefinitions": {}
}

```
### Whats the point of these transformations ?

These transformations enables us to mash up __different services together under a single OpenAPI specification__. For eg. 

While building a contact form with preview.

 - __/p/1__ may be  - store the contact form info
 - __/p/2__         - retrieve the contact form data
 - __/p/3__         - publish the final contact form data on keen

 Client doesn't need to know the what service it is interacting with! Client receives the OpenAPI specification that defines how it should interact with the server.


### Why [OpenAPI] specification ?

We have all the information required to call any [Process], it needs to transferred over to client.

 - The [OpenAPI] is becoming the defacto standard for describing the APIs.
 - There are a lot of open source projects that parse the spec & generates client side code.
  - The parser executes the API if the `operationId` is provided
  - Validate the request even before firing the request.
  - Generate a form based UI for testing purpose.
  - Generate integration tests.

## Client

To understand the working of widget on client, it is recommended to first read the documents on [Template] & [Session].

... coming soon ...



[keen]: https://keen.io
[Process]: process.md
[Template]: template.md
[Session]: session.md
[OpenAPI]: https://www.openapis.org
[swagger-js]: https://github.com/swagger-api/swagger-js
[OpenAPI v2.0]: https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md
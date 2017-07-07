Widget
-------

_To understand the working of widget on client, it is recommended to first read the documents on [Template] & [Session]._

> _This document defines how the Widget works on Client. if you are interested in knowing about how it works on the client, see [Widget - Server]_.

The client is responsible for:

 - Rendering the template
 - Exposing the session data to the children components

> _Currently, we have only one type interface, a single template that renders to iOS, Android & web._
> It made sense initially to separate the data out from the template,
> but with the addition of new interfaces like Voice & Bots, it should change &
> the client should receive the template with data filled.

### Rendering the template

... coming soon ...

### Exposing the session data to the children components

... coming soon ...

---


[Template]: ../template.md
[Session]: ../session.md
[Widget - Server]: ../server/widget.md
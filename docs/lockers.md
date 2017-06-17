X-Locker
-------

where X maybe [Runtime], [Widget] or [Process]


---
__Deprecated__: the assumption that these will be different service didn't workout as these are
highly coupled systems, we might be able to take these out later but currently
these represent a single service now.
---

### Widget Locker ?

A runtime can maintain the states of multiple widgets.
If Runtime & Widget were a part of the same service. There might have been
a direct relation either through `ForeignKey` of `ManyToManyField`.
But we have been making sure that these can be separated out easily
on different servers as different services.

So, instead of:

```
            --- Widget
            |
Runtime <------- Widget
            |
            --- Widget
```

we have:

```
                                --- Widget
                                |
Runtime <---> WidgetLocker -------- Widget
                                |
                                --- Widget
```

Widget Locker is just an interface to ease
the listing of widgets associated to a runtime.

Each Runtime however should be able identify the `Entity` accessing itself.
We might need to implement a functionality like [Referer] Header of HTTP Protocol.


[Referer]: https://www.w3.org/Protocols/HTTP/HTRQ_Headers.html#z14
[Process]: process.md
[Widget]: widget.md
[Runtime]: runtime.md

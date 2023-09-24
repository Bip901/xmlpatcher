# XML Patcher

A convenient library for patching XML files with XPath.

Usage example:

```python
from xmlpatcher import XMLDocument
from xmlpatcher.patches import SetValue, Remove

document = XMLDocument("./example.xml")
document.patch(
    SetValue("/Book/@color", "red"),
    Remove("/Book/Page[1]")
)
document.save()
```

The above code will transform this file:

```xml
<Book color="blue">
    <Page>Welcome</Page>
    <Page>Goodbye</Page>
</Book>
```

Into this:

```xml
<Book color="red">
    <Page>Goodbye</Page>
</Book>
```

# Fastapi - Openapi

**Pages:** 9

---

## Configure Swagger UI¶

**URL:** https://fastapi.tiangolo.com/how-to/configure-swagger-ui/

**Contents:**
- Configure Swagger UI¶
- Disable Syntax Highlighting¶
- Change the Theme¶
- Change Default Swagger UI Parameters¶
- Other Swagger UI Parameters¶
- JavaScript-only settings¶

You can configure some extra Swagger UI parameters.

To configure them, pass the swagger_ui_parameters argument when creating the FastAPI() app object or to the get_swagger_ui_html() function.

swagger_ui_parameters receives a dictionary with the configurations passed to Swagger UI directly.

FastAPI converts the configurations to JSON to make them compatible with JavaScript, as that's what Swagger UI needs.

For example, you could disable syntax highlighting in Swagger UI.

Without changing the settings, syntax highlighting is enabled by default:

But you can disable it by setting syntaxHighlight to False:

...and then Swagger UI won't show the syntax highlighting anymore:

The same way you could set the syntax highlighting theme with the key "syntaxHighlight.theme" (notice that it has a dot in the middle):

That configuration would change the syntax highlighting color theme:

FastAPI includes some default configuration parameters appropriate for most of the use cases.

It includes these default configurations:

You can override any of them by setting a different value in the argument swagger_ui_parameters.

For example, to disable deepLinking you could pass these settings to swagger_ui_parameters:

To see all the other possible configurations you can use, read the official docs for Swagger UI parameters.

Swagger UI also allows other configurations to be JavaScript-only objects (for example, JavaScript functions).

FastAPI also includes these JavaScript-only presets settings:

These are JavaScript objects, not strings, so you can't pass them from Python code directly.

If you need to use JavaScript-only configurations like those, you can use one of the methods above. Override all the Swagger UI path operation and manually write any JavaScript you need.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})


@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}
```

Example 2 (python):
```python
from fastapi import FastAPI

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})


@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}
```

Example 3 (json):
```json
# Code above omitted 👆

    dict[str, Any],
    Doc(
        """
        Default configurations for Swagger UI.

        You can use it as a template to add any other configurations needed.
        """
    ),
] = {
    "dom_id": "#swagger-ui",
    "layout": "BaseLayout",
    "deepLinking": True,
    "showExtensions": True,
    "showCommonExtensions": True,
}


# Code below omitted 👇
```

Example 4 (python):
```python
import json
from typing import Annotated, Any, Optional

from annotated_doc import Doc
from fastapi.encoders import jsonable_encoder
from starlette.responses import HTMLResponse

swagger_ui_default_parameters: Annotated[
    dict[str, Any],
    Doc(
        """
        Default configurations for Swagger UI.

        You can use it as a template to add any other configurations needed.
        """
    ),
] = {
    "dom_id": "#swagger-ui",
    "layout": "BaseLayout",
    "deepLinking": True,
    "showExtensions": True,
    "showCommonExtensions": True,
}


def get_swagger_ui_html(
    *,
    openapi_url: Annotated[
        str,
        Doc(
            """
            The OpenAPI URL that Swagger UI should load and use.

            This is normally done automatically by FastAPI using the default URL
            `/openapi.json`.
            """
        ),
    ],
    title: Annotated[
        str,
        Doc(
            """
            The HTML `<title>` content, normally shown in the browser tab.
            """
        ),
    ],
    swagger_js_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the Swagger UI JavaScript.

            It is normally set to a CDN URL.
            """
        ),
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
    swagger_css_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the Swagger UI CSS.

            It is normally set to a CDN URL.
            """
        ),
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    swagger_favicon_url: Annotated[
        str,
        Doc(
            """
            The URL of the favicon to use. It is normally shown in the browser tab.
            """
        ),
    ] = "https://fastapi.tiangolo.com/img/favicon.png",
    oauth2_redirect_url: Annotated[
        Optional[str],
        Doc(
            """
            The OAuth2 redirect URL, it is normally automatically handled by FastAPI.
            """
        ),
    ] = None,
    init_oauth: Annotated[
        Optional[dict[str, Any]],
        Doc(
            """
            A dictionary with Swagger UI OAuth2 initialization configurations.
            """
        ),
    ] = None,
    swagger_ui_parameters: Annotated[
        Optional[dict[str, Any]],
        Doc(
            """
            Configuration parameters for Swagger UI.

            It defaults to [swagger_ui_default_parameters][fastapi.openapi.docs.swagger_ui_default_parameters].
            """
        ),
    ] = None,
) -> HTMLResponse:
    """
    Generate and return the HTML  that loads Swagger UI for the interactive
    API docs (normally served at `/docs`).

    You would only call this function yourself if you needed to override some parts,
    for example the URLs to use to load Swagger UI's JavaScript and CSS.

    Read more about it in the
    [FastAPI docs for Configure Swagger UI](https://fastapi.tiangolo.com/how-to/configure-swagger-ui/)
    and the [FastAPI docs for Custom Docs UI Static Assets (Self-Hosting)](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/).
    """
    current_swagger_ui_parameters = swagger_ui_default_parameters.copy()
    if swagger_ui_parameters:
        current_swagger_ui_parameters.update(swagger_ui_parameters)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="{swagger_css_url}">
    <link rel="shortcut icon" href="{swagger_favicon_url}">
    <title>{title}</title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script src="{swagger_js_url}"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script>
    const ui = SwaggerUIBundle({{
        url: '{openapi_url}',
    """

    for key, value in current_swagger_ui_parameters.items():
        html += f"{json.dumps(key)}: {json.dumps(jsonable_encoder(value))},\n"

    if oauth2_redirect_url:
        html += f"oauth2RedirectUrl: window.location.origin + '{oauth2_redirect_url}',"

    html += """
    presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
    })"""

    if init_oauth:
        html += f"""
        ui.initOAuth({json.dumps(jsonable_encoder(init_oauth))})
        """

    html += """
    </script>
    </body>
    </html>
    """
    return HTMLResponse(html)


def get_redoc_html(
    *,
    openapi_url: Annotated[
        str,
        Doc(
            """
            The OpenAPI URL that ReDoc should load and use.

            This is normally done automatically by FastAPI using the default URL
            `/openapi.json`.
            """
        ),
    ],
    title: Annotated[
        str,
        Doc(
            """
            The HTML `<title>` content, normally shown in the browser tab.
            """
        ),
    ],
    redoc_js_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the ReDoc JavaScript.

            It is normally set to a CDN URL.
            """
        ),
    ] = "https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js",
    redoc_favicon_url: Annotated[
        str,
        Doc(
            """
            The URL of the favicon to use. It is normally shown in the browser tab.
            """
        ),
    ] = "https://fastapi.tiangolo.com/img/favicon.png",
    with_google_fonts: Annotated[
        bool,
        Doc(
            """
            Load and use Google Fonts.
            """
        ),
    ] = True,
) -> HTMLResponse:
    """
    Generate and return the HTML response that loads ReDoc for the alternative
    API docs (normally served at `/redoc`).

    You would only call this function yourself if you needed to override some parts,
    for example the URLs to use to load ReDoc's JavaScript and CSS.

    Read more about it in the
    [FastAPI docs for Custom Docs UI Static Assets (Self-Hosting)](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/).
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>{title}</title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    """
    if with_google_fonts:
        html += """
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    """
    html += f"""
    <link rel="shortcut icon" href="{redoc_favicon_url}">
    <!--
    ReDoc doesn't change outer page styles
    -->
    <style>
      body {{
        margin: 0;
        padding: 0;
      }}
    </style>
    </head>
    <body>
    <noscript>
        ReDoc requires Javascript to function. Please enable it to browse the documentation.
    </noscript>
    <redoc spec-url="{openapi_url}"></redoc>
    <script src="{redoc_js_url}"> </script>
    </body>
    </html>
    """
    return HTMLResponse(html)


def get_swagger_ui_oauth2_redirect_html() -> HTMLResponse:
    """
    Generate the HTML response with the OAuth2 redirection for Swagger UI.

    You normally don't need to use or change this.
    """
    # copied from https://github.com/swagger-api/swagger-ui/blob/v4.14.0/dist/oauth2-redirect.html
    html = """
    <!doctype html>
    <html lang="en-US">
    <head>
        <title>Swagger UI: OAuth2 Redirect</title>
    </head>
    <body>
    <script>
        'use strict';
        function run () {
            var oauth2 = window.opener.swaggerUIRedirectOauth2;
            var sentState = oauth2.state;
            var redirectUrl = oauth2.redirectUrl;
            var isValid, qp, arr;

            if (/code|token|error/.test(window.location.hash)) {
                qp = window.location.hash.substring(1).replace('?', '&');
            } else {
                qp = location.search.substring(1);
            }

            arr = qp.split("&");
            arr.forEach(function (v,i,_arr) { _arr[i] = '"' + v.replace('=', '":"') + '"';});
            qp = qp ? JSON.parse('{' + arr.join() + '}',
                    function (key, value) {
                        return key === "" ? value : decodeURIComponent(value);
                    }
            ) : {};

            isValid = qp.state === sentState;

            if ((
              oauth2.auth.schema.get("flow") === "accessCode" ||
              oauth2.auth.schema.get("flow") === "authorizationCode" ||
              oauth2.auth.schema.get("flow") === "authorization_code"
            ) && !oauth2.auth.code) {
                if (!isValid) {
                    oauth2.errCb({
                        authId: oauth2.auth.name,
                        source: "auth",
                        level: "warning",
                        message: "Authorization may be unsafe, passed state was changed in server. The passed state wasn't returned from auth server."
                    });
                }

                if (qp.code) {
                    delete oauth2.state;
                    oauth2.auth.code = qp.code;
                    oauth2.callback({auth: oauth2.auth, redirectUrl: redirectUrl});
                } else {
                    let oauthErrorMsg;
                    if (qp.error) {
                        oauthErrorMsg = "["+qp.error+"]: " +
                            (qp.error_description ? qp.error_description+ ". " : "no accessCode received from the server. ") +
                            (qp.error_uri ? "More info: "+qp.error_uri : "");
                    }

                    oauth2.errCb({
                        authId: oauth2.auth.name,
                        source: "auth",
                        level: "error",
                        message: oauthErrorMsg || "[Authorization failed]: no accessCode received from the server."
                    });
                }
            } else {
                oauth2.callback({auth: oauth2.auth, token: qp, isValid: isValid, redirectUrl: redirectUrl});
            }
            window.close();
        }

        if (document.readyState !== 'loading') {
            run();
        } else {
            document.addEventListener('DOMContentLoaded', function () {
                run();
            });
        }
    </script>
    </body>
    </html>
        """
    return HTMLResponse(content=html)
```

---

## Metadata and Docs URLs¶

**URL:** https://fastapi.tiangolo.com/tutorial/metadata/

**Contents:**
- Metadata and Docs URLs¶
- Metadata for API¶
- License identifier¶
- Metadata for tags¶
  - Create metadata for tags¶
  - Use your tags¶
  - Check the docs¶
  - Order of tags¶
- OpenAPI URL¶
- Docs URLs¶

You can customize several metadata configurations in your FastAPI application.

You can set the following fields that are used in the OpenAPI specification and the automatic API docs UIs:

You can set them as follows:

You can write Markdown in the description field and it will be rendered in the output.

With this configuration, the automatic API docs would look like:

Since OpenAPI 3.1.0 and FastAPI 0.99.0, you can also set the license_info with an identifier instead of a url.

You can also add additional metadata for the different tags used to group your path operations with the parameter openapi_tags.

It takes a list containing one dictionary for each tag.

Each dictionary can contain:

Let's try that in an example with tags for users and items.

Create metadata for your tags and pass it to the openapi_tags parameter:

Notice that you can use Markdown inside of the descriptions, for example "login" will be shown in bold (login) and "fancy" will be shown in italics (fancy).

You don't have to add metadata for all the tags that you use.

Use the tags parameter with your path operations (and APIRouters) to assign them to different tags:

Read more about tags in Path Operation Configuration.

Now, if you check the docs, they will show all the additional metadata:

The order of each tag metadata dictionary also defines the order shown in the docs UI.

For example, even though users would go after items in alphabetical order, it is shown before them, because we added their metadata as the first dictionary in the list.

By default, the OpenAPI schema is served at /openapi.json.

But you can configure it with the parameter openapi_url.

For example, to set it to be served at /api/v1/openapi.json:

If you want to disable the OpenAPI schema completely you can set openapi_url=None, that will also disable the documentation user interfaces that use it.

You can configure the two documentation user interfaces included:

For example, to set Swagger UI to be served at /documentation and disable ReDoc:

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI

description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="ChimichangApp",
    description=description,
    summary="Deadpool's favorite app. Nuff said.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


@app.get("/items/")
async def read_items():
    return [{"name": "Katana"}]
```

Example 2 (python):
```python
from fastapi import FastAPI

description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="ChimichangApp",
    description=description,
    summary="Deadpool's favorite app. Nuff said.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT",
    },
)


@app.get("/items/")
async def read_items():
    return [{"name": "Katana"}]
```

Example 3 (python):
```python
from fastapi import FastAPI

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)


@app.get("/users/", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]


@app.get("/items/", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]
```

Example 4 (python):
```python
from fastapi import FastAPI

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)


@app.get("/users/", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]


@app.get("/items/", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]
```

---

## OpenAPI docs¶

**URL:** https://fastapi.tiangolo.com/reference/openapi/docs/

**Contents:**
- OpenAPI docs¶
- fastapi.openapi.docs.get_swagger_ui_html ¶
- fastapi.openapi.docs.get_redoc_html ¶
- fastapi.openapi.docs.get_swagger_ui_oauth2_redirect_html ¶
- fastapi.openapi.docs.swagger_ui_default_parameters module-attribute ¶

Utilities to handle OpenAPI automatic UI documentation, including Swagger UI (by default at /docs) and ReDoc (by default at /redoc).

Generate and return the HTML that loads Swagger UI for the interactive API docs (normally served at /docs).

You would only call this function yourself if you needed to override some parts, for example the URLs to use to load Swagger UI's JavaScript and CSS.

Read more about it in the FastAPI docs for Configure Swagger UI and the FastAPI docs for Custom Docs UI Static Assets (Self-Hosting).

The OpenAPI URL that Swagger UI should load and use.

This is normally done automatically by FastAPI using the default URL /openapi.json.

The HTML <title> content, normally shown in the browser tab.

The URL to use to load the Swagger UI JavaScript.

It is normally set to a CDN URL.

TYPE: str DEFAULT: 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js'

The URL to use to load the Swagger UI CSS.

It is normally set to a CDN URL.

TYPE: str DEFAULT: 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css'

The URL of the favicon to use. It is normally shown in the browser tab.

TYPE: str DEFAULT: 'https://fastapi.tiangolo.com/img/favicon.png'

The OAuth2 redirect URL, it is normally automatically handled by FastAPI.

TYPE: Optional[str] DEFAULT: None

A dictionary with Swagger UI OAuth2 initialization configurations.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Configuration parameters for Swagger UI.

It defaults to swagger_ui_default_parameters.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Generate and return the HTML response that loads ReDoc for the alternative API docs (normally served at /redoc).

You would only call this function yourself if you needed to override some parts, for example the URLs to use to load ReDoc's JavaScript and CSS.

Read more about it in the FastAPI docs for Custom Docs UI Static Assets (Self-Hosting).

The OpenAPI URL that ReDoc should load and use.

This is normally done automatically by FastAPI using the default URL /openapi.json.

The HTML <title> content, normally shown in the browser tab.

The URL to use to load the ReDoc JavaScript.

It is normally set to a CDN URL.

TYPE: str DEFAULT: 'https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js'

The URL of the favicon to use. It is normally shown in the browser tab.

TYPE: str DEFAULT: 'https://fastapi.tiangolo.com/img/favicon.png'

Load and use Google Fonts.

TYPE: bool DEFAULT: True

Generate the HTML response with the OAuth2 redirection for Swagger UI.

You normally don't need to use or change this.

Default configurations for Swagger UI.

You can use it as a template to add any other configurations needed.

**Examples:**

Example 1 (rust):
```rust
get_swagger_ui_html(
    *,
    openapi_url,
    title,
    swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
    swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
    oauth2_redirect_url=None,
    init_oauth=None,
    swagger_ui_parameters=None
)
```

Example 2 (html):
```html
def get_swagger_ui_html(
    *,
    openapi_url: Annotated[
        str,
        Doc(
            """
            The OpenAPI URL that Swagger UI should load and use.

            This is normally done automatically by FastAPI using the default URL
            `/openapi.json`.
            """
        ),
    ],
    title: Annotated[
        str,
        Doc(
            """
            The HTML `<title>` content, normally shown in the browser tab.
            """
        ),
    ],
    swagger_js_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the Swagger UI JavaScript.

            It is normally set to a CDN URL.
            """
        ),
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
    swagger_css_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the Swagger UI CSS.

            It is normally set to a CDN URL.
            """
        ),
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    swagger_favicon_url: Annotated[
        str,
        Doc(
            """
            The URL of the favicon to use. It is normally shown in the browser tab.
            """
        ),
    ] = "https://fastapi.tiangolo.com/img/favicon.png",
    oauth2_redirect_url: Annotated[
        Optional[str],
        Doc(
            """
            The OAuth2 redirect URL, it is normally automatically handled by FastAPI.
            """
        ),
    ] = None,
    init_oauth: Annotated[
        Optional[dict[str, Any]],
        Doc(
            """
            A dictionary with Swagger UI OAuth2 initialization configurations.
            """
        ),
    ] = None,
    swagger_ui_parameters: Annotated[
        Optional[dict[str, Any]],
        Doc(
            """
            Configuration parameters for Swagger UI.

            It defaults to [swagger_ui_default_parameters][fastapi.openapi.docs.swagger_ui_default_parameters].
            """
        ),
    ] = None,
) -> HTMLResponse:
    """
    Generate and return the HTML  that loads Swagger UI for the interactive
    API docs (normally served at `/docs`).

    You would only call this function yourself if you needed to override some parts,
    for example the URLs to use to load Swagger UI's JavaScript and CSS.

    Read more about it in the
    [FastAPI docs for Configure Swagger UI](https://fastapi.tiangolo.com/how-to/configure-swagger-ui/)
    and the [FastAPI docs for Custom Docs UI Static Assets (Self-Hosting)](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/).
    """
    current_swagger_ui_parameters = swagger_ui_default_parameters.copy()
    if swagger_ui_parameters:
        current_swagger_ui_parameters.update(swagger_ui_parameters)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="{swagger_css_url}">
    <link rel="shortcut icon" href="{swagger_favicon_url}">
    <title>{title}</title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script src="{swagger_js_url}"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script>
    const ui = SwaggerUIBundle({{
        url: '{openapi_url}',
    """

    for key, value in current_swagger_ui_parameters.items():
        html += f"{json.dumps(key)}: {json.dumps(jsonable_encoder(value))},\n"

    if oauth2_redirect_url:
        html += f"oauth2RedirectUrl: window.location.origin + '{oauth2_redirect_url}',"

    html += """
    presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
    })"""

    if init_oauth:
        html += f"""
        ui.initOAuth({json.dumps(jsonable_encoder(init_oauth))})
        """

    html += """
    </script>
    </body>
    </html>
    """
    return HTMLResponse(html)
```

Example 3 (python):
```python
get_redoc_html(
    *,
    openapi_url,
    title,
    redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js",
    redoc_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
    with_google_fonts=True
)
```

Example 4 (html):
```html
def get_redoc_html(
    *,
    openapi_url: Annotated[
        str,
        Doc(
            """
            The OpenAPI URL that ReDoc should load and use.

            This is normally done automatically by FastAPI using the default URL
            `/openapi.json`.
            """
        ),
    ],
    title: Annotated[
        str,
        Doc(
            """
            The HTML `<title>` content, normally shown in the browser tab.
            """
        ),
    ],
    redoc_js_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the ReDoc JavaScript.

            It is normally set to a CDN URL.
            """
        ),
    ] = "https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js",
    redoc_favicon_url: Annotated[
        str,
        Doc(
            """
            The URL of the favicon to use. It is normally shown in the browser tab.
            """
        ),
    ] = "https://fastapi.tiangolo.com/img/favicon.png",
    with_google_fonts: Annotated[
        bool,
        Doc(
            """
            Load and use Google Fonts.
            """
        ),
    ] = True,
) -> HTMLResponse:
    """
    Generate and return the HTML response that loads ReDoc for the alternative
    API docs (normally served at `/redoc`).

    You would only call this function yourself if you needed to override some parts,
    for example the URLs to use to load ReDoc's JavaScript and CSS.

    Read more about it in the
    [FastAPI docs for Custom Docs UI Static Assets (Self-Hosting)](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/).
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>{title}</title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    """
    if with_google_fonts:
        html += """
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    """
    html += f"""
    <link rel="shortcut icon" href="{redoc_favicon_url}">
    <!--
    ReDoc doesn't change outer page styles
    -->
    <style>
      body {{
        margin: 0;
        padding: 0;
      }}
    </style>
    </head>
    <body>
    <noscript>
        ReDoc requires Javascript to function. Please enable it to browse the documentation.
    </noscript>
    <redoc spec-url="{openapi_url}"></redoc>
    <script src="{redoc_js_url}"> </script>
    </body>
    </html>
    """
    return HTMLResponse(html)
```

---

## Conditional OpenAPI¶

**URL:** https://fastapi.tiangolo.com/how-to/conditional-openapi/

**Contents:**
- Conditional OpenAPI¶
- About security, APIs, and docs¶
- Conditional OpenAPI from settings and env vars¶

If you needed to, you could use settings and environment variables to configure OpenAPI conditionally depending on the environment, and even disable it entirely.

Hiding your documentation user interfaces in production shouldn't be the way to protect your API.

That doesn't add any extra security to your API, the path operations will still be available where they are.

If there's a security flaw in your code, it will still exist.

Hiding the documentation just makes it more difficult to understand how to interact with your API, and could make it more difficult for you to debug it in production. It could be considered simply a form of Security through obscurity.

If you want to secure your API, there are several better things you can do, for example:

Nevertheless, you might have a very specific use case where you really need to disable the API docs for some environment (e.g. for production) or depending on configurations from environment variables.

You can easily use the same Pydantic settings to configure your generated OpenAPI and the docs UIs.

Here we declare the setting openapi_url with the same default of "/openapi.json".

And then we use it when creating the FastAPI app.

Then you could disable OpenAPI (including the UI docs) by setting the environment variable OPENAPI_URL to the empty string, like:

Then if you go to the URLs at /openapi.json, /docs, or /redoc you will just get a 404 Not Found error like:

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openapi_url: str = "/openapi.json"


settings = Settings()

app = FastAPI(openapi_url=settings.openapi_url)


@app.get("/")
def root():
    return {"message": "Hello World"}
```

Example 2 (json):
```json
{
    "detail": "Not Found"
}
```

---

## Separate OpenAPI Schemas for Input and Output or Not¶

**URL:** https://fastapi.tiangolo.com/how-to/separate-openapi-schemas/

**Contents:**
- Separate OpenAPI Schemas for Input and Output or Not¶
- Pydantic Models for Input and Output¶
  - Model for Input¶
  - Input Model in Docs¶
  - Model for Output¶
  - Model for Output Response Data¶
  - Model for Output in Docs¶
  - Model for Input and Output in Docs¶
- Do not Separate Schemas¶
  - Same Schema for Input and Output Models in Docs¶

Since Pydantic v2 was released, the generated OpenAPI is a bit more exact and correct than before. 😎

In fact, in some cases, it will even have two JSON Schemas in OpenAPI for the same Pydantic model, for input and output, depending on if they have default values.

Let's see how that works and how to change it if you need to do that.

Let's say you have a Pydantic model with default values, like this one:

If you use this model as an input like here:

...then the description field will not be required. Because it has a default value of None.

You can confirm that in the docs, the description field doesn't have a red asterisk, it's not marked as required:

But if you use the same model as an output, like here:

...then because description has a default value, if you don't return anything for that field, it will still have that default value.

If you interact with the docs and check the response, even though the code didn't add anything in one of the description fields, the JSON response contains the default value (null):

This means that it will always have a value, it's just that sometimes the value could be None (or null in JSON).

That means that, clients using your API don't have to check if the value exists or not, they can assume the field will always be there, but just that in some cases it will have the default value of None.

The way to describe this in OpenAPI, is to mark that field as required, because it will always be there.

Because of that, the JSON Schema for a model can be different depending on if it's used for input or output:

You can check the output model in the docs too, both name and description are marked as required with a red asterisk:

And if you check all the available Schemas (JSON Schemas) in OpenAPI, you will see that there are two, one Item-Input and one Item-Output.

For Item-Input, description is not required, it doesn't have a red asterisk.

But for Item-Output, description is required, it has a red asterisk.

With this feature from Pydantic v2, your API documentation is more precise, and if you have autogenerated clients and SDKs, they will be more precise too, with a better developer experience and consistency. 🎉

Now, there are some cases where you might want to have the same schema for input and output.

Probably the main use case for this is if you already have some autogenerated client code/SDKs and you don't want to update all the autogenerated client code/SDKs yet, you probably will want to do it at some point, but maybe not right now.

In that case, you can disable this feature in FastAPI, with the parameter separate_input_output_schemas=False.

Support for separate_input_output_schemas was added in FastAPI 0.102.0. 🤓

And now there will be one single schema for input and output for the model, only Item, and it will have description as not required:

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None

# Code below omitted 👇
```

Example 2 (python):
```python
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None


app = FastAPI()


@app.post("/items/")
def create_item(item: Item):
    return item


@app.get("/items/")
def read_items() -> list[Item]:
    return [
        Item(
            name="Portal Gun",
            description="Device to travel through the multi-rick-verse",
        ),
        Item(name="Plumbus"),
    ]
```

Example 3 (python):
```python
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None


app = FastAPI()


@app.post("/items/")
def create_item(item: Item):
    return item


@app.get("/items/")
def read_items() -> list[Item]:
    return [
        Item(
            name="Portal Gun",
            description="Device to travel through the multi-rick-verse",
        ),
        Item(name="Plumbus"),
    ]
```

Example 4 (python):
```python
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None


app = FastAPI()


@app.post("/items/")
def create_item(item: Item):
    return item

# Code below omitted 👇
```

---

## Additional Responses in OpenAPI¶

**URL:** https://fastapi.tiangolo.com/advanced/additional-responses/

**Contents:**
- Additional Responses in OpenAPI¶
- Additional Response with model¶
- Additional media types for the main response¶
- Combining information¶
- Combine predefined responses and custom ones¶
- More information about OpenAPI responses¶

This is a rather advanced topic.

If you are starting with FastAPI, you might not need this.

You can declare additional responses, with additional status codes, media types, descriptions, etc.

Those additional responses will be included in the OpenAPI schema, so they will also appear in the API docs.

But for those additional responses you have to make sure you return a Response like JSONResponse directly, with your status code and content.

You can pass to your path operation decorators a parameter responses.

It receives a dict: the keys are status codes for each response (like 200), and the values are other dicts with the information for each of them.

Each of those response dicts can have a key model, containing a Pydantic model, just like response_model.

FastAPI will take that model, generate its JSON Schema and include it in the correct place in OpenAPI.

For example, to declare another response with a status code 404 and a Pydantic model Message, you can write:

Keep in mind that you have to return the JSONResponse directly.

The model key is not part of OpenAPI.

FastAPI will take the Pydantic model from there, generate the JSON Schema, and put it in the correct place.

The correct place is:

The generated responses in the OpenAPI for this path operation will be:

The schemas are referenced to another place inside the OpenAPI schema:

You can use this same responses parameter to add different media types for the same main response.

For example, you can add an additional media type of image/png, declaring that your path operation can return a JSON object (with media type application/json) or a PNG image:

Notice that you have to return the image using a FileResponse directly.

Unless you specify a different media type explicitly in your responses parameter, FastAPI will assume the response has the same media type as the main response class (default application/json).

But if you have specified a custom response class with None as its media type, FastAPI will use application/json for any additional response that has an associated model.

You can also combine response information from multiple places, including the response_model, status_code, and responses parameters.

You can declare a response_model, using the default status code 200 (or a custom one if you need), and then declare additional information for that same response in responses, directly in the OpenAPI schema.

FastAPI will keep the additional information from responses, and combine it with the JSON Schema from your model.

For example, you can declare a response with a status code 404 that uses a Pydantic model and has a custom description.

And a response with a status code 200 that uses your response_model, but includes a custom example:

It will all be combined and included in your OpenAPI, and shown in the API docs:

You might want to have some predefined responses that apply to many path operations, but you want to combine them with custom responses needed by each path operation.

For those cases, you can use the Python technique of "unpacking" a dict with **dict_to_unpack:

Here, new_dict will contain all the key-value pairs from old_dict plus the new key-value pair:

You can use that technique to reuse some predefined responses in your path operations and combine them with additional custom ones.

To see what exactly you can include in the responses, you can check these sections in the OpenAPI specification:

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Item(BaseModel):
    id: str
    value: str


class Message(BaseModel):
    message: str


app = FastAPI()


@app.get("/items/{item_id}", response_model=Item, responses={404: {"model": Message}})
async def read_item(item_id: str):
    if item_id == "foo":
        return {"id": "foo", "value": "there goes my hero"}
    return JSONResponse(status_code=404, content={"message": "Item not found"})
```

Example 2 (json):
```json
{
    "responses": {
        "404": {
            "description": "Additional Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Message"
                    }
                }
            }
        },
        "200": {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Item"
                    }
                }
            }
        },
        "422": {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/HTTPValidationError"
                    }
                }
            }
        }
    }
}
```

Example 3 (json):
```json
{
    "components": {
        "schemas": {
            "Message": {
                "title": "Message",
                "required": [
                    "message"
                ],
                "type": "object",
                "properties": {
                    "message": {
                        "title": "Message",
                        "type": "string"
                    }
                }
            },
            "Item": {
                "title": "Item",
                "required": [
                    "id",
                    "value"
                ],
                "type": "object",
                "properties": {
                    "id": {
                        "title": "Id",
                        "type": "string"
                    },
                    "value": {
                        "title": "Value",
                        "type": "string"
                    }
                }
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": [
                    "loc",
                    "msg",
                    "type"
                ],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "msg": {
                        "title": "Message",
                        "type": "string"
                    },
                    "type": {
                        "title": "Error Type",
                        "type": "string"
                    }
                }
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        }
                    }
                }
            }
        }
    }
}
```

Example 4 (python):
```python
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel


class Item(BaseModel):
    id: str
    value: str


app = FastAPI()


@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Return the JSON item or an image.",
        }
    },
)
async def read_item(item_id: str, img: bool | None = None):
    if img:
        return FileResponse("image.png", media_type="image/png")
    else:
        return {"id": "foo", "value": "there goes my hero"}
```

---

## OpenAPI Callbacks¶

**URL:** https://fastapi.tiangolo.com/advanced/openapi-callbacks/

**Contents:**
- OpenAPI Callbacks¶
- An app with callbacks¶
- The normal FastAPI app¶
- Documenting the callback¶
- Write the callback documentation code¶
  - Create a callback APIRouter¶
  - Create the callback path operation¶
  - The callback path expression¶
  - Add the callback router¶
  - Check the docs¶

You could create an API with a path operation that could trigger a request to an external API created by someone else (probably the same developer that would be using your API).

The process that happens when your API app calls the external API is named a "callback". Because the software that the external developer wrote sends a request to your API and then your API calls back, sending a request to an external API (that was probably created by the same developer).

In this case, you could want to document how that external API should look like. What path operation it should have, what body it should expect, what response it should return, etc.

Let's see all this with an example.

Imagine you develop an app that allows creating invoices.

These invoices will have an id, title (optional), customer, and total.

The user of your API (an external developer) will create an invoice in your API with a POST request.

Then your API will (let's imagine):

Let's first see how the normal API app would look like before adding the callback.

It will have a path operation that will receive an Invoice body, and a query parameter callback_url that will contain the URL for the callback.

This part is pretty normal, most of the code is probably already familiar to you:

The callback_url query parameter uses a Pydantic Url type.

The only new thing is the callbacks=invoices_callback_router.routes as an argument to the path operation decorator. We'll see what that is next.

The actual callback code will depend heavily on your own API app.

And it will probably vary a lot from one app to the next.

It could be just one or two lines of code, like:

But possibly the most important part of the callback is making sure that your API user (the external developer) implements the external API correctly, according to the data that your API is going to send in the request body of the callback, etc.

So, what we will do next is add the code to document how that external API should look like to receive the callback from your API.

That documentation will show up in the Swagger UI at /docs in your API, and it will let external developers know how to build the external API.

This example doesn't implement the callback itself (that could be just a line of code), only the documentation part.

The actual callback is just an HTTP request.

When implementing the callback yourself, you could use something like HTTPX or Requests.

This code won't be executed in your app, we only need it to document how that external API should look like.

But, you already know how to easily create automatic documentation for an API with FastAPI.

So we are going to use that same knowledge to document how the external API should look like... by creating the path operation(s) that the external API should implement (the ones your API will call).

When writing the code to document a callback, it might be useful to imagine that you are that external developer. And that you are currently implementing the external API, not your API.

Temporarily adopting this point of view (of the external developer) can help you feel like it's more obvious where to put the parameters, the Pydantic model for the body, for the response, etc. for that external API.

First create a new APIRouter that will contain one or more callbacks.

To create the callback path operation use the same APIRouter you created above.

It should look just like a normal FastAPI path operation:

There are 2 main differences from a normal path operation:

The callback path can have an OpenAPI 3 expression that can contain parts of the original request sent to your API.

In this case, it's the str:

So, if your API user (the external developer) sends a request to your API to:

then your API will process the invoice, and at some point later, send a callback request to the callback_url (the external API):

with a JSON body containing something like:

and it would expect a response from that external API with a JSON body like:

Notice how the callback URL used contains the URL received as a query parameter in callback_url (https://www.external.org/events) and also the invoice id from inside of the JSON body (2expen51ve).

At this point you have the callback path operation(s) needed (the one(s) that the external developer should implement in the external API) in the callback router you created above.

Now use the parameter callbacks in your API's path operation decorator to pass the attribute .routes (that's actually just a list of routes/path operations) from that callback router:

Notice that you are not passing the router itself (invoices_callback_router) to callback=, but the attribute .routes, as in invoices_callback_router.routes.

Now you can start your app and go to http://127.0.0.1:8000/docs.

You will see your docs including a "Callbacks" section for your path operation that shows how the external API should look like:

**Examples:**

Example 1 (python):
```python
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Invoice(BaseModel):
    id: str
    title: str | None = None
    customer: str
    total: float


class InvoiceEvent(BaseModel):
    description: str
    paid: bool


class InvoiceEventReceived(BaseModel):
    ok: bool


invoices_callback_router = APIRouter()


@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    pass


@app.post("/invoices/", callbacks=invoices_callback_router.routes)
def create_invoice(invoice: Invoice, callback_url: HttpUrl | None = None):
    """
    Create an invoice.

    This will (let's imagine) let the API user (some external developer) create an
    invoice.

    And this path operation will:

    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").
    """
    # Send the invoice, collect the money, send the notification (the callback)
    return {"msg": "Invoice received"}
```

Example 2 (python):
```python
from typing import Union

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Invoice(BaseModel):
    id: str
    title: Union[str, None] = None
    customer: str
    total: float


class InvoiceEvent(BaseModel):
    description: str
    paid: bool


class InvoiceEventReceived(BaseModel):
    ok: bool


invoices_callback_router = APIRouter()


@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    pass


@app.post("/invoices/", callbacks=invoices_callback_router.routes)
def create_invoice(invoice: Invoice, callback_url: Union[HttpUrl, None] = None):
    """
    Create an invoice.

    This will (let's imagine) let the API user (some external developer) create an
    invoice.

    And this path operation will:

    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").
    """
    # Send the invoice, collect the money, send the notification (the callback)
    return {"msg": "Invoice received"}
```

Example 3 (json):
```json
callback_url = "https://example.com/api/v1/invoices/events/"
httpx.post(callback_url, json={"description": "Invoice paid", "paid": True})
```

Example 4 (python):
```python
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Invoice(BaseModel):
    id: str
    title: str | None = None
    customer: str
    total: float


class InvoiceEvent(BaseModel):
    description: str
    paid: bool


class InvoiceEventReceived(BaseModel):
    ok: bool


invoices_callback_router = APIRouter()


@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    pass


@app.post("/invoices/", callbacks=invoices_callback_router.routes)
def create_invoice(invoice: Invoice, callback_url: HttpUrl | None = None):
    """
    Create an invoice.

    This will (let's imagine) let the API user (some external developer) create an
    invoice.

    And this path operation will:

    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").
    """
    # Send the invoice, collect the money, send the notification (the callback)
    return {"msg": "Invoice received"}
```

---

## Extending OpenAPI¶

**URL:** https://fastapi.tiangolo.com/how-to/extending-openapi/

**Contents:**
- Extending OpenAPI¶
- The normal process¶
- Overriding the defaults¶
  - Normal FastAPI¶
  - Generate the OpenAPI schema¶
  - Modify the OpenAPI schema¶
  - Cache the OpenAPI schema¶
  - Override the method¶
  - Check it¶

There are some cases where you might need to modify the generated OpenAPI schema.

In this section you will see how.

The normal (default) process, is as follows.

A FastAPI application (instance) has an .openapi() method that is expected to return the OpenAPI schema.

As part of the application object creation, a path operation for /openapi.json (or for whatever you set your openapi_url) is registered.

It just returns a JSON response with the result of the application's .openapi() method.

By default, what the method .openapi() does is check the property .openapi_schema to see if it has contents and return them.

If it doesn't, it generates them using the utility function at fastapi.openapi.utils.get_openapi.

And that function get_openapi() receives as parameters:

The parameter summary is available in OpenAPI 3.1.0 and above, supported by FastAPI 0.99.0 and above.

Using the information above, you can use the same utility function to generate the OpenAPI schema and override each part that you need.

For example, let's add ReDoc's OpenAPI extension to include a custom logo.

First, write all your FastAPI application as normally:

Then, use the same utility function to generate the OpenAPI schema, inside a custom_openapi() function:

Now you can add the ReDoc extension, adding a custom x-logo to the info "object" in the OpenAPI schema:

You can use the property .openapi_schema as a "cache", to store your generated schema.

That way, your application won't have to generate the schema every time a user opens your API docs.

It will be generated only once, and then the same cached schema will be used for the next requests.

Now you can replace the .openapi() method with your new function.

Once you go to http://127.0.0.1:8000/redoc you will see that you are using your custom logo (in this example, FastAPI's logo):

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
```

Example 2 (python):
```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
```

Example 3 (python):
```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
```

Example 4 (python):
```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
```

---

## OpenAPI models¶

**URL:** https://fastapi.tiangolo.com/reference/openapi/models/

**Contents:**
- OpenAPI models¶
- fastapi.openapi.models ¶
  - SchemaType module-attribute ¶
  - SchemaOrBool module-attribute ¶
  - SecurityScheme module-attribute ¶
  - BaseModelWithConfig ¶
    - model_config class-attribute instance-attribute ¶
  - Contact ¶
    - name class-attribute instance-attribute ¶
    - url class-attribute instance-attribute ¶

OpenAPI Pydantic models used to generate and validate the generated OpenAPI.

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

Bases: BaseModelWithConfig

**Examples:**

Example 1 (unknown):
```unknown
SchemaType = Literal[
    "array",
    "boolean",
    "integer",
    "null",
    "number",
    "object",
    "string",
]
```

Example 2 (unknown):
```unknown
SchemaOrBool = Union[Schema, bool]
```

Example 3 (unknown):
```unknown
SecurityScheme = Union[
    APIKey, HTTPBase, OAuth2, OpenIdConnect, HTTPBearer
]
```

Example 4 (unknown):
```unknown
model_config = {'extra': 'allow'}
```

---

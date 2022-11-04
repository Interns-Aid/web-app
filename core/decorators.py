from flask_apispec.annotations import annotate, activate


def doc_protected(inherit=None, **kwargs):
    """
    Decorator to add authorization header in requests

    """

    def wrapper(func):
        params = {
            "params": {
                **kwargs.pop("params", {}),
                **{
                    "Authorization": {
                        "type": "string",
                        "description": "Refresh Token"
                        if kwargs.get("refresh", None)
                        else "Authorization Token",
                        "in": "header",
                        "required": True,
                    }
                },
            }
        }
        annotate(func, "docs", [{**kwargs, **params}], inherit=inherit)
        return activate(func)

    return wrapper

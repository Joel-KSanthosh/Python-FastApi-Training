# Important Concepts of FastApi

**FastApi Documentation**: <https://fastapi.tiangolo.com/>  
  
## General Idea
- FastApi is asychronous python based framework mainly used for building REST APIs.  
- Uses uvicorn for asgi.
- Built on top of Starlette and Pydantic.  
- Always use type hints.

## Main Concepts
- ### Note<hr>
    - **model_config = {"extra": "forbid"}**  
    forbids additional value to be inserted into a predefined model.

1. **Query()**
    - Used for query params.
    - Prefer using Annotated when using Query.
    - If query params of type is to be used use Annotated and Query with no paramters (i.e; Query()), else it'll not work.  
    - Supports number validations.
    - Query params model might be important.  
    eg: **async def read_items(filter_query: Annotated[FilterParams, Query()]):**  
    Where FilterParams is the model for using query params.

2. **Path()**
    - Prefer using Annotated when using Path.
    - Path parameter is always required (Cannot have a default value).
    - Supports number validations.  

3. **Body()**
    - Can define singular request body using Body.  
    eg: **importance: Annotated[int, Body()]**
    - Can use multiple request body  
    eg :

        ```yaml 
        {
            "item": {
                "name": "Foo",
                "description": "The pretender",
                "price": 42.0,
                "tax": 3.2
            },
            "user": {
                "username": "dave",
                "full_name": "Dave Grohl"
            },
            "importance": 5
        }
        ```
    - Can embed single body parameter  
    eg: **item: Annotated[Item, Body(embed=True)]**

        ```yaml
        {
            "item": {
                "name": "Foo",
                "description": "The pretender",
                "price": 42.0,
                "tax": 3.2
            }
        }
        ```

4. **Cookie()**

5. **Header()**

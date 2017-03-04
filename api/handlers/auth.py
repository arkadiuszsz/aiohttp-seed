from api.helpers.view import JsonView
from api.helpers.schema import query_schema
from api.schemas.auth import LoginSchema


class AuthView(JsonView):
    """AuthView
    ---
    parameters:
        - name: some
          in: path
          type: string
          description: Affiliate uuid
    """

    async def get(self):
        """Get token
        ---
        tags: ['auth']
        summary: Test
        responses:
            200:
                description: Something
        """
        return self.request.match_info

    @query_schema(LoginSchema(), default_in='formData')
    async def post(self):
        """Auth credentials action
        ---
        tags: ['auth']
        summary: Request authorization token
        responses:
            200:
                description: return authorisation token
        """
        return self.request.arguments

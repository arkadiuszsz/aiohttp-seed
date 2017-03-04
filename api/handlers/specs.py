from api.helpers.view import JsonView

from api.specs import spec


class SpecsView(JsonView):

    @staticmethod
    async def get():
        """API specifies
        ---
        tags: ["doc"]
        """
        return spec.to_dict()

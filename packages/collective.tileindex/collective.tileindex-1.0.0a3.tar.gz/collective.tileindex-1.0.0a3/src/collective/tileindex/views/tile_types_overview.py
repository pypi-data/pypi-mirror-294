from functools import cached_property
from plone import api
from Products.Five.browser import BrowserView


class TileTypesOverview(BrowserView):
    @cached_property
    def tile_index(self):
        catalog = api.portal.get_tool(name="portal_catalog")
        return catalog.Indexes.get("tile_types")

    @cached_property
    def block_index(self):
        catalog = api.portal.get_tool(name="portal_catalog")
        return catalog.Indexes.get("block_types")

    @cached_property
    def tileorblock(self):
        if self.tile_index and not self.block_index:
            return "tile"
        elif not self.tile_index and self.block_index:
            return "block"
        return

    @cached_property
    def indexname(self):
        return f"{self.tileorblock}_types"

    @cached_property
    def indexmethod(self):
        return f"{self.tileorblock}_index"

    @cached_property
    def numObjects(self):
        return getattr(self, self.indexmethod).numObjects()

    @cached_property
    def alphabetical(self):
        return sorted(getattr(self, self.indexmethod).uniqueValues())

    @cached_property
    def numerical(self):
        items = sorted(
            [
                (len(value), key)
                for (key, value) in getattr(self, self.indexmethod).items()
            ],
            reverse=True,
        )
        result = []
        for item in items:
            result.append({"number": item[0], "tile": item[1]})
        return result

    @cached_property
    def search_results(self):
        tile = self.request.get("tile")
        if not tile:
            return (None, None)
        unpublished = []
        published = []
        query = {"sort_on": "path", "sort_order": "ascending"}
        query[self.indexname] = tile
        for item in api.content.find(**query):
            if item["review_state"] == "published":
                published.append(item)
            else:
                unpublished.append(item)
        return (published, unpublished)

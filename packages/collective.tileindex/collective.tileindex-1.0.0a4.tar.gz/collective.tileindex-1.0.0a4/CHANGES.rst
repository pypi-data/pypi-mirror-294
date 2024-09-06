Changelog
=========


1.0.0a4 (2024-09-05)
--------------------

- Make ``plone.app.blocks`` dependency optional.
  If you don't have it yet, you have no tiles, so we do not create our ``tile_types`` catalog index.
  The control panel can then be used for search Volto blocks.
  [maurits]


1.0.0a3 (2024-09-05)
--------------------

- Make the package work for the ``blocks_index`` as well, so for use with Volto blocks.
  [fredvd]


1.0.0a2 (2023-11-21)
--------------------

- Add controlpanel link to the tile types overview. [fredvd]

- Show published and Private/other counts when using the tile_types_overview and
  clicking on individual tiles to see the found mosaic pages.
  [fredvd]


1.0.0a1 (2023-11-16)
--------------------

- Initial release.
  [fredvd, maurits]

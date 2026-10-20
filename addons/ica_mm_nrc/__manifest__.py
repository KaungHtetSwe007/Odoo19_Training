{
    "name": "Myanmar NRC",
    "summary": "Add Myanmar NRC data, township records, and NRC fields on contacts.",
    "version": "19.0.1.0.0",
    "category": "Contacts",
    "author": "Agga, IdeaCode Academy",
    "maintainer": "IdeaCode Academy",
    "website": "https://www.linkedin.com/company/ideacode-academy",
    "support": "hanzawnyineonline@gmail.com",
    "depends": ["base", "contacts"],
    "data": [
        "data/1KachinState.xml",
        "data/2KayahState.xml",
        "data/3KayinState.xml",
        "data/4ChinState.xml",
        "data/5SagaingRegion.xml",
        "data/6TanintharyiRegion.xml",
        "data/7BagoRegion.xml",
        "data/8MagwayRegion.xml",
        "data/9MandalayRegion.xml",
        "data/9NaypyidawUnionTerritoryRegion.xml",
        "data/10MonState.xml",
        "data/11RakhineState.xml",
        "data/12YangonRegion.xml",
        "data/13ShanState.xml",
        "data/14AyeyarwadyRegion.xml",

        "security/ir.model.access.csv",
        "views/res_country_state_township.xml",
        "views/res_partner.xml",
        "views/menus.xml",
    ],
    "description": """
Myanmar NRC
===========

Add Myanmar NRC information to contacts with state, township, township code,
state code, and NRC number fields.

Key Features
------------
* Load Myanmar state and region township data.
* Add township records linked to states and regions.
* Add NRC number and township fields on contacts.
* Show Myanmar NRC menus for maintaining township data.
* Support translated township and code values.
""",
    "images": ["static/description/img.png"],

    "installable": True,
    "license": "LGPL-3",
}

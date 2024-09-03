# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from carbon.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    INTEGRATIONS = "Integrations"
    FILES = "Files"
    UTILITIES = "Utilities"
    USERS = "Users"
    EMBEDDINGS = "Embeddings"
    WEBHOOKS = "Webhooks"
    ORGANIZATIONS = "Organizations"
    AUTH = "Auth"
    DATA_SOURCES = "Data Sources"
    GETTING_STARTED = "Getting Started"
    CARBON_CONNECT = "Carbon Connect"
    HEALTH = "Health"
    CONTACT_US = "Contact Us"

import copy
import datetime
import hashlib
import json
from abc import ABC


class Resource(ABC):
    """Base class for cloud resource object."""

    def __init__(self, d: dict):
        self._raw = d

        self._provider_type = d.get("provider_type", "simulator")

        self._id = d.get("id", None)
        self._account_id = d.get("accountId", None)
        self._name = d.get("name", None)
        self._type = d.get("type", None)
        self._location = d.get("location", None)
        self._tags = d.get("tags", {})

        self._environment = self._tags.get('Environment', None)
        self._app_name = self._tags.get('AppName', None)
        self._tag_name = self._tags.get('Name', None)
        self._tag_guid = self._get_tag_guid()

    @staticmethod
    def _jsonify(o):
        """Handle any non-json serializable types.

        :param o: object
        :return: str of json
        """
        if isinstance(o, datetime.datetime):
            return o.__str__()

    def _generate_hash(self, data):
        """Generate a hash of data provided.

        :param data: Data to use for hash
        :return: Sha-1 hash of data
        """
        stringified = json.dumps(data, ensure_ascii=True,
                                 sort_keys=True,
                                 default=self._jsonify).encode()

        return hashlib.sha1(stringified).hexdigest()

    def _get_tag_guid(self):
        """Get GUID for tag.

        :return: GUID
        """
        tag_guid = self._tags.get('TagGuid', None)
        if tag_guid is None:
            tag_guid = self._tags.get('AppDefined02', None)
        return tag_guid

    @property
    def raw(self):
        """
        :return: raw resource data
        """
        return self._raw

    @property
    def id(self):
        """
        :return: resource ID
        """
        return self._id

    @property
    def environment(self):
        """
        :return: environment of resource
        """
        return self._environment

    @property
    def app_name(self):
        """
        :return: app name
        """
        return self._app_name

    @property
    def tag_guid(self):
        """
        :return: guid of tag
        """
        return self._tag_guid

    @property
    def tag_name(self):
        """
        :return: name of tag
        """
        return self._tag_name

    @property
    def account_id(self):
        """
        :return: account ID for account resource lives in
        """
        return self._account_id

    @property
    def name(self):
        """
        :return: name of resource
        """
        return self._name

    @name.setter
    def name(self, value):
        """Set name of resource.

        :param value: new name
        :return: None
        """
        self._name = value

    @property
    def type(self):
        """
        :return: resource type
        """
        return self._type

    @property
    def location(self):
        """
        :return: location of resource
        """
        return self._location

    @location.setter
    def location(self, value):
        """Set location of resource.

        :param value: location
        :return: None
        """
        self._location = value

    @property
    def tags(self):
        """
        :return: Dictionary of tags
        """
        return self._tags

    @tags.setter
    def tags(self, value):
        """Set tags for resource.

        :param value: tags dictionary
        :return: None
        """
        self._tags = value

    @property
    def provider_type(self):
        """
        :return: Resource provider type
        """
        return self._provider_type

    @provider_type.setter
    def provider_type(self, provider_type):
        """Set resource provider type.

        :param provider_type: new provider type for resource
        :return: None
        """
        self._provider_type = provider_type

    def to_normalized_dict(self):
        """Create normalized dictionary for resource across cloud providers.

        :return: Normalized dictionary
        """

        out_dict = copy.deepcopy(self.raw)  # Populate with full meta-data?

        out_dict.update({'AppDefined02': self.tag_guid})
        out_dict.update({"Environment": self.environment})
        out_dict.update(
            {"ResourceType": self.type.replace("/", "_").replace(".", "_")})
        out_dict.update({"ResourceId": self.name})
        out_dict.update({"ARN": self.id})
        out_dict.update({"Name": self.tag_name})
        out_dict.update({"Type": self.type})
        out_dict.update({"Region": self.location})
        out_dict.update({"OwnerId": self.account_id})
        out_dict.update({"AppName": self.app_name})
        out_dict.update({"Tags": self.tags})

        out_dict.update({"Hash": self._generate_hash(out_dict)})

        return out_dict

    def to_dict(self):
        """
        :return: Dictionary with resource data
        """
        return {
            'id': self.id,
            'accountId': self._account_id,
            'name': self.name,
            'type': self.type,
            'location': self.location,
            'tags': self.tags,
            'providerType': self.provider_type
        }

    def to_str(self):
        """
        :return: JSON str of resource dictionary
        """
        return json.dumps(self.to_dict())

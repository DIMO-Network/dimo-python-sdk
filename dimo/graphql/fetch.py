class Fetch:
    def __init__(self, dimo_instance):
        self.dimo = dimo_instance

    # Primary query method
    def query(self, query, vehicle_jwt):
        return self.dimo.query("Fetch", query, token=vehicle_jwt)

    def get_index_keys(self, vehicle_jwt: str, did: str, limit=None, filter=None) -> dict:
        query = """
query GetIndexes($did: String!, $limit: Int, $filter: CloudEventFilter) {
  indexes(did: $did, limit: $limit, filter: $filter) {
    header {
      id
      source
      producer
      specversion
      subject
      time
      type
      datacontenttype
      dataschema
      dataversion
      signature
      tags
    }
    indexKey
  }
}"""
        variables = {"did": did}
        if limit is not None:
            variables["limit"] = limit
        if filter is not None:
            variables["filter"] = filter
        return self.dimo.query("Fetch", query, token=vehicle_jwt, variables=variables)

    def get_latest_index_key(self, vehicle_jwt: str, did: str, filter=None) -> dict:
        query = """
query GetLatestIndex($did: String!, $filter: CloudEventFilter) {
  latestIndex(did: $did, filter: $filter) {
    header {
      id
      source
      producer
      specversion
      subject
      time
      type
      datacontenttype
      dataschema
      dataversion
      signature
      tags
    }
    indexKey
  }
}"""
        variables = {"did": did}
        if filter is not None:
            variables["filter"] = filter
        return self.dimo.query("Fetch", query, token=vehicle_jwt, variables=variables)

    def get_latest_object(self, vehicle_jwt: str, did: str, filter=None) -> dict:
        query = """
query GetLatestCloudEvent($did: String!, $filter: CloudEventFilter) {
  latestCloudEvent(did: $did, filter: $filter) {
    header {
      id
      source
      producer
      specversion
      subject
      time
      type
      datacontenttype
      dataschema
      dataversion
      signature
      tags
    }
    data
    dataBase64
  }
}"""
        variables = {"did": did}
        if filter is not None:
            variables["filter"] = filter
        return self.dimo.query("Fetch", query, token=vehicle_jwt, variables=variables)

    def get_objects(self, vehicle_jwt: str, did: str, limit=None, filter=None) -> dict:
        query = """
query GetCloudEvents($did: String!, $limit: Int, $filter: CloudEventFilter) {
  cloudEvents(did: $did, limit: $limit, filter: $filter) {
    header {
      id
      source
      producer
      specversion
      subject
      time
      type
      datacontenttype
      dataschema
      dataversion
      signature
      tags
    }
    data
    dataBase64
  }
}"""
        variables = {"did": did}
        if limit is not None:
            variables["limit"] = limit
        if filter is not None:
            variables["filter"] = filter
        return self.dimo.query("Fetch", query, token=vehicle_jwt, variables=variables)

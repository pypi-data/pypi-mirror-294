
def es_bulk_item(index: str, id: str, source_json: str):
  return {
    '_op_type': 'index',
    '_index': index,
    '_id': id,
    '_source': source_json,
  }


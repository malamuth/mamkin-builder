class Service:
    def __init__(self):
        self.cache = {}
        self.documents = {("red", "42"): "red-private", ("blue", "42"): "blue-private"}
    def fetch(self, user, tenant, document_id):
        if document_id in self.cache:
            return self.cache[document_id]
        if tenant not in user["tenants"]:
            raise PermissionError("denied")
        result = self.documents[(tenant, document_id)]
        self.cache[document_id] = result
        return result

def migrate_sessions(sessions):
    return []

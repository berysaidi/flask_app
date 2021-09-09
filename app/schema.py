# Schema used to validate request data
SCHEMA = {
    "type" : "object",
    "properties" : {
        "profile" : {
            "type" : "object",
            "properties" : {
                "applications" : {
                    "type" : "array",
                    "minItems": 1,
                    "uniqueItems": True,
                    "properties" :             {
                        "applicationId" : {"type" : "string"},
                        "version" : {"type" : "string"},
                        },
                    "required": ["applicationId", "version"]
                    }
                },
            "required": ["applications"]
            }
        },
    "required": ["profile"]
}

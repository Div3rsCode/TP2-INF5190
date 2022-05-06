modifier_glissade_schema = {
    'type': 'object',
    'required': ['nom_installation', 'ouvert', 'deblaye', 'condition'],
    'properties': {
        'nom_installation': {
            'type': 'string'
        },
        'ouvert': {
            'type': 'boolean'
        },

        'deblaye': {
            'type': 'boolean'
        },

        'condition': {
            'type': 'string',
            'pattern': ""
        }
    },
    'additionalProperties': False
}

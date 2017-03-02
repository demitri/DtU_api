import json


def selection_to_where(selection):

    if selection is None:
        return ''

    selection = json.loads(selection)

    if selection['type'] == 'range':
        where = 'WHERE {x_attribute} >= {x_min} AND {x_attribute} <= {x_max}'.format(**selection)
    elif selection['type'] == 'rectangle':
        where = 'WHERE {x_attribute} >= {x_min} AND {x_attribute} <= {x_max} AND {y_attribute} >= {y_min} AND {y_attribute} <= {y_max}'.format(**selection)
    else:
        where = ''
    return where

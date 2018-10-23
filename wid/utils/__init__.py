def format_activities(tup):
    if len(tup) > 0:
        return dict([(t[0], {'name': t[1], 'description': t[2]}) for t in tup])
    else:
        return None


def format_activities_j(tup):
    return dict(id=tup[0], name=tup[2], description=tup[3])

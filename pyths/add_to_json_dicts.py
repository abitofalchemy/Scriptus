gjson.setdefault('edges',[]).append({'source': {'id': src_id[0],
  7                                                 'label': s},
  6                                                 'target': {'id': trg_id[0],
  5                                                 'label': t},
  4                                                 'value': relxn})

print(dumps(gjson, indent=4, sort_keys=True))



def format_records(records):
    if not records:
        return '(Empty recordset)'
    return '<br>'.join(str(rec) for rec in records)

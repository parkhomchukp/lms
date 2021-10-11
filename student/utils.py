def format_records(records):
    if not records:
        return '(Empty recordset)'
    return '<br>'.join(f'<a href="/students/edit/{rec.id}/">EDIT</a> {rec}' for rec in records)

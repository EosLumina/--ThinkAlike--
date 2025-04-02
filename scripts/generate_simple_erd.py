from graphviz import Digraph

dot = Digraph(comment='ThinkAlike ER Diagram')
dot.attr('node', shape='record')

# Define tables
tables = {
    'Users': ['user_id', 'username', 'email', 'password_hash', 'created_at', 'is_active', 'full_name'],
    'Profiles': ['profile_id', 'user_id', 'bio', 'birthdate', 'location', 'profile_picture_url', 'static_location_city', 'static_location_country'],
    'Communities': ['community_id', 'community_name', 'description', 'created_at'],
    'Matches': ['match_id', 'user_id_1', 'user_id_2', 'match_data', 'compatibility_score', 'created_at'],
    'Events': ['event_id', 'community_id', 'event_name', 'description', 'location', 'start_time', 'end_time', 'geofence_parameters', 'created_at'],
    'LiveLocationShares': ['share_id', 'user_id', 'recipient_id', 'start_time', 'end_time', 'active'],
    'EventProximityOptIns': ['event_id', 'user_id', 'opt_in_time', 'opt_out_time']
}

# Add tables to diagram
for table_name, columns in tables.items():
    table_def = f"{table_name} | "
    for i, col in enumerate(columns):
        if i == 0:
            table_def += f"<{col}> {col} (PK)"
        elif col.endswith('_id') and col != columns[0]:
            table_def += f"| <{col}> {col} (FK)"
        else:
            table_def += f"| {col}"
    
    dot.node(table_name, label='{' + table_def + '}')

# Add relationships
relationships = [
    ('Profiles:user_id', 'Users:user_id'),
    ('Matches:user_id_1', 'Users:user_id'),
    ('Matches:user_id_2', 'Users:user_id'),
    ('LiveLocationShares:user_id', 'Users:user_id'),
    ('Events:community_id', 'Communities:community_id'),
    ('EventProximityOptIns:event_id', 'Events:event_id'),
    ('EventProximityOptIns:user_id', 'Users:user_id')
]

for src, dst in relationships:
    dot.edge(src, dst)

# Save the diagram
output_path = '/workspaces/--ThinkAlike--/docs/architecture/assets/images/thinkalike_erd'
dot.render(output_path, format='png', cleanup=True)

print(f"ERD generated at {output_path}.png")
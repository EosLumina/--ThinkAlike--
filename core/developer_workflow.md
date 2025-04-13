# ...existing content...
# Replace links like '](../../core/' with '](..\/core/' to remove an extra level.
sed -i 's/](..\/..\/core\//](..\/core\//g' /workspaces/--ThinkAlike--/core/developer_workflow.md
sed -i 's/href="..\/..\/core\//href="..\/core\//g' /workspaces/--ThinkAlike--/core/developer_workflow.md
# Then update any links starting with '](docs/' to '](../docs/'
sed -i 's/](docs\//](..\/docs\//g' /workspaces/--ThinkAlike--/core/developer_workflow.md
sed -i 's/href="docs\//href="..\/docs\//g' /workspaces/--ThinkAlike--/core/developer_workflow.md
# ...existing content...

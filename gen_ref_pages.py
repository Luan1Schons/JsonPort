"""Generate reference pages for the API documentation."""

from mkdocs_gen_files import open as mkdocs_open

# Generate API reference pages
with mkdocs_open("api/reference.md", "w") as f:
    f.write("# API Reference\n\n")
    f.write("::: jsonport\n")
    f.write("    options:\n")
    f.write("      show_source: true\n")
    f.write("      show_root_heading: true\n")

# Generate core module reference (excluding JsonPortError to avoid conflicts)
with mkdocs_open("api/core.md", "w") as f:
    f.write("# Core Functions\n\n")
    f.write("::: jsonport.core\n")
    f.write("    options:\n")
    f.write("      show_source: true\n")
    f.write("      show_root_heading: true\n")
    f.write("      members_order: source\n")
    f.write("      filters: [\"!^JsonPortError$\"]\n") 
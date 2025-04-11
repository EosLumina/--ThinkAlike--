fix: resolve workflow issues and improve ethical compliance validation

This PR addresses several critical issues:

1. **Enhanced Phone Number Detection**: Improved pattern detection for phone numbers in ethical compliance validation

that now supports multiple formats:
    * (123) 456-7890
  * 123-456-7890
  * 123.456.7890
  * +1 123 456 7890

1. **Workflow Diagnostics**: Added diagnostic tools that help identify CI/CD issues, validate YAML files, and check

dependencies

1. **Great Expectations Integration**: Implemented robust error handling and fallback mechanisms in Great Expectations

integration to prevent CI failures

1. **Workflow Stability**: Created utility scripts to simplify workflow troubleshooting and maintenance

These changes improve workflow stability and strengthen our ethical validation capabilities by ensuring sensitive data
is properly detected across various formats.

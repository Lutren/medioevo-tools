# Next Run Options After Public-Safe Mission Control/MCP Update

Recommended options after this update:

1. Wabi MCP Server scaffold v0.2
   - Create localhost-only scaffold.
   - Implement read-only tools first.
   - Add tests proving no mutation from read-only calls.

2. POST delta falsifier/test v0.1
   - Select one registered delta.
   - Write falsifier/test before any selective extraction.
   - Keep raw adoption blocked.

3. Mission Control v0.2 read-only alerts and filters
   - Add filters and alert summaries.
   - Keep dashboard read-only.
   - Do not add direct execution buttons.

4. BrowserBridge read-only visual QA
   - Only if DevTools MCP becomes available.
   - Snapshot local UI only.
   - No external send.

Conservative recommendation: Wabi MCP Server scaffold v0.2 if public-safe update closes cleanly and scans pass.


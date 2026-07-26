# Continuity artifact selection

Ask:

1. Is the fact already clear from current source, Git, tests, or authoritative
   documentation?
2. Is it stable enough to remain useful?
3. Who must review or consume it?
4. Does an existing artifact own this category?
5. Could recording it expose sensitive information?

Use an ADR for a durable decision with alternatives and consequences. Use an
issue for remaining work. Use a runbook for a repeatable operation. Use a
handoff for temporary execution state. Keep `MEMORY.md` as the concise continuity
index and link to those deeper authorities. Update repository instructions only
for repeated rules that should affect every relevant agent task.

Delete or compact a temporary handoff after its work is integrated. Do not let
status notes become a shadow project history.

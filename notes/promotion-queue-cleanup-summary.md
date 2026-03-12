# Promotion Queue Cleanup - Summary

**Date:** 2026-03-09  
**Scope:** Workbench promotion queue improvements

## Changes Made

### 1. **Improved `promote-list` Defaults**
- **Before:** Showed all items regardless of status (pending, executed, failed, cancelled)
- **After:** Shows only `pending` items by default
- **Rationale:** The most common use case is reviewing active work, not browsing history

### 2. **Added `--all` Flag**
- New flag for `promote-list` to show all statuses when needed
- Preserves full visibility of history without cluttering the default view

### 3. **Added `promote-cancel` Command**
- New command to mark pending items as cancelled
- Syntax: `python3 projects/workbench/workbench.py promote-cancel <queue_id>`
- Only works on items with `pending` status
- Makes lifecycle state transitions explicit and discoverable

### 4. **Enhanced Status Reporting**
- `promote-list` now shows status counts for **all** items, not just filtered results
- Helps users understand the full queue state even when viewing a filtered subset
- Example output:
  ```
  Promotion queue: 0 item(s)
  Filter: status=pending (default)
  All statuses: executed=1, failed=2, cancelled=1
  ```

### 5. **Improved Documentation**
- Added comprehensive lifecycle documentation to README
- Documented queue hygiene best practices
- Added examples for all new flags and commands
- Clarified that history is retained by design

## Files Changed

- `projects/workbench/workbench.py` - Core implementation
- `projects/workbench/README.md` - Documentation updates

## Testing

All commands tested and working:
- ✅ `promote-list` (defaults to pending only)
- ✅ `promote-list --all` (shows everything)
- ✅ `promote-list --status failed` (filters by status)
- ✅ `promote-cancel <id>` (marks pending items as cancelled)
- ✅ Validation: Cannot cancel non-pending items
- ✅ Status counts display correctly

## Key Design Decisions

### Why default to pending-only?
The queue should feel like an actionable work list by default, not an archive browser. Completed and failed items are still accessible but don't create visual noise.

### Why keep cancelled items?
History is valuable for debugging and understanding past decisions. The cancelled state is explicit and searchable, unlike deletion.

### Why show all status counts?
Context matters. Even when filtering, users should know the overall queue state without switching views.

## Usage Examples

```bash
# View active work (new default behavior)
python3 projects/workbench/workbench.py promote-list

# Review everything including history
python3 projects/workbench/workbench.py promote-list --all

# Focus on failures
python3 projects/workbench/workbench.py promote-list --status failed

# Cancel an item you no longer want to execute
python3 projects/workbench/workbench.py promote-cancel 4
```

## Caveats

- **No pruning command:** Failed and cancelled items remain in the queue file indefinitely. This is by design for auditability, but could be addressed later if the file grows unwieldy.
- **Status immutability:** Once an item moves out of `pending` state, it cannot be modified or cancelled. This is intentional to preserve state history.
- **No re-queue:** If you want to retry a failed item, add the original capture to the queue again with `promote-add`.

## Acceptance Criteria Met

✅ Easier to inspect queue by status  
✅ Stale/failed items no longer clutter default view  
✅ Lifecycle behavior documented and testable  
✅ No changes that obscure state history  
✅ Did not turn it into a task manager  
✅ Debugging remains straightforward  
✅ No unnecessary abstractions added

## Commit

```
commit 5afc75c
workbench: improve promotion queue defaults and lifecycle clarity
```

# Annotation Display Mode Feature

## Overview
The annotation display mode feature controls how annotations named "Notes" are displayed in the task list. Other annotations (not named "Notes") are always displayed.

## Modes

### Mode 1: Hidden (Default)
- Annotations named "Notes" are hidden on all tasks
- Other annotations are displayed normally

### Mode 2: Selected Task Only
- Annotations named "Notes" are shown only on the currently focused/selected task
- Other annotations are displayed normally on all tasks

### Mode 3: All Tasks
- Annotations named "Notes" are shown on all tasks
- Other annotations are displayed normally on all tasks

## Usage

Press the key bound to `SWITCH_ANNOTATION_DISPLAY_MODE` action (configured in your keybindings) to cycle through the three display modes. A message will appear showing the current mode.

## Implementation Details

### Files Modified

1. **vit/formatter_base.py**
   - Added `annotation_display_mode` parameter to `__init__`
   - Added `get_focused_task_uuid` callback parameter
   - Added `should_show_notes_annotation()` method to determine if "Notes" should be shown for a task
   - Added `filter_annotations_by_mode()` method to filter annotations based on mode

2. **vit/formatter/description.py**
   - Modified `format()` to use filtered annotations
   - Added `get_filtered_annotations()` method
   - Modified `format_combined()` to accept filtered annotations
   - Modified `format_annotations()` to accept annotations list instead of task

3. **vit/formatter/description_oneline.py**
   - Updated `format_combined()` to accept filtered annotations parameter
   - Updated `format_annotations()` to accept annotations list instead of task

4. **vit/formatter/description_count.py**
   - Updated `format()` to use filtered annotations for counting
   - Modified `format_count()` and `format_annotation_count()` to work with filtered annotations

5. **vit/formatter/description_truncated_count.py**
   - Updated `format()` to use filtered annotations for counting

6. **vit/application.py**
   - Added `get_focused_task_uuid()` method to get currently focused task UUID
   - Modified `bootstrap()` to pass `annotation_display_mode` and UUID getter to `FormatterBase`
   - Added request_reply handler for 'application:focused_task_uuid'
   - Enhanced `task_action_switch_annotation_display_mode()` to:
     - Update the formatter's mode
     - Refresh the display
     - Show a message indicating the current mode

## Technical Notes

- The formatter needs access to the currently focused task UUID to determine which task is selected in mode 2
- This is achieved through the request_reply system to avoid circular dependencies
- The annotation filtering happens during the formatting phase, so it integrates seamlessly with all description formatter variants
- The default mode is 1 (hidden) as specified in the initial implementation

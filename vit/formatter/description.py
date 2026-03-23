from functools import reduce

from vit.formatter import String
from vit.util import unicode_len

class Description(String):
    def format(self, description, task):
        if not description:
            return self.empty()
        width = unicode_len(description)
        colorized_description = self.colorize_description(description)
        if task['annotations']:
            filtered_annotations = self.get_filtered_annotations(task)
            if filtered_annotations:
                annotation_width, colorized_description = self.format_combined(colorized_description, task, filtered_annotations)
                if annotation_width > width:
                    width = annotation_width
        return (width, colorized_description)

    def format_description_truncated(self, description):
        return '%s...' % description[:self.formatter.description_truncate_len] if unicode_len(description) > self.formatter.description_truncate_len else description

    def get_filtered_annotations(self, task):
        """Get annotations filtered based on display mode and 'Notes' filtering."""
        return self.formatter.filter_annotations_by_mode(task, task['annotations'])

    def format_combined(self, colorized_description, task, filtered_annotations):
        annotation_width, formatted_annotations = self.format_annotations(task, filtered_annotations)
        return annotation_width, colorized_description + [(None, "\n"), (None, formatted_annotations)]

    def format_annotations(self, task, annotations):
        def reducer(accum, annotation):
            width, formatted_list = accum
            formatted = self.format_annotation(task, annotation)
            new_width = unicode_len(formatted)
            if new_width > width:
                width = new_width
            formatted_list.append(formatted)
            return (width, formatted_list)
        width, formatted_annotations = reduce(reducer, annotations, (0, []))
        return width, "\n".join(formatted_annotations)

    def format_annotation(self, task, annotation):
        timestamp = annotation['entry'].strftime(self.formatter.annotation)
        description = annotation['description']
        
        # If this is a "Notes" annotation, try to read the actual notes file content
        if description == 'Notes':
            notes_content = self.formatter.get_notes_file_content(task['uuid'])
            if notes_content:
                # Format with the notes content, indenting each line
                lines = notes_content.split('\n')
                formatted_lines = ['  %s %s' % (timestamp, lines[0])] if lines else []
                formatted_lines.extend(['    %s' % line for line in lines[1:]])
                return '\n'.join(formatted_lines)
        
        return '  %s %s' % (timestamp, description)

    def colorize(self, part):
        return self.colorizer.keyword(part)

    def colorize_description(self, description):
        first_part, rest = self.colorizer.extract_keyword_parts(description)
        if first_part is None:
            return [(None, description)]
        def reducer(accum, part):
            if part:
                last_color, last_part = accum[-1]
                color, part = self.markup_element(part)
                if color == last_color:
                    accum[-1] = (last_color, last_part + part)
                    return accum
                else:
                    return accum + [(color, part)]
            return accum
        return reduce(reducer, rest, [self.markup_element(first_part)])

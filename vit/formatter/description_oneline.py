from vit.formatter.description import Description

class DescriptionOneline(Description):
    def format_combined(self, colorized_description, task, filtered_annotations):
        formatted_annotations = self.format_annotations(task, filtered_annotations)
        return 0, colorized_description + [(None, formatted_annotations)]

    def format_annotations(self, task, annotations):
        formatted_annotations = [self.format_annotation(task, annotation) for annotation in annotations]
        return "".join(formatted_annotations)

    def format_annotation(self, task, annotation):
        timestamp = annotation['entry'].strftime(self.formatter.annotation)
        description = annotation['description']
        
        # If this is a "Notes" annotation, try to read the first line of notes file
        if description == 'Notes':
            notes_content = self.formatter.get_notes_file_content(task['uuid'], max_lines=1)
            if notes_content:
                # For oneline, just show first line
                first_line = notes_content.split('\n')[0]
                return ' %s %s' % (timestamp, first_line)
        
        return ' %s %s' % (timestamp, description)

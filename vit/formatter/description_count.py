from vit.formatter.description import Description
from vit.util import unicode_len

class DescriptionCount(Description):
    def format(self, description, task):
        if not description:
            return self.empty()
        width = unicode_len(description)
        colorized_description = self.colorize_description(description)
        if not task['annotations']:
            return (width, colorized_description)
        else:
            filtered_annotations = self.get_filtered_annotations(task)
            if filtered_annotations:
                count_width, colorized_description = self.format_count(colorized_description, filtered_annotations)
                return (width + count_width, colorized_description)
            return (width, colorized_description)

    def format_count(self, colorized_description, filtered_annotations):
        count_string = self.format_annotation_count(filtered_annotations)
        return unicode_len(count_string), colorized_description + [(None, count_string)]

    def format_annotation_count(self, filtered_annotations):
        return " [%d]" % len(filtered_annotations)

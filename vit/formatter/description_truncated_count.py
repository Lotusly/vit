from vit.formatter.description_count import DescriptionCount
from vit.util import unicode_len

class DescriptionTruncatedCount(DescriptionCount):
    def format(self, description, task):
        if not description:
            return self.empty()
        truncated_description = self.format_description_truncated(description)
        width = unicode_len(truncated_description)
        colorized_description = self.colorize_description(truncated_description)
        if not task['annotations']:
            return (width, colorized_description)
        else:
            filtered_annotations = self.get_filtered_annotations(task)
            if filtered_annotations:
                count_width, colorized_description = self.format_count(colorized_description, filtered_annotations)
                return (width + count_width, colorized_description)
            return (width, colorized_description)

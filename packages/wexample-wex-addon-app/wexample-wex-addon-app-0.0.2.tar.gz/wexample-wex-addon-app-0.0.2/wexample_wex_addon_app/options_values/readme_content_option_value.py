from wexample_filestate.const.types_state_items import TargetFileOrDirectory
from wexample_filestate.options_values.aggregated_templates_option_value import AggregatedTemplatesOptionValue


class ReadmeContentOptionValue(AggregatedTemplatesOptionValue):
    def render(self, target: TargetFileOrDirectory, current_value: str) -> str:
        self.templates = [
            f'# {target.parent.get_name()}' ,
            '## Introduction',
            '## License'
        ]

        return super().render(target, current_value)

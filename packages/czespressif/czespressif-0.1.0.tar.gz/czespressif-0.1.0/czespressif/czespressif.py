from commitizen.cz.base import BaseCommitizen
from commitizen.defaults import Questions
from jinja2 import PackageLoader


class CzPluginEspressif(BaseCommitizen):  # pylint: disable=abstract-method
    template_loader = PackageLoader('czespressif', 'templates')
    # CHANGELOG SETUP
    bump_pattern = r'^(break|!:|BREAKING|feat|docs|ci|refactor|remove|change|test)'
    bump_map = {
        'break': 'MAJOR',
        '!:': 'MAJOR',
        'BREAKING': 'MAJOR',
        'feat': 'MINOR',
        'fix': 'PATCH',
        'docs': 'PATCH',
        'ci': 'PATCH',
        'refactor': 'PATCH',
        'remove': 'PATCH',
        'change': 'PATCH',
        'test': 'PATCH',
    }
    changelog_pattern = '^(break|!:|BREAKING|feat|docs|ci|refactor|remove|change|test)?(!)?'
    commit_parser = '^(?P<change_type>break|!:|BREAKING|feat|docs|ci|refactor|remove|change|test)(?P<scope>\\([a-zA-Z0-9_-]+\\))?:\\s(?P<message>.*)'  # noqa: E501  # pylint: disable=line-too-long

    # Emojis for changelog categories based on gitmoji standard (https://gitmoji.dev/)
    change_type_map = {
        '!:': ':boom: BREAKING CHANGES',
        'break': ':boom: BREAKING CHANGES',
        'BREAKING': ':boom: BREAKING CHANGES',
        'change': ':building_construction: Changes',
        'ci': ':gear: CI and project settings',
        'docs': ':memo: Documentation',
        'feat': ':sparkles: Features',
        'fix': ':bug: Bug Fixes',
        'refactor': ':recycle: Refactoring',
        'remove': ':fire: Removals',
        'test': ':test_tube: Testing',
    }

    # Questions = Iterable[MutableMapping[str, Any]]
    # It expects a list with dictionaries.
    def questions(self) -> Questions:
        """Questions regarding the commit message."""
        questions = [
            {'type': 'input', 'name': 'title', 'message': 'Commit title'},
            {'type': 'input', 'name': 'issue', 'message': 'Jira Issue number:'},
        ]
        return questions

    def message(self, answers: dict) -> str:
        """Generate the message with the given answers."""
        return f"{answers['title']} (#{answers['issue']})"

    def example(self) -> str:
        """Provide an example to help understand the style (OPTIONAL)

        Used by `cz example`.
        """
        return 'Problem with user (#321)'

    def schema(self) -> str:
        """Show the schema used (OPTIONAL)

        Used by `cz schema`.
        """
        return '<title> (<issue>)'

    def info(self) -> str:
        """Explanation of the commit rules. (OPTIONAL)

        Used by `cz info`.
        """
        return 'We use this because is useful'


discover_this = CzPluginEspressif  # pylint: disable=invalid-name

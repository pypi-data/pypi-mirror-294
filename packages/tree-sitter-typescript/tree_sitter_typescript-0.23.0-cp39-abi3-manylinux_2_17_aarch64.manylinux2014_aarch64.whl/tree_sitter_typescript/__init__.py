"TypeScript and TSX grammars for tree-sitter"

from importlib.resources import files as _files

from ._binding import language_typescript, language_tsx

def _get_query(name, file):
    query = _files(f"{__package__}.queries") / file
    globals()[name] = query.read_text()
    return globals()[name]

def __getattr__(name):
    if name == "HIGHLIGHTS_QUERY":
        return _get_query("HIGHLIGHTS_QUERY", "highlights.scm")
    if name == "LOCALS_QUERY":
        return _get_query("LOCALS_QUERY", "locals.scm")
    if name == "TAGS_QUERY":
        return _get_query("TAGS_QUERY", "tags.scm")

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

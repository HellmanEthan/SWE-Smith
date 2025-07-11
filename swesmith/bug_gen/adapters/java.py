import re
import warnings

from swesmith.constants import CodeEntity, TODO_REWRITE
from tree_sitter import Language, Parser, Query
import tree_sitter_java as tsjava

JAVA_LANGUAGE = Language(tsjava.language())


class JavaEntity(CodeEntity):
    @property
    def name(self) -> str:
        method_query = Query(
            JAVA_LANGUAGE,
            """
                (constructor_declaration name: (identifier) @name)
                (method_declaration name: (identifier) @name)
            """,
        )
        method_name = self._extract_text_from_first_match(
            method_query, self.node, "name"
        )
        if method_name:
            return method_name
        return ""

    @property
    def signature(self) -> str:
        body_query = Query(
            JAVA_LANGUAGE,
            """
            [
              (constructor_declaration body: (constructor_body) @body)
              (method_declaration body: (block) @body)
            ]
            """.strip(),
        )
        matches = body_query.matches(self.node)
        if matches:
            body_node = matches[0][1]["body"][0]
            signature = (
                self.node.text[: body_node.start_byte - self.node.start_byte]
                .rstrip()
                .decode("utf-8")
            )
            signature = re.sub(r"\(\s+", "(", signature).strip()
            signature = re.sub(r"\s+\)", ")", signature).strip()
            signature = re.sub(r"\s+", " ", signature).strip()
            return signature
        return ""

    @property
    def stub(self) -> str:
        return f"{self.signature} {{\n\t// {TODO_REWRITE}\n}}"

    @staticmethod
    def _extract_text_from_first_match(query, node, capture_name: str) -> str | None:
        """Extract text from tree-sitter query matches with None fallback."""
        matches = query.matches(node)
        return matches[0][1][capture_name][0].text.decode("utf-8") if matches else None


def get_entities_from_file_java(
    entities: list[JavaEntity],
    file_path: str,
    max_entities: int = -1,
) -> list[JavaEntity]:
    """
    Parse a .java file and return up to max_entities top-level funcs and types.
    If max_entities < 0, collects them all.
    """
    parser = Parser(JAVA_LANGUAGE)

    file_content = open(file_path, "r", encoding="utf8").read()
    tree = parser.parse(bytes(file_content, "utf8"))
    root = tree.root_node
    lines = file_content.splitlines()

    def walk(node):
        # stop if we've hit the limit
        if 0 <= max_entities == len(entities):
            return
        if node.type == "ERROR":
            warnings.warn(f"Error encountered parsing {file_path}")
            return

        if node.type in [
            "constructor_declaration",
            "method_declaration",
        ]:
            if node.type == "method_declaration" and not _has_body(node):
                pass
            else:
                entities.append(_build_entity(node, lines, file_path))
                if 0 <= max_entities == len(entities):
                    return

        for child in node.children:
            walk(child)

    walk(root)


def _has_body(node) -> bool:
    """
    Check if a method declaration has a body.
    """
    for child in node.children:
        if child.type == "block":
            return True
    return False


def _build_entity(node, lines, file_path: str) -> CodeEntity:
    """
    Turn a Tree-sitter node into CodeEntity.
    """
    # start_point/end_point are (row, col) zero-based
    start_row, _ = node.start_point
    end_row, _ = node.end_point

    # slice out the raw lines
    snippet = lines[start_row : end_row + 1]

    # detect indent on first line
    first = snippet[0]
    m = re.match(r"^(?P<indent>[\t ]*)", first)
    indent_str = m.group("indent")
    # tabs count as size=1, else use count of spaces, fallback to 4
    indent_size = 1 if "\t" in indent_str else (len(indent_str) or 4)
    indent_level = len(indent_str) // indent_size

    # dedent each line
    dedented = []
    for line in snippet:
        if len(line) >= indent_level * indent_size:
            dedented.append(line[indent_level * indent_size :])
        else:
            dedented.append(line.lstrip("\t "))

    return JavaEntity(
        file_path=file_path,
        indent_level=indent_level,
        indent_size=indent_size,
        line_start=start_row + 1,
        line_end=end_row + 1,
        node=node,
        src_code="\n".join(dedented),
    )

from swesmith.bug_gen.adapters.golang import get_entities_from_file_go
from swesmith.bug_gen.adapters.java import get_entities_from_file_java
from swesmith.bug_gen.adapters.php import get_entities_from_file_php
from swesmith.bug_gen.adapters.python import get_entities_from_file_py
from swesmith.bug_gen.adapters.ruby import get_entities_from_file_rb
from swesmith.bug_gen.adapters.rust import get_entities_from_file_rs

get_entities_from_file = {
    "go": get_entities_from_file_go,
    "java": get_entities_from_file_java,
    "php": get_entities_from_file_php,
    "py": get_entities_from_file_py,
    "rb": get_entities_from_file_rb,
    "rs": get_entities_from_file_rs,
}

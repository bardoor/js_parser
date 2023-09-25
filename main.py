from tree_sitter import Language, Parser

FILTERN_TOKENS = ['parenthesized_expression', 'binary_expression', 'assignment_expression',
                  'expression_statement', 'program', 'variable_declarator', 'lexical_declaration',
                  'update_expression', 'object', 'for_statement', 'while_statement', 'empty_statement']

CONTENT_TOKENS = ['identifier', 'number']


# Получение плоского списка токенов из дерева
def flatten_tree(node):
    tokens = []
    for child in node.children:
        tokens.extend(flatten_tree(child))
    tokens.append(node)
    return tokens


def main():
    Language.build_library('build/languages.so', ['./tree-sitter-javascript'])
    JS_LANG = Language('build/languages.so', 'javascript')

    parser = Parser()
    parser.set_language(JS_LANG)

    js_code = 'const x = y - (119 * num)'

    tree = parser.parse(bytes(js_code, 'utf8'))
    flat_tokens = flatten_tree(tree.root_node)

    filtered_tokens = [token for token in flat_tokens if token.type not in FILTERN_TOKENS]

    for token in filtered_tokens:
        if token.type in CONTENT_TOKENS:
            print(f"Type: {token.type}, Value: {token.text.decode('utf-8')}")
        else:
            print(f"Type: {token.type}")


if __name__ == '__main__':
    main()

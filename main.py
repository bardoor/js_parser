from tree_sitter import Language, Parser
import argparse

FILTERN_TOKENS = ['parenthesized_expression', 'binary_expression', 'assignment_expression',
                  'expression_statement', 'program', 'variable_declarator', 'lexical_declaration',
                  'update_expression', 'object', 'for_statement', 'while_statement', 'empty_statement',
                  'statement_block', 'string_fragment', 'call_expression', 'arguments', 'property_identifier',
                  'member_expression', '"', 'return_statement', 'else_clause', 'if_statement']

CONTENT_TOKENS = ['identifier', 'number', 'string']


# Получение плоского списка токенов из дерева
def flatten_tree(node):
    tokens = []
    for child in node.children:
        tokens.extend(flatten_tree(child))
    tokens.append(node)
    return tokens


def main():
    args_parser = argparse.ArgumentParser(description='JS парсер')
    args_parser.add_argument('-t', help='Добавить вывод типов токенов', action='store_true')
    args_parser.add_argument('input_file', help='Файл с JS кодом')

    args = args_parser.parse_args()

    try:
        js_code = open(args.input_file, 'r').read()
    except OSError:
        print("Невозможно открыть файл")
        return

    Language.build_library('build/languages.so', ['./tree-sitter-javascript'])
    JS_LANG = Language('build/languages.so', 'javascript')

    parser = Parser()
    parser.set_language(JS_LANG)

    tree = parser.parse(bytes(js_code, 'utf8'))
    flat_tokens = flatten_tree(tree.root_node)

    filtered_tokens = [token for token in flat_tokens if token.type not in FILTERN_TOKENS]

    tokens_description = ''
    for token in filtered_tokens:
        if args.t:
            tokens_description += f"Type: {token.type}"
            if token.type in CONTENT_TOKENS:
                tokens_description += f" Value: {token.text.decode('utf-8')}"
            tokens_description += '\n'
        else:
            tokens_description += f"'{token.text.decode('utf-8')}' "

    print(tokens_description)


if __name__ == '__main__':
    main()

import re

regexes = {
  'open': re.compile('^[ \t]*<(item|custom_item|if|then|else|condition)[ \t>]'),
  'close': re.compile('^[ \t]*</(item|custom_item|if|then|else|condition)[ \t>]'),
  'info': re.compile('^[ \t]*(description)[ \t]*:[ \t]*["\']*'),
}

def parse_audit_file(content=None):
    global regexes
    lines = []
    audit = []
    stack = []

    if content is not None:
        lines = [l.strip() for l in content.split('\n')] 
        for n in range(len(lines)):
            if regexes['open'].match(lines[n]): 
                finds = regexes['open'].findall(lines[n])
                stack.append(finds[0])
            elif regexes['close'].match(lines[n]): 
                finds = regexes['close'].findall(lines[n])
                if len(stack) == 0:
                    msg = 'Ran out of stack closing tag: {} (line {})'
                    display(msg.format(finds[0], n), exit=1)
                elif finds[0] == stack[-1]:
                    stack = stack[:-1]
                else:
                    msg = 'Unbalanced tag: {} - {} (line {})'
                    display(msg.format(stack[-1], finds[0], n), exit=2)
            elif regexes['info'].match(lines[n]): 
                info = ':'.join(lines[n].split(':')[1:]).strip()[1:-1]
                audit.append((n + 1, len(stack), info))
        audit = audit[2:-1]
    return audit
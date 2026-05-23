import re

def sync():
    print("Starting synchronization of ode.tsx to index.html...")
    with open('ode.tsx', 'r', encoding='utf-8') as f:
        code = f.read()

    # Strip import statements
    cleaned_code = re.sub(r"import\s+.*?\s+from\s+['\"].*?['\"];?\n?", "", code)

    # Convert export default function App to normal function
    cleaned_code = cleaned_code.replace("export default function App()", "function App()")

    # Read template HTML
    with open('index.template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    # Inject
    final_html = template.replace("// === INJECTED_REACT_APP_PLACEHOLDER ===", cleaned_code)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)

    print("Successfully synchronized ode.tsx to index.html!")

if __name__ == '__main__':
    sync()

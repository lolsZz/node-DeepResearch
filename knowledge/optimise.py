from typing import List, Dict
import os  # Import the 'os' module

def optimize_content_for_rag(file_content_map: Dict[str, str]) -> Dict[str, str]:
    """
    Analyzes and optimizes content for a RAG pipeline.

    Args:
        file_content_map: A dictionary where keys are file paths and values are
            the file contents.

    Returns:
        A dictionary where keys are file paths and values are the optimized
        file contents.  The optimization strategy can vary based on file type
        and content.
    """

    optimized_content = {}

    for file_path, content in file_content_map.items():
        if file_path.endswith(('.ts', '.js')):
            optimized_content[file_path] = optimize_typescript_code(content, file_path)
        elif file_path.endswith('.md'):
            optimized_content[file_path] = optimize_markdown(content)
        elif file_path.endswith(('.yml', '.yaml')):
            optimized_content[file_path] = optimize_yaml(content)
        elif file_path.endswith('.json'):
            optimized_content[file_path] = optimize_json(content)
        elif file_path.endswith(('.dockerignore', '.gitignore')):
            optimized_content[file_path] = content #.strip() Don't strip. Whitespace important
        elif file_path.endswith('package.json'):
             optimized_content[file_path] = optimize_json(content) # re-use json optimizer
        else:
            # Default: treat as plain text, focusing on line breaks and whitespace.
            optimized_content[file_path] = optimize_plain_text(content)

    return optimized_content


def optimize_typescript_code(content: str, file_path: str) -> str:
    """Optimizes TypeScript/JavaScript code for RAG."""

    lines = content.splitlines()
    optimized_lines = []
    in_multiline_comment = False
    in_code_block = False  # Track if we're inside a code block (e.g., within a function)

    for i, line in enumerate(lines):
        stripped_line = line.strip()
        next_line_stripped = lines[i+1].strip() if i+1 < len(lines) else ""

        # Detect start and end of multiline comments
        if stripped_line.startswith('/*') and '*/' not in stripped_line:
            in_multiline_comment = True
        if '*/' in stripped_line:  # removed  and not stripped_line.startswith('/*')  because /** */ on same line
            in_multiline_comment = False
            optimized_lines.append(line)  # Keep the closing comment line
            continue
        if in_multiline_comment:
            optimized_lines.append(line) # Keep the comment
            continue

        # Handle single-line comments (keep them)
        if stripped_line.startswith('//'):
            optimized_lines.append(line)
            continue

        # Code block detection (simplified heuristic, might need refinement)
        if '{' in stripped_line:
            in_code_block = True
        if '}' in stripped_line:
            in_code_block = False #Could be start and end of block.


        # Inside code, keep indentation, but remove *excessive* blank lines
        if in_code_block:
            if stripped_line or (next_line_stripped.startswith('}') == False and next_line_stripped.startswith(')') == False):
                optimized_lines.append(line)
        else: #if not stripped_line.startswith('import')
             optimized_lines.append(line) #Keep imports with their whitespace for readability.


    return "\n".join(optimized_lines)


def optimize_markdown(content: str) -> str:
    """Optimizes Markdown content for RAG."""
    lines = content.splitlines()
    cleaned_lines = []
    for line in lines:
      cleaned_lines.append(line) #.rstrip())  Markdown significant whitespace.
    return "\n".join(cleaned_lines)


def optimize_yaml(content: str) -> str:
    """Optimizes YAML content for RAG."""
    # For YAML, focus on preserving structure.  Remove only *completely* empty lines.
    lines = content.splitlines()
    cleaned_lines = [line for line in lines if line.strip() != ""]
    return "\n".join(cleaned_lines)


def optimize_json(content: str) -> str:
    """Optimizes JSON content for RAG."""
    # For JSON, focus on preserving structure.
    lines = content.splitlines()
    cleaned_lines = [line for line in lines]
    return "\n".join(cleaned_lines)


def optimize_plain_text(content: str) -> str:
    """Optimizes plain text content for RAG."""
    lines = content.splitlines()
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line) # Keep leading/trailing whitespace.

    return "\n".join(cleaned_lines)



def create_file_map(combined_content: str) -> Dict[str, str]:
    """
    Parses the combined content string and creates a dictionary mapping
    file paths to their contents.
    """
    file_map = {}
    current_file = None
    current_content = []

    lines = combined_content.split('\n')
    for line in lines:
        if line.startswith('=====') and "File: " in line:
            # Save previous file content
            if current_file is not None:
                file_map[current_file] = "\n".join(current_content)

            # Start a new file
            current_file = line.split("File: ")[1].split("\n")[0].strip()
            current_content = []
        elif current_file is not None:
            # Accumulate content lines
            current_content.append(line)

    # Save the last file
    if current_file is not None:
        file_map[current_file] = "\n".join(current_content)

    return file_map


def main():
    """
    Main function to read the combined content from 'reader.txt',
    process it, and optionally save the optimized content.
    """
    input_file = "jina-reader-mcp.txt"
    output_directory = "optimized_output"  # Or any desired output directory

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            combined_content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    file_map = create_file_map(combined_content)
    optimized_file_map = optimize_content_for_rag(file_map)

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Write optimized files to the output directory
    for file_path, optimized_content in optimized_file_map.items():
        # Construct the full output path, preserving directory structure
        full_output_path = os.path.join(output_directory, file_path)

        # Create any necessary parent directories
        os.makedirs(os.path.dirname(full_output_path), exist_ok=True)

        try:
            with open(full_output_path, 'w', encoding='utf-8') as outfile:
                outfile.write(optimized_content)
            print(f"Wrote optimized file: {full_output_path}")
        except Exception as e:
            print(f"Error writing to {full_output_path}: {e}")


if __name__ == "__main__":
    main()

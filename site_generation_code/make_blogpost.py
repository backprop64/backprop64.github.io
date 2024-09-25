import json
from jinja2 import Template
import os


def generate_blog_post(output_folder):
    # Construct paths
    config_file = os.path.join(output_folder, "config.json")
    content_folder = os.path.join(output_folder, "content")

    # Load JSON data
    with open(config_file, "r") as f:
        data = json.load(f)

    # Set up Jinja2 template
    template = Template(
        """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }
        h1, h2 {
            margin-bottom: 1.5rem;
            font-weight: 600;
        }
        h1 {
            font-size: 2.5rem;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.5rem;
        }
        h2 {
            font-size: 1.8rem;
            margin-top: 2rem;
        }
        img {
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .section-content {
            margin-bottom: 2rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ title }}</h1>
        {% for section, content in sections.items() %}
            <h2>{{ section }}</h2>
            <div class="row section-content">
                {% if content is string %}
                    {{ include_html(content) | safe }}
                {% else %}
                    {% for item in content %}
                        <div class="col-md-{{ item[1] }}">
                            {% if item[0].endswith('.txt') %}
                                {{ read_text_file(item[0]) | safe }}
                            {% elif item[0].endswith(('.jpeg', '.jpg', '.png', '.gif')) %}
                                <img src="content/{{ item[0] }}" alt="Image for {{ section }}" class="img-fluid">
                            {% endif %}
                        </div>
                    {% endfor %}
                {% endif %}
            </div>
        {% endfor %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    """
    )

    # Helper function to read text files
    def read_text_file(file_name):
        file_path = os.path.join(content_folder, file_name)
        with open(file_path, "r") as f:
            return f.read()

    # Helper function to include HTML files
    def include_html(file_name):
        file_path = os.path.join(content_folder, file_name)
        with open(file_path, "r") as f:
            return f.read()

    # Render the template
    html_content = template.render(
        title=data.get("title", "Blog Post"),
        sections=data.get("sections", {}),
        read_text_file=read_text_file,
        include_html=include_html,
    )

    # Write the output file
    output_file = os.path.join(output_folder, "blogpost.html")
    with open(output_file, "w") as f:
        f.write(html_content)

    print(f"Blog post generated and saved to {output_file}")


# Example usage
output_folder = "/Users/gauravkaul/Desktop/site/blog_posts/hungarian_patch_swap"
generate_blog_post(output_folder)

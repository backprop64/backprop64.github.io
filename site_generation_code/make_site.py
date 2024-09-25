import json
import random
from jinja2 import Template

# Read JSON files
with open('site_generation_code/blocks.json') as f:
    page_data = json.load(f)['blocks']

with open('site_generation_code/bio.json') as f:
    bio_data = json.load(f)

# Extract unique tags and assign colors
tags = set(tag for entry in page_data for tag in entry['Tags'])
colors = {tag: f"#{random.randint(0, 0xFFFFFF):06x}" for tag in tags}

# Jinja2 template for HTML
html_template = Template('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gaurav</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #A8BBCE;
            color: #ffffff;
            font-family: 'Arial', sans-serif;
            text-align: center;
        }
        .bio {
            font-family: 'Serif', sans-serif;
            font-size: 1.2em;
            line-height: 1.5;
            color: #333;
            margin: 20px 0;
        }
        .navbar {
            padding: 1rem;
            font-size: 1.5rem;
            font-weight: bold;
            text-transform: uppercase;
        }
        .filter-btn {
            margin: 5px 5px;
            padding: 6px 6px;
            border-radius: 25px;
            border: 2px solid;
            background-color: transparent;
            cursor: pointer;
            text-transform: uppercase;
            font-weight: bold;
            font-size: 0.9rem;
            text-transform: uppercase;
            --filter-border-color: #ffffff;
        }
        .filter-btn:hover {
            border-color: var(--filter-border-color);
        }
        .filter-row {
            display: flex;
            justify-content: flex-start;
            flex-wrap: wrap;
            margin-bottom: 10px;
        }
        .block {
            margin: 10px 10px;
            padding: 10px;
            border: 2px solid;
            border-radius: 0px;
            text-transform: uppercase;
            font-weight: bold;
            cursor: pointer;
            position: relative;
            max-width: 33.33%;
            --block-border-color: #000000;
        }
        .block.hidden {
            display: none;
        }
        .tags {
            position: absolute;
            top: 10px;
            right: 10px;
        }
        .pop-up {
            display: none;
            position: fixed;
            background: #CCCCFF;
            border: 2px solid #000000;
            border-radius: 5px;
            padding: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            z-index: 1000;
            width: 256px;
            height: 256px;
        }
        .close-btn {
            position: absolute;
            top: 5px;
            right: 5px;
            background-color: #9966CC;
            color: whitw;
            border: none;
            padding: 5px 10px;
            cursor: pointer;
            border-radius: 3px;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="navbar">GAURAV KAUL</div>
    <div class="container">
        <section class="bio">
            <p>{{ bio_data['text'] }}</p>
        </section>        
        <div class="filter-row">
            {% for tag, color in colors.items() %}
            <button class="filter-btn" onclick="filter('{{ tag }}')" style="--filter-border-color: {{ color }};">{{ tag }}</button>
            {% endfor %}
        </div>
        <div class="row">
            {% for entry in page_data %}
            <div class="col-md-4 block" data-tags="{{ entry['Tags'] | join(',') }}">
                {{ entry['text'] }}
                <div class="pop-up">
                    <button class="close-btn" onclick="closePopup(this)">Close</button>
                    <img src="{{ entry['gif'] }}" alt="Project GIF" style="width: 100%; height: auto;">
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    <script>
        let currentPopUp = null;
        let currentFilter = null;

        function assignRandomBorderColors() {
            const primaryColors = ['#FF0000', '#0000FF', '#FFFF00'];
            const secondaryColors = ['#00FF00', '#FFA500', '#9400D3'];
            const filterBtns = document.querySelectorAll('.filter-btn');

            filterBtns.forEach((btn, index) => {
                const color = index % 2 === 0 ? primaryColors[index % primaryColors.length] : secondaryColors[index % secondaryColors.length];
                btn.style.setProperty('--filter-border-color', color);
            });
        }

        function updateSelectedFilterBorder(tag) {
            const blocks = document.querySelectorAll('.block');
            const selectedFilterBtn = document.querySelector(`.filter-btn[onclick="filter('${tag}')"]`);
            const selectedColor = selectedFilterBtn.style.getPropertyValue('--filter-border-color');

            blocks.forEach(block => {
                block.style.setProperty('--block-border-color', selectedColor);
            });
        }

        function filter(tag) {
            const blocks = document.querySelectorAll('.block');
            blocks.forEach(block => {
                const tags = block.getAttribute('data-tags').split(',');
                if (tag === 'all' || tags.includes(tag)) {
                    block.classList.remove('hidden');
                } else {
                    block.classList.add('hidden');
                }
            });
            currentFilter = tag;
            updateSelectedFilterBorder(tag);
        }

        document.querySelectorAll('.block').forEach(block => {
            block.addEventListener('mouseover', function() {
                if (currentPopUp && currentPopUp !== this.querySelector('.pop-up')) {
                    currentPopUp.style.display = 'none';
                }
                const popUp = this.querySelector('.pop-up');

                // Apply random positions
                const screenWidth = window.innerWidth;
                const screenHeight = window.innerHeight;
                const popUpWidth = popUp.offsetWidth;
                const popUpHeight = popUp.offsetHeight;

                const minX = screenWidth * 0.7; 
                const maxX = screenWidth * 0.8; 
                const minY = screenHeight * 0.25; 
                const maxY = screenHeight * 0.65; 

                popUp.style.left = Math.random() * (maxX - minX) + minX + 'px';
                popUp.style.top = Math.random() * (maxY - minY) + minY + 'px';

                popUp.style.display = 'block';
                currentPopUp = popUp;
            });
        });

        function closePopup(button) {
            const popUp = button.closest('.pop-up');
            popUp.style.display = 'none';
            currentPopUp = null;
        }

        window.onload = assignRandomBorderColors;
    </script>
</body>
</html>
''')

# Render the HTML with the data
html_content = html_template.render(page_data=page_data, bio_data=bio_data, colors=colors)

# Save the HTML file
with open('index.html', 'w') as f:
    f.write(html_content)

print("Webpage generated successfully!")
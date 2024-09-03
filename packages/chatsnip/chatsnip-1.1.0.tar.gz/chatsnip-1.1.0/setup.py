from setuptools import setup, find_packages

setup(
    name="chatsnip",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[
        'Flask',
        'streamlit',
        'ijson',
        'Werkzeug',
    ],
    entry_points={
        'console_scripts': [
            'chatsnip=chatsnip.chatsnip:main', 
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    description="A tool for extracting and managing chat data from HTML files. It includes a file splitter function to split up large files so they can be loaded back into ChatGPT if needed.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    exclude_package_data={'': ['uploads/*', '*.log']},
    url="https://github.com/leighvdveen/chatsnip",
    author="Leigh-Anne Wells",
    author_email="leighanne.vdveen@gmail.com",
)
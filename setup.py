from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="srt_deepl",
    description="Traslate a .SRT file using DeepL and Selenium.",
    url='https://github.com/sinedie/SRT-DeepL-Translator',
    version="0.8.5",
    author="EAR",
    author_email="sinedie@protonmail.com",
    license='FREE',
    python_requires=">=3.6",
    install_requires=requirements,
    packages=find_packages(),
    keywords=["python", "srt", "deepl", "languages", "translator", "subtitles"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)

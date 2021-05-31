from setuptools import setup, find_packages

setup(
    name="srt_deepl",
    description="Traslate a .SRT file using DeepL and Selenium.",
    version="0.8.1",
    author="EAR",
    author_email="sinedie@protonmail.com",
    packages=find_packages(),
    python_requires=">=3.6",
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

# setup.py

from setuptools import setup, find_packages

setup(
    name='autotiktokuploader',
    version='0.02',
    packages=['autotiktokuploader'],
    description='Upload or schedules videos to tiktok with tiktok sounds and hashtags that work.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=['tiktok', 'autoupload', 'tiktokautoupload'],
    author='HAZIQ KHALID',
    author_email='haziqmk123@gmail.com',
    url='https://github.com/haziq-exe/TikTokAutoUploader',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'playwright>=1.0.0',
        'requests>=2.0.0',
        'Pillow>=8.0.0',
        'transformers>=4.0.0',
        'torch>=1.0.0',
        'scikit-learn>=0.24.0'
    ],
)

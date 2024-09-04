# -*- coding: utf-8 -*-


import os
import re


import fnmatch

from collections import defaultdict

from blitzdb3-ce import SqlBackend
from sqlalchemy import create_engine
from functools import reduce

def get_files_list(path):
    # Removed unused 'with_sha' parameter
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        files.extend([(os.path.join(dirpath, f))[len(path):]
                     for f in filenames])
    return files


def apply_filter(filename, patterns):
    # Simplified and more readable version
    return any(re.search(pattern, filename, re.UNICODE) for pattern in patterns)


def filter_filenames_by_analyzers(filenames, analyzers, language_patterns):
    filtered_filenames = []
    for filename in filenames:
        for analyzer_params in analyzers:
            if not analyzer_params['language'] in language_patterns:
                continue
            language_pattern = language_patterns[analyzer_params['language']]
            if not 'patterns' in language_pattern \
                    or not apply_filter(filename, language_pattern['patterns']):
                continue
            filtered_filenames.append(filename)
            break
    return filtered_filenames


def filter_filenames_by_checkignore(file_paths, checkignore_patterns):

    filtered_file_paths = []

    for file_path in file_paths:
        excluded = False
        always_included = False
        for pattern in checkignore_patterns:
            if pattern.startswith("!"):
                if fnmatch.fnmatch(file_path, pattern[1:]):
                    always_included = True
                    break
            if fnmatch.fnmatch(file_path, pattern):
                excluded = True
        if not excluded or always_included:
            filtered_file_paths.append(file_path)
    return filtered_file_paths


def parse_checkmate_settings(content):
    """
    Basically a simple .yml parser that returns a simple Python dict to be used later on.
    """
    # Use safe_load instead of load for security
    return yaml.safe_load(content)


def parse_checkignore(content):

    lines = [l for l in [s.strip() for s in content.split("\n")]
             if l and not l[0] == '#']

    return lines


def get_project_path():
    """
    Get the path to the project root directory.
    Assumes the project root contains a .checkmate directory.
    """
    current_dir = os.getcwd()
    while current_dir != '/':
        if os.path.exists(os.path.join(current_dir, '.checkmate')):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    raise FileNotFoundError("Could not find project root directory")

def get_project_config():
    """
    Load and return the project configuration from .checkmate/config.yaml
    """
    project_path = get_project_path()
    config_path = os.path.join(project_path, '.checkmate', 'config.yaml')
    
    if not os.path.exists(config_path):
        return {}
    
    with open(config_path, 'r') as config_file:
        return yaml.safe_load(config_file)

def save_project_config(config):
    """
    Save the project configuration to .checkmate/config.yaml
    """
    project_path = get_project_path()
    config_dir = os.path.join(project_path, '.checkmate')
    config_path = os.path.join(config_dir, 'config.yaml')
    
    os.makedirs(config_dir, exist_ok=True)
    
    with open(config_path, 'w') as config_file:
        yaml.dump(config, config_file, default_flow_style=False)

def get_project(backend):
    """
    Get or create a project based on the current directory
    """
    project_path = get_project_path()
    project_name = os.path.basename(project_path)
    
    try:
        project = backend.get('Project', {'name': project_name})
    except backend.DoesNotExist:
        project = backend.create('Project', {
            'name': project_name,
            'path': project_path
        })
        backend.commit()
    
    return project



from flask import current_app
from flask.cli import AppGroup
from flask.signals import Namespace
from babel.messages import pofile
import click
import tempfile
import os
import re
import subprocess
import contextlib
import json


_signals = Namespace()
translation_extracted = _signals.signal("translation_extracted")
translation_updated = _signals.signal("translation_updated")
translation_compiled = _signals.signal("translation_compiled")


babel_cli = AppGroup('babel', help='Commands to manage translations')


def exec_babel_extract(path, potfile, mapping=None, keywords=None):
    if mapping:
        mapping_file = tempfile.NamedTemporaryFile()
        mapping_file.write(mapping.encode('utf-8'))
        mapping_file.flush()

    if isinstance(keywords, str):
        keywords = list(map(str.strip, str(keywords).split(";")))
    elif not keywords:
        keywords = []
    keywords.extend(["_n:1,2", "lazy_gettext", "_lazy"])
    keywords.extend(current_app.config['BABEL_EXTRACT_KEYWORDS'])

    cmdline = [current_app.config["BABEL_BIN"], "extract", "-o", potfile]
    if mapping:
        cmdline.extend(["-F", mapping_file.name])
    for k in keywords:
        cmdline.append("-k")
        cmdline.append(k)
    cmdline.append(path)

    subprocess.run(cmdline)
    if mapping:
        mapping_file.close()


def get_pot_file():
    path = current_app.extensions["babel"].translation_directories[0]
    if not os.path.exists(path):
        os.mkdir(path)
    return os.path.join(path, "messages.pot")


def exec_extract():
    potfile = get_pot_file()
    click.echo("Extracting translatable strings from %s" % current_app.root_path)
    mapping = create_babel_mapping(current_app.config["BABEL_EXTRACT_JINJA_DIRS"],
        current_app.config["BABEL_EXTRACT_WITH_JINJA_EXTS"], current_app.config["BABEL_EXTRACTORS"])
    exec_babel_extract(current_app.root_path, potfile, mapping)

    # we need to extract message from other paths independently then
    # merge the catalogs because babel's mapping configuration does
    # not support absolute paths
    for path, jinja_dirs, jinja_exts, extractors in current_app.config["EXTRACT_DIRS"]:
        click.echo("Extracting translatable strings from %s" % path)
        mapping = create_babel_mapping(jinja_dirs, jinja_exts, extractors)
        path_potfile = tempfile.NamedTemporaryFile(delete=False)
        path_potfile.close()
        exec_babel_extract(path, path_potfile.name, mapping)
        merge_pofile(potfile, path_potfile.name)
        os.unlink(path_potfile.name)

    translation_extracted.send()


@babel_cli.command('extract')
def extract_cmd():
    exec_extract()


@babel_cli.command("init")
@click.argument('locale')
def init_translation(locale):
    path = current_app.extensions["babel"].translation_directories[0]
    potfile = get_pot_file()
    if not os.path.exists(potfile):
        exec_extract()
    click.echo("Initializing new translation '%s' in %s" % (locale, os.path.join(path, locale)))
    subprocess.run([current_app.config["BABEL_BIN"], "init", "-i", potfile, "-d", path, "-l", locale])
    translation_updated.send(None, locale=locale)


@babel_cli.command("update")
@click.option('--extract/--no-extract', default=True)
def update_translations(extract=True):
    path = current_app.extensions["babel"].translation_directories[0]
    potfile = get_pot_file()
    if not os.path.exists(potfile) or extract:
        exec_extract()
    click.echo("Updating all translations")
    subprocess.run([current_app.config["BABEL_BIN"], "update", "-i", potfile, "-d", path])
    for entry in os.scandir(path):
        if entry.is_dir():
            translation_updated.send(locale=entry.name)


@babel_cli.command("compile")
def compile_translations():
    click.echo("Compiling all translations")
    path = os.path.join(current_app.root_path, "translations")
    subprocess.run([current_app.config["BABEL_BIN"], "compile", "-d", path])
    if current_app.config['BABEL_COMPILE_TO_JSON']:
        output = os.path.join(current_app.static_folder, current_app.config['BABEL_COMPILE_TO_JSON'])
        for entry in os.scandir(path):
            if entry.is_dir():
                _po2json(entry.name, output % entry.name)
    if current_app.config['BABEL_COMPILE_TO_JS']:
        output = os.path.join(current_app.static_folder, current_app.config['BABEL_COMPILE_TO_JS'])
        for entry in os.scandir(path):
            if entry.is_dir():
                _po2js(entry.name, output % entry.name)
    translation_compiled.send()


def _po2json(locale, output=None):
    filename = os.path.join(current_app.root_path, "translations", locale, "LC_MESSAGES", "messages.po")
    dump = po_to_json(filename)
    if output:
        with open(output, 'w') as f:
            f.write(dump)
    else:
        click.echo(dump)


def _po2js(locale, output=None):
    filename = os.path.join(current_app.root_path, "translations", locale, "LC_MESSAGES", "messages.po")
    varname = current_app.config['BABEL_JS_CATALOG_VARNAME']
    dump = "const %s = %s;" % (varname % locale.upper(), po_to_json(filename))
    if output:
        with open(output, 'w') as f:
            f.write(dump)
    else:
        click.echo(dump)


@babel_cli.command('po2json')
@click.argument('locale')
@click.option('--output', '-o')
def po2json(locale, output=None):
    _po2json(locale, output)


@babel_cli.command('po2js')
@click.argument('locale')
@click.option('--output', '-o')
def po2js(locale, output=None):
    _po2js(locale, output)


def safe_placeholders(string, repl="##%s##"):
    placeholders = []
    def replace_placeholder(m):
        placeholders.append(m.group(1))
        return repl % (len(placeholders) - 1)
    string = re.sub(r"%\(([a-zA-Z_]+)\)s", replace_placeholder, string)
    return string, placeholders


def unsafe_placeholders(string, placeholders, repl="##%s##"):
    for i, placeholder in enumerate(placeholders):
        string = string.replace(repl % i, "%%(%s)s" % placeholder)
    return string


@contextlib.contextmanager
def edit_pofile(filename, autosave=True):
    with open(filename, "r") as f:
        catalog = pofile.read_po(f)
    yield catalog
    if autosave:
        with open(filename, "wb") as f:
            pofile.write_po(f, catalog)


def merge_pofile(filename1, filename2):
    with edit_pofile(filename1) as catalog1:
        with edit_pofile(filename2) as catalog2:
            for msg in catalog2:
                if msg.id not in catalog1:
                    catalog1[msg.id] = msg


def create_babel_mapping(jinja_dirs=None, jinja_exts=None, extractors=None):
    exts = ",".join(jinja_exts or [])
    conf = "[python:**.py]\n"
    if jinja_dirs:
        for jinja_dir in jinja_dirs:
            if jinja_dir == '.':
                jinja_dir = ''
            conf += "[jinja2:%s]\n" % os.path.join(jinja_dir, "**.html")
            if exts:
                conf += "extensions=%s\n" % exts
    if extractors:
        for extractor, settings in extractors:
            conf += "[%s]\n" % extractor
            for k, v in settings.items():
                conf += "%s = %s\n" % (k, v)
    return conf


def po_to_json(filename):
    json_dct = {}
    with edit_pofile(filename) as catalog:
        for message in catalog:
            if not message.id:
                continue
            if message.pluralizable:
                json_dct[_format_json_msg_id(message)] = [message.id[1]] + list(message.string)
            else:
                json_dct[_format_json_msg_id(message)] = [None, message.string]
    return json.dumps(json_dct)


def _format_json_msg_id(message):
    mid = message.id[0] if message.pluralizable else message.id
    if message.context:
        return "%s::%s" % (message.context, mid)
    return mid

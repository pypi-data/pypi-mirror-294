#!/usr/bin/env python

# Python standard library
import logging
import os
from urllib.parse import urlparse

# external dependencies
import click

# imports from this very package
from brother_ql.devicedependent import models, label_sizes, label_type_specs, DIE_CUT_LABEL, ENDLESS_LABEL, ROUND_DIE_CUT_LABEL
from brother_ql.models import ModelsManager
from brother_ql.backends import available_backends, backend_factory


logger = logging.getLogger('brother_ql')


printer_help = "The identifier for the printer. This could be a string like tcp://192.168.1.21:9100 for a networked printer or usb://0x04f9:0x2015/000M6Z401370 for a printer connected via USB."
@click.group()
@click.option('-b', '--backend', type=click.Choice(available_backends), envvar='BROTHER_QL_BACKEND')
@click.option('-m', '--model', type=click.Choice(models), envvar='BROTHER_QL_MODEL')
@click.option('-p', '--printer', metavar='PRINTER_IDENTIFIER', envvar='BROTHER_QL_PRINTER', help=printer_help)
@click.option('--debug', is_flag=True)
@click.version_option()
@click.pass_context
def cli(ctx, *args, **kwargs):
    """ Command line interface for the brother_ql Python package. """

    backend = kwargs.get('backend', None)
    model = kwargs.get('model', None)
    printer = kwargs.get('printer', None)
    debug = kwargs.get('debug')

    # Store the general CLI options in the context meta dictionary.
    # The name corresponds to the second half of the respective envvar:
    ctx.meta['MODEL'] = model
    ctx.meta['BACKEND'] = backend
    ctx.meta['PRINTER'] = printer

    logging.basicConfig(level='DEBUG' if debug else 'INFO')

@cli.command()
@click.pass_context
def discover(ctx):
    """ find connected label printers """
    backend = ctx.meta.get('BACKEND', 'pyusb')
    if backend is None:
        logger.info("Defaulting to pyusb as backend for discovery.")
        backend = "pyusb"
    from brother_ql.backends.helpers import discover, get_printer, get_status

    # linux_kernel backend will check for permissions and omit inaccessilble and incompatible devices
    # pyusb backend cannot do permission checks, will just have to try
    # network backend doesn't support discovery for now
    available_devices = []

    try:
        available_devices = discover(backend_identifier=backend)
    except NotImplementedError:
        logger.error(f"The {backend} backend does not support discovery yet.")
        return

    for device in available_devices:
        logger.debug(f"Probing device at {device['identifier']}")
        printer = get_printer(
            printer_identifier=device["identifier"],
            backend_identifier=backend,
        )
        status = get_status(printer)
        if status['model'] == "Unknown":
            print(f"Found unkown printer at: {device['identifier']}. Compatibility is unknown.")
        else:
            print(f"Found compatible printer {status['model']} at: {device['identifier']}")

def discover_and_list_available_devices(backend):
    from brother_ql.backends.helpers import discover
    available_devices = discover(backend_identifier=backend)
    from brother_ql.output_helpers import log_discovered_devices, textual_description_discovered_devices
    log_discovered_devices(available_devices)
    print(textual_description_discovered_devices(available_devices))

@cli.group()
@click.pass_context
def info(ctx, *args, **kwargs):
    """ list available labels, models etc. """

@info.command(name='models')
@click.pass_context
def models_cmd(ctx, *args, **kwargs):
    """
    List the choices for --model
    """
    print('Supported models:')
    for model in models: print(" " + model)

@info.command()
@click.pass_context
def labels(ctx, *args, **kwargs):
    """
    List the choices for --label
    """
    from brother_ql.output_helpers import textual_label_description
    print(textual_label_description(label_sizes))

@info.command()
@click.pass_context
def env(ctx, *args, **kwargs):
    """
    print debug info about running environment
    """
    import sys, platform, os, shutil
    from pkg_resources import get_distribution, working_set
    print("\n##################\n")
    print("Information about the running environment of brother_ql.")
    print("(Please provide this information when reporting any issue.)\n")
    # computer
    print("About the computer:")
    for attr in ('platform', 'processor', 'release', 'system', 'machine', 'architecture'):
        print('  * '+attr.title()+':', getattr(platform, attr)())
    # Python
    print("About the installed Python version:")
    py_version = str(sys.version).replace('\n', ' ')
    print("  *", py_version)
    # brother_ql
    print("About the brother_ql package:")
    pkg = get_distribution('brother_ql')
    print("  * package location:", pkg.location)
    print("  * package version: ", pkg.version)
    try:
        cli_loc = shutil.which('brother_ql')
    except Exception:
        cli_loc = 'unknown'
    print("  * brother_ql CLI path:", cli_loc)
    # brother_ql's requirements
    print("About the requirements of brother_ql:")
    fmt = "  {req:14s} | {spec:10s} | {ins_vers:17s}"
    print(fmt.format(req='requirement', spec='requested', ins_vers='installed version'))
    print(fmt.format(req='-' * 14, spec='-'*10, ins_vers='-'*17))
    requirements = list(pkg.requires())
    requirements.sort(key=lambda x: x.project_name)
    for req in requirements:
        proj = req.project_name
        req_pkg = get_distribution(proj)
        spec = ' '.join(req.specs[0]) if req.specs else 'any'
        print(fmt.format(req=proj, spec=spec, ins_vers=req_pkg.version))
    print("\n##################\n")

@cli.command('print', short_help='Print a label')
@click.argument('images', nargs=-1, type=click.File('rb'), metavar='IMAGE [IMAGE] ...')
@click.option('-l', '--label', required=True, type=click.Choice(label_sizes), envvar='BROTHER_QL_LABEL', help='The label (size, type - die-cut or endless). Run `brother_ql info labels` for a full list including ideal pixel dimensions.')
@click.option('-r', '--rotate', type=click.Choice(('auto', '0', '90', '180', '270')), default='auto', help='Rotate the image (counterclock-wise) by this amount of degrees.')
@click.option('-t', '--threshold', type=float, default=70.0, help='The threshold value (in percent) to discriminate between black and white pixels.')
@click.option('-d', '--dither', is_flag=True, help='Enable dithering when converting the image to b/w. If set, --threshold is meaningless.')
@click.option('-c', '--compress', is_flag=True, help='Enable compression (if available with the model). Label creation can take slightly longer but the resulting instruction size is normally considerably smaller.')
@click.option('--red', is_flag=True, help='Create a label to be printed on black/red/white tape (only with QL-8xx series on DK-22251 labels). You must use this option when printing on black/red tape, even when not printing red.')
@click.option('--600dpi', 'dpi_600', is_flag=True, help='Print with 600x300 dpi available on some models. Provide your image as 600x600 dpi; perpendicular to the feeding the image will be resized to 300dpi.')
@click.option('--lq', is_flag=True, help='Print with low quality (faster). Default is high quality.')
@click.option('--no-cut', is_flag=True, help="Don't cut the tape after printing the label.")
@click.pass_context
def print_cmd(ctx, *args, **kwargs):
    """ Print a label of the provided IMAGE. """
    backend = ctx.meta.get('BACKEND', 'pyusb')
    model = ctx.meta.get('MODEL')
    printer = ctx.meta.get('PRINTER')
    from brother_ql.conversion import convert
    from brother_ql.backends.helpers import send
    from brother_ql.raster import BrotherQLRaster
    qlr = BrotherQLRaster(model)
    qlr.exception_on_warning = True
    kwargs['cut'] = not kwargs['no_cut']
    del kwargs['no_cut']
    instructions = convert(qlr=qlr, **kwargs)
    send(instructions=instructions, printer_identifier=printer, backend_identifier=backend, blocking=True)

@cli.command(name='analyze', help='interpret a binary file containing raster instructions for the Brother QL-Series printers')
@click.argument('instructions', type=click.File('rb'))
@click.option('-f', '--filename-format', help="Filename format string. Default is: label{counter:04d}.png.")
@click.pass_context
def analyze_cmd(ctx, *args, **kwargs):
    from brother_ql.reader import BrotherQLReader
    br = BrotherQLReader(kwargs.get('instructions'))
    if kwargs.get('filename_format'): br.filename_fmt = kwargs.get('filename_format')
    br.analyse()

@cli.command(name='send', short_help='send an instruction file to the printer')
@click.argument('instructions', type=click.File('rb'))
@click.pass_context
def send_cmd(ctx, *args, **kwargs):
    from brother_ql.backends.helpers import send
    send(instructions=kwargs['instructions'].read(), printer_identifier=ctx.meta.get('PRINTER'), backend_identifier=ctx.meta.get('BACKEND'), blocking=True)


@cli.command(name="status", short_help="query printer status and the loaded media size")
@click.pass_context
def status_cmd(ctx, *args, **kwargs):
    from brother_ql.backends.helpers import get_status, get_printer

    printer=get_printer(ctx.meta.get("PRINTER"), ctx.meta.get("BACKEND"))
    logger.debug("Sending status information request to the printer.")
    result = get_status(printer)

    print(f"Model: {result['model']}")
    if result['model'] == "Unknown":
        print("Unknown printer detected")
        print(f"Series Code: 0x{result['series_code']:02x}")
        print(f"Model Code: 0x{result['model_code']:02x}")
    print(f"Status type: {result['status_type']}")
    print(f"Phase: {result['phase_type']}")
    if len(result['errors']) != 0:
        print(f"Errors: {result['errors']}")
    print(f"Media type: [{result['media_category']}] {result['media_type']}")
    if result['model'].startswith('QL') and result['media_sensor'] != 0x0:
        color = 'Black on White'
        if result['media_sensor'] == 0x23:
            color = 'Red/Black on White'
        print(f"Media color: {color}")
    if result['model'].startswith('PT'):
        print("Note: tape color information may be incorrect for aftermarket tape cartridges.")
        print(f"Tape color: {result['tape_color']}")
        print(f"Text color: {result['text_color']}")
    print(f"Media size: {result['media_width']} x {result['media_length']} mm")


@cli.command(name="configure", short_help="read and modify printer settings")
@click.argument('action', required=True, type=click.Choice(['get', 'set']), metavar='[ACTION]')
@click.argument('key', required=True, type=click.Choice(['power-off-delay', 'auto-power-on']), metavar='[KEY]')
@click.argument('value', type=int, metavar='[VALUE]', default=-1)
@click.pass_context
def configure_cmd(ctx, *args, **kwargs):
    from brother_ql.backends.helpers import configure

    if kwargs.get('action') == 'set' and kwargs.get('value') == -1:
        raise ValueError(f"Specify a valid value for key {kwargs.get('key')}")

    configure(
        printer_identifier=ctx.meta.get("PRINTER"),
        backend_identifier=ctx.meta.get("BACKEND"),
        action=kwargs.get('action'),
        key=kwargs.get('key'),
        value=kwargs.get('value')
    )

if __name__ == '__main__':
    cli()

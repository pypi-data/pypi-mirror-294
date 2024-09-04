import json
import logging
import pathlib

import click
from packaging.requirements import Requirement
from packaging.version import Version

from fromager import clickext, context, hooks, progress, sdist, server, sources, wheels

logger = logging.getLogger(__name__)


@click.command()
@click.argument("dist_name")
@click.argument("dist_version", type=clickext.PackageVersion())
@click.argument("sdist_server_url")
@click.pass_obj
def build(
    wkctx: context.WorkContext,
    dist_name: str,
    dist_version: Version,
    sdist_server_url: str,
) -> None:
    """Build a single version of a single wheel

    DIST_NAME is the name of a distribution

    DIST_VERSION is the version to process

    SDIST_SERVER_URL is the URL for a PyPI-compatible package index hosting sdists

    1. Downloads the source distribution.

    2. Unpacks it and prepares the source via patching, vendoring rust
       dependencies, etc.

    3. Prepares a build environment with the build dependencies.

    4. Builds the wheel.

    Refer to the 'step' commands for scripting these stages
    separately.

    """
    server.start_wheel_server(wkctx)
    wheel_filename = _build(wkctx, dist_name, dist_version, sdist_server_url)
    print(wheel_filename)


@click.command()
@click.argument("build_order_file")
@click.argument("sdist_server_url")
@click.option(
    "--skip-existing",
    default=False,
    is_flag=True,
)
@click.pass_obj
def build_sequence(
    wkctx: context.WorkContext,
    build_order_file: str,
    sdist_server_url: str,
    skip_existing: bool,
) -> None:
    """Build a sequence of wheels in order

    BUILD_ORDER_FILE is the build-order.json files to build

    SDIST_SERVER_URL is the URL for a PyPI-compatible package index hosting sdists

    Performs the equivalent of the 'build' command for each item in
    the build order file.

    """
    server.start_wheel_server(wkctx)

    with open(build_order_file, "r") as f:
        for entry in progress.progress(json.load(f)):
            dist_name = entry["dist"]
            dist_version = Version(entry["version"])

            if skip_existing and _is_wheel_built(wkctx, dist_name, dist_version):
                logger.info(
                    "%s: skipping building wheels for %s==%s since it already exists",
                    dist_name,
                    dist_name,
                    dist_version,
                )
                continue

            logger.info("%s: building %s==%s", dist_name, dist_name, dist_version)
            wheel_filename = _build(wkctx, dist_name, dist_version, sdist_server_url)

            server.update_wheel_mirror(wkctx)
            # After we update the wheel mirror, the built file has
            # moved to a new directory.
            wheel_filename = wkctx.wheels_downloads / wheel_filename.name
            print(wheel_filename)


def _build(
    wkctx: context.WorkContext,
    dist_name: str,
    dist_version: Version,
    sdist_server_url: str,
) -> pathlib.Path:
    req = Requirement(f"{dist_name}=={dist_version}")

    # Download
    source_filename, version, source_url, _ = sources.download_source(
        wkctx,
        req,
        [sdist_server_url],
    )
    logger.debug(
        "%s: saved sdist of version %s from %s to %s",
        req.name,
        dist_version,
        source_url,
        source_filename,
    )

    # Prepare source
    source_root_dir = sources.prepare_source(wkctx, req, source_filename, dist_version)

    # Build environment
    sdist.prepare_build_environment(wkctx, req, source_root_dir)
    build_env = wheels.BuildEnvironment(wkctx, source_root_dir.parent, None)

    # Make a new source distribution, in case we patched the code.
    sdist_filename = sources.build_sdist(
        ctx=wkctx,
        req=req,
        version=dist_version,
        sdist_root_dir=source_root_dir,
        build_env=build_env,
    )

    # Build
    wheel_filename = wheels.build_wheel(
        ctx=wkctx,
        req=req,
        sdist_root_dir=source_root_dir,
        version=dist_version,
        build_env=build_env,
    )

    hooks.run_post_build_hooks(
        ctx=wkctx,
        req=req,
        dist_name=dist_name,
        dist_version=str(dist_version),
        sdist_filename=sdist_filename,
        wheel_filename=wheel_filename,
    )

    return wheel_filename


def _is_wheel_built(
    wkctx: context.WorkContext, dist_name: str, dist_version: Version
) -> bool:
    req = Requirement(f"{dist_name}=={dist_version}")

    try:
        logger.info(f"{req.name}: checking if {req} was already built")
        sdist.resolve_prebuilt_wheel(wkctx, req, [wkctx.wheel_server_url])
        return True
    except Exception:
        logger.info(f"{req.name}: could not locate prebuilt wheel. Will build {req}")
        return False

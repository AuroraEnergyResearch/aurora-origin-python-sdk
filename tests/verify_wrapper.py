from email.parser import BytesParser
from email.policy import default
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
from typing import Optional
import venv
import zipfile


ROOT = Path(__file__).parents[1]
DIST = ROOT / "dist"
REPLACEMENT_REQUIREMENT = "auroraer-origin-sdk<1,>=0.31.0"
NOTEBOOKS_REQUIREMENT = 'auroraer-origin-sdk[notebooks]<1,>=0.31.0; extra == "notebooks"'


def metadata_from_wheel(wheel: Path):
    with zipfile.ZipFile(wheel) as archive:
        metadata_name = next(
            name for name in archive.namelist() if name.endswith(".dist-info/METADATA")
        )
        return BytesParser(policy=default).parsebytes(archive.read(metadata_name))


def write_wheel(
    directory: Path,
    distribution: str,
    version: str,
    *,
    extra: Optional[str] = None,
    dependency: Optional[str] = None,
):
    normalized = distribution.replace("-", "_")
    wheel = directory / f"{normalized}-{version}-py3-none-any.whl"
    dist_info = f"{normalized}-{version}.dist-info"
    metadata = [
        "Metadata-Version: 2.1",
        f"Name: {distribution}",
        f"Version: {version}",
    ]
    if extra:
        metadata.extend((f"Provides-Extra: {extra}", f"Requires-Dist: {dependency}"))
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr(f"{dist_info}/METADATA", "\n".join(metadata) + "\n")
        archive.writestr(
            f"{dist_info}/WHEEL",
            "Wheel-Version: 1.0\nGenerator: wrapper-test\nRoot-Is-Purelib: true\nTag: py3-none-any\n",
        )
        archive.writestr(f"{dist_info}/RECORD", "")
    return wheel


def run_pip(environment: Path, *arguments: str, succeeds: bool = True):
    pip = environment / ("Scripts" if sys.platform == "win32" else "bin") / "pip"
    result = subprocess.run(
        [str(pip), *arguments], capture_output=True, text=True, check=False
    )
    if (result.returncode == 0) != succeeds:
        raise AssertionError(result.stdout + result.stderr)


def installed_version(environment: Path, distribution: str):
    python = environment / ("Scripts" if sys.platform == "win32" else "bin") / "python"
    result = subprocess.run(
        [
            str(python),
            "-c",
            f"from importlib.metadata import version; print(version('{distribution}'))",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def verify_artifacts(wheel: Path, sdist: Path):
    metadata = metadata_from_wheel(wheel)
    assert metadata["Name"] == "aurora-origin-sdk"
    assert metadata["Version"] == "0.32.0"
    assert metadata.get_all("Provides-Extra") == ["notebooks"]
    assert set(metadata.get_all("Requires-Dist")) == {
        REPLACEMENT_REQUIREMENT,
        NOTEBOOKS_REQUIREMENT,
    }

    with zipfile.ZipFile(wheel) as archive:
        members = archive.namelist()
        assert members
        assert all(".dist-info/" in member for member in members), members
        assert not any(
            member.startswith(("origin_sdk/", "core/")) for member in members
        ), members

    with tarfile.open(sdist) as archive:
        members = [member.name for member in archive.getmembers()]
        forbidden = ("/src/", "/origin_sdk/", "/core/", "/tests/", ".py")
        assert not any(any(item in member for item in forbidden) for member in members), members


def verify_resolver_boundaries(wrapper: Path):
    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary = Path(temporary_directory)
        wheelhouse = temporary / "wheelhouse"
        wheelhouse.mkdir()
        wrapper_copy = wheelhouse / wrapper.name
        wrapper_copy.write_bytes(wrapper.read_bytes())

        write_wheel(
            wheelhouse,
            "auroraer-origin-sdk",
            "0.31.0",
            extra="notebooks",
            dependency='notebook-sentinel; extra == "notebooks"',
        )
        write_wheel(wheelhouse, "auroraer-origin-sdk", "1.0.0")
        write_wheel(wheelhouse, "notebook-sentinel", "1.0.0")

        environment = temporary / "compatible"
        venv.EnvBuilder(with_pip=True).create(environment)
        run_pip(
            environment,
            "install",
            "--no-index",
            "--find-links",
            str(wheelhouse),
            f"{wrapper_copy}[notebooks]",
        )
        assert installed_version(environment, "auroraer-origin-sdk") == "0.31.0"
        assert installed_version(environment, "notebook-sentinel") == "1.0.0"

        incompatible_wheelhouse = temporary / "incompatible-wheelhouse"
        incompatible_wheelhouse.mkdir()
        (incompatible_wheelhouse / wrapper.name).write_bytes(wrapper.read_bytes())
        write_wheel(incompatible_wheelhouse, "auroraer-origin-sdk", "1.0.0")
        environment = temporary / "incompatible"
        venv.EnvBuilder(with_pip=True).create(environment)
        run_pip(
            environment,
            "install",
            "--no-index",
            "--find-links",
            str(incompatible_wheelhouse),
            str(incompatible_wheelhouse / wrapper.name),
            succeeds=False,
        )


def main():
    wheels = list(DIST.glob("aurora_origin_sdk-0.32.0-*.whl"))
    sdists = list(DIST.glob("aurora_origin_sdk-0.32.0.tar.gz"))
    assert len(wheels) == len(sdists) == 1, (wheels, sdists)
    verify_artifacts(wheels[0], sdists[0])
    verify_resolver_boundaries(wheels[0])
    print("Wrapper artifacts and dependency resolution verified.")


if __name__ == "__main__":
    main()

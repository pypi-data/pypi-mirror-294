import os
import re
import shutil
import sys
import tempfile

from sqlalchemy import testing
from sqlalchemy import util
from sqlalchemy.testing import config
from sqlalchemy.testing import eq_
from sqlalchemy.testing import fixtures


class MypyPluginTest(fixtures.TestBase):
    __requires__ = ("sqlalchemy2_stubs",)

    @testing.fixture(scope="function")
    def per_func_cachedir(self):
        for item in self._cachedir():
            yield item

    @testing.fixture(scope="class")
    def cachedir(self):
        for item in self._cachedir():
            yield item

    def _cachedir(self):
        with tempfile.TemporaryDirectory() as cachedir:
            with open(
                os.path.join(cachedir, "sqla_mypy_config.cfg"), "w"
            ) as config_file:
                config_file.write(
                    """
                    [mypy]\n
                    plugins = sqlalchemy.ext.mypy.plugin\n
                    """
                )
            with open(
                os.path.join(cachedir, "plain_mypy_config.cfg"), "w"
            ) as config_file:
                config_file.write(
                    """
                    [mypy]\n
                    """
                )
            yield cachedir

    @testing.fixture()
    def mypy_runner(self, cachedir):
        from mypy import api

        def run(path, use_plugin=True, incremental=False):
            args = [
                "--strict",
                "--raise-exceptions",
                "--cache-dir",
                cachedir,
                "--config-file",
                os.path.join(
                    cachedir,
                    "sqla_mypy_config.cfg"
                    if use_plugin
                    else "plain_mypy_config.cfg",
                ),
            ]

            if incremental:
                args.append(path)
            else:
                # mypy as of 0.990 is more aggressively blocking messaging
                # for paths that are in sys.path, and as pytest puts currdir,
                # test/ etc in sys.path, just copy the source file to the
                # tempdir we are working in so that we don't have to try to
                # manipulate sys.path and/or guess what mypy is doing
                filename = os.path.basename(path)
                test_program = os.path.join(cachedir, filename)
                shutil.copyfile(path, test_program)
                args.append(test_program)

            # I set this locally but for the suite here needs to be
            # disabled
            os.environ.pop("MYPY_FORCE_COLOR", None)

            result = api.run(args)
            return result

        return run

    def _incremental_dirs():
        path = os.path.join(os.path.dirname(__file__), "incremental")
        files = []
        for d in os.listdir(path):
            if os.path.isdir(os.path.join(path, d)):
                files.append(
                    os.path.join(os.path.dirname(__file__), "incremental", d)
                )

        for extra_dir in testing.config.options.mypy_extra_test_paths:
            if extra_dir and os.path.isdir(extra_dir):
                for d in os.listdir(os.path.join(extra_dir, "incremental")):
                    if os.path.isdir(os.path.join(path, d)):
                        files.append(os.path.join(extra_dir, "incremental", d))
        return files

    @testing.combinations(
        *[(pathname,) for pathname in _incremental_dirs()], argnames="pathname"
    )
    @testing.requires.patch_library
    def test_incremental(self, mypy_runner, per_func_cachedir, pathname):
        import patch

        cachedir = per_func_cachedir

        dest = os.path.join(cachedir, "mymodel")
        os.mkdir(dest)

        patches = set()

        print("incremental test: %s" % pathname)

        for fname in os.listdir(pathname):
            if fname.endswith(".py"):
                shutil.copy(
                    os.path.join(pathname, fname), os.path.join(dest, fname)
                )
                print("copying to: %s" % os.path.join(dest, fname))
            elif fname.endswith(".testpatch"):
                patches.add(fname)

        for patchfile in [None] + sorted(patches):
            if patchfile is not None:
                print("Applying patchfile %s" % patchfile)
                patch_obj = patch.fromfile(os.path.join(pathname, patchfile))
                assert patch_obj.apply(1, dest), (
                    "pathfile %s failed" % patchfile
                )
            print("running mypy against %s" % dest)
            result = mypy_runner(
                dest,
                use_plugin=True,
                incremental=True,
            )
            eq_(
                result[2],
                0,
                msg="Failure after applying patch %s: %s"
                % (patchfile, result[0]),
            )

    def _file_combinations():
        path = os.path.join(os.path.dirname(__file__), "files")
        files = []
        for f in os.listdir(path):
            if f.endswith(".py"):
                files.append(
                    os.path.join(os.path.dirname(__file__), "files", f)
                )

        for extra_dir in testing.config.options.mypy_extra_test_paths:
            if extra_dir and os.path.isdir(extra_dir):
                for f in os.listdir(os.path.join(extra_dir, "files")):
                    if f.endswith(".py"):
                        files.append(os.path.join(extra_dir, "files", f))
        return files

    @testing.combinations(
        *[(filename,) for filename in _file_combinations()], argnames="path"
    )
    def test_mypy(self, mypy_runner, path):
        filename = os.path.basename(path)
        use_plugin = True

        expected_errors = []
        expected_re = re.compile(r"\s*# EXPECTED(_MYPY)?: (.+)")
        py_ver_re = re.compile(r"^#\s*PYTHON_VERSION\s?>=\s?(\d+\.\d+)")

        from sqlalchemy.ext.mypy.util import mypy_14

        with open(path) as file_:
            for num, line in enumerate(file_, 1):
                m = py_ver_re.match(line)
                if m:
                    major, _, minor = m.group(1).partition(".")
                    if sys.version_info < (int(major), int(minor)):
                        config.skip_test(
                            "Requires python >= %s" % (m.group(1))
                        )
                    continue
                if line.startswith("# NOPLUGINS"):
                    use_plugin = False
                    continue

                m = expected_re.match(line)
                if m:
                    is_mypy = bool(m.group(1))
                    expected_msg = m.group(2)
                    expected_msg = re.sub(r"# noqa[:]? ?.*", "", m.group(2))

                    if mypy_14 and util.py39:
                        # use_lowercase_names, py39 and above
                        # https://github.com/python/mypy/blob/304997bfb85200fb521ac727ee0ce3e6085e5278/mypy/options.py#L363  # noqa: E501

                        # skip first character which could be capitalized
                        # "List item x not found" type of message
                        expected_msg = expected_msg[0] + re.sub(
                            r"\b(List|Tuple|Dict|Set|Type)\b",
                            lambda m: m.group(1).lower(),
                            expected_msg[1:],
                        )

                    if mypy_14 and util.py310:
                        # use_or_syntax, py310 and above
                        # https://github.com/python/mypy/blob/304997bfb85200fb521ac727ee0ce3e6085e5278/mypy/options.py#L368  # noqa: E501
                        expected_msg = re.sub(
                            r"Optional\[(.*?)\]",
                            lambda m: f"{m.group(1)} | None",
                            expected_msg,
                        )

                    expected_errors.append(
                        (num, is_mypy, expected_msg.strip())
                    )

        result = mypy_runner(path, use_plugin=use_plugin)

        not_located = []

        if expected_errors:
            # mypy 0.990 changed how return codes work, so don't assume a
            # 1 or a 0 return code here, could be either depending on if
            # errors were generated or not

            print(result[0])

            errors = []
            for e in result[0].split("\n"):
                if re.match(r".+\.py:\d+: error: .*", e):
                    errors.append(e)

            for num, is_mypy, msg in expected_errors:
                msg = msg.replace("'", '"')
                prefix = "[SQLAlchemy Mypy plugin] " if not is_mypy else ""
                for idx, errmsg in enumerate(errors):
                    if (
                        f"{filename}:{num + 1}: error: {prefix}{msg}"
                        in errmsg.replace("'", '"')
                    ):
                        break
                else:
                    not_located.append(msg)
                    continue
                del errors[idx]

            if not_located:
                print(f"Couldn't locate expected messages: {not_located}")
                assert False, "expected messages not found, see stdout"

            assert not errors, "errors remain: %s" % "\n".join(errors)

        else:
            eq_(result[2], 0, msg=result)
